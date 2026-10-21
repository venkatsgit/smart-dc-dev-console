# Extra run-to-failure scenarios for RDA (beyond the current pack)

This folder is the working brief for **new** physics cases to ask Red Dot Analytics (RDA) to generate. It is **not** tied to one brand of chiller. The same physical faults appear in Trane, Carrier, York / Johnson Controls, and Daikin manuals, and in the ASHRAE RP-1043 FDD experiment.

**Scenario id = the primary root cause** (not a later trip name). High condenser pressure, low evaporator pressure, and surge are what the meters and safeties do after one of these causes.

## Already in the current RDA pack (`../80/`, `../58/`) — do not request again

| Existing family | Pack ids | Why it is out of this list |
| --- | --- | --- |
| Condenser fouling | `cond_fouling_SL1` … `SL4` | Already delivered |
| Evaporator fouling | `evap_fouling_SL1` … `SL4` | Already delivered (not in the “three” you named, but already in the pack) |
| Refrigerant gas leak (discharge) | `leak_gas_slow`, `leak_gas_moderate` | Already delivered |
| Refrigerant liquid leak (high side) | `leak_liquid_slow`, `leak_liquid_moderate` | Already delivered |
| Healthy baseline | `healthy_*` | Already delivered |

## What to ask RDA for next

Ask for the same 21 August water day, at **both 58% and 80% load**, same sensor / truth / cascade files as the current pack. For rows marked **trip**, `stop_on` should be the protection event, the way the moderate gas leak already trips.

| # | Scenario id (root cause) | Typical end | Evidence | Detail note |
| --- | --- | --- | --- | --- |
| 1 | `reduced_condenser_water_flow` | High condenser pressure trip | **ASHRAE RP-1043** (fault FWC) | [reduced_condenser_water_flow.md](reduced_condenser_water_flow.md) |
| 2 | `reduced_evaporator_water_flow` | Low evaporator pressure / freeze trip | **ASHRAE RP-1043** (fault FWE) | [reduced_evaporator_water_flow.md](reduced_evaporator_water_flow.md) |
| 3 | `refrigerant_overcharge` | High condenser pressure | **ASHRAE RP-1043** (fault RO) | [refrigerant_overcharge.md](refrigerant_overcharge.md) |
| 4 | `noncondensable_gas` | High condenser pressure | **ASHRAE RP-1043** (fault NC) | [noncondensable_gas.md](noncondensable_gas.md) |
| 5 | `excess_oil` | Capacity loss; looks like evaporator fouling | **ASHRAE RP-1043** (fault EO) | [excess_oil.md](excess_oil.md) |
| 6 | `expansion_valve_stuck_closed` | Low evaporator pressure / high superheat trip | **OEM manuals** — Trane, Carrier, York / JCI | [expansion_valve_stuck_closed.md](expansion_valve_stuck_closed.md) |
| 7 | `expansion_valve_stuck_open` | Flooded evaporator; oil dilution / slugging | **OEM manuals** — Trane, Carrier, York / JCI | [expansion_valve_stuck_open.md](expansion_valve_stuck_open.md) |
| 8 | `igv_stuck_closed` | Capacity shortfall; surge risk | **OEM manuals** — Trane, Carrier, York / JCI | [igv_stuck_closed.md](igv_stuck_closed.md) |
| 9 | `cooling_tower_fan_failed` | High entering condenser water → high head / surge | **OEM manuals** — Trane, Carrier, York / JCI, Daikin | [cooling_tower_fan_failed.md](cooling_tower_fan_failed.md) |
| 10 | `low_oil_pressure` | Low oil-pressure trip | **OEM manuals** — Trane, Carrier, York / JCI | [low_oil_pressure.md](low_oil_pressure.md) |
| 11 | `compressor_surge` | Surge trip | **OEM manuals** — Trane, York / JCI, Daikin | [compressor_surge.md](compressor_surge.md) |

Each scenario note has only two sections, matching the style of [`../_analysis/80/leak_gas_moderate_80pct_detail.md`](../_analysis/80/leak_gas_moderate_80pct_detail.md):

- **0. The Healthy State**
- **1. The Fault** (root cause, then the chain of symptoms to the trip)

## Local files in [`references/`](references/)

Run [`download_oem_manuals.ps1`](download_oem_manuals.ps1) to refresh the PDFs. The official ASHRAE RP-1043 report is **sold** (not a free PDF); the open evidence paper that describes the experiment and the fault list is what we keep locally.

