# Physics Foundation Models for Failure Prediction

**Focus:** Polymathic AI / Walrus vs Athena failure-prediction needs  
**Status:** Exploration notes  
**Refs:** [polymathic-ai.org](https://polymathic-ai.org/), [Walrus, arXiv:2511.15684](https://arxiv.org/abs/2511.15684) (ICML 2026), [Hugging Face](https://huggingface.co/polymathic-ai/walrus), [GitHub](https://github.com/PolymathicAI/walrus), The Well

---

## 1. Athena solutions (current state)

Athena already has multi-year production and experimental capabilities. This is not a greenfield problem.


| Capability                        | Stage              | Role                                                                |
| --------------------------------- | ------------------ | ------------------------------------------------------------------- |
| **Anomaly Detection**             | Production         | Autoencoder + regression-based early warning (cooling / electrical) |
| **Time-to-Threshold (TTH)**       | Production         | Forecast when parameters approach operating limits                  |
| **Physics-Embedded Models**       | Experimental       | Physics equations in the loss (beyond residual-only)                |
| **GAT / Topology**                | Experimental       | Upstream/downstream structure for root-cause context                |
| **Digital Twin / Run-to-Failure** | Experimental       | Physics-based failure scenarios (e.g. condenser fouling)            |
| **Survival / Failure Prediction** | Experimental       | Failure mode + time-to-failure                                      |
| **SME Agent**                     | Partial production | Agentic RAG + tools; physics engine under consideration             |


**Ultimate objective:** Predict *what* will fail (condenser fouling, evaporator fouling, refrigerant leak, …) and *when*.

---

## 2. Core problem (the remaining gap)

Practical stacks above already cover anomaly, thresholds, simulation, and early survival work.

The open question is whether a **foundation model** can handle the **numerical / physics** side of failure prediction — not just text reasoning via a generic LLM.


| We are sceptical of                                 | We are interested in                                                                       |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Conventional generative LLM as the numerical engine | Physics-aware / physics-pretrained foundation model as dynamics backbone or SME-agent base |


**Gap in one line:** Can a scientific foundation model learn cooling-system dynamics well enough that predicted trajectories feed failure mode + TTF — or is it still “just another statistical predictor”?

The next section unpacks that sentence. “Foundation model” here does **not** mean another Llama/Qwen. “Numerical” does **not** mean “cannot handle numbers.”

---

## 3. From zero: LLM, Transformer, and a numerical foundation model

### Same machinery

A **neural network** is the general family. A **Transformer** is one design inside that family. Llama, Qwen, and Walrus are all Transformers. Each step works the same way:

1. Turn the input into vectors.
2. Build **query (Q)**, **key (K)**, and **value (V)** for each piece.
3. **Self-attention** lets every piece look at the others.
4. Predict the **next step** of the sequence.
5. Feed that prediction back in and repeat (**autoregressive** generation).

The difference is what one step of the sequence **is**.


|                   | Llama / Qwen                                               | Walrus                                                                                       |
| ----------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Kind of model     | Neural network, Transformer                                | Neural network, Transformer                                                                  |
| One step          | A **text token** (a word piece such as `fouling` or `3.2`) | A **patch of a physical field** (a small block of a temperature, velocity, or pressure grid) |
| Training target   | Next token in a sentence                                   | Next physical snapshot, as a change Δu                                                       |
| What you read out | Text                                                       | Numbers on a grid: the next state of the simulation                                          |


**Walrus is a neural network and a Transformer. It is not an LLM.**

### “Foundation model” means the training strategy

**Foundation model** means: train one large model on a huge, varied dataset so it learns general patterns, then reuse or fine-tune it instead of training from scratch.

- Llama and Qwen are foundation models **for language**.
- Walrus is a foundation model **for continuum dynamics** (how physical fields evolve in space and time).

“Foundation” does not mean the model reads text.

### What “numerical” means

Two ideas get mixed together.

**A generic LLM handles numbers as text.** The string `12.47` is chopped into tokens the same way a word is. The model then predicts the next token. It can write “approach temperature = CHWR − CHWS” because that is a sentence pattern. It is not evaluating the equation. Arithmetic, units, and long chains of physical consequences are unreliable unless a calculator or a physics tool does the math. That is why a conventional LLM is a weak engine for numerical failure prediction.

**A numerical / physics foundation model starts from arrays of numbers.** Walrus never sees a prompt such as “Will this chiller foul in 20 days?” Its input is field snapshots. Its loss is numeric (per-field L1), so the output is the next field, not the next word. “Numerical foundation model” means **the native data is numbers, and the model is trained to predict the next numbers.**

### It does not “solve the equation” either

Neither model understands equations the way an engineer does.

- Llama / Qwen can **recite** an equation as text.
- Walrus **never sees the equation text**, and the equation is not a term in the loss. The loss is per-field L1 on the change Δu. PDE coefficients and the time step are not inputs. The paper uses history instead of constitutive models, and the model must infer the timescale from the snapshots.
- The training movies were produced by PDE solvers, so the data already obeys those equations. The weights store an approximate next-state rule. That rule is not a formula you can print (no derived heat-transfer equation). A long rollout can still drift or break physics. Polymathic’s Physics Steering work treats “do the internal representations match real physical concepts?” as an open research question.
- This is different from Athena’s physics-embedded experiments, where the equation is written into the loss.

### “Generative and text-only”

**Generative** means the model produces a new sequence by repeatedly predicting the next step. Llama generates the next word. Walrus generates the next physical state. Both are generative.

**Text-only** fits a conventional LLM such as Llama or Qwen: the core task is next-token prediction over a vocabulary of text pieces. Walrus does not chat. You give it a short history of field snapshots and it returns the next snapshot.

### One prediction step, side by side

Llama / Qwen:

```text
"condenser approach rose to"  →  next token "3.2" or "high"
```

The number is a piece of text. The model continues the sentence.

Walrus:

```text
6 grids of T, velocity, pressure  →  next grid Δu  →  u(t+1)
```

The sequence is a short movie of the physical field. The model continues the movie.

### What each model can answer


| Question                                                                        | Who can answer it                                                                             |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| “Explain condenser fouling in words.”                                           | Llama / Qwen                                                                                  |
| “Given this physical state, what should the fields look like at the next step?” | Walrus, once the data is in its grid form                                                     |
| “Is this condenser fouling, and in how many days?”                              | Neither by itself. That still needs the failure / TTH / survival layer on top of a trajectory |


Athena’s 1-minute table (`CHWS`, `CHWR`, flow, power, …) is a sparse sensor row. Walrus expects a spatial field, like a simulation frame. Bridging those two representations is the integration problem. The architecture family is the one already familiar: attention, Q/K/V, predict the next step.

---

## 4. What Walrus is

**Walrus** (Polymathic AI) is a **1.3B-parameter physics foundation model** — a space-time Transformer pretrained across many physical systems (The Well). It predicts the next physical state. It does not emit a failure label.

Sources: [arXiv:2511.15684](https://arxiv.org/abs/2511.15684), [Hugging Face model card](https://huggingface.co/polymathic-ai/walrus), [GitHub](https://github.com/PolymathicAI/walrus).


| Property         | Detail                                                                                    |
| ---------------- | ----------------------------------------------------------------------------------------- |
| Role             | Learn shared physical dynamics across domains                                             |
| Scale            | ~~1.3B params; public weights (~~5.1 GB safetensors); MIT                                 |
| Pretraining      | ~19 physical systems, ~63 variables, 2D/3D                                                |
| Domains seen     | Fluids, turbulence, acoustics, rheology, plasma, geoscience, astrophysics, …              |
| Native task      | Physical state history → next state (Δu, then reconstruct)                                |
| Intended uses    | Next-step prediction, surrogate simulation, autoregressive rollout, fine-tune to new PDEs |
| Not demonstrated | Sensor history → failure mode + probability + TTF on industrial assets                    |


**Framing that fits Athena:** Walrus is a candidate **physics/dynamics backbone**, not a drop-in “failure-prediction foundation model.”

### Inside one forward pass

From the paper and the GitHub overview, one step is:

1. **Encoder.** Cut each snapshot into patches and embed them (an MLP-style patch embedder). Stride is adjusted so 2D and 3D grids produce a similar number of tokens.
2. **Processor.** A stack of Transformer blocks. Attention is split: one pass attends across **space**, the next across **time**. Time attention is causal, so a frame only looks at the past — the same constraint an LLM has when predicting the next token. Q/K normalization is used for training stability.
3. **Decoder.** Turn the tokens back into a field: the predicted Δu.

Pretraining used 96 NVIDIA H100 GPUs. The mix of 19 systems is the foundation-model bet: patterns shared across many physical systems transfer to a new system with less new data.

Other design points called out by the authors: patch jittering (long-rollout stability), tensor-law-aware augmentation (rotate vector fields correctly when 2D data is embedded in 3D), and asymmetric normalization (inputs normalized by RMS; the predicted Δu is de-normalized with the RMS of Δ).

Related Polymathic pieces worth tracking: The Well, Multiple Physics Pretraining, xVal (how to represent scientific numbers inside Transformers), Physics Steering, sim→lab transfer work, BubbleML fine-tunes (thermal/fluid bridge).

---

## 5. Direct use today: window, inputs, outputs

Sources for the call shape: the released checkpoint config and [Running Walrus](https://github.com/PolymathicAI/walrus/blob/main/demo_notebooks/walrus_example_1_RunningWalrus.ipynb). Well-format conversion is in [example 0](https://github.com/PolymathicAI/walrus/blob/main/demo_notebooks/walrus_example_0_ConvertingDataIntoWellFormat.ipynb).

### Window


| Setting                           | Value in the released checkpoint                                                               |
| --------------------------------- | ---------------------------------------------------------------------------------------------- |
| Input snapshots                   | **6** (`n_steps_input: 6`). The paper calls this the Walrus context.                           |
| Output of one forward pass        | **1** next snapshot (`n_steps_output: 1`)                                                      |
| What that snapshot is             | Δu, then u(next) = u(last) + Δu                                                                |
| Gap between frames in pretraining | Random stride of **1 to 5** simulation steps. The clock interval is not passed in as a number. |


Two future steps means two calls: predict step 1, append that grid, drop the oldest of the 6, predict step 2. A window of 10 rows is longer than the trained context. The official example uses 6.

### Tensor the notebook actually passes

```text
input_fields:        [batch, T_in, height, width, depth, n_fields]
field_indices:       which named vocabulary slot each field uses
boundary_conditions: [batch, 3, 2]
padded_field_mask:   which channels are real
```

The synthetic example in the notebook is `T_in = 6`, grid `128 × 128 × 1`, and 5 fields. One rollout step returns the next grid of those same fields.

### How many fields, and are the names generic?

There is no minimum or maximum column count to fill. There is a **fixed vocabulary of named fields**. The checkpoint lists slots 0–66 (`pressure`, `velocity_x`, `density`, `temperature`, `entropy`, …). The first encoder layer is a `Conv3d` with 67 input channels, one slot per known name.

At inference you pass only the fields that system has. The demo passes 5, and `field_indices` says which slots they are. The other slots stay empty. You do not pass all 63.

A new name (the demo adds a fake field `blubber`) gets a new slot. Old weights are kept. The new slot starts untrained and only becomes meaningful after fine-tuning.

`pressure` is slot 3. `temperature` is slot 46. There is no slot named `flow`, `CHWS`, `CHWR`, approach, kilowatts, or amps. The closest pretrained flow names are `velocity_x` / `velocity_y` / `velocity_z` and `momentum_*`.

### What you do not get out of the box

- Failure mode label
- Failure probability
- Time-to-failure / survival curve

Those require a layer on top of the trajectory (thresholds, engineering indicators, survival / classifier / TTH / SME rules).

### This call does not match the released model

```text
10 rows of (temperature, pressure, flow)  →  next 2 rows
```

Three mismatches: trained length is 6 and one call returns 1 snapshot; each snapshot must be a spatial grid, not one number per sensor; `flow` and the chiller tag names are not in the vocabulary. Mapping a chiller table onto `temperature` and `pressure` and inventing a grid would run the code and would not mean the weights know those columns. That use needs a fine-tune, or a digital-twin grid that already looks like the training data.

---

## 6. Space, time, grids, and Athena’s data

### Space and time

**Time** is the sequence of snapshots. Walrus uses 6 frames in, then the next frame. The condenser-fouling pack `cond_fouling_SL1_80pct_sensors.csv` is one row per minute, 2,880 rows over 48 hours.

**Space** is where on the object the number is measured. Walrus stores a map: a value at many points across a surface or through a volume. The chiller file stores one number per tag. `CH-EVA-E-TEMP` is entering evaporator water at one point. `CH-CON-E-TEMP` is another point. They are two columns, not a map of the tube bundle.

### 2D and 3D grids

A grid is that map, stored as a block of numbers.


| Grid   | What one snapshot is                                                                                                   | Picture                                                                            |
| ------ | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **2D** | A sheet of cells, for example 512×512. Each cell holds the fields. Walrus stores the sheet as a volume of thickness 1. | A photograph whose pixels are temperature, velocity, and pressure instead of color |
| **3D** | A volume of cells, for example 64×64×64. Each small cube holds the same kind of fields.                                | A CT scan of the fluid                                                             |


The sensor CSV is neither. To look like Walrus, the condenser would need temperature and velocity at many points along the tubes and through the water box, for 6 frames. The model would return that whole map one frame later. The pack we have is already collapsed to plant tags: one pressure, one power, one approach.

### The 63 fields are not the chiller tag list

A few names rhyme with thermodynamics. They are generic slots from the pretraining simulations, not Keppel tags under shorter names.


| Walrus slot                              | What it is there                     | Chiller tags                                                                               |
| ---------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------ |
| `temperature` (one slot, index 46)       | One temperature map on the grid      | Several tags: entering evaporator water, entering condenser water, refrigerant temperature |
| `pressure` (one slot, index 3)           | One pressure map on the grid         | Condenser pressure and refrigerant pressure, as separate tags                              |
| `density`, `internal_energy`, `entropy`  | Fluid state inside those simulations | Not in the Keppel tag list                                                                 |
| `velocity_x`, `velocity_y`, `velocity_z` | Flow direction at every grid point   | Plant flow is one sensor, not a 3-direction map                                            |


Other slots are unrelated to a chiller: magnetic field, electron fraction, stress-tensor components (`C_xx`, `D_xx`, …), acoustic pressure stored as real and imaginary parts, planetary surface height.

### The 19 simulations are not the R2F scenarios

Same word, different thing.

The 80 percent pack (`poc/smart-dc-dev-console/r2f/_analysis/80/README.md`) is **one machine, many faults**. Thirteen cases: healthy, condenser fouling SL1–SL4, evaporator fouling SL1–SL4, gas leak slow/moderate, liquid leak slow/moderate. Each case is a 1-minute sensor table for chiller HT-CH-01. The fault is a knob held for a day, such as 12 percent of condenser tube surface lost.

Walrus’s 19 are **19 different physical worlds**, from The Well and FlowBench. Public examples include shear flow, Rayleigh–Bénard convection, Rayleigh–Taylor instability, acoustic scattering, magnetohydrodynamics, a supernova, a viscoelastic fluid, and planetary shallow water. None of them is a chiller, a fouling severity, or a refrigerant leak.

Both are simulated trajectories, so a model can learn what happens next. The R2F files answer what the tags do when the condenser is 12 percent fouled. Walrus’s files answer how a fluid grid evolves under that other physics. BubbleML pool boiling, a later fine-tune, is the nearest thermal neighbor. It is still a boiling-research grid, not HT-CH-01.

### Electrical equipment

The pretrained model does not suit electrical equipment. Training worlds are fluids, acoustics, rheology, plasma, geoscience, and astrophysics. The field list has no voltage, current, power, harmonics, or breaker state. Compressor kilowatts and the three currents in the fouling pack are electrical consequences of the thermal fault. Walrus has no channel for them. Plasma and magnetic-field slots come from astrophysics simulations, not switchboards, UPS, or VSDs.

### Walrus vs TimeGPT

TimeGPT (Nixtla, [arXiv:2310.03589](https://arxiv.org/abs/2310.03589)) is the other “foundation model for numbers” people usually mean. It is also a Transformer. It is the closer match to an Athena table.


|                            | TimeGPT                                                                          | Walrus                                                    |
| -------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Job                        | Forecast a time series                                                           | Continue a physical field in space and time               |
| Training data              | Ordinary series (retail, electricity, finance, IoT)                              | 19 physics simulations, spatial grids                     |
| One time step              | One number, or a row of numbers                                                  | A full grid                                               |
| What you pass              | A table: time, series id, value, optional extra columns. Column names are yours. | The tensor in section 5, plus a field-id for each channel |
| What you get               | The next `h` values of that series, in one call                                  | The next grid, one step per call                          |
| Equations inside the model | No                                                                               | No                                                        |
| How you run it             | Nixtla API / hosted model                                                        | Open weights (MIT) and the GitHub notebooks               |


---

## 7. How it can support failure prediction (short)

Do **not** treat Walrus as a direct replacement for GBR/anomaly models. Use it as the dynamics layer:

1. **Fine-tune on chiller dynamics** — real telemetry and/or digital-twin / R2F trajectories (e.g. condenser fouling progression).
2. **Roll out a future physical trajectory** — temperatures, flows, pressures (and derived fields if mapped).
3. **Derive engineering indicators** — effectiveness, approach, ΔT, pressure drop, COP, HTC proxies, limit proximity.
4. **Map indicators → failure layer** — existing survival / mode classifier / TTH / anomaly / SME tools → mode + TTF.
5. **SME Agent tool** — “what should physics do next?” queries against the FM, alongside RAG and rules — not as the sole LLM brain for numbers.
6. **Value test** — fewer real failure examples needed for useful lead time / degradation path (physical priors from pretraining), plus sim→real transfer — not just +2–5% MAE.

**Concrete ask for Polymathic (sharper than “can it predict failure?”):**  
Can Walrus be fine-tuned on multivariate industrial telemetry and/or physics-based simulation trajectories so predicted trajectories support failure-mode and time-to-failure inference — starting with **chiller condenser fouling**?

---

## 8. Bottom line


| Question                         | Answer                                                                                                                                                                                             |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Relevant to Athena?              | As a physics-grid backbone next to the digital twin, once the data is a spatial field. The current 1-minute tag tables are the wrong shape.                                                        |
| Fits the R2F packs as they are?  | No. Those packs are one chiller, fault knobs, and point sensors. Walrus was trained on 19 other physical worlds, on 2D/3D grids.                                                                   |
| Electrical equipment?            | No. No voltage, current, power, or harmonics in the pretrained field list.                                                                                                                         |
| Sensor-table forecasting?        | TimeGPT is the model shaped like a tag table. Walrus is the model shaped like a field grid.                                                                                                        |
| Solves failure prediction today? | No. One call returns the next grid (6 frames in, 1 frame out). Failure mode and time-to-failure still sit in a layer above that.                                                                   |
| Best next use                    | One asset + one mode (condenser fouling), and only if the twin can emit a spatial field Walrus can fine-tune on. Compare trajectory quality, lead time, and how much real failure data that takes. |


**Engagement framing:**  
*You demonstrated a foundation model for physical dynamics. We want to test transfer to data-centre cooling dynamics and use predicted trajectories for failure-mode and time-to-failure — not replace our stack with a generic LLM.*