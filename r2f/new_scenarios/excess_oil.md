# Excess oil in the refrigerant loop

Primary root cause: **too much oil circulating with the refrigerant** (overfill, failed oil-return, or oil logged in the evaporator).  
Not evaporator tube scale. The water side can be clean. The "dirt" is an oil film on the refrigerant side.

**Evidence:** From **ASHRAE RP-1043** (fault EO, +14/+32/+50/+68% extra oil). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** York YK evaporator note: an excessive quantity of oil in the evaporator contributes to erratic performance and can look like fouled tubes or low charge. Carrier / Trane oil systems assume oil stays in the sump and a thin film returns — not a flooded evaporator.

---

## 0. The Healthy State

The chiller is a closed loop where oil and refrigerant have strictly separated roles.

1. **Refrigerant (The Shuttle).** Moves heat from the evaporator to the condenser. To do this efficiently, it must touch the copper tubes directly to boil or condense.
2. **Oil (The Lubricant).** Essential for the **compressor's high-speed bearings and gears**. 
    *   **Oil Tank / Sump:** The reservoir where the oil is stored.
    *   **Oil Pump:** Circulates the oil from the tank to the compressor parts that need lubrication.
    *   **Oil Filter:** Removes contaminants to ensure only clean oil reaches the bearings.
    *   **Separation:** A healthy machine keeps the oil in the lubrication circuit. Any tiny amount of oil that escapes into the refrigerant loop is caught and returned via an **oil-return system** (eductor/separator).
3. **Lift (The Climb).** The compressor lifts gas from the evaporator "floor" (~92 kPa) to the condenser "ceiling" (~185 kPa). In a healthy machine, the heat transfer in the evaporator is high, keeping the "floor" at an efficient level.
4. **What "healthy" looks like.** 
    *   Oil level is steady in the **sump sight-glass**.
    *   Oil differential pressure (\(\Delta P\)) across the **pump and filter** is normal (e.g., 18–25 psid).
    *   Evaporator approach is small (the refrigerant temperature is very close to the leaving chilled-water temperature).

---

## 1. The Fault: Excess Oil

**The knob.** Raise the oil inventory in the refrigerant circuit (ASHRAE starts at **+14%** extra oil) and hold it. Chilled-water flow and refrigerant charge remain at design levels.

**Sensors to watch.** This fault is "sneaky" because it looks like fouling, but it happens on the refrigerant side of the evaporator tubes.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| Evaporator Approach | Heat transfer gap | **Widens.** Oil coats the tubes, blocking heat from reaching the refrigerant. |
| Evaporator Refrigerant Pressure | The **floor** of the climb | **Collapses.** The refrigerant can't boil as easily, so the floor drops. |
| Condenser Refrigerant Pressure | The **ceiling** of the climb | Stays near normal at first. |
| Lift (Condenser - Evaporator) | The hill the compressor climbs | **Grows** because the floor drops. |
| Compressor Power / kW | Cost of that hill | **Rises** with lift. |
| Cooling Capacity (Tons) | Total heat removed | **Falls.** The machine becomes sluggish and inefficient. |

### Understanding Pressure and Lift

To diagnose excess oil, you must look at why the "floor" is falling:

*   **Evaporator Refrigerant Pressure:** The "floor." It collapses because a thick film of oil acts as an insulator on the evaporator tubes. The refrigerant "can't see" the heat from the building water, so it sits at a lower pressure and temperature.
*   **Condenser Refrigerant Pressure:** The "ceiling." It usually stays normal because the condenser isn't the problem—the "sink" is still working, but the "source" (evaporator) is blocked.
*   **Lift:** The physical "climb." Since the floor is dropping while the ceiling stays still, the compressor must work much harder to "suck" gas from the insulated evaporator. The climb gets steeper.

### Understanding Approach Temperatures

**Approach** is the temperature "gap" between the refrigerant and the water it is exchanging heat with. It tells you how efficient the heat transfer is across the tube walls.

*   **Evaporator Approach** = (Leaving Chilled Water Temp) — (Saturated Evaporator Temp).
    *   In a healthy machine, this gap is very small (**1–2 °C**).
    *   In the **Excess Oil** fault, this gap **widens** because the oil film acts as a blanket, making the refrigerant much colder than the water it is trying to cool.
*   **Condenser Approach** = (Saturated Condenser Temp) — (Leaving Condenser Water Temp).
    *   In a healthy machine, this gap is also small (**0.5–2 °C**).
    *   If this gap widens, it usually points to **Condenser Fouling** or **Non-condensables (Air)**.

**Why you must check both:** If you only look at the condenser, you might think the machine is healthy because the "ceiling" is normal. But by looking at the evaporator refrigerant pressure, you can see the floor is falling, forcing the compressor to work much harder to "suck" gas from an insulated source.

**The chain.**

1. **Extra oil enters the loop.** It doesn't stay in the sump; it travels to the cold evaporator and gets "logged" there.
2. **Tubes are coated.** A thick film of oil covers the copper tubes. Refrigerant can no longer boil efficiently.
3. **Heat transfer fails.** The "UA" (heat transfer coefficient) of the evaporator drops. The **evaporator approach widens**.
4. **Evaporator pressure collapses.** The refrigerant boils at a lower temperature to try and compensate for the oil insulation. The **floor moves down**.
5. **Lift grows.** With a lower floor, the compressor work and **kW rise**. The machine becomes a "power hog" for the amount of cooling it provides.
6. **End State.** The machine may continue running inefficiently or eventually trip on **Low Evaporator Pressure** (freeze protection) because the floor has dropped too far.

**Easy mix-up.** Evaporator fouling. Both widen the approach and drop the floor. Split: Fouling is dirt *inside* the tubes (water side). Excess oil is oil *outside* the tubes (refrigerant side). If the water-side flow and pressure drop across the evaporator are healthy, but the approach is wide, it is likely a refrigerant-side problem like excess oil.
