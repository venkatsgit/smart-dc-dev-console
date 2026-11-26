# Failure prediction notebook (`r2f2.ipynb`) — step by step

This note explains what `r2f2.ipynb` does, in the same order as the cells. The notebook builds three models from Red Dot / R2F chiller experiment CSVs:

1. **Binary classification** — is this window healthy or faulty?
2. **Multiclass classification** — which fault family is it?
3. **RUL / survival** — given that a fault is already on, how likely is a trip in the next N hours?

---

## 1. What one CSV file looks like

Each file is one **scenario × severity × load** run.

Example: condenser fouling, severity SL1, load 80% → one CSV.

| Phase | Rough time | Meaning |
| --- | --- | --- |
| Steady healthy | First **24 hours** | Fault not yet injected. Used as the healthy baseline for that run. |
| Fault injection | At **t = 24 h** | The fault knob turns on (fouling, leak, low flow, etc.). |
| Run-to-failure (R2F) | After 24 h | Sensors evolve under the fault. |

**End state of a run** can be one of:

| End state | Meaning |
| --- | --- |
| **Degraded (right-censored)** | Simulation ends while the machine is still running. No confirmed protection trip. Useful as censored survival data. |
| **Trip** | A protection trip happens (high head, low evaporator pressure, etc.). That trip time is the event used for RUL. |

Folder naming is parsed as:

```text
<root>/<fault>/<load_XX>/.../SLN/.../<file>.csv
```

Key stored as `(fault, load, severity, injection)`. Healthy files use severity `"healthy"`.

Data root in the notebook:

```text
DATA_DIR = ../data/raw/experiments/data
```

---

## 2. Step A — Load and inspect (cells 0–3)

### Load

`load_red_dot_dataset` walks every CSV under `DATA_DIR`, builds:

- `datasets`: dict of DataFrames keyed by scenario
- `metadata`: one row per file (rows, duration, path)

Timestamps become the index when a parseable time column exists. Object columns that look numeric are converted.

### Inspect

- Grouped summary by fault / load / injection
- One sample head / shape / columns
- `plot_all_faults`: overlays healthy vs each severity for each sensor, with a red vertical line at the **assumed fault onset = 24 h**

This plot step is for understanding only. It does not train models.

### The Clock: `elapsed_hours`
**`elapsed_hours`** is a relative clock for each individual simulation file, measuring the time passed since the start of that specific run.
*   **0–24 hours:** The machine is physically healthy (Healthy stretch).
*   **Exactly 24 hours:** The fault (root cause) is injected into the machine.
*   **> 24 hours:** The machine is operating under a fault ("sick").
*   **Sickness Duration:** How long the machine has been sick is calculated as `elapsed_hours - 24`.

---

## 3. Step B — Dataset preparation for binary classification (cells 4–7)

Step B turns the raw per-file time series from Step A into a **training table of windows** with a binary label. This table (`df_windows`) is what binary classification trains on. Multiclass later reuses the same table and keeps only `label == 1`.

### Important: it is not a time-merge across scenarios

Condenser fouling SL1 and refrigerant leak SL2 are **not** aligned on a shared calendar clock and merged by timestamp.

What actually happens:

1. Process **each CSV independently** (each scenario × severity × load file).
2. Inside that file, slide windows and attach labels using **elapsed hours from that file’s own start**.
3. **Stack (append)** all window rows into one big table.

So the final dataset is a **row-concatenated catalogue of windows**, not one continuous timeline.

Each file can have its own 24 h steady stretch. Those healthy stretches are **not** merged into one healthy day. Each contributes its own `label = 0` windows, tagged with that file’s `scenario_id`.

---

### Step-by-Step Dataset Assembly

The final table `df_windows` is built by harvesting data from **every file** in the collection.

1.  **Harvesting Healthy Data (Label 0):**
    *   **From Pure Healthy Files:** 100% of the data generates Label 0 windows.
    *   **From Fault Files:** Only the data **before the 24h injection mark** generates Label 0 windows. Since the fault hasn't started yet, this is physically "Healthy" data.
2.  **Harvesting Failure Data (Label 1):**
    *   Only windows that **end at or after the 24h mark** in fault files are labeled as 1.
