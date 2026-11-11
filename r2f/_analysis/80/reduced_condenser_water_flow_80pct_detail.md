# Reduced condenser water flow — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `reduced_cond_water_flow_80pct`.  
This guide explains what happens when the "Heat Dump" part of the machine stops moving enough water to carry heat away.

---

## 0. The Healthy State: How it should work

The condenser’s only job is to get rid of heat.

1.  **The Tower Loop:** Heat from your building is carried by refrigerant to the condenser. From there, **Condenser Water** (the red loop) carries it to the cooling towers on the roof.
2.  **Steady Flow:** In a healthy machine, the Condenser Water Pump moves a steady stream of water (~200 l/s). This water enters cool and leaves warm, carrying the building's heat with it.
3.  **Heat Capacity:** The amount of heat the water can carry depends on its **Flow Rate**. If the flow slows down, the water can't carry enough heat.

---

## 1. The Fault: Reduced Condenser Flow

**What it means.** This is a blockage or a pump failure. It’s like a clogged drain—the pump is trying to push, but the path is restricted.

**What SL2 means.** Severity Level 2. In this scenario, exactly **20 percent** of the water flow is lost.

**The "Backup" Chain (How it hurts):**
1.  **Stage 1: Blockage (Midnight).** Water flow immediately drops by 20% (**Tag: `CH-CWS-FLOW`**).
2.  **Stage 2: Heat Stagnation.** Because there is less water moving through the tubes, each liter of water has to pick up "extra" heat. The water in the condenser gets hotter.
3.  **Stage 3: Pressure Lift.** Heat "backs up" into the refrigerant. The refrigerant gas gets hotter and its **pressure (High Side Pressure) rises**. You will see **Tag: `CH-CON-RFT-PRES`** climb.
4.  **Stage 4: Compressor Strain.** The compressor now has to work much harder to push gas into this high-pressure chamber. 
5.  **Outcome: High Head.** The machine uses **more Power (`CH-KW_A`)** and risks a "High Condenser Pressure" trip as the operating point moves toward the surge boundary.

---

## 3. The Telemetry: Key Signs

*   **Flow Rate:** **`CH-CWS-FLOW`**. This is the "Smoking Gun." It drops and stays low.
*   **Refrigerant Pressure:** **`CH-CON-RFT-PRES`**. This **rises** because heat is trapped in the shell.
*   **Refrigerant Temperature:** **`CH-CON-RFT-TEMP`**. This **rises** along with the pressure, following the saturation line.
*   **Power:** **`CH-KW_A`**. This **rises** as the compressor struggles against the "Head Pressure."

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The flow blockage occurs.
2.  **+Order 1:** **Flow (`CH-CWS-FLOW`) drops** immediately.
3.  **+Subsequent:** **Condenser Pressure (`CH-CON-RFT-PRES`) rises.** Heat starts backing up.
4.  **+Subsequent:** **Power (`CH-KW_A`) rises.** The compressor feels the "heavier lift."
5.  **Outcome:** The machine settles into a new, higher-power state. If the flow drops further, it will hit a High Pressure Limit and trip.

---

## 9. The Big Picture

```
Water Pump (Input)  -->  Condenser Tubes  -->  Heat to Tower
        |                        |
        v                        v
   ONE KNOB: Blockage       ONE RESULT: Heat Backup
        |                        |
        v                        v
   83 Keppel Tags (Output)  Final Outcome: High Power / High Pressure
   (Flow down | Pressure up | Power up)
```

**Summary:** Reduced condenser flow is a "efficiency drain" that leads to a mechanical trip. It looks similar to fouling, but the **Flow meter** tells you it's a water-side problem (pump/valve) rather than a dirt problem (tubes).
