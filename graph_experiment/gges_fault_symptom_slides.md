# GGES Fault–Symptom Graph Framework
## Chiller Root-Cause Diagnosis Slides (HT-CH-01)

---

## Slide 1 — GGES Scoring and ASHRAE Background

**Graph-Grounded Evidence Scoring (GGES)** converts continuous chiller telemetry into a physics-consistent fault verdict.

### What does ASHRAE mean?
**ASHRAE** = **American Society of Heating, Refrigerating and Air-Conditioning Engineers**.

It is the industry standards body for HVAC and refrigeration. The fault–symptom knowledge used here comes from ASHRAE research project **RP-1043**, which published laboratory-validated chiller fault signatures (pressure, temperature, flow, power patterns) used as the physics basis for this graph.

**Problem it solves**
- Chillers (vapour-compression cycle) couple evaporator, compressor, condenser, and water loops.
- Different faults share overlapping sensor signatures (e.g. Non-Condensable Gases vs Refrigerant Overcharge both raise condenser pressure).
- Closed-set ML can force an unseen fault into the nearest known class.

**ASHRAE foundation**
- Built on **ASHRAE RP-1043** chiller FDD benchmark and thermodynamic first principles.
- Research frame (SSRN-7656122 / PCLC-PGM): sensor deviations → directional symptoms → graph scoring → root cause.
- Two-layer diagnostic core used here:
  1. **Fault nodes** (hypotheses)
  2. **Symptom nodes** (directional physical evidence)

**Scoring idea (one line)**

```text
GGES(fault) = Support (indicates) + Bonus (distinguishes) - Penalty (contradiction)
```

**Our asset focus:** HT-CH-01 (`C_100`) in `sgp7_dev`, using 1-min telemetry aggregates.

---

## Slide 2 — Fault Nodes, Symptom Nodes, and Edge Types

**Many-to-many, two-layer graph**

```text
Fault  --(indicates / distinguishes)-->  Symptom
```

| Layer | Count (paper) | Examples (names) |
| --- | --- | --- |
| Fault nodes | 6 | Condenser Fouling, Refrigerant Leak, Refrigerant Overcharge, Reduced Condenser Water Flow, Reduced Evaporator Water Flow, Non-Condensable Gases |
| Symptom nodes | 14 | Condenser Pressure Rise, Condenser Flow Drop, Flooding Indicator, Heat Balance Residual |

**Edge types used for GGES scoring**

| Relation | Meaning | Role in score |
| --- | --- | --- |
| `indicates` | Fault is expected to produce this symptom | Adds `weight × confidence` |
| `distinguishes` | Symptom uniquely separates one fault from competitors | Adds `beta × confidence` bonus |

**Why both edges matter**
- Shared symptoms alone cannot separate Non-Condensable Gases vs Refrigerant Overcharge.
- A `distinguishes` edge (Non-Condensable Gases → Discharge Temperature Rise) breaks the tie when discharge temperature rises.

**DB tables in `sgp7_dev`**
- `gges_fault_nodes`
- `gges_symptom_nodes`
- `gges_edges`

---

## Slide 3 — Symptoms, Z-Score, and Confidence Activation

### What defines a Symptom?
In GGES, a **Symptom** is not just a sensor; it is a **Directional Event**.
- **Example:** "Condenser Pressure" is a sensor. "**Condenser Pressure Rise**" is the symptom.
- Physics dictates the direction (Rise or Drop). If the sensor moves as predicted, the symptom is **Supportive**. If it moves opposite, it is **Contradictory**.

### Symptom Activation (z-score basis)
We use **z-scores** (standard deviations from normal) to determine if a symptom is "active."

```text
z = (current_value - normal_mean) / normal_std
a_s = expected_direction × z
```

### Explaining Confidence (conf)
**Confidence** is a value from **0.0 to 1.0** that represents how "sure" we are of the symptom. It filters out noise:

| Activation Magnitude (\( |a_s| \)) | Confidence (\( conf \)) | Meaning |
| :--- | :--- | :--- |
| Below `tau_weak` (0.3) | **0.0** | **Noise Floor:** Ignore tiny deviations. |
| Above `tau_strong` (1.5) | **1.0** | **Saturation:** Full certainty of a physical shift. |
| Between 0.3 and 1.5 | **0.0 to 1.0** | **Linear Scale:** Partial evidence. |

**Key point:** We do not train models for "Subcooling Rise." We calculate the physics feature, convert it to a z-score, and use this **Confidence Activation** to trigger the graph.

---

## Slide 4 — How ASHRAE / Paper Weights Are Arrived At

