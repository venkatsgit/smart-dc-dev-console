# Reduced condenser-water flow

Primary root cause: **less cooling-tower water through the condenser** (blocked strainer, valve failing closed, or condenser-water pump losing capacity).  
Not condenser fouling. The tubes can be clean. The water simply does not arrive.

**Evidence:** From **ASHRAE RP-1043** (fault FWC, −10/−20/−30/−40% flow). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane `HIGH DISCH PRESSURE` — reduced condenser water flow, pump, strainer, valve. Carrier 19XR protect **230** low condenser-water flow and **235** high condenser pressure (low water flow). York YK: “insufficient condensing water flow” → raise the quantity of water. Daikin Magnitude: `No Condenser Water Flow` / condenser pump fault.

---

## 0. The Healthy State

The chiller is a closed refrigerant loop that shuttles heat out of the building.

1. **Evaporator.** Cold liquid refrigerant boils and soaks up heat from the chilled-water loop.
2. **Compressor.** It squeezes that gas, making it hot and high-pressure. That squeeze is the climb, or **lift**, from evaporator pressure up to condenser pressure.
3. **Condenser.** A steady stream of **condenser water** from the cooling towers flows through the tubes. The hot gas dumps its heat into that water and turns back into liquid.
4. **Why flow matters.** The water is the only way heat leaves the machine. In a healthy hour the flow is near design. The water warms a few degrees as it crosses the condenser (typical leaving minus entering of about 5 °C). Condenser pressure stays in a band the compressor can climb (on the current HT-CH-01 packs, about 92 kPa up to about 185 kPa).
5. **What “healthy” looks like on meters.** Condenser-water flow is steady. Entering condenser-water temperature follows the tower, not a sudden jump. Condenser refrigerant temperature and pressure sit close to the water. Compressor power is the normal lift cost, not a fight against a blocked heat sink.

---

## 1. The Fault

**The knob.** Cut condenser-water flow and hold it (ASHRAE sizes: 10, 20, 30, then 40 percent less than design). The primary cause is the water path — strainer, valve, or pump — not dirt on the tube wall.

**The chain.**

1. **Less water, same heat.** The compressor is still delivering roughly the same heat into the condenser. Fewer kilograms of water must carry that heat, so each kilogram warms more. **Condenser-water ΔT rises** and **flow falls**. That pair is the first split from fouling (fouling leaves flow alone).
2. **The refrigerant cannot dump heat.** With a weaker heat sink, the gas stays hotter. Condenser refrigerant temperature rises. Pressure follows it up the saturation line.
3. **The climb gets taller.** Evaporator pressure is still near normal at first. The “ceiling” (condenser pressure) rises. Lift and compressor power rise. Kilowatts per ton get worse.
4. **Approach and surge margin.** The gap between hot refrigerant and the remaining water widens. The compressor operating point walks toward the stall / surge line.
5. **Trip.** OEM safeties stop the machine on **high condenser (discharge) pressure**. Trane calls it high discharge / HPCO. Carrier 235. Daikin high condenser pressure. If lift goes far enough first, the trip can be **surge** instead of the pressure cutout.

**Easy mix-up.** Condenser fouling also raises head pressure and power. Fouling does **not** drop condenser-water flow. This case does.
