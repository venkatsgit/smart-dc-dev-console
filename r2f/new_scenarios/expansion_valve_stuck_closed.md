# Expansion valve stuck closed

Primary root cause: **the device that meters liquid into the evaporator is stuck shut or blocked** (EXV, TXV, float, or York “variable orifice”).  
The charge is still in the machine. This is not a leak; it is a mass-distribution fault.

**Evidence:** Taken from the **Trane**, **Carrier**, and **York / JCI** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf), [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf). The RP-1043 evidence paper also lists a faulty expansion valve.  
**Sources (same trip names in OEM manuals):** Trane `LOW EVAP PRESSURE` — EXV not opening, plugged filter-drier, liquid-line valve. Carrier 19XR **232** low refrigerant temperature — check float operation. York YK low suction — “variable orifice problem; remove obstruction.”

---

## 0. The Healthy State

The chiller relies on an expansion device to act as the "faucet" that controls the cooling process.

1. **What is the Expansion Valve (EXV)?** Think of it as a high-tech faucet or a garden hose nozzle. 
    *   **High-Pressure Side:** On one side is the **Condenser**, full of high-pressure liquid refrigerant.
    *   **Low-Pressure Side:** On the other side is the **Evaporator**, where the cooling happens.
    *   **The Flash:** When the valve opens, it "sprays" the liquid into the evaporator. This sudden drop in pressure causes the liquid to "flash" into a cold mist, which is what allows it to soak up heat from the building.
2. **The Gatekeeper's Job.** The valve's primary role is to meter the flow. 
    *   If the building gets hotter, the valve opens wider to let more "mist" into the evaporator. 
    *   If the building is cool, the valve throttles back (closes slightly) to save energy.
3. **Balancing the Pools.** 
    *   **Condenser Pool:** The "storage tank" (~270 kg). 
    *   **Evaporator Pool:** The "working pool" (~810 kg) that must stay deep enough to cover the cooling tubes.
    *   In a healthy machine, the valve ensures liquid arrives at the exact same rate that the compressor sucks gas out.
4. **Superheat (The Dryness Meter).** When the valve is working correctly and the tubes are wet, the gas leaving the evaporator is only slightly warmer than the boiling liquid (Healthy = **1–2 °C**).
5. **What "healthy" looks like.** The valve position (%) moves smoothly up and down with the building load. Evaporator pressure is normal (~92 kPa). Superheat is low. Subcooling is steady (4–5 °C).

---

## 1. The Fault: Stuck Closed

**The knob.** Freeze the expansion valve at a 0% or very small opening, or simulate a blocked filter-drier. No refrigerant is lost to the atmosphere; the total kilograms remain at design (**1150 kg**).

**Sensors to watch.** The primary signature is an empty evaporator despite having a full charge in the condenser.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| EXV Position (Feedback) | The gate state | **Stuck low / zero.** Does not follow the controller's command. |
| Evaporator Superheat | Dryness indicator | **Spikes.** Tubes go dry; gas picks up massive heat from building water. |
| Subcooling | Condenser pool depth | **Rises.** Liquid refrigerant piles up in the condenser, unable to leave. |
| Evaporator Refrigerant Pressure | The **floor** of the climb | **Collapses.** No liquid is arriving to boil and maintain pressure. |
| Lift (Condenser - Evaporator) | The hill the compressor climbs | **Grows** because the floor drops. |
| Compressor Power / kW | Cost of that hill | **Rises** as lift increases. |

### Understanding Pressure and Lift

To diagnose a stuck valve, you must look at the "floor" and the "ceiling" together:

*   **Evaporator Refrigerant Pressure:** The "floor." It collapses because the compressor is still sucking gas out, but the "gate" (EXV) is shut, preventing any new liquid from arriving to replace it. The source is starved.
*   **Condenser Refrigerant Pressure:** The "ceiling." It usually stays normal or rises slightly. The condenser becomes a "storage tank" for the entire refrigerant charge, which pushes up the pressure.
*   **Lift:** The physical "climb." Because the floor is dropping rapidly while the ceiling remains high, the compressor work increases. The hill becomes much steeper.

**Why this is different from a Leak:** Both cause a falling floor and high superheat. However, in a **leak**, the subcooling drains to zero. In a **stuck closed valve**, the subcooling **rises** because the liquid is trapped in the condenser. The machine is "choking" on its own liquid supply at the gate.

**The chain.**

1. **Valve jams or blockage occurs.** The "gate" between the high and low side shuts.
2. **Liquid stacks in the condenser.** The compressor is still pumping gas into the condenser, where it turns into liquid. But this liquid cannot leave. **Subcooling rises**.
3. **Evaporator pool drains.** The compressor is sucking gas out of the evaporator, but no new liquid is coming in. The level falls.
4. **Tubes go dry.** Refrigerant is no longer boiling on the tubes. Gas flows past dry copper and picks up heat. **Superheat spikes** (from 1 °C to 20 °C+).
5. **Lift grows.** The evaporator pressure (the floor) collapses. The compressor work increases, and **kW rise**.
6. **Trip.** The machine hits the **Low Evaporator Pressure** or **Low Refrigerant Temperature** trip to prevent freezing the evaporator, or a **High Superheat** alarm.

**Easy mix-up.** Refrigerant leak. Split: Leak = Low Subcooling (empty condenser). Stuck Closed = **High Subcooling** (condenser full of trapped liquid).
