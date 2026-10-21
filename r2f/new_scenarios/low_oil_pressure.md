# Low oil pressure — Zero to Hero Guide

Chiller **HT-CH-01**. This guide explains a critical bearing-protection scenario: what happens when the lubrication system fails to protect the high-speed rotating parts of the compressor.

---

## 0. The Healthy State: How it should work

A centrifugal chiller is a high-speed machine spinning at thousands of RPM. Without a constant film of oil, the metal bearings would melt in seconds. In a healthy state, the oil system is winning a **"Pressure Fight."**

1.  **The Oil Pump's Job:** The oil pump must force oil *into* the compressor bearings. However, these bearings are already sitting inside a chamber filled with high-pressure refrigerant gas.
2.  **The "Pressure Fight" (Differential Pressure):** To get oil inside, the pump must push **harder** than the refrigerant. This "extra push" is called **Differential Pressure (ΔP)**.
    *   **The Opponent:** Refrigerant pressure (Discharge Pressure).
    *   **The Defender:** Oil Pump pressure.
    *   **The Result (ΔP):** The difference between the two.
3.  **Healthy Numbers:** A healthy machine maintains a "win" of about **18–25 psid** (pounds per square inch differential). 
    *   *Example:* If the refrigerant is pushing at 100 psi, the oil pump must push at 120 psi. The **Net Oil Pressure** is 20 psid.
4.  **Temperature & Level:** The oil must stay warm (~55°C). If it gets too cold, refrigerant dissolves into the oil, making it "thin" and watery, which fails to protect the metal. 

---

## 1. The Fault: Lubrication Failure

**What "Low Oil Pressure" means.** It is not a refrigerant leak. It is a mechanical failure of the support system. It means the "conveyor belt" of oil has slowed down or stopped, leaving the bearings at risk of melting.

**Primary Root Causes:**
*   **Plugged Filter:** Debris blocks the path. The pump pushes, but nothing gets through.
*   **Weak Pump:** The pump motor is dying and can't create enough "push" (ΔP).
*   **Oil Foaming:** If the refrigerant boils inside the oil sump, it turns the oil into a "milkshake" of foam. A pump cannot move foam.
*   **Low Level:** There isn't enough oil to keep the pump primed.

**The "Bearing Death" Chain:**
1.  **Stage 1: The Pressure Sag.** The ΔP falls out of the safe 18-25 psid band. This is the very first sign of trouble.
2.  **Stage 2: The Heat-Up.** Without a fresh flow of cool oil, the bearings start to get hot. Metal-on-metal friction begins to create heat that the sensors can pick up.
3.  **Stage 3: Vibration.** As the oil film disappears, the shaft starts to wobble. Small pulses of vibration become heavy shakes.
4.  **Stage 4: TRIP.** The chiller's computer sees the low pressure (or high bearing temperature) and shuts down instantly. Unlike a slow leak, this happens in minutes, not hours.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The oil pump begins to degrade (or the filter starts to block).
2.  **+1 min:** **Differential Pressure falls.** The oil pump loses its "lead" in the pressure fight. (Keppel Tags: **`CH-OIL-DIS-PRES`** falls closer to **`CH-OIL-TK-PRES`**). This is the "Smoking Gun."
3.  **+5 min:** **Bearing Temperature rises.** The friction begins. (Keppel Tag: **`CH-OIL-TK-TEMP`** or specific bearing sensors).
4.  **+8 min:** **Vibration increases.** The machine starts to "growl." (Keppel Tags: **`CH-V-A`**, **`CH-H-A`**).
5.  **+10 min:** **TRIP.** Safety shutdown to save the shaft and bearings.

---

## 9. The Big Picture

```
Dedicated Oil Pump  -->  Filter & Cooler  -->  Compressor Bearings
                               |
                               v
                     ONE KNOB: Pump Capacity / Filter Blockage
                               |
                               v
                     83 Keppel Tags (Output)
                     (Oil ΔP down -> Bearing Temp up -> Vibration up -> TRIP)
```

**Summary:** This is a "Fast Failure" scenario. While the refrigerant side (pressures and temperatures) might look perfect, the machine is internally destroying itself. The only way to catch this is to watch the **Oil Differential Pressure**.
