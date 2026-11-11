# Refrigerant overcharge — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `overcharge_80pct`.  
This guide explains what happens when a maintenance error leaves "too much" refrigerant in the machine.

---

## 0. The Healthy State: How it should work

A healthy chiller is carefully "balanced" with the exact right amount of refrigerant mass (~1150 kg).

1.  **The Gas Space:** There must be enough empty space in the condenser for hot refrigerant gas to spread out and touch the cooling tubes.
2.  **The Surface Area:** As gas touches the cool tubes, it turns into liquid and falls to the bottom.
3.  **The Subcooler:** A small pool of liquid at the bottom is healthy—it ensures only liquid (no gas) goes back to the building.

---

## 1. The Fault: Overcharge (Too much mass)

**What it means.** During a service, an operator adds too many kilograms of refrigerant. 

**The scenario.** In this file, the machine has **10 percent extra charge** (~115 kg too much, bringing the total mass to **1265 kg**).

**The "Drowning" Chain (How it hurts):**
1.  **Stage 1: Drowning the Tubes.** The extra refrigerant has nowhere to go but the bottom of the condenser shell. The liquid level rises (**`cond_level_fraction`**) until it starts covering (drowning) the upper tubes that were meant for gas condensation.
2.  **Stage 2: Lost Surface.** Tubes covered in liquid can't be used to cool down hot gas effectively. The "active" condensing area of the shell shrinks.
3.  **Stage 3: Pressure Lift.** Because the condenser is now effectively "smaller," it can't get rid of heat fast enough. Heat backs up, and the **High Side Pressure (`CH-CON-RFT-PRES`) rises**.
4.  **Outcome: Efficiency Drain.** The compressor has to push harder against this higher ceiling. **Subcooling (`subcooling_K`) rises** because there is so much liquid to cool, but **Efficiency (`CH-KW/RTON`) degrades** significantly.

---

## 3. The Telemetry: Key Signs

Overcharge is tricky because some "Health" signs look *too* good:

*   **Subcooling:** **`subcooling_K`** (Truth-Only). This **rises**. In a leak, this falls to zero. In overcharge, it stays high as the pool deepens.
*   **Refrigerant Pressure:** **`CH-CON-RFT-PRES`**. This **rises** because the condenser is "drowning."
*   **Power:** **`CH-KW_A`**. This **rises** as the compressor works against the higher ceiling.

---

## 8. What happens after the fault (The Timeline)

1.  **Midnight:** The machine starts the day with 10% extra charge.
2.  **Order 1:** **Subcooling is high.** The "Smoking Gun." (Internal: `subcooling_K`).
3.  **Subsequent:** **Condenser Pressure is high.** (Tag: `CH-CON-RFT-PRES`).
4.  **Subsequent:** **Power usage is high.** (Tag: `CH-KW_A`).
5.  **Outcome:** The machine runs all day, but it costs more than it should. It risks a High Pressure trip during the heat of the day.

---

## 9. The Big Picture

```
Extra Refrigerant (Error)  -->  Condenser Drowns  -->  High Head Pressure
            |                            |                        |
            v                            v                        v
      ONE KNOB: Mass +10%         ONE RESULT: Lost Area    FINAL OUTCOME: High $
            |                            |                        |
            v                            v                        v
      83 Keppel Tags (Output)      "Sickness": High Subcooling + High Power
```

**Summary:** Overcharge is the opposite of a leak. While a leak starves the machine, overcharge "drowns" it. You catch it by seeing **High Subcooling** paired with **Higher than normal Power**.
