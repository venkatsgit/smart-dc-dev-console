# Condenser fouling, severity level 1 — how to read this pack

Chiller **HT-CH-01**. Files start with `cond_fouling_SL1_80pct`.  
Read top to bottom. Each block says what it is, why it is there, and where the number comes from.

---

## 1. The fault first

**What SL means.** SL is severity level. ASHRAE research project 1043 (a published chiller-fault experiment) uses four steps: **SL1, SL2, SL3, SL4**. SL1 is the mildest. SL4 is the dirtiest.

**What SL1 means in this file.** Twelve percent of the condenser tube surface is treated as lost. The field is `surface_loss: 0.12`. It is 12 percent, not 13. The tubes are a bit dirty, not failed.

**Why that matters — the chain in plain steps.**

1. **Job of the condenser.** Hot refrigerant sits inside metal tubes. Cooler water from the cooling towers flows past those tubes. Heat must cross the tube wall into that water and leave the building.
2. **What 12 percent fouling does.** Severity level 1 treats 12 percent of the tube surface as blocked by scale. That blocked part almost stops passing heat. The heat has to squeeze through the remaining 88 percent.
3. **Why the refrigerant runs hotter.** To push the same heat through less good surface, the temperature difference across the tube must grow. The refrigerant side runs hotter. Hotter refrigerant also means higher condenser pressure.
4. **Why the compressor uses more power.** The compressor is the pump that lifts refrigerant from the cold evaporator up to the hot condenser. A hotter, higher-pressure condenser is a taller climb. A taller climb costs more electricity.
5. **How big the effect is at SL1.** On this pack the rise is only a few kilowatts on a machine already near 350 kW. The chiller does not trip. So this file asks: can a detector even notice that small rise?
6. **How SL4 compares.** Severity level 4 treats **45 percent** of the surface as lost (`cond_fouling_SL4_58pct`, field `surface_loss` 0.45). Same chain — hotter condenser, harder compressor — but much stronger.

**How it is applied.** At 22 August 00:00 the physics program sets one knob, condenser fouling resistance, to that 12 percent step, and **holds it for 24 hours**. It does not grow hour by hour. The manifest says this in `scenario.severity_anchor` and `severity_profile` (`kind` is `step`).

**Where this is written.** `cond_fouling_SL1_80pct_manifest.json`:


| Item                | Field                                                               |
| ------------------- | ------------------------------------------------------------------- |
| Fault name          | `scenario.fault` = `chiller.condenser_fouling`                      |
| The knob            | `fault_definitions.targets` = `fouling_resistance` on the condenser |
| 12 percent          | `severity_anchor.surface_loss`                                      |
| Held, not growing   | `severity_anchor.note`                                              |
| If it became severe | `fault_definitions.terminal` = high condenser pressure              |
| Did this run trip?  | `terminal_event` is empty. No.                                      |


