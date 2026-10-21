# R2F labeling: classification, t_event, and RUL

Scope for this note: **80% load pack only** (`../80/`). Leave the 58% pack out.

Two-stage model:

1. **Classify** the failure family.
2. **Estimate remaining useful life (RUL)** until a named event, given that class.

Healthy (`healthy_80pct`) is the no-fault reference. It is a class for stage 1 and always censored for stage 2.

`drop` is a stage-1 class. It means **do not name a fault family**, and do not estimate time to failure. It is not a label for “something is wrong.”

It covers two opposite stretches of a fault file:

1. **Before the meters move.** From `t_inject` until `t_visible`. The knob is already on, but the Keppel tags still look like the clean day. Calling this `cond_fouling` or `gas_leak` would teach a signature that is not visible yet.
2. **After the machine has tripped.** The failure has already happened. These minutes are not a running fault, and there is no remaining life left to estimate.

The classifier is trained to output `drop` the same way it outputs `healthy` or `gas_leak`. On live telemetry, split the two meanings with the chiller’s running state. Still running and `drop`: wait for a later window. Already off and `drop`: the trip is in the past. In either case, do not call the survival model.

---

## 1. Scenario families (stage 1 classes)

| Class | Packs |
| --- | --- |
| `healthy` | `healthy_80pct`, and every fault pack **before** fault injection. Also an allowed label for `t_inject` → `t_visible` if you do not want a separate `drop` class. |
| `drop` | Do not name a fault family. Two stretches: `t_inject` → `t_visible` (fault on, meters still look clean), and every minute **after trip** (machine already off). Not “something is wrong,” and not an input to the RUL model. |
| `cond_fouling` | SL1 → SL4 |
| `evap_fouling` | SL1 → SL4 |
| `gas_leak` | slow → moderate |
| `liquid_leak` | slow → moderate |

Severity (SL1 vs SL4, slow vs moderate) is **not** the first label. It only changes how fast the signature develops.

There is **one classification model**. It is trained on every 80% pack. Its label set is the six names above. SL2 is not a different class from SL1. A slow leak is not a different class from a moderate leak.

---

## Worked samples

Read this section before the rest. It is the same rules as above, written as rows you could put in a training file.

### What `drop` means, on a real row

`drop` means **do not name a fault family**. It does not mean “something is wrong.”

Two stretches get this label. They look different if you know the machine state.

| Stretch | Example row | What is true | Class | Call the RUL model? |
| --- | --- | --- | --- | --- |
| Fault is on, meters still look clean | Gas leak, moderate, `2026-08-22T00:30` (30 min after injection; first Keppel move is at +69 min) | Hole is open. `CH-KW_A` has not left the clean-day noise yet. | `drop` | No |
| Machine has already tripped | Gas leak, moderate, `2026-08-22T18:00` (trip was at +17.6 h) | Failure is in the past. Chiller is off. | `drop` | No |

A row on 21 Aug in that same gas-leak file is **`healthy`**, not `drop`. The hole is not open yet.

### One classification dataset

Every row is one time window of Keppel sensors from `../80/*_sensors.csv`. The label is only the class. Severity stays in the file name so you can see it. It is not a column the classifier predicts.

`t_visible` below is the first Keppel tag that clears the cascade hold in that pack.

