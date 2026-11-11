# Reduced chilled water flow — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `reduced_chw_flow_80pct`.  
This guide explains what happens when the "Heat Sponge" can't move enough water to soak up building heat.

---

## 0. The Healthy State: How it should work

The evaporator’s job is to "sponge up" heat from the building.

1.  **The Building Loop:** A pump moves **Chilled Water** (the blue loop) from your server rooms to the chiller. In the chiller, the water is cooled down and sent back to the building.
2.  **Steady Flow:** A healthy machine moves a steady stream of water (~150 l/s). This water enters warm and leaves cool.
3.  **Heat Removal:** The amount of heat removed depends on the **Flow Rate**. If the flow is too slow, the water stays in the machine too long and can get "over-cooled."

---

## 1. The Fault: Reduced Chilled Water Flow

**What it means.** A pump degradation or a valve blockage in the building loop. The machine is trying to cool water that is barely moving.

**What SL2 means.** Severity Level 2. In this scenario, exactly **20 percent** of the chilled water flow is lost.

**The "Freeze" Chain (How it hurts):**
1.  **Stage 1: Blockage (Midnight).** Chilled water flow immediately drops by 20% (**Tag: `CH-CHWR-FLOW`**).
2.  **Stage 2: Over-Cooling.** Because the water is moving slower, it stays in contact with the freezing refrigerant for longer. The water temperature drops lower than the setpoint.
3.  **Stage 3: Pressure Collapse.** The chiller computer sees the water getting too cold. It drops its **boiling pressure (Suction Pressure)** even lower to try and maintain control. You will see **Tag: `CH-EVA-RFT-PRES`** fall.
4.  **Outcome: Freeze Risk.** If the flow drops too far, the water can actually **freeze** inside the tubes, which would rupture the metal and destroy the chiller.
5.  **Efficiency:** Like evaporator fouling, the lower Suction Pressure makes the machine less efficient.

---

## 3. The Telemetry: Key Signs

*   **Flow Rate:** **`CH-CHWR-FLOW`**. This is the "Smoking Gun." It drops and stays low.
*   **Refrigerant Pressure:** **`CH-EVA-RFT-PRES`**. This **falls** as the "floor" of the machine drops to prevent the water from over-cooling.
*   **Refrigerant Temperature:** **`CH-EVA-RFT-TEMP`**. This **falls** along with the pressure.
*   **Leaving Water:** **`CH-CHWST`**. This may drop lower than the setpoint (e.g., 6.5°C -> 5.5°C) before the machine manages to unload.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The flow blockage occurs.
2.  **+Order 1:** **Flow (`CH-CHW-FLOW`) drops** immediately.
3.  **+Subsequent:** **Evaporator Pressure (`CH-EVA-RFT-PRES`) falls.** The machine "digs deeper."
4.  **+Subsequent:** **Efficiency degrades.** Power usage rises relative to the cooling delivered.
5.  **Terminal:** **TRIP.** Safety shutdown on Low Evaporator Pressure (to prevent freezing).

---

## 9. The Big Picture

```
Water Pump (Input)  -->  Evaporator Tubes  -->  Cool to Building
        |                        |
        v                        v
   ONE KNOB: Blockage       ONE RESULT: Over-Cooling / Freeze
        |                        |
        v                        v
   83 Keppel Tags (Output)  Final Outcome: Low Pressure Trip
   (Flow down | Pressure down | Efficiency down)
```

**Summary:** Reduced chilled water flow is a "Safety Risk." While fouling is a slow drain, flow loss can lead to a catastrophic freeze event. The machine will usually trip on **Low Evaporator Pressure** to protect itself.