3.  **The Windowing "Squash" with Overlap:**
    *   A "Window" is **60 raw minutes**.
    *   The "Stride" is **10 minutes**.
    *   **Overlapping Logic:** Because the window (60m) is longer than the stride (10m), windows share data. 
        *   Window 1: Minutes 1–60.
        *   Window 2: Minutes 11–70 (shares 50 mins with Window 1).
        *   Window 3: Minutes 21–80 (shares 50 mins with Window 2).
4.  **No Merging or Time-Sorting:**
    *   The final dataset is a **simple vertical stack** (append) of these windows.
    *   There is **no joining** of files based on timestamps. Condenser Fouling SL1 and Refrigerant Leak SL2 are just two different groups of rows in the same table.
    *   The model doesn't care about the absolute time; it only cares about the **summary stats** (Mean, Std, Slope, Last) and the **Label**.

### Numerical Example: How many rows?

Assume 1-minute sampling, a 60-minute window, and a 10-minute stride.

| Component | Raw Data Duration | Calculation | Approx. Rows in `df_windows` | Binary Label |
| :--- | :--- | :--- | :--- | :--- |
| **Healthy Stretch (any file)** | 24 Hours | (24*60 - 60) / 10 + 1 | **139 rows** | **0** |
| **Fault SL1 (ends fast)** | 10 Hours post-onset | (10*60) / 10 | **60 rows** | **1** |
| **Fault SL2 (runs longer)** | 20 Hours post-onset | (20*60) / 10 | **120 rows** | **1** |

**The final `df_windows` is a stack of these rows:**
[139 rows from File A Healthy] + [60 rows from File A Fault] + [139 rows from File B Healthy] + [120 rows from File B Fault] ...

---

### What `df_windows` finally looks like

One **row = one window**. Sketch (only a few feature columns shown):

| scenario_id | fault | severity | elapsed_hours | label | CH-CON-RFT-PRES__mean | CH-CON-RFT-PRES__std | CH-CON-RFT-PRES__slope | CH-CON-RFT-PRES__last | … |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01_healthy__load_80__healthy__healthy_24h | 01_healthy | healthy | 5.0 | **0** | … | … | … | … | … |
| 01_healthy__… | 01_healthy | healthy | 12.0 | **0** | … | … | … | … | … |
| 02_condenser_fouling__load_80__SL1__scenario | 02_condenser_fouling | SL1 | 10.0 | **0** | … | … | … | … | … |
| 02_condenser_fouling__…__SL1__… | 02_condenser_fouling | SL1 | 24.0 | **1** | … | … | … | … | … |
| 02_condenser_fouling__…__SL1__… | 02_condenser_fouling | SL1 | 30.0 | **1** | … | … | … | … | … |
| 02_condenser_fouling__load_80__SL2__scenario | 02_condenser_fouling | SL2 | 8.0 | **0** | … | … | … | … | … |
| 02_condenser_fouling__…__SL2__… | 02_condenser_fouling | SL2 | 25.0 | **1** | … | … | … | … | … |
| 04_refrigerant_vapour_leakage__…__SL1__… | 04_… | SL1 | 20.0 | **0** | … | … | … | … | … |
| 04_refrigerant_vapour_leakage__…__SL1__… | 04_… | SL1 | 28.0 | **1** | … | … | … | … | … |
| 04_…__SL2__… | 04_… | SL2 | 26.0 | **1** | … | … | … | … | … |
| 06_reduced_condenser_water_flow__…__SL1__… | 06_… | SL1 | 24.5 | **1** | … | … | … | … | … |
| … | … | … | … | … | … | … | … | … | … |

Notes:

- `label` is only **0 or 1**. Fault name / severity are metadata, not the binary target.
- Pre-24 h windows from fouling and from leak are **both** label 0. The model is not asked to tell those healthy stretches apart yet.
- Post-24 h windows from fouling SL1 and leak SL2 are **both** label 1 for binary. Multiclass later uses the `fault` column to split those.

### Direct answers to the usual questions

| Question | Answer |
| --- | --- |
| Is it one consolidated dataset? | Yes — one table `df_windows`, rows appended from every file. |
| Sorted / merged by shared timestamp across faults? | **No.** Each file uses its own elapsed clock; rows are stacked. |
| Same or different 24 h steady data per file? | **Different per file.** Each fault CSV carries its own pre-injection stretch. |
| Is label 1 everything after 24 h injection? | **Yes**, for windows whose **end** is at/after 24 h on a fault file. |
| What does a window look like in the frame? | One row of aggregated sensor stats + metadata + `label`. |

