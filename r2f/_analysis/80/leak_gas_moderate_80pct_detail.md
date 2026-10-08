# Refrigerant leak (discharge gas), moderate rate — how to read this pack

Chiller **HT-CH-01**. Files start with `leak_gas_moderate_80pct`.  
Read top to bottom. Each block says what it is, why it is there, and where the number comes from.

---

## 1. The fault first

**What “moderate” means.** This is a **leak rate**, not a fouling severity level. ASHRAE RP-1043 defines undercharge at 10, 20, 30, and 40 percent charge lost. **Moderate** means the hole is sized so that, at the design condition, the machine loses about **5 percent of its charge per hour**, reaching the **40 percent** milestone in about **8 hours**.

**What this file actually does.** At 22 August 00:00, the model opens one hole on the **discharge side**: hot gas leaving the compressor, still at condenser pressure, before it becomes liquid again. The only control is `vapour_leak_area` on the condenser. The hole is about **20.4 mm²** (about 5.1 mm across), which at design pressure and density leaks about **57.5 kg/h** — 5 percent of the ~1150 kg charge per hour.

**Why this hole loses mass slowly.** Liquid and vapour at the same pressure do not have the same density. Discharge gas is about **thirty times less dense** than liquid refrigerant, so the same-size hole lets much less refrigerant escape by mass. The condenser liquid pool therefore shrinks slowly. High-side meters can look almost normal for a long time even though the machine is already losing the refrigerant it needs to keep cooling.

**Why that matters — the chain in plain steps.**

1. **What a healthy charge is doing.** The chiller is a closed loop containing a fixed amount of refrigerant. In the evaporator, liquid boils and removes heat from the building water. The vapour then leaves the evaporator and enters the compressor. The compressor raises its pressure. In the condenser, tower water cools the hot gas until it becomes liquid again and cools that liquid a few degrees below its boiling point. That margin is **subcooling**. It exists while there is enough liquid stored in the condenser. The expansion valve then sends that liquid back to the evaporator. If nothing leaks, the refrigerant mass stays constant and both vessels remain properly filled.

   The mass that has to be maintained is those two stored pools, not the flow through the compressor. At the start of this run the model holds about **1150 kg**. About **810 kg** of that sits in the evaporator (level about 0.42), which is what keeps the tubes wet. About **270 kg** sits as liquid in the condenser (level about 0.19), which is what produces the subcooling. The compressor only circulates the vapour that boils off, about **20 kg each second**. That circulation can still look normal while one of the stored pools is already shrinking.
2. **What the hole removes.** The hole vents hot, high-pressure gas from the loop. The refrigerant mass keeps falling while the hole is open: rate of change of charge = minus leak flow. The scenario sets only the hole area. Refrigerant density and condenser pressure determine how many kilograms per hour actually escape.
3. **Why subcooling falls.** The hole removes gas, so the liquid pool does not disappear immediately. The kilograms leave the condenser pool first. Over the first 4 hours that pool falls from about **270 kg to about 80 kg**, and its level falls from about 0.19 to about 0.05. The evaporator is still near **800 kg** in that same stretch, so the tubes there are still covered. A shallower condenser pool cannot be cooled as far below its boiling point. **Subcooling therefore falls** (about 4.3 °C down toward 1.2 °C). In this run, it is the first signal to leave the noise band (+59 min). It exists only in `truth.csv`. Keppel has no subcooling meter.
4. **Why power rises while the machine still looks full.** **Pressure lift** is the climb from evaporator pressure up to condenser pressure. On the clean morning the evaporator is near **92 kPa** and the condenser near **185 kPa**, so every kilogram is raised by about **90 kPa**. That is a pressure ratio of about **2**. The same climb is stored in the model as `lift_K`: about **20 °C** between the cold boiling temperature and the hot condensing temperature. Compressor power is the kilograms per second making that climb, times the energy each kilogram needs to climb it, divided by efficiency. Same flow and a taller climb means more kilowatts. Less flow and the same climb means fewer kilowatts.

   For the first few hours the climb barely changes. Both pressures stay close to the clean day, evaporator mass is still about 800 kg, and flow is still about 20 kg/s. At +69 min, power is only about **1 kW** above the same minute of the clean day. It clears the noise test then because the shift is steady. It is not yet a 44 kW rise, and the barrel is not empty.

   The large rise comes once the evaporator pool starts to empty and its pressure falls, while condenser pressure is still near 185 kPa. The bottom of the climb drops and the top does not, so the climb gets taller. The gap versus the clean day peaks near **+43 kW at about 11 hours**. At that hour the pressure ratio is about **2.14** instead of **2.0**, `lift_K` is about **22 °C**, flow is still near **19 kg/s**, and cooling is still close to the clean day. Almost the same amount of vapour simply costs more electricity. That is the harder lift.

   After about 14 hours the evaporator level is near the bottom. Flow falls from about 20 kg/s to about **8 kg/s** at the trip, and power comes back down even though the pressure ratio is still high. Fewer kilograms per second means fewer kilowatts. The same pattern shows on percent of rated amps, line current, and kilowatts per ton.
