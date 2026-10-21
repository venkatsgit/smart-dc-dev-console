# Cooling-tower fan failed

Primary root cause: **a cooling-tower fan (or a cell) stops**, so the tower cannot reject heat.  
The entering condenser-water temperature rises. The chiller tubes are clean and the water flow is normal, but the "sink" is too hot.

**Evidence:** Taken from the **Trane**, **Carrier**, **York / JCI**, and **Daikin** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVX005E-EN.pdf`](references/Trane_CVHE-SVX005E-EN.pdf), [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf), [`Daikin_IOM1210_Magnitude_WMC-D.pdf`](references/Daikin_IOM1210_Magnitude_WMC-D.pdf), [`Daikin_IOM1372_Magnitude_WME-D.pdf`](references/Daikin_IOM1372_Magnitude_WME-D.pdf).  
**Sources (same trip names in OEM manuals):** Trane high discharge — **high condenser water entering temperature**. Carrier 19XR **235** — high condenser water temperatures. York YK: reduce condenser-water inlet temperature. Daikin: condenser-water temperature and flow as high-pressure causes.

---

## 0. The Healthy State

The cooling tower is the "heat dump" for the entire chiller plant.

1. **The Heat Dump.** Hot water leaves the chiller condenser, goes to the tower, gets cooled by outdoor air (moved by fans), and returns to the chiller as **Entering Condenser Water**.
2. **The Fan's Job.** The fans pull air through the tower to evaporate a small amount of water, which carries the building's heat away into the atmosphere. 
3. **Lift (The Climb).** The compressor lifts heat from the building "floor" to the tower "ceiling." A healthy tower keeps the ceiling low (e.g., **29 °C** return water), making the compressor's job easier.
4. **What "healthy" looks like.** The **Entering Condenser Water Temperature** (`CH-CON-E-TEMP`) follows a smooth daily swing based on the weather. Tower fans are running. Condenser pressure is normal for the current outdoor temperature. Chiller power (kW) is steady.

---

## 1. The Fault: Fan Failure

**The knob.** Fail one or more tower fans, or simulate a dead tower cell. This causes the **Entering Condenser Water Temperature** to rise sharply while the water **flow** stays normal.

**Sensors to watch.** The primary signature is that the water arrives at the chiller already "too hot."

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| Entering Condenser Water Temp | The "sink" temperature | **Spikes.** The water comes back from the tower without being cooled. |
| Condenser Refrigerant Pressure | The **ceiling** of the climb | **Rises.** The gas cannot dump heat into hot water, so pressure builds. |
| Condenser Water Flow | The transport rate | **Normal.** The pumps are still moving water, but the water is hot. |
| Evaporator Refrigerant Pressure | The **floor** of the climb | Stays normal. |
| Lift (Condenser - Evaporator) | The hill the compressor climbs | **Grows** because the ceiling rises. |
| Compressor Power / kW | Motor effort | **Rises** as lift increases. |

### Understanding Pressure and Lift

To diagnose a tower failure, you must look at the water temperature entering the machine:

*   **Entering Condenser Water Temp:** This is the temperature of the "sink." If this rises, the refrigerant has nowhere to dump its heat.
*   **Condenser Refrigerant Pressure:** The "ceiling." It rises because the refrigerant gas stays hot. It cannot condense into a liquid if the water touching the tubes is already near the refrigerant's boiling point.
*   **Lift:** The physical "climb." Since the building "floor" (Evaporator) is fine, but the outdoor "ceiling" (Condenser) has risen due to the fan failure, the compressor must work much harder.

**Why this is different from Fouling:** In **fouling**, the water entering the machine is cool, but the tubes are dirty. In **fan failure**, the tubes are clean, but the water entering the machine is **already hot**.

**The chain.**

1. **Tower fan stops.** The air flow through the tower fill disappears. Heat rejection stops.
2. **Entering water temperature rises.** The water loop quickly warms up because it isn't being cooled outdoors.
3. **Condenser pressure rises.** The hot refrigerant gas in the condenser meets hot water. Heat transfer slows down, and pressure builds. The **ceiling moves up**.
4. **Lift grows.** With a normal floor (Evaporator) and a rising ceiling (Condenser), the compressor work and **kW rise**.
5. **Trip.** The machine hits the **High Condenser (Discharge) Pressure** limit or potentially **Surge** as the lift becomes too steep for the compressor to handle.

**Easy mix-up.** Condenser fouling and reduced flow. Split:
*   **Reduced Flow:** Flow is down, water ΔT is up, but entering temperature is normal.
*   **Fouling:** Flow is normal, entering temperature is normal, but pressure is high.
*   **Fan Failure:** Flow is normal, but **Entering Temperature is high**.
