# Non-condensable gas — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `noncondensables_80pct`.  
This guide explains what happens when "Air" (which doesn't belong) gets trapped inside the machine.

---

## 0. The Healthy State: How it should work

A centrifugal chiller is a "Pure" system. It should contain **only** refrigerant.

1.  **Pure Vapor:** In a healthy machine, the condenser contains 100% refrigerant gas. 
2.  **Saturation:** At any given temperature, pure refrigerant has a predictable pressure. This is called the **Saturation Line**. If you know the temperature, you know the pressure.
3.  **The Heat Dump:** Heat transfers smoothly from the pure gas to the cooling tubes.

---

## 1. The Fault: Non-Condensable Gas (Air)

**What it means.** Air or moisture has leaked into the machine (usually through a low-side seal during a vacuum) or the "Purge" system has failed. Air is a "non-condensable" gas—it won't turn into liquid like refrigerant does.

**What this scenario does.** It introduces a **2 percent** mole fraction of inert gas into the condenser.

**The "Blanket" Chain (How it hurts):**
1.  **Stage 1: Partial Pressure.** Air has its own pressure. When air mixes with refrigerant, the **Total Pressure (`CH-CON-RFT-PRES`)** rises (Total = Refrigerant Saturation Pressure + Air Pressure).
2.  **Stage 2: The Blanket.** Air collects in the top of the condenser and "blankets" the cooling tubes. 
3.  **Stage 3: Insulation.** Heat can't get through the "air blanket" to reach the tubes. This looks exactly like **severe fouling** in terms of efficiency.
4.  **Outcome: High Head.** The total pressure is now **Higher than the Saturation Line** (Dalton's Law). The compressor has to pedal against this "fake" pressure that doesn't correspond to the refrigerant's temperature.

---

## 3. The Telemetry: Key Signs

This is the most important "Detective" scenario because it mimics fouling:

*   **Approach:** **`CH-CON-APP-TEMP`**. This **rises** (gap widens) just like dirty tubes because of the blanketing.
*   **Pressure Gap:** Comparing **`CH-CON-RFT-PRES`** against the Saturation Chart. If the pressure is **higher** than it should be for the measured **`CH-CON-RFT-TEMP`**, you have air.
*   **Internal Proof:** **`P_noncondensable_Pa`** (Truth-Only) rises from zero.
*   **Power:** **`CH-KW_A`**. This **rises** as the machine fights the extra pressure.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** Air is introduced into the condenser.
2.  **+Order 1:** **Partial Pressure rises.** (Internal: `P_noncondensable_Pa`).
3.  **+Order 2:** **Total Pressure rises.** (Tag: `CH-CON-RFT-PRES`). It departs from the "Healthy" saturation line.
4.  **+Order 2:** **Tube Conductance falls.** The "blanket" effect starts.
5.  **+Order 4:** **Power usage rises.** The "Inefficiency" settles in.

---

## 9. The Big Picture

```
Inert Air (The Intruder)  -->  Tube Blanketing  -->  Fake High Pressure
            |                          |                       |
            v                          v                       v
      ONE KNOB: Mole %          ONE RESULT: Insulation  FINAL OUTCOME: High $
            |                          |                       |
            v                          v                       v
      83 Keppel Tags (Output)   "Sickness": Pressure > Saturation Line
```

**Summary:** Non-condensables are "Efficiency Thieves." They mimic fouling, but with one difference: **The pressure is too high for the temperature.** While fouling is a water-side problem, air is an internal chemistry problem.
