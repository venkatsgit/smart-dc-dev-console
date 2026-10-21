# Cooling-tower fan failed

Primary root cause: **a cooling-tower fan (or a cell) stops**, so the tower cannot reject heat.  
Entering condenser-water temperature rises. The chiller tubes can be clean. The water flow can be normal.

**Evidence:** Taken from the **Trane**, **Carrier**, **York / JCI**, and **Daikin** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf), [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf), [`Daikin_IOM1210_Magnitude_WMC-D.pdf`](references/Daikin_IOM1210_Magnitude_WMC-D.pdf), [`Daikin_IOM1372_Magnitude_WME-D.pdf`](references/Daikin_IOM1372_Magnitude_WME-D.pdf).  
**Sources:** Trane high discharge — **high condenser water entering temperature**. Carrier 19XR **235** — high condenser water temperatures. York YK: reduce condenser-water inlet temperature; check cooling tower and water circulation. Daikin: condenser-water temperature and flow as high-pressure causes. This is the Singapore-typical “hot afternoon” plant fault.

---

## 0. The Healthy State

1. **The tower is the heat dump for the whole plant.** Condenser water leaves the chiller hot, is cooled in the tower fill by air, and comes back as **entering condenser-water temperature**.
2. **On the current 80% site day** that return sat about **28.5–31.0 °C** (mean ~29.1 °C). The chiller’s condenser pressure is built on that water. The compressor climb is sized for that ceiling.
3. **Fans and cells are the air side.** Fill, fan, and water flow together set tower approach (how close leaving tower water gets to wet-bulb).
4. **What “healthy” looks like.** `CH-CON-E-TEMP` follows a smooth daily swing, not a step up of several degrees with no weather change. Condenser pressure tracks that water. Fans are running. Chiller power is the usual lift cost.

---

## 1. The Fault

**The knob.** Fail one (or more) tower fans, or raise the **entering condenser-water** boundary as if a cell died, and hold it. Do not reduce condenser-water **flow** unless the cell also isolates (that would be a combined case). The clean first pack is: **flow stays**, **entering temperature rises**.

**The chain.**

1. **The heat sink gets hotter.** Water comes back from the tower warmer. `CH-CON-E-TEMP` is the first site tag. This is **not** fouling. Fouling does not heat the water entering the machine.
2. **Condenser refrigerant must run hotter.** To dump heat into warmer water, the gas sits at a higher temperature and pressure.
3. **Lift grows.** Same evaporator, higher condenser. Power and current rise. kW/ton worsens. Surge margin falls.
4. **Plant totals move.** Other chillers on the same loop see the same hot water. This is why a later “subsystem” pack matters — but the first R2F case can still be one chiller on a hotter CW-in boundary.
5. **Trip.** **High condenser pressure** and/or **surge**. Same cutouts as low condenser-water flow, but the first mover is **entering temperature**, not flow.

**Easy mix-up.** Condenser fouling and reduced condenser-water flow. Split:

| First mover | Case |
| --- | --- |
| Flow down, ΔT up, CW-in normal | Reduced condenser-water flow |
| Approach up, flow and CW-in normal | Condenser fouling (already in pack) |
| **CW-in up**, flow normal | **This case** |
