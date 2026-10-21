# Refrigerant overcharge

Primary root cause: **too much refrigerant was charged into the closed loop.**  
This is the physical opposite of the gas and liquid leaks already in the current pack.

**Evidence:** From **ASHRAE RP-1043** (fault RO, +10/+20/+30/+40% extra charge). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane high discharge warning: high subcooling with high head indicates overcharge or non-condensables. Carrier 19XR high condenser pressure list (with fouling / flow / air). York YK high discharge with air or dirty tubes — overcharge sits in the same high-head family.

---

## 0. The Healthy State

The chiller is a closed loop with a fixed mass of refrigerant (approx. **1150 kg** for the HT-CH-01 twin).

1. **The Two Pools.** Refrigerant is stored in two liquid pools:
    *   **Evaporator Pool:** Large (~810 kg). Must cover the tubes so they can boil refrigerant and cool the building.
    *   **Condenser Pool:** Smaller (~270 kg). Acts as a "seal" and allows for extra cooling of the liquid.
2. **Subcooling (The "Liquid Coldness").** After gas turns back into liquid in the condenser, it stays in contact with the cool tower water and drops a few degrees below its boiling point. This is **subcooling** (Healthy = **4–5 °C**).
3. **Lift (The Climb).** The compressor lifts gas from the evaporator "floor" (~92 kPa) to the condenser "ceiling" (~185 kPa). Power consumption depends on the height of this climb.
4. **What "healthy" looks like.** Refrigerant mass is at nameplate design. Subcooling is steady. Condenser pressure follows the tower water temperature. The expansion valve meters liquid back to the evaporator at the same rate the compressor sends gas up.

---

## 1. The Fault: Overcharge

**The knob.** Inject extra refrigerant mass into the system (ASHRAE steps: 10%, 20%, 30%, 40% above design). There is no leak; the total kilograms in the machine **increase**.

**Sensors to watch.** Subcooling is the primary diagnostic signature that separates this from a leak.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| Refrigerant Mass | The knob | **Increases.** More kilograms are in the loop. |
| Subcooling | The "pool depth" indicator | **Rises.** A deeper pool in the condenser gets extra cooling. |
| Condenser Refrigerant Pressure | The **ceiling** of the climb | **Rises.** Excess liquid blocks the gas from condensing. |
| Evaporator Refrigerant Pressure | The **floor** of the climb | Stays near normal at first. |
| Lift (Condenser - Evaporator) | The hill the compressor climbs | **Grows** because the ceiling rises. |
| Compressor Power / kW | Cost of that hill | **Rises** with lift. |

### Understanding Pressure and Lift

To diagnose overcharge, you must look at why the "ceiling" is moving:

*   **Evaporator Refrigerant Pressure:** The "floor." In overcharge, the evaporator tubes are fully submerged, so the floor stays healthy and stable.
*   **Condenser Refrigerant Pressure:** The "ceiling." It rises because the extra liquid refrigerant floods the condenser tubes, leaving less room for the hot gas to turn back into liquid. The pressure builds up as a result.
*   **Lift:** The physical "climb." Since the floor is stable but the ceiling is rising, the compressor has to work much harder to push gas into the flooded condenser.

**Why Subcooling is the "Smoking Gun":** In a **leak**, subcooling **falls** because the condenser pool is empty. In **overcharge**, subcooling **rises** because the condenser pool is too deep. This single sensor tells you if the machine is "starving" or "choking."

**The chain.**

1. **Extra mass enters.** The liquid pool in the condenser begins to stack up.
2. **Subcooling rises.** The deep pool of liquid refrigerant is cooled significantly by the tower water. Subcooling moves from 5 °C toward 10 °C or higher.
3. **Condensing area shrinks.** Liquid occupies the tube space that was meant for gas. The "condensing capacity" drops.
4. **Condenser pressure rises.** Because the gas has less room to condense, it stays as a high-pressure vapour longer. The **ceiling moves up**.
5. **Lift grows.** With a normal floor (Evaporator) and a rising ceiling (Condenser), the compressor work increases. **kW and kW/ton rise**.
6. **Trip.** The machine hits the **High Condenser (Discharge) Pressure** limit (Trane HPCO, Carrier 235).

**Easy mix-up.** Condenser fouling also raises pressure and power. However, **fouling does not raise subcooling** (it usually lowers it slightly as heat transfer fails). Only overcharge or non-condensables (air) will show the "High Pressure + High Subcooling" signature.
