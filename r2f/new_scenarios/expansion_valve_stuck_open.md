# Expansion valve stuck open

Primary root cause: **the metering device is stuck too far open**, so liquid is not held back.  
Not a leak and not overcharge. The gate is simply jammed open.

**Evidence:** Taken from the **Trane**, **Carrier**, and **York / JCI** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf), [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf).  
**Sources:** Inverse of the OEM “EXV / float / orifice not feeding” notes (Trane EXV position feedback; Carrier float; York variable orifice). If the same device can fail closed, it can fail open. Carrier also warns that opening inlet vanes too fast foams oil — a flooded, low-pressure evaporator is the same family of risk.

---

## 0. The Healthy State

1. **The valve is a meter, not a pipe.** It opens just enough to replace the liquid that boiled off. Evaporator tubes stay wet. Almost no extra liquid climbs into the suction line.
2. **Superheat is the dryness check.** Healthy suction gas is only **1–2 °C** above boiling. That means the last liquid finished boiling in the bundle, not in the compressor.
3. **Oil stays pumpable.** A dry, properly fed evaporator does not dilute the oil sump with a flood of liquid refrigerant.
4. **What “healthy” looks like.** Valve position tracks load. Superheat is small but **not zero**. Evaporator level is in band. No liquid hammer, no collapsing oil ΔP from foam.

---

## 1. The Fault

**The knob.** Drive the expansion device to a high opening and hold it there, independent of level / superheat control.

**The chain.**

1. **Too much liquid enters the evaporator.** The condenser pool is dumped downstream faster than the bundle can boil it in an orderly way.
2. **Superheat collapses.** Suction gas is wet. Superheat falls toward **zero**. This is the opposite of a leak and of a stuck-closed valve.
3. **Flood and carryover.** Liquid can leave the evaporator toward the compressor. That is slugging: liquid does not compress. The machine risks mechanical damage, not just inefficiency.
4. **Oil dilution and foam.** Liquid refrigerant mixes into the oil. Oil ΔP and lubrication suffer. Carrier describes foam when suction pressure drops suddenly; a stuck-open valve is a sustained version of “too much liquid, wrong place.”
5. **Capacity can look fine at first.** The hall may still be cold. The danger is at the compressor, not at leaving-water temperature.
6. **Trip / end.** **Low oil pressure**, **high motor or discharge temperature** after liquid damage, or a surge / vibration trip. Some machines simply keep running poorly with zero superheat until an oil or motor limit hits. Ask RDA to stop on the first protect limit the twin already models (oil ΔP or surge), and to keep `exv_position` saturated open in `truth.csv`.

**Easy mix-up.** Overcharge also raises condenser liquid. Overcharge: extra **mass**, valve still in control. Stuck open: **mass is normal**, valve is the fault. Superheat direction (down) also splits this from leaks.
