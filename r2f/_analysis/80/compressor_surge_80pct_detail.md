# Compressor surge (high-lift) — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `compressor_surge_80pct`.  
This guide explains one of the most violent mechanical events a chiller can experience: **Surge**.

---

## 0. The Healthy State: How it should work

A centrifugal compressor is like a high-performance jet engine. 

1.  **Lift vs. Flow:** The compressor's job is to "lift" gas from a low-pressure floor (Evaporator) to a high-pressure ceiling (Condenser).
2.  **Momentum:** As long as there is enough gas moving fast enough, it has the momentum to stay moving in one direction (toward the condenser).
3.  **Stability:** In a healthy machine, the compressor operates far away from its "stability limit." This safe gap is called the **Surge Margin**.

---

## 1. The Fault: Compressor Surge (Stall)

**What "Surge" means.** Surge is essentially the "stalling" of the compressor's engine. If the "ceiling" (Condenser Pressure) gets too high, or the "momentum" (Gas Flow) gets too low, the gas can no longer make the climb. It slips and falls backward into the compressor.

**The scenario.** In this file, we force a surge by spiking the **Entering Condenser Water Temperature** from a healthy **29.1°C to 44.1°C** (+15°C jump). 

**The "Bark" Chain (What happens):**
1.  **Stage 1: High Head.** The water returning from the tower gets hotter (**Tag: `HT-CH-01-CWST`**). Because the water is too hot to remove heat from the refrigerant gas, the gas temperature rises. In the closed volume of the condenser shell, this causes **Refrigerant Pressure (`CH-CON-RFT-PRES`)** to spike.
2.  **Stage 2: Instability.** The Surge Margin collapses to zero. The compressor begins to "pant" as it struggles to push gas into the high-pressure condenser.
3.  **Stage 3: The Surge Event.** The gas momentum fails. The flow reverses and crashes backward through the impeller. This creates a violent "thump" or "bark" and a massive vibration shock. It is like throwing a car into reverse while driving at 100 km/h.
4.  **Stage 4: LOCKOUT.** If the machine surges repeatedly, it will shatter internal seals and bearings. The safety system tracks the **Surge Count** and trips the machine after **12 pulses** to prevent total mechanical destruction.

---

## 3. The Telemetry: Key Signs

Surge is the most "Violent" scenario in the telemetry:

*   **Vibration:** **`CH-V-A`** (Vertical) and **`CH-H-A`** (Horizontal). These **spike** vertically during each surge pulse as the shaft is hammered by reversing gas.
*   **Power:** **`CH-KW_A`**. The electricity usage will **pulse or wobble** as the motor fights the shocks.
*   **Surge Count:** `surge_count` (Truth-Only). This increments with every "bark."
*   **Pressures:** **`CH-CON-RFT-PRES`** and **`CH-EVA-RFT-PRES`**. These will fluctuate wildly as gas rushes backward, momentarily balancing the two sides of the machine.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** Tower water temperature begins to spike.
2.  **+Order 1:** **Condenser Pressure rises.** The "Pressure Hill" becomes too steep.
3.  **+Order 2:** **Surge Margin collapses.** (Internal: `surge_margin` -> 0).
4.  **+Order 3:** **First SURGE occurs.** A violent vibration spike on **`CH-V-A`**.
5.  **+Subsequent:** Repeated surges occur as the machine tries to recover.
6.  **Terminal:** **TRIP.** The machine is locked out after 12 surges to save the thrust bearing.

---

## 9. The Big Picture

```
Hot Tower Water (Root Cause)  -->  High Head Pressure  -->  Gas Slip (Surge)
            |                            |                        |
            v                            v                        v
      ONE KNOB: CW Temp +15K      ONE RESULT: Stall        FINAL OUTCOME: Lockout
            |                            |                        |
            v                            v                        v
      83 Keppel Tags (Output)      "Violent Pulse": Vibration Spikes + Power Pulse
```

**Summary:** Surge is a "Mechanical Emergency." While fouling costs money, surge destroys parts. It is the result of an imbalance between the pressure the machine is fighting and the amount of gas it has to work with.