Output of Step B: **`df_windows`** — this **is** the dataset used for binary model training (Step C).

---

## 4. Step C — Binary classification (cells 8–16)

Step C builds the **Fault Detector**. It takes the windowed stats from Step B and predicts whether the machine is healthy or faulty.

### The Challenge of Overlapping Windows
Because our windows overlap by 50 minutes (from Step B), we cannot use a normal random split. A random split would lead to **data leakage**, where the model "cheats" by seeing almost identical data in both training and testing.

### The Solution: Leave-One-Scenario-Out (LOSO)
To get a fair result, the notebook uses a **Leave-One-Scenario-Out** cross-validation strategy:
1.  **Select a "Test" Scenario:** For example, take the entire *Condenser Fouling SL1* file.
2.  **Train on the Rest:** Train the model using all windows from every *other* file in the dataset.
3.  **Predict:** Ask the model to predict the status (0 or 1) for the windows in the *Condenser Fouling SL1* file.
4.  **Repeat:** Do this until every file has been used as the "Test" set exactly once.

This proves the model can detect a fault in a simulation it has **never seen before**.

### Model Configurations

| Model | Role | Characteristics |
| :--- | :--- | :--- |
| **Logistic Regression** | Linear Baseline | Uses a `StandardScaler` to normalize sensors. Good for finding simple trends. |
| **XGBoost** | Non-Linear Expert | Uses decision trees to find complex relationships between sensors. Uses `scale_pos_weight` to handle the fact that we have more healthy data than failure data. |

### Outputs and Interpretation
*   **Confusion Matrix:** Shows exactly how many healthy windows were called "faulty" (False Alarms) and how many faulty windows were missed.
*   **Probability vs. Time Plots:** This is the most intuitive output. We plot the predicted probability (0% to 100%) against the `elapsed_hours`. 
    *   **Success:** The probability stays near 0 until 24h, then jumps toward 100% shortly after the fault is injected.
    *   **Failure:** The probability jumps around randomly or fails to rise even after the fault is active.

### Why this is the "Stage 1" Model
This binary model is the first part of our two-stage prediction system. Its only job is to say: **"Something is wrong."** Once it fires, we pass the data to the Multiclass model (Step D) to ask: **"What is wrong?"**

---

## 5. Step D — Multiclass classification (cells 17–22)

Step D builds the **Fault Diagnostician**. Once Step C detects a problem, this model identifies the specific root cause (e.g., *Condenser Fouling* vs. *Vapour Leakage*).

### Filtering to "Faulty Only"
This model is specialized. It only trains on windows where **label == 1**. It does not try to tell "Healthy" from "Faulty"; it assumes the machine is already failing and asks: **"What is the cause?"**

### Example Multiclass Dataset Table
Here is how the data looks for this model. Note that all rows are from post-injection periods, and we now have a **fault_label** and a **sample_weight**.

| scenario_id | fault | fault_label | elapsed_hours | sensor_1__mean | ... | sample_weight |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| fouling__SL1 | Condenser Fouling | 0 | 25.0 | 192.4 | ... | 0.85 |
| fouling__SL1 | Condenser Fouling | 0 | 26.0 | 195.1 | ... | 0.85 |
| leak__SL2 | Vapour Leak | 1 | 24.5 | 180.2 | ... | 1.20 |
| leak__SL2 | Vapour Leak | 1 | 25.5 | 175.5 | ... | 1.20 |
| gas__SL1 | Non-Condensable | 2 | 24.0 | 210.0 | ... | 3.50 |

### The Imbalance Problem
Not all simulations are the same length. A slow SL1 leak might provide 100 windows, while a fast SL4 trip might only provide 10 windows. Without intervention, the model would become biased toward the "slower" faults because it sees them more often.

### The Solution: Scenario & Class Weighting
To keep the diagnostician unbiased, the notebook calculates a unique weight for every single training row.

**Important: The weight is NOT a feature.** 
The model never "sees" the weight when it is making a prediction. There is a big difference:
*   **Features (Pressures, kW, etc.):** Data the model uses to "guess" the answer. Used during both training and live prediction.
*   **Sample Weights:** Instructions used **ONLY** during training to tell the model how much to care about a specific row.

**The "Megaphone" Analogy:**
Imagine you are in a room with 10 people. 9 are talking about "Fouling" and 1 is talking about "Gas". If you listen equally, you'll only learn about Fouling. **Weighting** is like giving a megaphone to that 1 person so their voice is just as loud as the other 9 combined. This ensures the model treats every fault family as equally important.

