# Expansion valve stuck closed

Primary root cause: **the device that meters liquid into the evaporator is stuck shut or blocked** (EXV, TXV, float, or York “variable orifice”).  
The charge is still in the machine. This is not a leak.

**Evidence:** Taken from the **Trane**, **Carrier**, and **York / JCI** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf), [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf). The RP-1043 evidence paper also lists a faulty expansion valve.  
**Sources:** Trane `LOW EVAP PRESSURE` — EXV not opening, plugged filter-drier, liquid-line valve. Carrier 19XR **232** low refrigerant temperature — check float operation and charge. York YK low suction — “variable orifice problem; remove obstruction.”

---

## 0. The Healthy State

1. **The expansion device is the gate.** Liquid leaves the condenser pool, passes the valve, and flashes into the evaporator. The valve’s job is to keep evaporator tubes **covered** without flooding the compressor.
2. **Level or superheat control.** Many centrifugals hold evaporator level. Others hold a small superheat (about **1–2 °C** when tubes are wet). The valve opens if the evaporator starts to go dry; it closes if the evaporator gets too full.
3. **Two pools stay in balance.** Condenser pool feeds the valve. Evaporator pool boils and returns gas to the compressor. Total charge is constant.
4. **What “healthy” looks like.** Valve position moves with load. Superheat stays small. Evaporator pressure is normal. Subcooling is a few degrees. The compressor is not sucking a dry barrel.

---

## 1. The Fault

**The knob.** Freeze the expansion device at a too-small opening (or close it over a short ramp) and hold it. Do **not** remove refrigerant mass.

**The chain.**

1. **Liquid cannot reach the evaporator.** The condenser still makes liquid. The gate is shut. The evaporator pool starts to fall.
2. **Superheat is the first dryness meter.** Wet tubes: a degree or two. Dry tubes: vapour is heated by bare metal. **Superheat rises.** Evaporator temperature and pressure fall together (saturation).
3. **The condenser side can look “too full.”** Liquid that cannot leave stacks upstream. Subcooling may **hold or rise**, the opposite of a leak. That is the split: stuck-closed starves the evaporator while the machine is still **charged**.
4. **Capacity collapses.** Leaving chilled water rises. Tons fall. The compressor may draw less mass flow because there is little gas to pump — or it may work harder on a taller lift as evaporator pressure caves in (same lift paradox as a late leak).
5. **Trip.** Trane / Carrier / Daikin: **low evaporator pressure**, **low refrigerant temperature**, or **high superheat / loss of charge** logic — even though the kilograms never left the shells. The repair is the valve or the drier, not a gas bottle.

**Easy mix-up.** Discharge-gas or liquid leak. Both dry the evaporator and raise superheat. Leak: `charge_kg` falls. Stuck valve: `charge_kg` stays; condenser inventory often **rises**.