| Pack | Family class once meters have moved | `t_visible` | Trip |
| --- | --- | --- | --- |
| `healthy_80pct` | `healthy` the whole file | none | none |
| `cond_fouling_SL1_80pct` | `cond_fouling` | +9 min (`CH-KW_A`) | none |
| `cond_fouling_SL2_80pct` | `cond_fouling` | +5 min (`CH-KW_A`) | none |
| `cond_fouling_SL3_80pct` | `cond_fouling` | +3 min (`CH-CON-RFT-TEMP`) | none |
| `cond_fouling_SL4_80pct` | `cond_fouling` | +2 min (`CH-CON-APP-TEMP`) | none |
| `evap_fouling_SL1_80pct` | `evap_fouling` | +2 min (`CH-EVA-APP-TEMP`) | none |
| `evap_fouling_SL2_80pct` | `evap_fouling` | +1 min (`CH-EVA-RFT-TEMP`) | none |
| `evap_fouling_SL3_80pct` | `evap_fouling` | +1 min (`CH-EVA-APP-TEMP`) | none |
| `evap_fouling_SL4_80pct` | `evap_fouling` | +1 min (`CH-CHWST`) | none |
| `leak_gas_slow_80pct` | `gas_leak` | +185 min (`CH-KW_A`) | +52.6 h |
| `leak_gas_moderate_80pct` | `gas_leak` | +69 min (`CH-KW_A`) | +17.6 h |
| `leak_liquid_slow_80pct` | `liquid_leak` | +187 min (`CH-KW_A`) | +53.1 h |
| `leak_liquid_moderate_80pct` | `liquid_leak` | +69 min (`CH-KW_A`) | +17.8 h |

Sample rows. `X` stands for the sensor window. All of these rows go into **the same** classifier.

| episode | Event time | X | class | Why this class |
| --- | --- | --- | --- | --- |
| `healthy_80pct` | 21 Aug 12:00 | window | `healthy` | No fault in this file. |
| `cond_fouling_SL1_80pct` | 21 Aug 12:00 | window | `healthy` | Fault file, but injection is still tonight. |
| `cond_fouling_SL1_80pct` | 22 Aug 00:04 | window | `drop` | Fouling is on. First meter move is +9 min. |
| `cond_fouling_SL1_80pct` | 22 Aug 00:20 | window | `cond_fouling` | Past +9 min. Same label you would use for SL4. |
| `cond_fouling_SL4_80pct` | 22 Aug 00:01 | window | `drop` | SL4 moves faster (+2 min), but this minute is still before that. |
| `cond_fouling_SL4_80pct` | 22 Aug 12:00 | window | `cond_fouling` | Dirtier than SL1. The class is still condenser fouling. No trip later in the file. |
| `evap_fouling_SL1_80pct` | 22 Aug 00:10 | window | `evap_fouling` | Past +2 min. |
| `evap_fouling_SL4_80pct` | 22 Aug 08:00 | window | `evap_fouling` | Higher severity, same class. |
| `leak_gas_moderate_80pct` | 22 Aug 00:30 | window | `drop` | 30 min in. Visible only at +69 min. |
| `leak_gas_moderate_80pct` | 22 Aug 06:00 | window | `gas_leak` | Meters have moved. Machine still running. |
| `leak_gas_moderate_80pct` | 22 Aug 18:00 | window | `drop` | Trip was at +17.6 h. Machine is off. |
| `leak_gas_slow_80pct` | 22 Aug 02:00 | window | `drop` | Slow leak is not visible until +185 min. |
| `leak_gas_slow_80pct` | 22 Aug 06:00 | window | `gas_leak` | Same class as the moderate leak. It just trips much later (+52.6 h). |
| `leak_liquid_moderate_80pct` | 22 Aug 06:00 | window | `liquid_leak` | Different family from the gas leak. |
| `leak_liquid_slow_80pct` | 22 Aug 02:00 | window | `drop` | Visible only at +187 min. |
| `leak_liquid_slow_80pct` | 22 Aug 06:00 | window | `liquid_leak` | Same class as the moderate liquid leak. |

### One RUL dataset, and how many models

The RUL model does **not** take the class as its only input. Each training row is:

| Column | What it is |
| --- | --- |
| `X` | The same Keppel sensor window the classifier used |
| `class` | Copied from the classifier label, so you can filter |
| `delta` | 1 if this episode’s trip is in the file, 0 if the file ends with the machine still running |
| `rul_min` | Minutes from this row until the trip, only when `delta` = 1 |