Weights (`w0`) on `indicates` edges are **expert physics priors**, not data-learned correlations.

**Three-step protocol from the paper**
1. Start from ASHRAE RP-1043 thermodynamic primacy of each fault–symptom link.
2. SME ranking of primary vs secondary vs weak indicators.
3. Keep weights fixed so zero-shot diagnosis of unseen faults remains valid.

**Weight tiers**

| Tier | Weight range | Meaning |
| --- | --- | --- |
| Primary | 7–10 | Must-happen signature (smoking gun) |
| Secondary | 3–6 | Common downstream / partially masked effects |
| Weak | 1–2 | Noisy / incidental support |

**Important separation**
- `indicates` carries `w0` (support strength).
- `distinguishes` does not use a per-edge learned weight; it triggers a global bonus `beta` (paper default 2.0).
- Contradiction uses penalty `gamma` (paper default 0.5) when the sensor moves opposite to physics.

---

## Slide 5 — Graph Built from Tables (Reference Image)

The image below is **generated from the live DB tables**. Symptom boxes show the **symptom name**, direction arrow, and sensor/derived tag.

![GGES Fault–Symptom Knowledge Graph](gges_fault_symptom_graph.jpg)

**How to regenerate the artifact**

```bash
# from graph_experiment/
set PGPASSWORD=<dev_password>
python render_gges_graph.py --out gges_fault_symptom_graph.jpg
```

**Current seed counts (HT-CH-01)**
- 6 faults
- 14 symptoms (8 direct sensors + 6 derived)
- 25 edges

---

## Slide 6 — Traversal Example: Root Cause Selection

**Telemetry (z-scores)**
- Condenser Pressure Rise = +2.0 (\( conf=1.0 \))
- Subcooling Rise = +1.8 (\( conf=1.0 \))
- Discharge Temperature Rise = +2.2 (\( conf=1.0 \))
- Flooding Indicator ≈ 0 (\( conf=0.0 \))

**ROC Score (Overcharge)**
- indicates Pressure Rise: 8.0 × 1.0 = 8.0
- indicates Subcooling Rise: 8.0 × 1.0 = 8.0
- **Total = 16.0**

**NC Score (Non-Condensable Gases)**
- indicates Pressure Rise: 8.0 × 1.0 = 8.0
- indicates Subcooling Rise: 6.0 × 1.0 = 6.0
- indicates Discharge Temp Rise: 8.0 × 1.0 = 8.0
- **distinguishes** Discharge Temp Rise: **beta bonus +2.0**
- **Total = 24.0** (Verdict: NC)

---

## Slide 7 — Autonomous SME Agent Tooling

This GGES framework is designed to be a **Core Tool** for an **Autonomous SME Agent**.

### Workflow Integration
1. **Anomaly Detection:** A specialized model (e.g. Autoencoder or LSTM) monitors all chiller sensors and throws an "Anomaly Alert" when behavior shifts from normal.
2. **Agent Activation:** Our Autonomous SME Agent receives the alert. It doesn't just see "high pressure"; it needs to know "Why?"
3. **GGES Tool Call:** The Agent passes the current sensor z-scores into the **GGES Engine**.
4. **Root Cause Identification:** The GGES Engine traverses the Knowledge Graph and returns:
   - The most likely **Root Cause** (e.g. Condenser Fouling).
   - The **Evidence Score** (GGES).
   - The **Supporting Symptoms** that led to the verdict.
5. **Human-in-the-loop Explanation:** The Agent uses this graph-grounded evidence to explain the fault to the operator with physical certainty.

---

## Slide 8 — Limitations and Framework Extensibility

The current implementation follows the **SSRN-7656122** research paper faithfully, but it is important to recognize its scope:

### Current Limitations
- **Fault Coverage:** Only **6 primary thermodynamic faults** are included (ASHRAE RP-1043 set). It does not yet cover mechanical issues (e.g. bearing wear, oil pump failure).
- **Static Weights:** The expert weights are fixed priors. While robust for zero-shot diagnosis, they don't adapt to specific site variations without manual tuning.
- **Sensor Dependency:** The engine is only as good as the sensors mapped. Missing critical sensors (like discharge temp) reduces the "distinguishing" power of the graph.

### A Physics-Informed Framework
This is not a "black box" model, but a **Framework**.
- **Extensible:** We can add the 7th, 8th, or 100th fault just by adding rows to the `gges_fault_nodes` and `gges_edges` tables.
- **Traceable:** Every diagnosis is 100% explainable by thermodynamic first principles.
- **Zero-Shot Ready:** Can identify faults that have never occurred on this specific chiller before, because the physics is universal.
