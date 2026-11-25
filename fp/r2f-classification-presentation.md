# Presentation: Chiller Failure Classification System
**A Two-Stage AI Approach for Data Center Reliability**

---

## Slide 1: Introduction
*   **The Problem:** Data center chillers fail in diverse ways (Leaks, Fouling, Blockages). Detecting "that" something is wrong is easy, but identifying "what" is wrong early is difficult.
*   **The Goal:** Build an intelligent system that detects anomalies and provides a specific root-cause diagnosis.
*   **Our Solution:** A Two-Stage Classification Pipeline.

---

## Slide 2: Data Assembly (The Windowing Logic)
*   **Input:** High-resolution sensor data (1-minute intervals).
*   **Windowing Strategy:**
    *   **Window Size:** 60 minutes (60 samples per window).
    *   **Stride:** 10 minutes (Next window starts 10 minutes later).
    *   **Overlap:** 50 minutes of data is shared between adjacent windows to ensure the model sees the continuous evolution of faults.
*   **Statistical Summaries (Features):** Every sensor in the window is converted into 4 dimensions:
    1.  **Mean:** The average level.
    2.  **Std Dev:** The stability/fluctuation of the sensor.
    3.  **Slope:** The linear trend (Is it rising or falling?).
    4.  **Last:** The current instantaneous value.
*   **Outcome:** A feature matrix that captures the temporal *behavior* of the machine.

---

## Slide 3: Stage 1 — The Detector (Binary)
*   **Question:** Is the machine Healthy or Faulty?
*   **The Data Leakage Challenge:** Because windows overlap (Slide 2), neighboring windows are nearly identical. A standard random split would let the model "see the future" or "cheat" by memorizing adjacent timestamps.
*   **The Solution: Leave-One-Scenario-Out (LOSO):**
    *   We hold out **entire simulation files** (scenarios) for testing.
    *   We prove the model works by testing it on a simulation run it has **never seen before**.
*   **Primary Metric:** High detection rate while minimizing False Alarms during the 24-hour healthy stretch.

### Binary Training Dataset (Sample)
One row = one 60-minute window summary.

| scenario_id | fault | severity | elapsed_hours | label | sensor_1__mean | sensor_1__std | ... |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| healthy__load_80 | 01_healthy | healthy | 5.0 | **0** | ... | ... | ... |
| fouling__SL1 | 02_fouling | SL1 | 10.0 | **0** | ... | ... | ... |
| fouling__SL1 | 02_fouling | SL1 | 24.0 | **1** | ... | ... | ... |
| leak__SL2 | 04_leak | SL2 | 26.0 | **1** | ... | ... | ... |

---

## Slide 4: Stage 2 — The Diagnostician (Multi-class)
*   **Question:** Which specific fault is occurring? (e.g., Gas Leak, Water Flow Loss, Fouling).
*   **Balanced Learning (Megaphone Logic):** Simulation durations vary (SL1 is long, SL4 is short). To prevent the model from favoring "slow" faults, we apply a sample weight formula during training:
    *   **Weight = 1.0 / (Windows per Scenario × Scenarios per Fault)**
*   **Training vs. Inference:**
    *   **Training:** Weights ensure every fault family has an equal "voice."
    *   **Inference (Live):** Weights are **not required**. The model uses its learned "brain" to classify based only on sensor features.
*   **Outcome:** Specific root-cause identification with a confidence score.

### Multiclass Training Dataset (Sample)
Only includes faulty windows (`label == 1`).

| scenario_id | fault | fault_label | elapsed_hours | sensor_1__mean | ... | sample_weight |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| fouling__SL1 | 02_fouling | 0 | 25.0 | 192.4 | ... | 0.85 |
| leak__SL2 | 04_leak | 1 | 24.5 | 180.2 | ... | 1.20 |
| gas__SL1 | 09_gas | 2 | 24.0 | 210.0 | ... | 3.50 |

---

## Slide 5: Real-time Prediction Workflow
1.  **Ingest:** Chiller sensors arrive every minute.
2.  **Process:** Preprocessing engine builds the 60-minute window stats (using the 10-minute stride).
3.  **Detect:** Stage-1 Binary model checks if a fault is active.
4.  **Diagnose:** If (and only if) Stage-1 fires, Stage-2 Multi-class model identifies the specific failure family.
5.  **Action:** Maintenance is alerted with the exact root cause (e.g., "92% confident: Condenser Fouling").

---

## Slide 6: Continuous Improvement (MLflow)
*   **Tracking:** Every model version, hyperparameter, and performance metric is stored in MLflow.
*   **Governance:** Clear audit trail of model performance across different loads (58% vs 80%).
*   **Scalability:** The pipeline is designed to easily ingest new failure scenarios (e.g., SL1 vs SL4) as they are simulated.