| Local file | What it is |
| --- | --- |
| [`ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf) | Open paper on the **ASHRAE RP-1043** experiment: reduced condenser/evaporator water flow, refrigerant leak, overcharge, excess oil, condenser fouling, non-condensables, and faulty expansion valve |
| [`Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf) | **Trane** CenTraVac CVHE / CVHF / CVHG IOM |
| [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf) | **Trane** CH530 operation (high/low pressure limits, oil ΔP, surge) |
| [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf) | **Carrier** 19XR start-up / cycle (oil ΔP, IGV, motor/oil cooling) |
| [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf) | **York / JCI** YK Style G O&M 160.75 (troubleshooting table, PRV, surge) |
| [`Daikin_IOM1210_Magnitude_WMC-D.pdf`](references/Daikin_IOM1210_Magnitude_WMC-D.pdf) | **Daikin** Magnitude WMC-D IOM (flow, pressure, surge trips) |
| [`Daikin_IOM1372_Magnitude_WME-D.pdf`](references/Daikin_IOM1372_Magnitude_WME-D.pdf) | **Daikin** Magnitude WME-D IOM (high/low pressure, water-flow loss) |

Official RP-1043 store listing (paywalled): [ASHRAE / Accuris](https://store.accuristech.com/ashrae/standards/rp-1043-fault-detection-anddiagnostic-fdd-requirements-and-evaluation-toolsfor-chillers?product_id=1716217).

## Why these eleven, and not more

ASHRAE RP-1043 induced **seven** thermodynamic faults on a centrifugal chiller. The current pack already covers two of them (condenser fouling, refrigerant leak). The five that are still missing — and whose evidence is **ASHRAE RP-1043** — are: **reduced condenser water flow**, **reduced evaporator water flow**, **overcharge**, **non-condensables**, and **excess oil**.

The remaining six are taken from **OEM name and manuals** (Trane, Carrier, York / JCI, Daikin): expansion device stuck, inlet vanes stuck, tower-fan / no condenser-water flow, low oil pressure, and surge. Those names appear as protect limits on Trane CH530, Carrier 19XR, York YK OptiView, and Daikin Magnitude.

Electrical starter faults, sensor-wire faults, and bearing-metal wear are real, but they are not the first physics cases for a refrigerant-loop twin. Leave them for a later mechanical pack.

## How each case is different from fouling and leaks (so the classifier can split them)

| New case | First thing that moves | Easy mix-up | How it is not that mix-up |
| --- | --- | --- | --- |
| Reduced condenser-water flow | Condenser water ΔT **rises**, flow **falls**, then head pressure rises | Condenser fouling | Fouling: flow stays normal, approach widens. Flow loss: flow and ΔT move first. |
| Reduced evaporator-water flow | Chilled-water ΔT **rises**, flow **falls**, leaving water warms | Evaporator fouling | Fouling: flow stays normal, evaporator approach widens. |
| Overcharge | **Subcooling rises**, condenser pressure rises | Gas/liquid leak | Leak: subcooling **falls**. Overcharge: subcooling **rises**. |
| Non-condensables | Condenser pressure rises; purge / “air in condenser” | Fouling or overcharge | York: same high head as fouling until you purge. After purge, fouling remains; air does not. |
| Excess oil | Evaporator approach widens; capacity falls | Evaporator fouling | Oil is in the refrigerant, not scale on the water side. |
| EXV stuck closed | Superheat up, evaporator pressure down, **charge still in the machine** | Refrigerant leak | Leak: total charge falls. Stuck valve: charge is still there, often piled in the condenser. |
| EXV stuck open | Superheat collapses; risk of liquid at the compressor | Overcharge | Valve position is the knob, not extra kilograms. |
| IGV stuck closed | Capacity stuck low; leaving chilled water rises | Late-stage leak | Pressures can still look charged. Vanes do not follow load. |
| Tower fan failed | **Entering** condenser-water temperature rises | Condenser fouling | Fouling does not lift entering tower water. The tower does. |
| Low oil pressure | Oil ΔP falls; machine trips on oil, not on refrigerant | Leak (oil can leave with gas) | First trip is oil pressure, not superheat. |
| Surge | Surge margin collapses; vibration / surge count | High head from fouling or low CW flow | Surge is the **end state**. Ask RDA to drive it from high lift so the trip is surge, not only high pressure. |

## Sources (parent index)

### Research catalogue (ASHRAE RP-1043 — the seven classic faults)

| Source | What it names | Local / link |
| --- | --- | --- |
| ASHRAE RP-1043 — *Fault Detection and Diagnostic (FDD) Requirements and Evaluation Tools for Chillers* | Reduced condenser-water flow; reduced evaporator-water flow; condenser fouling; non-condensable gas; refrigerant leak; refrigerant overcharge; excess oil. Four severity steps each. | Sold on the [ASHRAE store](https://store.accuristech.com/ashrae/standards/rp-1043-fault-detection-anddiagnostic-fdd-requirements-and-evaluation-toolsfor-chillers?product_id=1716217) |
| J-STAGE AIUE 2019 (open evidence paper for RP-1043) | Same experiment: loss of condenser/evaporator water flow, leak, overcharge, excess oil, condenser fouling, non-condensables, **faulty expansion valve** | [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf) |
| MDPI *Buildings* 2024 (XGBoost on RP-1043) | Table of the seven faults and SL1 sizes: FWC −10%, FWE −10%, CF 12%, NC +1%, RL −10%, RO +10%, EO +14% | [doi:10.3390/buildings14061835](https://doi.org/10.3390/buildings14061835) (PDF blocked for automated download) |
| MDPI *Actuators* 2023 | Same RP-1043 table with SL1–SL4 percentages | [doi:10.3390/act12060242](https://doi.org/10.3390/act12060242) (PDF blocked for automated download) |

### Trane (CenTraVac CVHE / CVHF / CVHG, CH530)

| Source | What it names | Local / link |
| --- | --- | --- |
| CVHE-SVX005E-EN IOM | Water-cooled centrifugal operation and limits | [`references/Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf) |
| CVHE-SVU01E-EN (CH530) | High condenser / low evaporator adaptive limits; oil ΔP 18–22 psid; surge / condenser-limit mode | [`references/Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf) |
| Trane CH530 diagnostic list (secondary compilation of official text) | `HIGH DISCH PRESSURE` ← reduced CW flow, high entering CW, fouling, non-condensables, overcharge. `LOW EVAP PRESSURE` ← low charge, EXV not opening, low CHW flow. `LOW OIL PRESSURE` ← pump, level, filter | [errorcodefixes compilation](https://errorcodefixes.com/posts/trane-chiller-fault-codes/) |

### Carrier (19XR / 19XRV)

| Source | What it names | Local / link |
| --- | --- | --- |
| 19XR start-up / cycle | Oil ΔP 18–25 psid; oil foaming if vanes open too fast; motor cooling and oil cooler on refrigerant | [`references/Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf) |
| 19XR / 19XRV ICVC protect limits | 229 low chilled-water flow; 230 low condenser-water flow; 228 low oil pressure; 231 high discharge temp; 232 low refrigerant temp; 233 high motor temp; 234 high bearing temp; 235 high condenser pressure (high CW temp, low CW flow, fouled tubes, gasket bypass, non-condensables) | [manualsdir p.82](https://www.manualsdir.com/manuals/65103/carrier-19xrxrv-hermetic-centrifugal-liquid-chillers.html?page=82) |

### York / Johnson Controls (YK)

| Source | What it names | Local / link |
| --- | --- | --- |
| YK Style G O&M 160.75 | High discharge pressure ← air in condenser, dirty/scaled tubes, high CW in, insufficient CW flow. Low suction ← low charge, variable-orifice problem, dirty evaporator tubes. PRV fail to open. Oil pump / oil pressure. Hot-gas bypass for surge at light load or high head | [`references/York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf) |

### Daikin Applied (Magnitude WMC / WME)

| Source | What it names | Local / link |
| --- | --- | --- |
| IOM 1210 Magnitude WMC-D | Unit/compressor faults: no condenser-water flow; no evaporator-water flow; low evaporator / suction pressure; high condenser pressure; high discharge temperature; surge (high suction superheat while running) | [`references/Daikin_IOM1210_Magnitude_WMC-D.pdf`](references/Daikin_IOM1210_Magnitude_WMC-D.pdf) |
| IOM 1372 Magnitude WME-D | High condenser pressure (>160 psi); low evaporator pressure ← low/no evap flow, low refrigerant level; condenser/evaporator water-flow loss; pump faults | [`references/Daikin_IOM1372_Magnitude_WME-D.pdf`](references/Daikin_IOM1372_Magnitude_WME-D.pdf) |

## Suggested wording to send RDA

Please generate run-to-failure packs for HT-CH-01 (same model already shared), using `site_day_80` and `site_day_58`, for the eleven scenario ids in the table above. Each pack should use **one knob** (the primary root cause), hold or ramp that knob as noted in the detail file, and stop on the named protection trip where the detail file says the machine trips. Keep the same Keppel `sensors.csv` / `truth.csv` / `cascade.csv` shape as `leak_gas_moderate_80pct`.
