# Reduced condenser-water flow

Primary root cause: **less cooling-tower water through the condenser** (blocked strainer, valve failing closed, or condenser-water pump losing capacity).  
Not condenser fouling. The tubes can be clean. The water simply does not arrive.

**Evidence:** From **ASHRAE RP-1043** (fault FWC, −10/−20/−30/−40% flow). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane `HIGH DISCH PRESSURE` — reduced condenser water flow, pump, strainer, valve. Carrier 19XR protect **230** low condenser-water flow and **235** high condenser pressure (low water flow). York YK: “insufficient condensing water flow” → raise the quantity of water. Daikin Magnitude: `No Condenser Water Flow` / condenser pump fault.

---

## 0. The Healthy State

The chiller is a closed refrigerant loop that shuttles heat out of the building by moving it from a low-pressure side to a high-pressure side.

1. **Evaporator (the source).** Cold liquid refrigerant boils at low pressure and soaks up heat from the building chilled-water loop. That boil creates the **gas** the compressor will ingest.
2. **Compressor (the work).** The compressor pulls that low-pressure gas from the evaporator and squeezes it. The squeeze makes the gas **hot and high-pressure**. The heat in the discharge gas is the building heat plus the compressor’s own work.
3. **Lift (the climb).** **Lift** is the gap the compressor must climb: condenser pressure minus evaporator pressure (or saturated condenser temperature minus saturated evaporator temperature). Condenser pressure is the ceiling. Evaporator pressure is the floor. A taller ceiling, or a lower floor, is a steeper climb.
4. **Condenser (the sink).** Hot discharge gas enters the condenser. **Condenser water** from the cooling towers flows through the tubes. The gas is hotter than that water, so heat leaves the refrigerant, the gas condenses, and the water carries the heat to the tower.
5. **What “healthy” looks like.** Condenser-water flow is near design. The water warms a few degrees across the condenser (typical leaving minus entering of about 5 °C). On the current HT-CH-01 packs, refrigerant pressure sits about 92 kPa in the evaporator and about 185 kPa in the condenser. Power is the normal lift cost, not a fight against a blocked heat sink.

---

## 1. The Fault

**The knob.** Cut condenser-water flow and hold it (ASHRAE sizes: 10, 20, 30, then 40 percent less than design). The primary cause is the water path — strainer, valve, or pump — not dirt on the tube wall.

**Sensors to watch.** Lift is not a condenser-only story. You need both refrigerant pressures, plus the water that is supposed to dump the heat.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| Condenser-water flow | The knob | Falls first. This is the split from fouling. |
| Condenser-water ΔT (leaving minus entering) | How hard each kilogram of water is working | Rises. Same heat, fewer kilograms. |
| Condenser refrigerant pressure | The **ceiling** of the climb | Rises as heat fails to leave. |
| Evaporator refrigerant pressure | The **floor** of the climb | Stays near normal at first. You still need it, or you cannot see lift. |
| Lift (condenser pressure − evaporator pressure) | The hill the compressor climbs | Grows because the ceiling rises. |
| Compressor power / current | Cost of that hill | Rises with lift. |

Do not stop at condenser refrigerant pressure. The gas the compressor squeezes **comes from the evaporator**. If you never look at evaporator pressure, you cannot tell whether the extra work is a higher ceiling (this case), a collapsing floor (a leak), or both.

### Understanding Pressure and Lift

To diagnose this fault, you must distinguish between the measured pressures and the safety limits:

*   **Evaporator Refrigerant Pressure:** The "floor" of the cycle. It represents the state of the gas **before** it enters the compressor.
*   **Condenser Refrigerant Pressure:** The "ceiling" of the cycle. It represents the state of the gas **after** it has been compressed and is entering the condenser to be cooled.
*   **High Condenser (Discharge) Pressure:** This is not a separate measurement, but a **safety trip point**. When the condenser pressure (which is the same as the compressor's discharge pressure) rises too high, the machine shuts down to prevent damage.
*   **Lift:** The physical "climb" the compressor performs. It is calculated as the difference between the high-pressure ceiling (Condenser) and the low-pressure floor (Evaporator).

**Why you must check both:** The compressor doesn't just "create" pressure in the condenser; it **squeezes** the gas it gets from the evaporator. If you only look at the condenser, you are only seeing the result, not the work. Monitoring the evaporator refrigerant pressure tells you if the compressor is starting from a healthy "floor."

**The chain.**

1. **Flow drops.** Fewer kilograms of tower water pass the condenser tubes.
2. **Water heats up.** The compressor is still delivering roughly the same heat. Each remaining kilogram of water warms more, so **condenser-water ΔT rises**.
3. **Condenser refrigerant pressure rises.** The heat sink is weaker. The gas stays hotter. Pressure follows temperature up the saturation line. That is the ceiling moving up.
4. **Lift grows.** Evaporator pressure is still near normal at first, so the floor has not moved. Ceiling up, floor still: lift and kilowatts rise. kW per ton gets worse.
5. **Approach and surge margin.** The gap between hot refrigerant and the remaining water widens. The compressor operating point walks toward the stall / surge line.
6. **Trip.** OEM safeties stop the machine on **high condenser (discharge) pressure**. Trane: high discharge / HPCO. Carrier: 235. Daikin: high condenser pressure. If lift goes far enough first, the trip can be **surge** instead of the pressure cutout.

**Easy mix-up.** Condenser fouling also raises head pressure and power. Fouling does **not** drop condenser-water flow. This case does. High head with **normal** flow points to fouling (or non-condensables / overcharge). High head with **low** flow points to a pump, strainer, or valve.
