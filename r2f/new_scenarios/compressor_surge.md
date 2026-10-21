# Compressor Surge — Zero to Hero Guide

Chiller **HT-CH-01**. This guide explains one of the most violent events a chiller can experience: **Surge**. It is essentially the "stalling" of the compressor's engine.

---

## 0. The Healthy State: How it should work

A centrifugal compressor is like a high-performance jet engine. It uses a spinning wheel (impeller) to throw refrigerant gas outward at incredible speeds, creating pressure. In a healthy state, the machine is in a perfect balance of **"Momentum vs. Resistance."**

1.  **The "Hill" (Lift):** The compressor's job is to push gas from the cold evaporator up to the hot condenser. Think of the pressure difference between these two as a **Hill**. The hotter the outside weather, the steeper the hill.
2.  **The "Momentum" (Flow):** As long as the compressor moves enough gas (Flow) at high enough speeds, the gas has the momentum to make it over the hill.
3.  **Surge Margin (The Safety Gap):** The chiller's computer calculates how much "extra momentum" it has before the gas would fail to climb the hill. This gap is the **Surge Margin**.
    *   **Healthy:** Large gap (e.g., 20%). The gas flows smoothly in one direction.
    *   **Unhealthy:** Small gap (e.g., <5%). The gas is "panting" and ready to slip.

---

## 1. The Fault: Compressor Surge (The Stall)

**What "Surge" means.** It is the sudden **reversal of flow**. If the hill becomes too steep (High Head Pressure) or the momentum becomes too weak (Low Flow), the gas stops moving forward and "falls" back into the compressor.

**Primary Root Causes:**
*   **The "Steep Hill" (High Head):** The Cooling Tower fans fail or the condenser tubes are fouled. The pressure the compressor must fight against becomes too high.
*   **The "Slow Speed" (Low Load):** The building isn't asking for much cooling, so the "throttle" (Inlet Guide Vanes) closes. If it closes too much, the flow loses the momentum needed to stay on the hill.

**The "Violent Stall" Chain:**
1.  **Stage 1: The Wobble.** Before the crash, the electricity usage (**`CH-KW_A`**) starts to pulse. The compressor is struggling to keep the gas moving, like a car engine sputtering before it stalls.
2.  **Stage 2: The Crash (Surge).** The gas finally slips. It rushes backward through the spinning impellers with a violent "thump" or "bark."
3.  **Stage 3: The Shockwave.** This reversal creates a massive vibration spike. It’s like throwing a metal rod into a spinning fan.
4.  **Stage 4: Automatic TRIP.** To prevent the internal seals and bearings from shattering, the machine shuts itself down immediately.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The root cause begins (e.g., a Cooling Tower fan trips).
2.  **+2 min:** **Condenser Pressure rises.** The "Hill" gets steeper. (Keppel Tag: **`CH-CON-RFT-PRES`**).
3.  **+5 min:** **Surge Margin collapses.** The machine is now at the edge of the cliff. (Internal calculation: `surge_margin`).
4.  **+7 min:** **Power Pulsing.** Electricity usage becomes unstable. (Keppel Tag: **`CH-KW_A`**).
5.  **+8 min:** **SURGE.** A violent mechanical shock occurs. (Keppel Tags: **`CH-V-A`**, **`CH-H-A`** jump).
6.  **+9 min:** **TRIP.** The machine shuts down to prevent catastrophic mechanical failure.

---

## 9. The Big Picture

```
Momentum (Flow)  vs.  Resistance (Lift)  -->  Smooth One-Way Flow
      |                      |
      +----------+-----------+
                 |
                 v
      IF LIFT > MOMENTUM = SURGE
                 |
                 v
      83 Keppel Tags (Output)
      (Power Pulsing -> Vibration Shock -> Machine TRIP)
```

**Summary:** While fouling is like a "slow leak" in your wallet, Surge is a "heart attack" for the machine. It is a violent mechanical event caused by the compressor losing its fight against pressure. The primary warning signs are **Power Instability** and **Shrinking Surge Margins**.
