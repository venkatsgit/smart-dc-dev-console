# Inlet guide vanes stuck closed

Primary root cause: **capacity control stuck too far closed** (inlet guide vanes on a centrifugal, or York PRV).  
The refrigerant charge and the water flows are healthy. The compressor simply will not "swallow" the gas it needs to cool the building.

**Evidence:** Taken from the **Trane**, **Carrier**, and **York / JCI** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`Carrier_19XR_startup.pdf`](references/Carrier_19XR_startup.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf).  
**Sources (same trip names in OEM manuals):** York YK: high evaporator pressure / high chilled-water temperature — “PRVs fail to open.” Carrier 19XR: check inlet guide vane and diffuser actuator. Trane CH530 modulates vanes as the main capacity handle.

---

## 0. The Healthy State

The chiller uses Inlet Guide Vanes (IGVs) as its primary "throttle" to manage the cooling load.

1. **What are Inlet Guide Vanes (IGVs)?** 
    *   **Mechanical Flaps:** They are a ring of movable metal blades located at the **intake** of the compressor. They look like a camera shutter or venetian blinds.
    *   **The Throttle:** By pivoting these blades, the chiller controls exactly how much refrigerant gas the compressor "swallows." 
    *   **Open (High Load):** The blades turn sideways to allow maximum gas flow.
    *   **Closed (Low Load):** The blades pivot to block most of the opening, restricting gas flow when the building doesn't need much cooling.
2. **Capacity Control Logic.** The chiller's computer monitors the **Leaving Chilled Water Temperature**. 
    *   If the water is too warm, it commands the IGVs to open further.
    *   If the water is too cold, it commands them to close. 
    *   In a healthy state, this maintains the building at a steady setpoint (e.g., 7 °C).
3. **The Refrigerant Loop.** A healthy machine has a full charge (~1150 kg). The compressor "lifts" the gas from the evaporator floor (~92 kPa) to the condenser ceiling (~185 kPa).
4. **What "healthy" looks like.** 
    *   **Movement:** The **IGV Position (%)** is dynamic. It moves up and down throughout the day as the building load changes.
    *   **Stability:** The leaving chilled-water temperature stays locked on its setpoint.
    *   **Proportional Work:** The compressor's power (kW) and current (RLA%) move in sync with the vane position. If the vanes are 80% open, the motor should be doing significantly more work than at 20% open.

---

## 1. The Fault: Stuck Closed

**The knob.** Freeze the IGV position at a low percentage (e.g., 20% open) even as the building load increases. The refrigerant charge and water flows remain perfectly normal.

**Sensors to watch.** The primary signature is a "lazy" machine that refuses to cool despite having plenty of refrigerant and water.

| Sensor | Role | What happens in this fault |
| --- | --- | --- |
| IGV Position (Feedback) | The throttle state | **Stuck Low.** Does not open even when the building warms up. |
| Cooling Capacity (Tons) | Total heat removed | **Flatlines.** The machine cannot move enough gas to meet the load. |
| Chilled-Water Temp (Out) | The building's comfort | **Rises.** The building gets warmer because the chiller is "choked." |
| Evaporator Refrigerant Pressure | The **floor** of the climb | **Rises.** The gas is not being "sucked out" fast enough, so it piles up. |
| Compressor Power / kW | Motor effort | **Stays Low.** The compressor isn't doing much work because it's restricted. |
| Lift (Condenser - Evaporator) | The hill the compressor climbs | **Shrinks.** The floor (Evaporator) rises toward the ceiling. |

### Understanding Pressure and Lift

To diagnose stuck vanes, you must look at how the "floor" (Evaporator) responds to the "throttle":

*   **Evaporator Refrigerant Pressure:** The "floor." It **rises** because the compressor is "choking" its intake. Gas is boiling off the tubes, but the closed vanes prevent the compressor from sucking it away. The gas piles up in the evaporator.
*   **Condenser Refrigerant Pressure:** The "ceiling." It stays normal or falls slightly because less heat is being delivered to the condenser.
*   **Lift:** The physical "climb." The "hill" actually gets **shorter** (because the floor is rising). However, the machine is failing because it isn't moving enough mass, not because the climb is too hard.

**Why this is "Lazy" behavior:** Unlike fouling (where the machine works too hard) or a leak (where the machine starves), stuck vanes make the machine act like it's "sleeping." It draws low power and has low lift, but the building is not getting cold.

**The chain.**

1. **Vanes jam at a low opening.** The "throttle" is stuck in the idle position.
2. **Building load rises.** The hall gets hotter and sends warmer water to the chiller.
3. **Evaporator boils more gas.** The warmer water makes the refrigerant boil faster.
4. **Gas piles up in the evaporator.** Because the vanes are closed, the compressor cannot "swallow" this extra gas. **Evaporator pressure rises**.
5. **Leaving chilled-water temperature rises.** The machine cannot remove enough heat. The building starts to lose cooling.
6. **Lift shrinks.** With a rising floor and a steady ceiling, the compressor does very little work. **kW remains low**.
7. **Trip.** The machine may not trip on a refrigerant fault at all. Instead, it might trigger a **High Chilled-Water Temperature** alarm or eventually **Surge** if the flow gets too low for the current lift.

**Easy mix-up.** Refrigerant leak. Split: A leak makes the evaporator pressure **collapse** (floor drops). Stuck closed vanes make the evaporator pressure **rise** (floor moves up).