5. **Why the expansion valve opens.** Level control tries to keep liquid covering the evaporator tubes. As the condenser pool shrinks, less liquid is available to send through the system, and evaporator level starts to fall. The valve opens to maintain the level and eventually reaches its maximum travel. Valve position is inside the model (+203 min), not a Keppel tag.
6. **Why the evaporator starves and the machine trips.** Once the tubes become uncovered, four things follow from the same loss of liquid. Boiling moves to a lower temperature, so evaporator pressure also falls (saturation links pressure and temperature). The water is no longer cooled properly, so leaving chilled-water temperature rises and cooling capacity falls. Vapour leaving a dry tube also becomes much hotter; **superheat** is the difference between suction temperature and boiling temperature. Wet tubes mean a few degrees. Dry tubes mean tens of degrees. Protection alarms when superheat reaches 18 °C (about 14.7 h) and trips when it stays above 25 °C for five minutes (about 17.6 h). The trip is caused by loss of charge: the evaporator bundle is no longer properly covered. Condenser temperature and pressure on the meters fall only later (~12 h), when there is clearly much less vapour left to condense.

**How it is applied — the hole opens, then the physics drains the machine.**

* `severity_profile.kind` is **`ramp`**. The ramp is the **hole area**, not the charge.
* The hole grows from closed to full size over the first **1.2 hours** (`duration_s` = 4320 s), which is 15 percent of the 8-hour design path to 40 percent loss. After that, the area stays fixed.
* The refrigerant does not stop leaking when the hole area stops growing. Gas continues to escape through the open hole until protection trips. The meters therefore keep changing for the rest of the fault.
* `stop_on` is `trip`. The recipe allows up to 18 hours (`run.duration_s` = 64800). The trip arrives at about **17.6 hours** after midnight, with about **87.5 percent** of the charge gone — well beyond the 40 percent sizing milestone.


**Where this is written.** `leak_gas_moderate_80pct_manifest.json`:


| Item               | Field                                                                     |
| ------------------ | ------------------------------------------------------------------------- |
| Fault name         | `scenario.fault` = `chiller.refrigerant_leak_discharge`                   |
| The knob           | `fault_definitions.targets` = `vapour_leak_area` on the condenser         |
| Rate class         | `severity_anchor.rate_class` = moderate, 5 %/h, 8 h to SL4 milestone      |
| Orifice size       | `severity_anchor.valve.area_mm2` ≈ 20.4                                   |
| Opens then holds   | `severity_anchor.note` + `severity_profile.kind` = `ramp`                 |
| Catalogue ending   | `fault_definitions.terminal` = `low_evaporator_pressure`                  |
| Did this run trip? | `terminal_event` = protection `loss_of_charge` on `superheat_K` — **yes** |


The catalogue ending and the trip that actually fired are the same starvation. Low evaporator pressure is what the fault definition names. This run’s protection logic stops the machine on suction superheat.

