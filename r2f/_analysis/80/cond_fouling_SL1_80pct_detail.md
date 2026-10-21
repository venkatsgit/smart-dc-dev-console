# Condenser fouling, severity level 1 — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `cond_fouling_SL1_80pct`.  
This guide explains how a small amount of dirt on a machine changes its performance, moving from a healthy state to a "mildly sick" one.

---

## 0. The Healthy State: How it should work

Before looking at the fault, we must understand the "Normal Day" (21 August). A healthy chiller is a masterpiece of efficiency, moving heat from where it's not wanted to where it can be released.

1.  **The Cooling Loop (The Heat Shuttle):** The chiller acts like a "heat shuttle." It uses a special fluid called refrigerant to move heat from inside the building to the outside air.
    *   **Evaporator (Heat Sponge):** Cold **liquid** refrigerant boils into a gas to "soak up" heat from your building's chilled water.
    *   **Compressor (The Heart):** Squeezes that gas, making it **very hot** and high-pressure.
    *   **Condenser (Heat Dump):** Tower water flows through copper tubes. The hot refrigerant gas touches these tubes, releases its heat, and turns back into liquid.
2.  **Clean Tubes are Key:** In a healthy machine, the copper tubes in the condenser are perfectly clean. Heat crosses the thin metal wall instantly into the tower water.
3.  **Efficiency:** Because heat leaves easily, the compressor doesn't have to work very hard. It "lifts" the gas to a moderate pressure, using the minimum amount of electricity needed.
4.  **Key Terms in Health:**
    *   **Subcooling:** The liquid in the condenser is "extra cold" compared to its boiling point (Healthy = ~4-5°C).
    *   **Approach:** The temperature "gap" between the hot refrigerant and the cooling water. (Healthy = very small, ~1-2°C).

---

## 1. The Fault: Condenser Fouling (Scale)

**What "Fouling" means.** Over time, minerals in the tower water can build up a thin crust of "scale" (like the white stuff in a kettle) inside the condenser tubes. This crust acts like a **thermal insulator**.

**What SL1 means.** SL stands for **Severity Level**. Level 1 is the mildest possible fault. In this file, **12 percent** of the condenser tube surface is treated as "lost" or blocked by this scale. It’s not enough to stop the machine, but it makes it "sick."

**The "Inefficiency" Chain (How it hurts):**
1.  **Stage 1: Insulation (Midnight).** 12% of the tube surface is now covered in scale. Heat can no longer cross the metal wall easily.
2.  **Stage 2: Heat Backup.** Because heat is "trapped" in the refrigerant, the gas stays hotter than it should.
3.  **Stage 3: Pressure Rise.** In a closed loop, hotter gas = **higher pressure**. 
4.  **Stage 4: Compressor Strain.** The compressor now has to "pedal" against a higher pressure. It’s like a cyclist hitting a headwind—the bike still moves, but it takes more energy. **Power (`CH-KW_A`) rises** to compensate.
5.  **Outcome:** The machine doesn't trip. It keeps the building cold. But it uses more electricity every minute to do it.

**How it is applied.** At midnight on 22 August, the simulation jumps to this 12% dirt level and **holds it constant**. It is a "Step Fault"—it doesn't get dirtier as the day goes on; it stays exactly 12% sick for 24 hours.

---

## 2. What you gave, and what you get back

**The Background:** We used a real operating day from your site (21 August 2026). The simulation takes the entering water temperatures from that day as the "source of truth."

**The Result:** You get a spreadsheet (`sensors.csv`) with 48 hours of data:
*   **Day 1 (21 Aug):** The "Clean" day. The twin simulates how the machine *should* have behaved.
*   **Day 2 (22 Aug):** The "Dirty" day. The twin simulates how the machine *actually* behaves with 12% fouling.

Both days follow the same building load and water patterns, so any difference you see is caused **only** by the fouling.

---

## 3. The Telemetry: Making sense of the 83 names

The file `sensors.csv` has 83 columns (Keppel tags). Think of these as the dashboard of the chiller.

*   **Most names don't move:** Things like building totals, pump vibration, or chemical tank pH stay the same because fouling doesn't affect them.
*   **The "Main 9":** Only 9 tags really matter here. These are the ones that show the "sickness":
    *   **Power & Current:** `CH-KW_A`, `CH-RLA`, and the three phase currents (`CH-L1-A`, etc.). These all **rise** because the compressor is working harder.
    *   **Refrigerant State:** `CH-CON-RFT-TEMP` and `CH-CON-RFT-PRES`. These **rise** because heat is backing up.
    *   **Efficiency:** `CH-KW/RTON`. This **rises** (meaning the machine is less efficient).
    *   **Approach:** `CH-CON-APP-TEMP`. This measures the "gap" between water and refrigerant. A wider gap means worse heat exchange.

---

## 4. The "Boundary Profile" (The Environment)

The simulation is tied to a specific environment called `site_day_80`. 
*   It uses the real weather/water conditions of **21 August 2026**.
*   The tower water entered at **28.47 °C to 31.00 °C**.
*   This ensures the "Hero" doesn't just look at flat lines, but sees a machine living through a real day.

---

## 5. The Twin Model: The Brains

The simulation uses a high-fidelity physics model of your specific chiller (HT-CH-01). 
*   **116 internal numbers:** The model calculates "Ground Truth" values like `cond_UA_W_K` (how well the tubes conduct heat). These are stored in `truth.csv`.
*   **Calculated, not copied:** Except for the water temperatures you fed in, every number is a result of the physics equations solving for the evaporator, compressor, and condenser.

---

## 6. Mapping the Names

There are different lists of names for the same things:
*   **83 Keppel Tags:** The ones you see on your site dashboard.
*   **116 Truth Columns:** The model's internal "perfect" knowledge (no noise).
*   **20 Measured Tags:** The bridge where a model variable is renamed to match a Keppel sensor.

---

## 7. Four types of data columns

1.  **Measured:** Direct results from the model (like Power or Pressure).
2.  **Derived:** Calculated formulas (like "Approach" or "Efficiency").
3.  **Replay:** Data simply copied from the real day (like Tank pH).
4.  **Total:** Plant-wide sums that are updated to include this simulated chiller.

---

## 8. What happens after the fault (The Timeline)

At midnight on 22 August, the dirt is "applied." Here is the sequence:

1.  **+1 min:** Tube conductance (`cond_UA_W_K`) drops immediately by 12%. This is the root cause. (Internal only).
2.  **+9 min:** **Power (`CH-KW_A`) rises.** This is the first thing a site operator would see. The compressor feels the "heavier lift" right away.
3.  **+11 min:** **Refrigerant temperature (`CH-CON-RFT-TEMP`) rises.** The gas is now getting hotter because the tubes are dirty.
4.  **+15 min:** **Pressure and Approach move.** The pressure follows the temperature up. The approach "gap" widens (on the Keppel tag, this number actually falls because of how the site calculates it: Water - Refrigerant).

**The Result:** Within 15 minutes, the chiller settles into a new, slightly less efficient operating point. It stays there for the rest of the day, following the normal midday heat swing but always slightly "sicker" than Day 1.

---

## 9. The Big Picture

```
Real Water Day (Input)  -->  Physics Model (Brain)  -->  116 Truth Values (Internal)
                                     |
                                     v
                          One Knob: 12% Dirt Step
                                     |
                                     v
                          83 Keppel Tags (Output)
                          (Meters move in ~15 mins)
```

**Summary:** SL1 fouling is a "hidden" efficiency drain. It won't cause a trip, but it makes the machine work harder and cost more to run. You can see it by comparing today's power and temperatures to a clean baseline.
