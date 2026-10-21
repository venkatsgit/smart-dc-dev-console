# Reduced evaporator-water flow

Primary root cause: **less building chilled water through the evaporator** (blocked strainer, valve failing closed, or chilled-water pump losing capacity).  
Not evaporator fouling. The tubes can be clean. The water simply does not arrive.

**Evidence:** From **ASHRAE RP-1043** (fault FWE, −10/−20/−30/−40% flow). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane `LOW EVAP PRESSURE` — low chilled-water flow. Carrier 19XR protect **229** low chilled-water flow and **232** low refrigerant temperature (check fluid flow). Daikin Magnitude: `No Evaporator Water Flow`, evaporator pump fault, low evaporator pressure from low/no evaporator flow.

---

## 0. The Healthy State

1. **Job of chilled water.** A pump sends a steady stream of building water through the evaporator tubes. The cold refrigerant boils on the other side of those tubes and pulls heat out of that water. The water leaves colder (leaving chilled-water temperature) and goes back to the hall.
2. **Why flow must stay up.** Design flow gives the water enough time in the tubes and enough mass to carry the cooling load. Leaving water holds the setpoint. Evaporator pressure sits on the saturation line of a wet, covered bundle.
3. **The rest of the loop.** The compressor still lifts gas to the condenser. Tower water still rejects heat. Charge and oil are normal. Nothing is leaking.
4. **What “healthy” looks like.** Evaporator-water flow is steady. The water ΔT (entering minus leaving) is the normal few degrees. Leaving chilled-water temperature holds setpoint. Evaporator refrigerant pressure is not collapsing.

---

## 1. The Fault

**The knob.** Cut evaporator (chilled-water) flow and hold it. Primary cause is the water path, not scale on the tubes.

**The chain.**

1. **Less water, same compressor still trying to cool.** Fewer kilograms of water pass the tubes. Each kilogram that does pass is cooled more, so **chilled-water ΔT rises** and **flow falls**. That is the first meter pair that is not fouling.
2. **The hall starts to lose cooling.** Total tons fall because tons are flow times ΔT, and flow has dropped more than ΔT can make up. **Leaving chilled-water temperature** eventually cannot hold setpoint if the plant cannot send enough water.
3. **The refrigerant side gets too cold.** With less heat arriving from the water, boiling can drop to a lower temperature. Evaporator pressure falls with it. Approach (water versus refrigerant) changes.
4. **Freeze and low-pressure risk.** OEM text is blunt: low or no evaporator flow is a listed cause of **low evaporator pressure** and of **evaporator freeze** while the machine is off or starving. Daikin names both. Trane and Carrier trip or warn on low evaporator pressure / low refrigerant temperature.
5. **Trip.** Typical ends: **low evaporator pressure**, **low refrigerant temperature**, or **loss of evaporator-water flow** (flow switch / ΔP). The compressor is not “out of charge.” The water that feeds it heat has been throttled.

**Easy mix-up.** Evaporator fouling also widens evaporator approach and can raise leaving-water temperature. Fouling leaves **flow** alone. This case drops flow first.