References: [ASHRAE RP-1043](https://store.accuristech.com/ashrae/standards/rp-1043-fault-detection-anddiagnostic-fdd-requirements-and-evaluation-toolsfor-chillers?product_id=1716217) (undercharge milestones 10/20/30/40 % charge loss). The pack uses those percentages to size the leak rate. This run does not stop at 40 percent.

---

## 2. What you gave, and what you get back

**What you gave** is one normal operating day from the data center, 21 August 2026. That file is **not in this folder**. You cannot find it by opening the CSVs. The manifest only names it: `background.file` = `site_day_80_background.csv`.

**What you get back** is the twin’s spreadsheet, `leak_gas_moderate_80pct_sensors.csv`:


|                         |                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------- |
| Length                  | **Not** a full 48 hours. About **2,507** Keppel rows (~41.8 h), one row per minute |
| First 24 hours (21 Aug) | Same entering-water day, **no leak**                                               |
| From 22 Aug 00:00       | Hole opens, charge drains, until **trip ~17:36**                                   |
| After the trip          | Machine unavailable; file ends shortly after (~17:46)                              |


Both days are calculated by the twin. Your original file is not pasted in as the first 24 hours. Sample count in the manifest (`counts.samples` = 2509) matches a run that **stops on trip**, not a fixed 48-hour wall clock.

The numbers still move every minute. “Normal day” here means a real operating day, not a flat line. On 22 August the entering-water temperatures keep following that day while the refrigerant inventory falls underneath them.

---

## 3. The telemetry, and how many of the 83 names matter

**What the 83 are.** Keppel tags: the column names already used for this chiller at the Keppel site. The list is `keppel_tags` in the manifest. The file is `sensors.csv`. “Building tag” in these notes means a Keppel tag.

**They are not 83 physical probes.** Some are meter-style readings, some are formulas, some are copies of the real day, some are building totals.

**How many are useful for this leak case.**


| Role                          | How many                                                                          | Why                                                                                                                                                                     |
| ----------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Drive the model               | **2**                                                                             | Entering evaporator water `CH-EVA-E-TEMP`, entering condenser water `CH-CON-E-TEMP`. Taken from your day.                                                               |
| Actually move after the fault | **many** (~45+ Keppel tags clear the cascade hold; 49 departures including truth) | Power, currents, kW/ton early; evaporator pressure/temperature and approach mid-run; leaving chilled water and capacity late; plant totals follow. Listed in section 8. |
| Truth-only signatures         | several                                                                           | `charge_kg`, `subcooling_K`, `exv_position`, `superheat_K` — in `truth.csv` / cascade, not Keppel meters.                                                               |
| Do not carry this fault       | the rest                                                                          | Context, copies of tags this fault does not change, and some building totals that stay in noise.                                                                        |


The twin does **not** need all 83, and it does **not** map all 83 one-to-one onto its internal model.

The four truth-only names above are the physics of the leak itself: how much refrigerant is left, whether the condenser still has a liquid pool, how far the expansion valve has opened, and how dry the evaporator tubes are. Keppel sees the consequences (power, pressures, leaving water), not those four internals.

---

## 4. What “boundary profile” means

**Where.** `scenario.boundary_profile` in the manifest. Its id is `site_day_80`.

**What it is.** The description of the real day the twin must follow. It is not a start time and end time for every sensor, and it is not the allowed range of all 83 tags.

**What this one actually says.**

- The day is **21 August 2026**.
- It was picked because it was a typical day of that fortnight (load about 81 percent).
- Condenser water that day ran from **28.47 °C to 31.00 °C** (mean 29.12 °C). That sentence describes the day. It is not a limit stamped on every column.
- Only **entering chilled water** and **entering condenser water** are copied from the export, one point every **10 minutes**, not smoothed.

**Why.** The twin should live through a real day’s water temperatures, not a made-up flat test. Those two temperatures are the heat source and the heat sink. Charge, power, pressures, and the trip are what the refrigerant loop does between them once the hole is open.

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

**What the 116 are.** The model’s own state, written to `leak_gas_moderate_80pct_truth.csv` (`truth_columns` in the manifest). They are calculated, not copied from your 83 tags.

**How a row is produced.** Read the two entering-water temperatures for that minute. Set the hole area from the ramp (growing for 1.2 h, then fixed). Subtract the gas that left through the hole from the refrigerant mass. Solve the evaporator, compressor, condenser, and expansion valve with whatever mass is left. Store temperatures, pressures, power, charge, subcooling, superheat, valve position, and the fault label. Two of those stored numbers are the water temperatures you fed in. The rest are the model’s answers.

**Charge on this run (conservation).** Start mass ≈ **1150 kg**. End mass ≈ **144 kg** (~**87.5 percent** lost by trip). The 8-hour / 40 percent figure only sized the hole. The hole stayed open, so the mass balance kept integrating the leak until superheat protection stopped the machine.

**Why this is not the same as telemetry.** Telemetry is the real chiller as Keppel meters saw it. The 116 are the model’s chiller. Some ideas match a meter (power, refrigerant temperature). Some have no meter (charge mass, subcooling, valve position, superheat, the fault name).

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


| Keppel tag        | Twin variable (`source`) | In your original telemetry?                       |
| ----------------- | ------------------------ | ------------------------------------------------- |
| `CH-EVA-E-TEMP`   | `T_chw_entering_K`       | Yes. This one is fed in, then written back.       |
| `CH-CON-E-TEMP`   | `T_cw_entering_K`        | Yes. Same.                                        |
| `CH-EVA-RFT-TEMP` | `T_evap_K`               | No. The model calculated the boiling temperature. |
| `CH-KW_A`         | `power_elec_W`           | No. The model calculated the power.               |


### Derived — a formula, configured in the manifest

**Source of the formula:** the tag’s `description` inside `keppel_tags`. The twin company wrote the site’s arithmetic there.  
**Source of the numbers inside the formula:** the measured Keppel columns (and sometimes another derived column). Not a second physics solve.


| Keppel tag        | Formula in the manifest                                                          |
| ----------------- | -------------------------------------------------------------------------------- |
| `CH-EVA-APP-TEMP` | Leaving chilled water (`CH-EVA-L-TEMP`) minus evaporator refrigerant temperature |
| `CH-KW/RTON`      | `CH-KW_A` divided by `CH-CHW-RTON`                                               |
| `CH-L1-A`         | Current from power, voltage, and the site’s phase imbalance                      |


These are not in the raw telemetry as independent sensors. The real site computes the same kind of formula. Here the inputs are the twin’s meters.

### Replay — pasted from telemetry

**Source:** your real day, unchanged. The model does not calculate them. This leak case does not move them.


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

The program changes **one** thing starting at 00:00: vapour leak area (grows for ~72 minutes, then holds). **Charge keeps falling** until trip, because the hole stays open. A tag is listed only after it stays outside the clean-day noise for **10 minutes** (`cascade.departure_test`, `hold_min`; comparison window **15 minutes**). That 10 minutes is a noise rule. It is not a second stage of the hole opening.

Source: `cascade.order_observed` and `leak_gas_moderate_80pct_cascade.csv`. First departure: `subcooling_K` at **+59 min**. Over the whole fault the signature check agrees with the catalogue directions: charge down, condenser pressure down, subcooling down, expansion valve saturates, superheat up. Those directions describe the end state. The minute a tag clears the noise band can be earlier or later than that catalogue order.

### After midnight — full detail (selected path)


| After midnight | Name                                                    | What it is                                                                                                                                          | Direction                                                            | Visible on Keppel?     | Source                                             | Maps to section 1 | Why it moves                                                                                                                                                                                                                   |
| -------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------- | -------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 59 min         | Subcooling (`subcooling_K`)                             | Degrees the condenser liquid sits below its boiling point                                                                                           | Falls                                                                | No — `truth.csv` only  | Twin model                                         | Step 3            | The liquid pool is getting shallower, so it cannot be cooled as far below boiling. First quantity to clear the noise band.                                                                                                     |
| 69 min         | `CH-KW_A`                                               | Electrical power of the compressor, in kilowatts                                                                                                    | Rises, peaks near +43 kW around 11 h, then falls back     | Yes                    | Twin meter of `power_elec_W`                       | Step 4            | At +69 min the climb is almost unchanged and power is only about 1 kW above the clean day; the noise test fires because the shift is steady. The large rise is later: evaporator pressure falls, condenser pressure does not, so the lift gets taller while flow is still about 20 kg/s. After about 14 h, flow collapses and power falls.                                        |
| 71 min         | `CH-RLA`                                                | Percent of **rated load amps**. Rated load amps = motor full-load current on the nameplate (here 831 A). RLA % = average motor current ÷ 831 × 100. | Rise                                                                 | Yes                    | Formula in `keppel_tags`                           | Step 4            | Same electrical load as `CH-KW_A`, written as a percent of nameplate current.                                                                                                                                                  |
| 73 min         | `CH-L1-A`, `CH-L2-A`, `CH-L3-A`                         | Motor current on lines 1, 2, and 3, in amps                                                                                                         | Rise                                                                 | Yes                    | Formula (from power, voltage, phase imbalance)     | Step 4            | More power at roughly the same voltage means more current.                                                                                                                                                                     |
| 94 min         | `CH-KW/RTON`                                            | Kilowatts of electricity per ton of cooling                                                                                                         | Rise                                                                 | Yes                    | Formula: `CH-KW_A` / `CH-CHW-RTON`                 | Step 4            | The compressor is using more electricity for the cooling it is still delivering.                                                                                                                                               |
| 137 min        | Charge (`charge_kg`)                                    | Kilograms of refrigerant still inside the machine                                                                                                   | Fall (ends ~144 kg, about 12.5 % left)                               | No — truth only        | Twin model                                         | Step 2            | This is the mass balance. It is the cause of every later change. It clears the hold later than subcooling because total kilograms have to move farther, relative to their own noise test, before the test calls them departed. |
| 203 min        | EXV position (`exv_position`)                           | How far open the expansion valve is                                                                                                                 | Rise, then saturate                                                  | No — truth only        | Twin model                                         | Step 5            | Level control opens the valve to keep liquid on the evaporator tubes, and then runs out of travel.                                                                                                                             |
| 229–231 min    | `CH-EVA-RFT-TEMP`, `CH-EVA-RFT-PRES`                    | Boiling temperature in the evaporator, and the pressure that belongs to it                                                                          | Fall                                                                 | Yes                    | Twin meters of evaporator temperature and pressure | Step 6            | Less liquid on the tubes, so boiling shifts colder. Pressure follows that temperature along the saturation line.                                                                                                               |
| 241 min        | `CH-EVA-APP-TEMP`                                       | Site approach = leaving chilled water minus evaporator refrigerant temperature                                                                      | Rise                                                                 | Yes                    | Formula                                            | Step 6            | Refrigerant temperature falls farther than the leaving water, so water minus refrigerant gets larger. The gap between the water and the boiling refrigerant is widening.                                                       |
| 248 min        | `CH-OIL-TK-PRES`                                        | Oil-sump pressure                                                                                                                                   | Fall                                                                 | Yes                    | Twin / site relation to evaporator pressure        | Step 6            | The oil sump sits at evaporator pressure, so it falls with `CH-EVA-RFT-PRES`.                                                                                                                                                  |
| 462 min        | Superheat (`superheat_K`)                               | Degrees the suction vapour sits above the evaporator boiling temperature                                                                            | Rise (order of +24 K by the end)                                     | No — truth only        | Twin model                                         | Step 6            | Bare tubes heat the vapour after it has boiled. This is the dryness measurement that later trips the machine.                                                                                                                  |
| ~11 h          | `CH-CHWST`, `CH-EVA-L-TEMP`, `CH-CHW-KW`, `CH-CHW-RTON` | Leaving chilled-water temperature, and the cooling the machine is still delivering                                                                  | Temperature rises (~~+4.6 °C); cooling falls (~~−557 ton, ~−1960 kW) | Yes                    | Twin meters and the cooling formulas               | Step 6            | The water entering the evaporator is still the site-day temperature, but there is no longer enough boiling liquid to pull it down to setpoint.                                                                                 |
| ~12–12.5 h     | `CH-CON-RFT-TEMP`, `CH-CON-RFT-PRES`                    | Condenser refrigerant temperature and pressure                                                                                                      | Fall (pressure about −20 kPa at the departure)                       | Yes                    | Twin meters                                        | Steps 2–3         | Less vapour is arriving to be condensed, so the high side finally sags. Temperature and pressure move together on the saturation line. On this gas leak that sag is late.                                                      |
| ~14.7 h        | High-superheat **alarm**                                | Protection warning                                                                                                                                  | Alarm at superheat 18 °C                                             | Events in the manifest | `superheat_K`                                      | Step 6            | The dryness has crossed the warning line. The machine is still running.                                                                                                                                                        |
| ~17.6 h        | **Trip** `loss_of_charge`                               | Protection stops the machine                                                                                                                        | Trip at superheat 25 °C, held five minutes                           | `terminal_event`       | `superheat_K`                                      | Step 6            | The evaporator bundle is uncovered and the charge is gone. The file ends soon after (~17:46).                                                                                                                                  |


### Physics step → what you see


| Section 1 step                          | What you see after midnight                                                                                                              | On Keppel tags?                                                |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 2. Gas leaves, charge falls             | `charge_kg` clears the hold at +137 min and keeps falling to ~144 kg                                                                     | No — truth only                                                |
| 3. Condenser liquid pool shrinks        | `subcooling_K` at +59 min; condenser temperature and pressure on meters only at ~12 h                                                    | Subcooling no; condenser meters yes, but late                  |
| 4. Each kilogram costs more electricity | `CH-KW_A` at +69 min, `CH-RLA` at +71 min, line currents at +73 min, `CH-KW/RTON` at +94 min                                             | Yes                                                            |
| 5. Valve tries to refill the evaporator | `exv_position` at +203 min                                                                                                               | No — truth only                                                |
| 6. Tubes go dry, then the trip          | Evaporator temperature and pressure ~+4 h; approach ~+4 h; superheat ~+7.7 h; leaving water and tons ~+11 h; alarm ~14.7 h; trip ~17.6 h | Pressures, approach, leaving water, and tons yes; superheat no |


### What happens for the rest of that fault day (and why it keeps getting worse)

The ramp finishes at about **+72 minutes**. That only means the hole has reached full size. The hole then stays at that size. Gas keeps leaving, so the inventory keeps shrinking until protection trips. You are not watching a mild offset that has already settled.

**Right picture, in clock order.**

- **First hour.** The hole is still growing. The condenser liquid pool is already shallower (subcooling down). The compressor is already working harder per kilogram (power, amps, kW/ton up). The machine is still cooling.
- **About 2 to 4 hours.** Charge itself has clearly fallen. The expansion valve is opening toward its stop. Evaporator boiling temperature and pressure drop. Oil-sump pressure follows them.
- **About 7 to 12 hours.** Superheat is climbing because tubes are dry. Leaving chilled water rises and delivered tons collapse. Only then do condenser temperature and pressure fall far enough to clear the noise band.
- **About 14.7 hours, then 17.6 hours.** High-superheat alarm, then loss-of-charge trip. There is no remainder of 22 August with the machine still running, and no second copy of the day the way the fouling pack has.

**Easy mix-up.** The 1.2-hour ramp is the hole growing. It is not the charge loss finishing. After the ramp the area is constant and the mass balance is still `charge decreases by the leak flow`. The 8 hours to 40 percent is how the hole was sized. This file continues past 40 percent and stops at the superheat trip, near 87 percent lost.


| Question                                                 | Answer                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Do power and kW/ton keep rising until hour 48?           | No. Power is only about 1 kW high at the +69 min noise flag. The climb gets taller once evaporator pressure falls, and the gap versus the clean day peaks near +43 kW at about 11 h. After about 14 h, flow collapses and power falls. The file stops at the trip, about 17.6 h after midnight.                                                                                         |
| Does charge stop falling when the hole finishes opening? | No. Full-open is the maximum leak area. Kilograms keep leaving: about 1150 kg down to about 144 kg.                                                                                                                                                                             |
| Why does subcooling move before the charge tag does?     | Both come from the same missing mass. Subcooling is a sensitive reading of a shrinking liquid pool, so it leaves its noise band at +59 min. Total kilograms need a larger move before their own noise test calls them departed (+137 min).                                      |
| Why is condenser pressure late on the meters?            | The hole removes low-density gas, so the high side does not collapse in the first hour. `CH-CON-RFT-PRES` clears the hold only around +12.5 h, once much less vapour is left to condense. Over the whole run the pressure does fall, which is what the signature check records. |
| Does the chiller trip?                                   | Yes. `terminal_event` is `loss_of_charge` on `superheat_K` (limit 25 °C, held five minutes) at about 17.6 h. A high-superheat alarm fires earlier, at 18 °C, about 14.7 h.                                                                                                      |
| So what is the final result of this pack?                | A run to failure. The machine loses most of its charge, stops cooling, and trips with the evaporator tubes uncovered. The end state is an unavailable chiller.                                                                                                                  |


---

## 9. The path in one picture

```
Your telemetry day                         NOT in this folder
    boundary profile = which day,
    and the two entering-water temperatures
            |
            v
Vendor chiller model of HT-CH-01          manifest block "model"
    one knob: hole area for discharge gas
    area grows for 1.2 h, then stays open;
    kilograms drain until superheat trips (~17.6 h)
            |
            v
116 internal numbers                       truth.csv
    charge, subcooling, valve, superheat
            |
            +-- 25 twin instrument names   sensor_schema  -> twin_sensors.csv
            |
            +-- 20 Keppel meter names      keppel measured -> sensors.csv
            +-- 33 formulas                keppel derived description
            +-- 7 pasted from telemetry    keppel replay
            +-- 23 rebuilt plant totals    keppel total
            |
            v
83 Keppel columns, until trip              sensors.csv (~2507 rows)
```