**One RUL model**, not one per class and not one per severity. Train it only on rows whose class is `gas_leak` or `liquid_leak` and whose machine is still running. Those are the only rows in this pack that have a trip to predict. Healthy, `drop`, condenser fouling, and evaporator fouling stay out of this file. Fouling never trips here, so there is no fouling RUL target.

Slow and moderate leaks go into that **same** model. A slow leak at +6 h still has about two days left. A moderate leak at +6 h has about 12 hours left. The sensor window is what tells those apart. The class column is only there so you know both leak families are allowed in.

Sample rows for that one model. RUL minutes use the trip times above (moderate gas 17.6 h, slow gas 52.6 h, moderate liquid 17.8 h, slow liquid 53.1 h).

| episode | Event time | class | delta | rul_min | In the RUL training file? |
| --- | --- | --- | --- | --- | --- |
| `healthy_80pct` | 21 Aug 12:00 | `healthy` | 0 | — | No |
| `cond_fouling_SL1_80pct` | 22 Aug 00:20 | `cond_fouling` | 0 | — | No. Dirty and still running. No trip in the file. |
| `cond_fouling_SL4_80pct` | 22 Aug 12:00 | `cond_fouling` | 0 | — | No. Same reason at higher severity. |
| `evap_fouling_SL4_80pct` | 22 Aug 08:00 | `evap_fouling` | 0 | — | No |
| `leak_gas_moderate_80pct` | 22 Aug 00:30 | `drop` | — | — | No. Do not teach “time to trip” on a window that still looks healthy. |
| `leak_gas_moderate_80pct` | 22 Aug 06:00 | `gas_leak` | 1 | 696 | Yes. 17.6 h − 6 h. |
| `leak_gas_moderate_80pct` | 22 Aug 17:00 | `gas_leak` | 1 | 36 | Yes. 17.6 h − 17 h. Same episode, shorter RUL, different sensors. |
| `leak_gas_moderate_80pct` | 22 Aug 18:00 | `drop` | — | — | No. Already tripped. |
| `leak_gas_slow_80pct` | 22 Aug 06:00 | `gas_leak` | 1 | 2796 | Yes. 52.6 h − 6 h. Same model as the moderate row above. |
| `leak_liquid_moderate_80pct` | 22 Aug 06:00 | `liquid_leak` | 1 | 708 | Yes. 17.8 h − 6 h. Same model. |
| `leak_liquid_slow_80pct` | 22 Aug 06:00 | `liquid_leak` | 1 | 2826 | Yes. 53.1 h − 6 h. Same model. |

On live telemetry: run the **one** classifier. If it says `gas_leak` or `liquid_leak`, pass that same sensor window to the **one** leak RUL model. If it says `healthy`, `drop`, `cond_fouling`, or `evap_fouling`, stop. There is no second model to call.

---

## 2. Which files are X, which are labels

| File | Used as model input? | Role |
| --- | --- | --- |
| `*_sensors.csv` | **Yes — this is X** | Keppel tags a live site would have. Training features and prediction input both come from here. |
| `*_cascade.csv` | **No** | Offline analysis: which tags left the clean-day noise, at which minute, rise/fall. Use it to **pick columns** and to set `t_visible`. Do not feed it at train or predict time. |
| `*_truth.csv` | **Labels / clocks only** | Twin internals (`label.fault_ids`, `cond_UA_W_K`, subcooling, trip physics). Use for **episode class from the manifest**, trip time, and debugging. At prediction you do **not** have this file. |
| `*_manifest.json` | Metadata | `scenario.fault`, `severity_profile.kind`, `terminal_event`. |
| `*_twin_sensors.csv` | Optional | Generic twin names; not the live Keppel feature set. |

**Do not copy `truth.csv` `label.fault_ids` onto every minute.** In `cond_fouling_SL1_80pct_truth.csv` that field is `chiller.condenser_fouling` even on **21 Aug** (clean day). The physics knob only turns at **22 Aug 00:00**. Use the **clock**, not that pack-level label.