1.  **Scenario Weight:** Reduces the influence of very long simulation runs (so one 50-hour run doesn't drown out everything else).
2.  **Class Weight:** Increases the influence of rare fault families (giving them a "louder voice" during learning).
3.  **Result:** Every fault family has an equal "vote" in the model's learning process.

### Model Configurations

| Model | Logic |
| :--- | :--- |
| **Logistic Regression** | Uses "One-vs-Rest" or Multinomial logic to find the unique signature of each fault. |
| **XGBoost** | Uses `objective: multi:softprob` to output a list of probabilities for every possible fault. |

### Outputs and Evaluation
*   **Multiclass Confusion Matrix:** This is the primary scorecard. It shows if the model is confusing one fault for another (e.g., misidentifying *Reduced Flow* as *Fouling*).
*   **Confidence Score:** The model doesn't just name a fault; it says how sure it is (e.g., "90% confident this is a Vapour Leak").

### The Output: A Probability Vector (Understanding the Diagnostician)

While the **Binary** model outputs a single number (0 to 1), the **Multiclass** model outputs a **vector of probabilities**—one for every possible fault family.

1.  **Probability for Every Class:** If you have 6 fault families, the model returns 6 numbers. For example:
    *   `02_condenser_fouling`: 0.85 (85%)
    *   `04_refrigerant_vapour_leakage`: 0.05 (5%)
    *   `06_reduced_condenser_water_flow`: 0.10 (10%)
    *   ... (others at 0%)
2.  **Sum to 100%:** All these probabilities sum exactly to **1.0 (100%)**. This is usually achieved via a *Softmax* function in the model.
3.  **The "Winner" (Prediction):** The final prediction is the fault with the **highest probability** (the *Argmax*). In the example above, the prediction is "Condenser Fouling."
4.  **Confidence Score:** The highest probability value (0.85) is treated as the **Confidence Score**. It tells the operator how sure the model is that it has found the right root cause.

**In the inference cascade:** We only look at these probabilities if the Binary model has already confirmed that a fault is active.

---

## 6. Understanding Performance Metrics

To evaluate how well our Detector and Diagnostician are performing, we use three primary metrics: **Precision**, **Recall**, and the **F1-Score**.

### 6.1 Binary Classification (Stage 1: The Detector)

In this stage, the **Positive Class (1)** is a **Fault** and the **Negative Class (0)** is **Healthy**.

| Metric | Question for the Model | Penalty (What to avoid) | Risk if Low |
| :--- | :--- | :--- | :--- |
| **Precision** | "Of all the times you shouted 'FAULT!', how many were real?" | **False Positives** (Crying wolf) | Maintenance fatigue; unnecessary downtime. |
| **Recall** | "Of all the actual faults that happened, how many did you catch?" | **False Negatives** (Missing a problem) | Machine damage; unmanaged degradation. |
| **F1-Score** | "How well are you balancing being reliable and being thorough?" | **Both** | Unreliable or incomplete monitoring system. |

**Goal:** A high F1-score proves the model is a reliable detector that finds real problems without causing constant false alarms.

### 6.2 Multiclass Classification (Stage 2: The Diagnostician)

In this stage, we use **Macro-averaged** metrics. This means we calculate the score for every individual fault family (e.g., Gas Leak, Fouling, Flow Loss) and then take the average.

| Metric | Focus for the Diagnostician | Penalty (What to avoid) | Why it matters |
| :--- | :--- | :--- | :--- |
| **Macro Precision** | Not misidentifying one fault as another. | **Misclassification** (e.g., calling a Leak "Fouling") | Prevents technicians from bringing the wrong tools or parts. |
| **Macro Recall** | Not missing any specific type of failure family. | **Class Missing** (e.g., being blind to Gas Leaks) | Ensures the system is equally good at finding all types of root causes. |
| **Macro F1-Score** | Balance across all fault families. | **Bias** (Favoring common faults over rare ones) | Ensures a fair and consistent diagnostic across the entire plant. |

---

## 7. Step E — Survival / RUL setup (cells 23–26)

Step E prepares the data for the **Time-to-Trip** question. Unlike classification (which asks "Is it failing?"), this stage asks: **"Given it is already failing, how many hours until it trips?"**

### The "Target" is a Count Down (RUL)
In classification, the label is a fixed 0 or 1. In survival/RUL modeling, the target is the **Remaining Useful Life (RUL)**. 
*   As time moves forward, the target value **decreases** (counts down).
*   Example: If a machine will trip at Hour 30, then at Hour 25, the RUL target is **5.0 hours**. At Hour 29, the RUL target is **1.0 hour**.

### Trips vs. Censoring (`event_observed`)
Not every simulation ends in a trip. We must tell the model whether we actually *saw* the failure or if the simulation just ended while the machine was still degraded.
*   **`event_observed = 1` (Trip):** We know exactly when the machine died. This is the ground truth for a completed failure path.
*   **`event_observed = 0` (Right-Censored):** The simulation ended (e.g., at 48 hours) while the machine was still running. We don't know when it *would* have tripped, only that it lasted *at least* 48 hours. The model uses this to learn "resilience."

### Data Source and Filtering
The RUL dataset is built **only from the failure segments** of all failure files.
*   **Healthy data is ignored:** The first 24 hours (pre-injection) of every file are discarded for this model.
*   **Post-Onset Only:** Windows are only generated starting from one hour *after* the fault is injected (Hour 25+).
*   **All Failure Files:** Data is harvested from SL1, SL2, SL3, and SL4 for every fault family.

### Windowing and Stride: No Overlap
For RUL, the sampling is much slower than for classification.
*   **Window Size:** 60 minutes.
*   **Stride (Prediction Interval):** 1 hour (`PREDICTION_INTERVAL_HOURS = 1`).
*   **No Overlap:** Because the stride (1 hr) matches the window size (1 hr), the rows are **disjoint**. 
    *   Window 1: Uses data from 24-25h (ends at Hour 25).
    *   Window 2: Uses data from 25-26h (ends at Hour 26).
    *   This reduces data redundancy for the slow-moving RUL calculation.

### Does the table contain the Failure Class?
In the training DataFrame (`survival_df`), the **fault type** (e.g., `02_condenser_fouling`) is stored as metadata in the `run_name` or `fault` column. This is used to:
1.  **Group for Validation:** Ensuring we leave out entire fault scenarios during testing.
2.  **Categorical Feature (Optional):** Some survival models use the "Fault Type" as an input feature so one global model can handle all faults.

### Example Survival / RUL Dataset Table

| run_name | hours_since_onset | duration_h (RUL Target) | event_observed | sensor_1__mean | ... |
| :--- | :--- | :--- | :--- | :--- | :--- |
| fouling__SL4 | 1.0 | 4.5 | **1** | 195.2 | ... |
| fouling__SL4 | 2.0 | 3.5 | **1** | 198.5 | ... |
| fouling__SL4 | 5.5 | 0.0 | **1** | 215.0 | (Trip) |
| fouling__SL1 | 1.0 | 24.0+ | **0** | 192.1 | ... |

---

## 7. The Inference Cascade (The Prediction Chain)

In a live production environment, the three models form a **Logic Cascade** triggered by the same incoming 60-minute window of sensor data.

### Step 1: The Detector (Binary Model)
*   **Question:** "Is something wrong?"
*   **Input:** Current 60-min window stats.
*   **Action:** If `fault_probability < 0.5`, the machine is **Healthy**. Stop. If `prob >= 0.5`, proceed.

### Step 2: The Diagnostician (Multiclass Model)
*   **Question:** "What exactly is wrong?"
*   **Input:** The **same 60-minute window** stats.
*   **Action:** Identify the failure class (e.g., "Non-condensable Gas"). Output the fault name and confidence. Proceed to Step 3.

### Step 3: The Countdown (RUL Model)
*   **Question:** "How much time is left before it trips?"
*   **Input:** The **same 60-minute window** stats.
*   **Crucial Logic:** The RUL model is an "Expert on Failure." It is only consulted *after* Step 1 and Step 2 confirm a fault. This prevents "Healthy" data from confusing the RUL model into giving a random countdown.

### Summary: Training vs. Inference

| Stage | Training Data | Inference Trigger |
| :--- | :--- | :--- |
| **1. Binary** | Healthy + Faulty (Overlap) | Runs every 10 mins |
| **2. Multiclass** | Faulty Only (Overlap) | Only if Binary says "Faulty" |
| **3. RUL** | Faulty Only (**No Overlap**) | Only if Binary says "Faulty" |

---

## 8. Step F — Train survival (RUL) models (cells 27–34)

### Models compared

| Short name | Family | What it predicts |
| --- | --- | --- |
| weibull | Weibull AFT (lifelines) | Survival curve → P(trip by horizon) |
| xgb | XGBoost survival AFT | Same via AFT distribution |
| cox | Cox proportional hazards | Same via baseline hazard |
| rsf | Random survival forest | Same via ensemble survival functions |

### Horizons

Default evaluation horizons (hours):

```text
6, 12, 24, 48
```

For each horizon H, the model outputs something like `weibull_p12h` = probability that a trip occurs **within the next 12 hours** from that prediction time.

Conversion used for AFT / Cox / RSF style outputs:

```text
P(trip within H) = 1 - S(H)
```

where **S(H)** is the predicted survival probability at horizon H.

### Validation

**Leave-one-run-out on trip scenarios only for testing:**

- Train on all other runs (trips **and** censored)
- Test on one held-out **confirmed trip** run
- Repeat

Censored runs help the model learn “still running” behaviour; scoring focuses on runs where a true trip time is known.

### Preprocessing per fold

- Drop features with >20% missing on train
- Drop constant features
- Median impute
- Standard scale (for lifelines models)

### Evaluation

For each horizon:

- True label = trip already known to occur within H hours from that row
- Only rows where the outcome at horizon H is knowable (tripped already, or observation lasted at least H)
- Metrics: **Brier score** (lower better), **ROC-AUC**

Plots show predicted trip probability vs hours since onset, with the actual trip line.

---

## 9. Step G — Trip / duration audits (cells 35–38)

These are sanity checks, not training:

- `check_actual_trips`: read `Chiller trip status` and report whether / when a trip appears after onset
- `summarize_fault_duration`: how many minutes of post-onset fault data each severity has

Useful to reconcile the hand-coded `TRIP_TIMES_MINUTES` map with what is actually in the CSVs.

---

## 10. How the three stages fit together

```text
CSV (24 h healthy → inject → R2F → degrade or trip)
        |
        v
  Sliding 60-min windows
        |
        +--> Binary: Healthy vs Faulty
        |
        +--> Multiclass (faulty windows only): Which fault?
        |
        +--> Survival (post-onset): P(trip within 6/12/24/48 h)
                                      ≈ remaining useful life risk
```

In live use, the intended cascade is:

1. Binary detector fires → something is wrong.
2. Multiclass names the failure family.
3. Survival / RUL estimates how soon a protection trip may arrive under that degradation path.

---

## 11. Important modelling choices (keep these in mind)

| Choice | Why it matters |
| --- | --- |
| Assumed onset = 24 h | Labels and survival clocks are tied to this convention for every file. |
| Drop post-trip samples | Avoid training on dead / tripped machine states. |
| Leave-one-scenario-out | Prevents leakage from neighbouring windows of the same run. |
| Censored runs in survival train | Mild severities that never trip still teach “not yet failed.” |
| Only confirmed trips in survival test | Fair evaluation of trip timing when the end event is known. |
| Window stats, not raw sequences | Simple tabular models (logistic / XGB / classical survival) instead of deep sequence models. |

---

## 12. Notebook map (cell index → purpose)

| Cells | Purpose |
| --- | --- |
| 0–2 | Config, load CSVs, metadata summary |
| 3 | Exploratory plots vs healthy |
| 4–7 | Build binary window table + feature list |
| 8–16 | Train / score / plot binary models |
| 17–22 | Build / train / plot multiclass models |
| 23–26 | Build survival events + survival feature rows |
| 27–34 | Train / evaluate / plot survival (RUL) models |
| 35–38 | Trip and duration audits |

---

## 13. Short glossary

| Term | Meaning in this notebook |
| --- | --- |
| Scenario | One CSV / one (fault, load, severity, injection) key |
| Onset | Fault injection time, fixed at 24 h from file start |
| Window | 60 minutes of sensors turned into mean/std/slope/last |
| Binary label | 0 = healthy stretch, 1 = after onset on a fault file |
| Multiclass label | Fault family name among faulty windows |
| event_observed = 1 | Confirmed protection trip used as survival event |
| event_observed = 0 | Right-censored or non-trip end |
| duration_h | Remaining hours from prediction time to event_time (RUL at that instant) |
| Horizon | “Will it trip within the next H hours?” |