References: [ASHRAE RP-1043](https://store.accuristech.com/ashrae/standards/rp-1043-fault-detection-anddiagnostic-fdd-requirements-and-evaluation-toolsfor-chillers?product_id=1716217). An open paper that calls SL1 the early, least severe level: [PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0320563).

---

## 2. What you gave, and what you get back

**What you gave** is one normal operating day from the data center, 21 August 2026. That file is **not in this folder**. You cannot find it by opening the CSVs. The manifest only names it: `background.file` = `site_day_80_background.csv`.

**What you get back** is the twin’s spreadsheet, `cond_fouling_SL1_80pct_sensors.csv`:


|                         |                                                                |
| ----------------------- | -------------------------------------------------------------- |
| Length                  | 48 hours, 2,880 rows, one row per minute                       |
| First 24 hours (21 Aug) | Same entering-water day, **clean** tubes                       |
| Next 24 hours (22 Aug)  | Same entering-water pattern again, **12 percent fouling held** |


Both days are calculated by the twin. Your original file is not pasted in as the first 24 hours.

The numbers still move every minute. “Normal day” here means a real operating day, not a flat line.

---

## 3. The telemetry, and how many of the 83 names matter

**What the 83 are.** Keppel tags: the column names already used for this chiller at the Keppel site. The list is `keppel_tags` in the manifest. The file is `sensors.csv`. “Building tag” in these notes means a Keppel tag.

**They are not 83 physical probes.** Some are meter-style readings, some are formulas, some are copies of the real day, some are building totals.

**How many are useful for this fouling case.**


| Role                          | How many          | Why                                                                                                                                          |
| ----------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Drive the model               | **2**             | Entering evaporator water `CH-EVA-E-TEMP`, entering condenser water `CH-CON-E-TEMP`. Taken from your day.                                    |
| Actually move after the fault | **9** Keppel tags | Power, percent of rated amps, three currents, refrigerant temperature, approach, condenser pressure, kilowatts per ton. Listed in section 8. |
| Do not carry this fault       | the rest          | Context, copies of tags this fault does not change, and building totals.                                                                     |


The twin does **not** need all 83, and it does **not** map all 83 one-to-one onto its internal model.

---

## 4. What “boundary profile” means

**Where.** `scenario.boundary_profile` in the manifest. Its id is `site_day_80`.

**What it is.** The description of the real day the twin must follow. It is not a start time and end time for every sensor, and it is not the allowed range of all 83 tags.

**What this one actually says.**

- The day is **21 August 2026**.
- It was picked because it was a typical day of that fortnight (load about 81 percent).
- Condenser water that day ran from **28.47 °C to 31.00 °C** (mean 29.12 °C). That sentence describes the day. It is not a limit stamped on every column.
- Only **entering chilled water** and **entering condenser water** are copied from the export, one point every **10 minutes**, not smoothed.

**Why.** The twin should live through a real day’s water temperatures, not a made-up flat test. Everything else about the chiller (power, refrigerant temperature, pressure) is calculated, so the fouling can change them.

---

## 5. The twin model, and where the 116 numbers come from

**What the model is.** The vendor’s physics model of HT-CH-01, named in the manifest block `model`:


| Field        | Value                       |
| ------------ | --------------------------- |
| `id`         | `keppel_ht_ch01_validation` |
| `name`       | HT-CH-01 validation harness |
| `graph_hash` | `GF-8783EE06`               |
| Refrigerant  | R1233zd(E)                  |


**What you did not supply.** You did not supply the 116 equations. Your part is the operating day (the two water temperatures, and the tags that get pasted back). Their part is this chiller model. The equations sit in their program. This JSON only names the model and tells it which knob to turn.

**What the 116 are.** The model’s own state, written to `cond_fouling_SL1_80pct_truth.csv` (`truth_columns` in the manifest). They are calculated, not copied from your 83 tags.

**How a row is produced.** Read the two entering-water temperatures for that minute. Solve the evaporator, compressor, condenser, and valve. Store temperatures, pressures, power, refrigerant mass, tube conductance, surge margin, and the fault label. Two of those stored numbers are the water temperatures you fed in. The rest are the model’s answers.

**Why this is not the same as telemetry.** Telemetry is the real chiller as Keppel meters saw it. The 116 are the model’s chiller. Some ideas match a meter (power, refrigerant temperature). Some have no meter (how dirty the tubes are, surge margin, the fault name).

---

## 6. Mapping: 25, 20, 83, and 116 are not the same list

There is **no** one-to-one map from the 83 Keppel tags onto the 116.


| List                           | Count   | What it maps                                                                          | File               |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------- | ------------------ |
| `sensor_schema`                | **25**  | A twin variable → a twin instrument name such as `HT-CH-01-CONDT`, with noise and lag | `twin_sensors.csv` |
| `keppel_tags` class `measured` | **20**  | A twin variable → a Keppel meter name such as `CH-CON-RFT-TEMP`                       | `sensors.csv`      |
| `keppel_tags` all classes      | **83**  | The spreadsheet shape. Only the 20 measured tags point at a twin variable.            | `sensors.csv`      |
| `truth_columns`                | **116** | The model’s own names. No Keppel name on most of them.                                | `truth.csv`        |


The 25 and the 20 overlap in meaning (both can read condensing temperature) but they are two name lists. The 25 do **not** map the other 63 Keppel tags. Formulas, replay, and totals are outside `sensor_schema`.

---

## 7. The four kinds of Keppel column, with examples

Configured in `keppel_tags`. The `class` field says which kind. For a formula, read that tag’s `description`. For a meter, read `source`.

### Measured — twin result renamed to a Keppel tag

**Source of the number:** the twin model variable in `source`, then noise and delay.  
**Not** your original telemetry, except the two driving temperatures, which are telemetry written back out.


| Keppel tag        | Twin variable (`source`) | In your original telemetry?                           |
| ----------------- | ------------------------ | ----------------------------------------------------- |
| `CH-EVA-E-TEMP`   | `T_chw_entering_K`       | Yes. This one is fed in, then written back.           |
| `CH-CON-E-TEMP`   | `T_cw_entering_K`        | Yes. Same.                                            |
| `CH-CON-RFT-TEMP` | `T_cond_K`               | No. The model calculated the refrigerant temperature. |
| `CH-KW_A`         | `power_elec_W`           | No. The model calculated the power.                   |


### Derived — a formula, configured in the manifest

**Source of the formula:** the tag’s `description` inside `keppel_tags`. The twin company wrote the site’s arithmetic there.  
**Source of the numbers inside the formula:** the measured Keppel columns (and sometimes another derived column). Not a second physics solve.


| Keppel tag        | Formula in the manifest                                                     |
| ----------------- | --------------------------------------------------------------------------- |
| `CH-CON-APP-TEMP` | Condenser leaving-water temperature minus condenser refrigerant temperature |
| `CH-KW/RTON`      | `CH-KW_A` divided by cooling tons                                           |
| `CH-L1-A`         | Current from power, voltage, and the site’s phase imbalance                 |


These are not in the raw telemetry as independent sensors. The real site computes the same kind of formula. Here the inputs are the twin’s meters.

### Replay — pasted from telemetry

**Source:** your real day, unchanged. The model does not calculate them. This fouling case does not move them.


| Keppel tag                                               | What it is           |
| -------------------------------------------------------- | -------------------- |
| `CHEM-TK-01-PH`                                          | Chemical tank pH     |
| `CH-OIL-TK-TEMP`                                         | Oil-tank temperature |
| `TOT-DPM-CT-KW`                                          | Cooling-tower power  |
| `CH-CHWP-V-A`, `CH-CHWP-H-A`, `CH-CWP-V-A`, `CH-CWP-H-A` | Pump vibration       |


### Total — building totals rebuilt

**Source:** telemetry for the rest of the plant, plus the twin for HT-CH-01.  
Rule in the descriptions: real site total, **remove the real HT-CH-01**, **insert the simulated chiller**. Headers, other chillers, pumps, and towers stay in the total. These 23 are not a sum of the 20 meters and the 33 formulas.


| Keppel tag        | What it is                                                                     |
| ----------------- | ------------------------------------------------------------------------------ |
| `TOT-DPM-CH-KW`   | Total chiller power, with this simulated machine in place of the real HT-CH-01 |
| `TOT-HDR-CHW-KW`  | Header chilled-water cooling, rebuilt the same way                             |
| `TOT-SYS-KW/RTON` | Whole-plant kilowatts per ton                                                  |


---

## 8. What changes after the fault (maps to the six steps above)

Section 1 is the physics story. This section is what the file records after midnight on 22 August. Same chain.

The program changes **one** thing at 00:00: fouling resistance (12 percent, held 24 hours). Everything else follows. A Keppel tag is listed only after it stays outside the clean-day noise for **10 minutes** (`cascade.departure_test`, `hold_min`). That 10 minutes is a noise rule, not a second stage of fouling.

Source: `cascade.order_observed` and `cond_fouling_SL1_80pct_cascade.csv`.

### After midnight — full detail

| After midnight | Name | What it is | Direction | Visible on Keppel? | Source | Maps to section 1 | Why it moves |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 min | Tube conductance (`cond_UA_W_K`) | How easily heat crosses the condenser tubes | Falls about 12 percent | No — `truth.csv` only | Twin model | Step 2 | This is the knob. 12 percent of the surface is treated as lost, so conductance drops first. |
| 1 min | Surge margin (`surge_margin`) | Room left before the centrifugal compressor stalls. Surge = stall (flow can break down). Margin = safety gap before that stall. High = safe. Falling = closer to the cliff, still running. | Falls a little | No — `truth.csv` only | Twin model | Step 4 | Hotter, higher-pressure condenser = taller climb at the same speed → operating point moves toward the stall line. Drop is small. Run does not trip. Severe case would end at high condenser pressure. SL1 does not. |
| 9 min | `CH-KW_A` | Electrical power of the compressor, in kilowatts | Rise | Yes | Twin meter of `power_elec_W` | Step 4 | Taller lift costs more electricity. First Keppel tag that clears the hold. Rise is only a few kW on a machine near 350 kW (step 5). |
| 9 min | `CH-RLA` | Percent of **rated load amps**. Rated load amps = motor full-load current on the nameplate (here 831 A). So RLA % = average motor current ÷ 831 × 100. Not a separate probe. | Rise | Yes | Formula in `keppel_tags` | Step 4 | More power → higher percent of rated amps. Moves with `CH-KW_A`. |
| 10 min | `CH-L1-A`, `CH-L2-A`, `CH-L3-A` | Motor current on electrical lines 1, 2, and 3, in amps | Rise | Yes | Formula (from power, voltage, phase imbalance) | Step 4 | More power at roughly the same voltage → more current. About one minute after power because the hold test clears slightly later. |
| 11 min | `CH-CON-RFT-TEMP` | Temperature of the refrigerant in the condenser | Rise | Yes | Twin meter of `T_cond_K` | Step 3 | 12 percent of the tube surface is blocked, so the refrigerant is not cooled well enough. Heat cannot leave as easily → refrigerant runs hotter. |
| 15 min | `CH-CON-RFT-PRES` | Pressure of the refrigerant in the condenser | Rise | Yes | Twin meter of `P_cond_Pa` | Step 3 | Temperature and pressure sit on the same saturation line: hotter refrigerant → higher pressure. That higher pressure is the taller climb the compressor must make (step 4). |
| 15 min | `CH-KW/RTON` | Kilowatts per refrigeration ton (electricity per unit of cooling) | Rise | Yes | Formula | Steps 4–5 | More electricity for the same cooling. |
| 15 min | `CH-CON-APP-TEMP` | Approach = temperature gap between refrigerant and water. Wider gap = worse heat exchange. Site formula: leaving-water temperature (`CH-CON-L-TEMP`) **minus** refrigerant temperature (`CH-CON-RFT-TEMP`). | Falls on the Keppel tag | Yes | Formula | Step 3 | Refrigerant gets hotter; leaving water does not rise as much. Water minus hotter refrigerant → logged number falls. The real gap widens; the site’s subtraction has the opposite sign. |

### Physics step → what you see

| Section 1 step | What you see after midnight | On Keppel tags? |
| --- | --- | --- |
| 2. Surface blocked | Tube conductance falls at +1 min | No — truth only |
| 3. Refrigerant hotter | `CH-CON-RFT-TEMP` at +11 min; pressure and approach at +15 min | Yes |
| 4. Compressor works harder | `CH-KW_A` and `CH-RLA` at +9 min; line currents at +10 min; surge margin at +1 min | Power and currents yes; surge margin no |
| 5. Effect is small at SL1 | Few kilowatts, no trip | Yes — that is the point of this pack |

### What happens for the rest of that 24 hours (and why it does not keep climbing)

The fouling is a **step held constant**. At midnight it jumps to 12 percent and stays there until the end of 22 August. It does **not** grow to 13 percent, then 20 percent, then SL4. So after the first ~15 minutes you are not watching a fault that keeps getting worse. You are watching a chiller that has already settled into a **mildly dirty** operating point, still following the day’s entering-water temperatures.

**Right picture.** Right after midnight the meters move (power up, refrigerant temperature up, physics approach gap wider). Within about 15 minutes they have reached the new state that matches “tubes locked at 12 percent.” Then they **stay in that band** for the rest of the dirty day. They do not keep climbing toward a trip.

**Easy mix-up.** That early move is the machine **responding** to a dirt level that is already fully on. It is not the 12 percent surface slowly increasing over 24 hours. The dirt amount is fixed from minute 1.

| Question | Answer |
| --- | --- |
| Do power, refrigerant temperature, and pressure keep rising until hour 48? | No. They shift soon after midnight, then mostly follow the normal day swing (morning vs afternoon load and water temperature). Midday averages can even sit a bit lower than the first hour because the **day** changed, not because the dirt healed. |
| Does the heat-exchange gap stay worse? | Yes. The physics gap (refrigerant hotter relative to the water) stays worse for the whole dirty day, because the tubes stay at 12 percent. On the Keppel tag `CH-CON-APP-TEMP` that shows as a **lower** logged number (water minus hotter refrigerant), not as a rising approach reading. |
| Does surge margin keep falling until the compressor stalls? | No. It steps down a little at minute 1 and stays in a safe band. The machine is closer to the stall line, but still far from surge. |
| Does the chiller trip? | No. `terminal_event` is empty. High condenser pressure is the catalogue ending for a **severe** foul. SL1 never gets there. |
| So what is the “final result” of this pack? | A full dirty day at mild severity: meters stay a bit worse than the clean day (more power, hotter refrigerant, higher pressure, worse exchange), the compressor does **not** surge or trip, and the file ends with the machine still running. |

---

## 9. The path in one picture

```
Your telemetry day                         NOT in this folder
    boundary profile = which day,
    and the two entering-water temperatures
            |
            v
Vendor chiller model of HT-CH-01          manifest block "model"
    one knob: 12 percent fouling at midnight, held 24 h
            |
            v
116 internal numbers                       truth.csv
            |
            +-- 25 twin instrument names   sensor_schema  -> twin_sensors.csv
            |
            +-- 20 Keppel meter names      keppel measured -> sensors.csv
            +-- 33 formulas                keppel derived description
            +-- 7 pasted from telemetry    keppel replay
            +-- 23 rebuilt plant totals    keppel total
            |
            v
83 Keppel columns, 48 hours                sensors.csv
```