---

## 3. Fault clock (example: condenser fouling SL1)

From `cond_fouling_SL1_80pct_sensors.csv` / the SL1 detail note:

- **21 Aug 00:00 → 22 Aug 00:00** (first 1,440 minutes): **clean** — same entering-water day, no fouling.
- **22 Aug 00:00 onward**: fault **starts**. One row per minute; time column is `Event time`.

Same injection midnight applies to the other 80% fault packs. Healthy has no injection.

---

## 4. Three clocks on every run

Fouling is a **step**; meters lag. A leak is a **ramp of hole area**, then charge keeps falling until trip. Those are different “final states.” Stamp each 1-minute row using three times, not one class for the whole file.

| Clock | Meaning | SL1 cond fouling (12%) | Moderate gas leak |
| --- | --- | --- | --- |
| `t_inject` | Knob changes (dirt step / hole starts opening) | 22 Aug 00:00 | 22 Aug 00:00 |
| `t_visible` | First **Keppel** tag stays outside noise (`cascade`, ~10 min hold) | ~+9 min (`CH-KW_A`) | ~+69 min (`CH-KW_A`; subcooling in truth at +59 min, not a site meter) |
| `t_event` | The ending used for RUL | **None** (settled dirty, no trip) | **Trip** ~+17.6 h (`terminal_event` = `loss_of_charge` on `superheat_K`) |

How to read “takes time to reach the final state”:

- **Fouling:** final *severity* is already 12% at minute 1 of 22 Aug (`severity_profile.kind` = `step`). Keppel meters take ~15 min to **show** it, then they stay in that band. `terminal_event` is **null** even at SL4 in this 80% pack.
- **Leak:** hole size is the knob (full size ~+72 min on moderate gas). **Charge keeps falling** until trip. There is no settled “leak state” before the trip.

So each minute needs **two labels**: class (stage 1) and event / RUL (stage 2).

---

## 5. How to label for classification

Never mark the whole CSV as the fault.

**Default rule for a first classifier:**

| Minutes | Class label | Why |
| --- | --- | --- |
| Before `t_inject` (21 Aug on fault packs; all of `healthy_80pct`) | `healthy` | Same water day, fault off. |
| `t_inject` → `t_visible` | `drop` or `healthy` | Default is `drop`: knob on, site meters still look like yesterday, so this is not a fault family. `healthy` is the other allowed label for this same window. Do not leave the minutes blank, and do not call them `cond_fouling` or `gas_leak`. |
| After `t_visible` until end of run (or last running minute before trip) | family name (`cond_fouling`, `evap_fouling`, `gas_leak`, `liquid_leak`) | Signature is on the sensors the live model will see. |
| After trip | `drop` | Machine already off. Same label as the pre-visible window: do not name a fault family. The trip is in the past, so there is no RUL. |

Worked cases:

- **SL1 fouling:** 00:00–00:08 is `drop` (or `healthy`). Start `class = cond_fouling` from ~00:09 (or from 00:15 if you wait until pressure/approach also move). All later 22 Aug minutes stay `cond_fouling` — the 12% is already the final dirt level.
- **Moderate gas leak:** 00:00–01:08 is `drop` (or `healthy`). `class = gas_leak` from the first **visible** Keppel move (~+69 min) through the last running minute before trip. After the trip, `class = drop`.

If you need more leak samples in the “early, almost invisible” stretch, treat them as **weak labels** or a separate head (`fault_injected = 1` from manifest/truth), not as the same class as “looks like a leak on meters.”

### Feature columns (cascade picks them; sensors supply values)

Do not dump all 83 tags. For condenser fouling SL1, cascade tags that clear the hold include:

`CH-KW_A`, `CH-RLA`, `CH-L1-A` / `CH-L2-A` / `CH-L3-A`, `CH-CON-RFT-TEMP`, `CH-CON-RFT-PRES`, `CH-KW/RTON`, `CH-CON-APP-TEMP`

Drivers that do **not** encode the fault: `CH-EVA-E-TEMP`, `CH-CON-E-TEMP` (boundary). Replay/totals (pH, pump vibration, plant totals) stay out.

Other families: take the Keppel tags that actually depart in **that** pack’s `*_cascade.csv`. Union of departing tags across families is a reasonable shared feature list.

### One training row

One training row = one time **window** of Keppel sensors (for example 30 minutes, 1-minute samples), plus a class from the rule above.

Flatten the window (30 × N tags) **or** use summary stats (mean, delta vs 21 Aug same minute, slope).

- Same window on `healthy_80pct_sensors.csv` → `healthy`
- Fault packs from `t_inject` until `t_visible` → `drop` or `healthy`
- Fault packs after `t_visible` → family class
- Slide the window on the **visible, still-running** stretch only. Do not mix 21 Aug rows into the fouling/leak class.

### Prediction input

**Same shape as X only.** No cascade file, no truth file. A 30-minute slice of the same Keppel columns from live telemetry (or a held-out `sensors.csv` window).

Output: class probabilities over `{healthy, drop, cond_fouling, evap_fouling, gas_leak, liquid_leak}`.

---

## 6. t_event and RUL for the survival model

This is **not** the class name. It is time left to a **named** event.

For each minute `t` after inject, while the machine is still running:

```text
RUL(t) = t_event - t
```

and a censor flag `delta`.

| Pack | `t_event` | At a 1-min row | `delta` |
| --- | --- | --- | --- |
| Gas / liquid leak | `terminal_event` (protection trip, `loss_of_charge` on `superheat_K` in the 80% leaks) | e.g. moderate gas leak at +2 h, RUL ≈ 15.6 h; at +17 h, RUL ≈ 0.6 h | 1 (event observed) |
| Cond / evap fouling SL1–SL4 | **no trip** in this 80% pack | RUL to trip is **undefined** | 0 (censored at end of file) |
| Healthy | no event | censored | 0 |

**Do not** set RUL = 0 on every 22 Aug fouling minute. The chiller has not reached a failure end state; it has reached a **dirty running** state.

Optional extra event for fouling only: time to **visible** (9–15 min on SL1). That is **detection latency**, not remaining useful life. Keep it on a separate head if you need it.

Leaks: `severity_profile.kind` is `ramp`; hole stays open; machine trips. Fouling: `kind` is `step`; dirt is held; `terminal_event` is null even at SL4. Mixing those two clocks in one RUL head will give nonsense times. Train **class-conditional** survival (or competing risks with a clearly named event per cause).

Censoring is required: healthy and all fouling SL1–SL4 never fail in these files.

If you later want fouling RUL-to-trip, you need ramp-to-terminal fouling runs. This 80% set does not have them.

---

## 7. How one 1-minute row looks

**Cond fouling SL1**, `Event time` = `2026-08-22T00:20` (after `t_visible`):

| Field | Value |
| --- | --- |
| X | that minute’s (or a 30-min window ending here) Keppel tags |
| `class` | `cond_fouling` |
| `event_trip` | 0 (censored) |
| `rul_trip_min` | NA |
| `minutes_since_inject` | 20 |

**Moderate gas leak**, `2026-08-22T06:00` (~+6 h):

| Field | Value |
| --- | --- |
| X | sensors at that minute / window |
| `class` | `gas_leak` |
| `event_trip` | 1 (trip will occur) |
| `rul_trip_min` | about 17.6 × 60 − 360 ≈ 696 |
| `minutes_since_inject` | 360 |

Same leak file at `2026-08-21T12:00`: **`class = healthy`**, RUL censored. The leak has not started.

Survival table (one row per window or per minute used in training):

