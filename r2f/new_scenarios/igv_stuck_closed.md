# Inlet guide vanes stuck closed

Primary root cause: **capacity control stuck too far closed** (inlet guide vanes on a centrifugal, or York PRV).  
The refrigerant charge and the water flows can be healthy. The compressor simply will not swallow the load.

**Evidence:** Taken from the **Trane**, **Carrier**, and **York / JCI** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf).  
**Sources:** York YK: high evaporator pressure / high chilled-water temperature — “PRVs fail to open.” Carrier 19XR: check inlet guide vane and diffuser actuator on high discharge temperature; check IGV on low refrigerant temperature. Trane CH530 modulates vanes as the main capacity handle below the speed / current limits.

---

## 0. The Healthy State

1. **Vanes are the throttle on the compressor inlet.** At light load they close and reduce mass flow. At heavy load they open so the impeller can move more gas.
2. **Leaving-water control.** The controller opens vanes until leaving chilled water is at setpoint, unless a current, condenser-pressure, or surge limit holds them back.
3. **The refrigerant loop is otherwise normal.** Charge, oil, tower water, and chilled-water flow are in band. Lift is the usual 92 → 185 kPa class climb on these packs.
4. **What “healthy” looks like.** `CH-IGV1-POS` (or the twin `igv_position`) **moves** when load or water temperature moves. Leaving chilled water holds setpoint. The machine is not stuck at a low RLA while the hall warms.

---

## 1. The Fault

**The knob.** Freeze inlet-guide-vane (or PRV) position at a low opening and hold it. Water boundaries and charge stay at the site day.

**The chain.**

1. **Mass flow is capped.** The impeller is not allowed to take the gas the hall needs. Refrigerant “conveyor belt” stays too slow.
2. **Capacity will not rise with load.** Leaving chilled-water temperature **rises**. Tons stay low. Power may stay modest — this is not the “harder lift” of fouling. The machine looks lazy, not strained.
3. **Evaporator can run warmer.** If too little boiling is happening, chilled water is not pulled down. Evaporator pressure may sit high relative to a starved-leak case.
4. **Surge risk at the wrong map point.** Closed vanes plus a tall lift (hot tower, dirty condenser) is a classic surge corner. York fits hot-gas bypass for “light load or high head.” A stuck-closed vane **is** light compressor flow.
5. **Trip.** Often **no refrigerant trip** — the hall just misses setpoint. If lift is high, the end is **surge**. York’s other branch: if vanes fail **open**, motor overload / high evaporator pressure. This file is the fail-closed branch only.

**Easy mix-up.** Late-stage leak also loses capacity. Leak: charge and subcooling already gone; evaporator pressure **down**; superheat **up**. Stuck vanes: charge still there; vanes do not travel; superheat stays near healthy.
