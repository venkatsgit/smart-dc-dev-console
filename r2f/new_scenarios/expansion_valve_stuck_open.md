# Expansion valve stuck open

Primary root cause: **the metering device is stuck too far open**, so liquid is not held back.  
Not a leak and not overcharge. The "gate" is simply jammed open, allowing the high-pressure condenser to flood the low-pressure evaporator.

**Evidence:** Taken from the **Trane**, **Carrier**, and **York / JCI** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf), [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf).  
**Sources:** Inverse of the OEM “EXV / float / orifice not feeding” notes (Trane EXV position feedback; Carrier float; York variable orifice). If the same device can fail closed, it can fail open. Carrier also warns that opening inlet vanes too fast foams oil — a flooded, low-pressure evaporator is the same family of risk.

---

## 0. The Healthy State

The chiller relies on an expansion device to act as the "faucet" that controls the cooling process.

1. **What is the Expansion Valve (EXV)?** Think of it as a high-tech faucet or a garden hose nozzle. 
    *   **High-Pressure Side:** On one side is the **Condenser**, full of high-pressure liquid refrigerant.
    *   **Low-Pressure Side:** On the other side is the **Evaporator**, where the cooling happens.
    *   **The Flash:** When the valve opens, it "sprays" the liquid into the evaporator. This sudden drop in pressure causes the liquid to "flash" into a cold mist, which is what allows it to soak up heat from the building.
2. **The Gatekeeper's Job.** The valve's primary role is to meter the flow. 
    *   It opens just enough to replace the liquid that boiled off. 
    *   It ensures the evaporator tubes stay wet, but not so full that liquid splashes out and enters the compressor.
3. **Balancing the Pools.** 
    *   **Condenser Pool:** The "storage tank" (~270 kg). 
    *   **Evaporator Pool:** The "working pool" (~810 kg) that must stay deep enough to cover the cooling tubes.
    *   In a healthy machine, the valve maintains a steady pool depth in both shells.
4. **Superheat (The Dryness Meter).** When the valve is working correctly and the tubes are wet, the gas leaving the evaporator is slightly warmer than the boiling liquid (Healthy = **1–2 °C**). This confirms that all liquid has turned to gas before entering the compressor.
5. **What "healthy" looks like.** The valve position (%) moves smoothly with the building load. Evaporator pressure is normal (~92 kPa). Superheat is low but **positive**. Subcooling is steady (4–5 °C).

---

## 1. The Fault: Stuck Open

**The knob.** Drive the expansion valve to a 100% or very large opening and hold it. The refrigerant charge is still at design (**1150 kg**), but the "gate" between the sides is gone.

**Sensors to watch.** The primary signature is a flooded evaporator and a collapsing superheat.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| EXV Position (Feedback) | The gate state | **Stuck High.** Open much wider than the load requires. |
| Evaporator Superheat | Dryness indicator | **Collapses to 0 °C.** Liquid is flooding out of the evaporator. |
| Subcooling | Condenser pool depth | **Falls.** The condenser "storage tank" is drained into the evaporator. |
| Evaporator Refrigerant Pressure | The **floor** of the climb | **Rises.** The evaporator is flooded with high-pressure liquid from the condenser. |
| Condenser Refrigerant Pressure | The **ceiling** of the climb | **Falls.** The pressure "leaks" through the open valve into the low side. |
| Lift (Condenser - Evaporator) | The hill the compressor climbs | **Collapses.** The pressure difference between the two sides disappears. |

### Understanding Pressure and Lift

To diagnose a stuck open valve, you must look at how the "ceiling" and the "floor" are moving toward each other:

*   **Evaporator Refrigerant Pressure:** The "floor." It rises because the high-pressure liquid from the condenser is pouring into it without restriction.
*   **Condenser Refrigerant Pressure:** The "ceiling." It falls because the pressure is being "vented" through the wide-open valve into the low side.
*   **Lift:** The physical "climb." The "hill" between the two sides disappears. While this sounds easier for the compressor, it is actually dangerous because the compressor is now ingesting liquid refrigerant ("slugging").

**Why Superheat is the "Smoking Gun":** In this fault, superheat **falls to zero**. This tells you the evaporator is so full that the refrigerant hasn't finished boiling before it leaves. If you see zero superheat along with a falling subcooling, the machine is "choking" on a flood of liquid.

**The chain.**

1. **Valve jams open.** The "gate" between the high and low side is removed.
2. **Condenser pool drains.** The high-pressure liquid rushes through the open valve. **Subcooling falls**.
3. **Evaporator floods.** The liquid level in the evaporator rises until the tubes are completely submerged and liquid starts splashing into the suction line.
4. **Superheat collapses.** The suction gas is wet. **Superheat falls to 0 °C**.
5. **Lift collapses.** The pressure in the two shells begins to equalize. The compressor has no "hill" to climb, but it is now hitting liquid slugs.
6. **Oil dilution.** Liquid refrigerant mixes with the oil in the sump. Oil foams and its lubricating quality drops.
7. **Trip.** The machine hits a **Low Oil Pressure** trip (due to foaming), a **High Vibration** trip (due to liquid slugging), or a motor protection limit.

**Easy mix-up.** Refrigerant overcharge. Split: Overcharge = High Subcooling (too much liquid in the machine). Stuck Open = **Low Subcooling** (liquid is in the machine, but it's in the wrong place—the evaporator).