| Column | Meaning |
| --- | --- |
| `episode_id` | e.g. `cond_fouling_SL1_80pct` |
| `t` | minutes since `t_inject` (or since window start — pick one and keep it) |
| `class` | stage 1 label (`healthy`, `drop`, or a fault family) |
| `event_time` | `t_event` if observed |
| `delta` | 1 = event observed, 0 = censored |
| `rul` | `t_event - t` when `delta` = 1; else time to end of observation |
| X | sensor window / features |

Libraries that consume this shape: `lifelines`, `scikit-survival` (`sksurv`), `pycox` / DeepHit (competing risks).

---

## 8. Why “wait for the final state” is the wrong class rule

If you only labelled the **last** minutes (trip, or end of dirty day):

- **Fouling:** last 24 h all look the same mildly dirty band. Including from +15 min onward is correct; waiting for a worse end state never comes.
- **Leak:** last minutes are **starved / about to trip**. That is a different signature from +2 h (almost normal power, falling subcooling in truth only). A classifier trained only on the trip hour will miss early leaks.

So for **class**: label the whole **visible-and-still-running** stretch as that family.

For **RUL**: every one of those minutes gets a **different** time-to-trip (leaks) or is **censored** (fouling / healthy).

---

## 9. Practical default (what to implement first)

1. Use only `../80/`.
2. Split each fault CSV at **22 Aug 00:00**. Before = `healthy`.
3. Read first Keppel `departs_at_min` from `*_cascade.csv` → `t_visible`.
4. `class` = family name from manifest `scenario.fault` for rows with `Event time` ≥ `t_visible` and machine still running.
5. Label `t_inject` → `t_visible` as `drop` or `healthy`. Keep the rows. `drop` means do not name a fault family, and do not estimate RUL.
6. If `terminal_event` exists, `rul_trip = t_trip - t` and `delta` = 1; else censored at end of file. After the trip, `class` = `drop`.
7. Never use `truth.csv` `label.fault_ids` as the per-minute class.
8. Predict with sensors only, same window length and columns as training.

---

## 10. Two-stage inference

```
sensor window
    → Stage 1: P(class) ∈ {healthy, drop, cond_fouling, evap_fouling, gas_leak, liquid_leak}
    → Stage 2: remaining time to named event | class
```

Example outputs:

- “This looks like a **gas leak** (p = 0.8). Median time to **trip** is ~X hours (P10–P90).”
- If stage 1 says fouling: “detectable / already at a dirty setpoint; **no trip in this 80% corpus** (censored).”
- If stage 1 says `drop`: do not estimate a failure time. Still running means the window is in the pre-visible gap. Already off means the trip has already happened.

Joint alternative later: competing risks (cause = class, cumulative incidence = time to that cause’s event). Two-stage is easier to debug with 13 packs.

Suggested models: any tabular classifier first (RF / gradient boosting); then class-conditional Random Survival Forest / GB survival / Cox; DeepHit if joining cause + time.

Metrics: class F1 / confusion matrix; survival C-index, time-dependent AUC, integrated Brier score, calibration. Split by **episode**, not by random minutes.

---

## 11. What this pack can and cannot support

| Goal | 80% pack as-is |
| --- | --- |
| Classify the four families vs healthy | Yes |
| RUL to **trip** for leaks | Yes (all four leak runs trip) |
| RUL to **trip** for fouling | No — none trip |
| One survival model for “failure of any kind” | Only if the event is defined separately per family |

See also:

- [../_analysis/80/README.md](../_analysis/80/README.md) — scenario index
- [../_analysis/80/cond_fouling_SL1_80pct_detail.md](../_analysis/80/cond_fouling_SL1_80pct_detail.md) — step fouling, no trip
- [../_analysis/80/leak_gas_moderate_80pct_detail.md](../_analysis/80/leak_gas_moderate_80pct_detail.md) — ramp leak, trip ~17.6 h
