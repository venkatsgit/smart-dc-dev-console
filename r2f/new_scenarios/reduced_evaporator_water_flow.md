# Reduced evaporator-water flow

Primary root cause: **less building chilled water through the evaporator** (blocked strainer, valve failing closed, or chilled-water pump losing capacity).  
Not evaporator fouling. The tubes can be clean. The water simply does not arrive.

**Evidence:** From **ASHRAE RP-1043** (fault FWE, −10/−20/−30/−40% flow). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane `LOW EVAP PRESSURE` — low chilled-water flow. Carrier 19XR protect **229** low chilled-water flow and **232** low refrigerant temperature (check fluid flow). Daikin Magnitude: `No Evaporator Water Flow`, evaporator pump fault, low evaporator pressure from low/no evaporator flow.

---

## 0. The Healthy State

The chiller is a closed refrigerant loop that shuttles heat out of the building by moving it from a low-pressure side to a high-pressure side.

1. **Evaporator (the source).** Cold liquid refrigerant boils at low pressure and soaks up heat from the building chilled-water loop. That boil creates the **gas** the compressor will ingest.
2. **Compressor (the work).** The compressor pulls that low-pressure gas from the evaporator and squeezes it. The squeeze makes the gas **hot and high-pressure**. The energy used to do this squeeze comes from the motor (kW).
3. **Lift (the climb).** **Lift** is the gap the compressor must climb: condenser pressure (the ceiling) minus evaporator pressure (the floor). In a healthy machine, the floor is high enough that the climb is efficient.
4. **Condenser (the sink).** Hot discharge gas enters the condenser, dumps its heat to the tower water, and turns back into a liquid to be sent back to the evaporator.
5. **What “healthy” looks like.** Chilled-water flow is near design. The water cools by several degrees across the evaporator (e.g., entering 12 °C, leaving 7 °C). Evaporator refrigerant pressure sits steady at the "floor" (about 92 kPa on these packs).

---

## 1. The Fault

**The knob.** Cut evaporator-water flow and hold it (ASHRAE sizes: 10, 20, 30, then 40 percent less than design). The primary cause is the water path — strainer, valve, or pump — not scale on the tubes.

**Sensors to watch.** Lift depends on both sides. In this case, the floor is collapsing.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| Evaporator-water flow | The knob | Falls first. This is the split from fouling. |
| Chilled-water ΔT (entering minus leaving) | How much each kilogram is being cooled | Rises. Same cooling demand, fewer kilograms. |
| Evaporator refrigerant pressure | The **floor** of the climb | Collapses. Heat source is throttled; pressure drops. |
| Condenser refrigerant pressure | The **ceiling** of the climb | Stays near normal at first. |
| Lift (condenser pressure − evaporator pressure) | The hill the compressor climbs | Grows because the floor drops. |
| Compressor power / current | Cost of that hill | Rises as lift increases. |

### Understanding Pressure and Lift

To diagnose this fault, you must distinguish between the measured pressures and the safety limits:

*   **Evaporator Refrigerant Pressure:** The "floor" of the cycle. It represents the state of the gas **before** it enters the compressor.
*   **Condenser Refrigerant Pressure:** The "ceiling" of the cycle. It represents the state of the gas **after** it has been compressed.
*   **Low Evaporator Pressure (or Low Refrigerant Temp):** This is a **safety trip point**. When the evaporator pressure (the floor) drops too low, the machine shuts down to prevent the water in the tubes from freezing.
*   **Lift:** The physical "climb" the compressor performs. In this case, the climb gets harder not because the ceiling rose, but because the **floor dropped**.

**Why you must check both:** If you only look at the condenser, you might think the machine is healthy because the "ceiling" is normal. But by looking at the evaporator refrigerant pressure, you can see the floor is falling, forcing the compressor to work much harder to "suck" gas from a starved source.

**The chain.**

1. **Flow drops.** Fewer kilograms of building water pass the evaporator tubes.
2. **Water cools more.** The compressor is still trying to pull heat. Each remaining kilogram of water is cooled further, so **chilled-water ΔT rises**.
3. **Evaporator refrigerant pressure collapses.** With less heat arriving from the water, the refrigerant boils at a lower and lower temperature. The **floor drops**.
4. **Lift grows.** Condenser pressure (the ceiling) is still normal, but since the floor is lower, the **lift increases**. The compressor must work harder, and power (kW) rises.
5. **Capacity falls.** Even with a higher ΔT, the drop in flow is so great that total cooling tons fall. The building starts to warm up.
6. **Trip.** The machine hits the **Low Evaporator Pressure** or **Low Refrigerant Temperature** trip to prevent freezing the evaporator tubes.

**Easy mix-up.** Evaporator fouling also widens evaporator approach and drops pressure. However, **fouling does not drop the water flow**. High approach with **normal** flow points to fouling. High approach with **low** flow points to a pump, strainer, or valve.
