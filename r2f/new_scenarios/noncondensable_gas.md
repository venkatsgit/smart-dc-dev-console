# Non-condensable gas in the refrigerant

Primary root cause: **air or nitrogen in the refrigerant circuit** (poor evacuation after service, or a failed purge on a low-pressure machine).  
Not dirt. Not extra refrigerant. A gas that **will not condense** at condenser temperature is occupying space and adding pressure.

**Evidence:** From **ASHRAE RP-1043** (fault NC, +1/+2/+3/+5% non-condensable). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane high head: non-condensable gases in the circuit. Carrier 19XR **235** — check for non-condensables. York YK: high discharge with condensing-to-water difference high -> “Air is in the condenser”; purging removes foul gas and reveals whether fouling remains.

---

## 0. The Healthy State

The chiller is a closed loop that should contain only refrigerant and a small amount of oil.

1. **Pure Refrigerant.** After a correct deep vacuum, no air or moisture is left in the shells. The pressure in the machine follows the **saturation line** (a fixed relationship between temperature and pressure).
2. **Condensing Action.** In the condenser, hot gas from the compressor meets the cool tower water. Because it is pure refrigerant, it turns into liquid at a predictable pressure based on its temperature.
3. **The Compressor Climb.** Gas is lifted from the evaporator "floor" (~92 kPa) to the condenser "ceiling" (~185 kPa). 
4. **What "healthy" looks like.** Condenser refrigerant pressure matches the saturation pressure for the observed temperature. Subcooling is normal (4–5 °C). The compressor work is steady.

---

## 1. The Fault: Non-Condensables

**The knob.** Introduce a small volume of air or nitrogen into the high-pressure side (ASHRAE steps: 1%, 2%, 3%, 5%). Air is a "non-condensable" gas—it stays a gas no matter how much the tower water cools it.

**Sensors to watch.** The key is seeing pressure that is "too high" for the current temperature.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| Condenser Refrigerant Pressure | The **ceiling** of the climb | **Rises.** Air adds its own "partial pressure" to the refrigerant. |
| Evaporator Refrigerant Pressure | The **floor** of the climb | Stays near normal. |
| Lift (Condenser - Evaporator) | The hill the compressor climbs | **Grows** because the ceiling rises. |
| Condenser Approach | Heat transfer gap | **Widens.** Air blocks the gas from reaching the tube surface. |
| Subcooling | Pool depth indicator | Stays **normal** or rises slightly (unlike overcharge which spikes). |
| Compressor Power / kW | Cost of that hill | **Rises** with lift. |

### Understanding Pressure and Lift

To diagnose non-condensables, you must look at the "ceiling" vs. the "floor":

*   **Evaporator Refrigerant Pressure:** The "floor." Since the air usually sits in the condenser (the high-pressure side), the evaporator remains relatively unaffected at first.
*   **Condenser Refrigerant Pressure:** The "ceiling." It rises because the air takes up space in the condenser and adds its own pressure to the refrigerant's pressure. The total pressure is now **Refrigerant + Air**.
*   **Lift:** The physical "climb." The compressor has to push against this "extra" air pressure, making the hill much taller and harder to climb.

**Why this is different from Overcharge:** Both raise the ceiling. However, **Overcharge** is extra liquid (high subcooling). **Non-condensables** are extra gas (normal subcooling but "extra" pressure above the saturation line).

**The chain.**

1. **Air enters the loop.** It gathers in the top of the condenser because it won't turn into liquid.
2. **Partial pressure builds.** The compressor is now discharging into a space filled with two gases. The **condenser pressure rises** beyond what the temperature suggests it should be.
3. **Heat transfer is blocked.** The air forms a "blanket" around the condenser tubes, preventing the refrigerant gas from touching the cold metal. **Condenser approach widens**.
4. **Lift grows.** The "ceiling" is pushed up by the air pressure. The compressor work increases, and **kW / current rise**.
5. **Trip.** The machine eventually hits the **High Condenser (Discharge) Pressure** limit or potentially **Surge** if the air makes the climb too steep.

**Easy mix-up.** Condenser fouling. Split: Fouling is dirt on the tubes (steady pressure rise, high approach). Non-condensables are air in the gas (often leads to **fluctuating discharge pressure** or pressure that is higher than the saturation temperature allows). If you purge the air and the pressure drops, it was non-condensables. If it stays high, it's fouling.
