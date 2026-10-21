# Refrigerant leak (discharge gas), moderate rate — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `leak_gas_moderate_80pct`.  
This guide explains a "Run-to-Failure" scenario where a gas leak causes a machine to slowly starve until it trips.

---

## 0. The Healthy State: How it should work

Before the leak, we must understand the "Normal Day" (21 August). A healthy chiller relies on a precise balance of refrigerant mass and pressure.

1.  **The Cooling Cycle (The Heat Shuttle):** 
    *   The chiller acts like a "heat shuttle." Cold **liquid** refrigerant in the **evaporator** boils into a gas at a very low temperature. As it boils, it "soaks up" heat from the building's water.
    *   The **compressor** sucks in this low-pressure gas and squeezes it, making it **very hot** and high-pressure.
    *   In the **condenser**, tower water cools this hot gas back into a liquid pool.
2.  **The Two Pools (Charge Storage):** 
    *   A healthy chiller (~1150 kg charge) keeps two specific pools of liquid refrigerant.
    *   **The Evaporator Pool (~810 kg):** This pool must cover the copper tubes. If the tubes are wet, they can boil refrigerant and cool the building efficiently.
    *   **The Condenser Pool (~270 kg):** This pool "seals" the loop and allows the liquid to be cooled below its boiling point (**Subcooling**). This extra cooling makes the machine more efficient.
3.  **The Flows (The Conveyor Belts):** 
    *   **Building Water Flow:** Heat from your building is carried into the chiller by a steady stream of **Chilled Water**.
    *   **Tower Water Flow:** Heat is carried away to the outside world by a steady stream of **Condenser Water**.
    *   **Refrigerant Mass Flow:** Inside the machine, the compressor moves a high-speed "conveyor belt" of refrigerant gas (~20 kg every second). This flow is what actually moves the heat from the building water to the tower water.
4.  **Pressure Lift:** The compressor "lifts" the refrigerant from the cold evaporator side (~92 kPa) to the hot condenser side (~185 kPa). In a healthy machine, this climb is steady and predictable.
5.  **Key Terms in Health:**
    *   **Subcooling:** The "extra coldness" of the liquid in the condenser. (Healthy = ~4-5°C).
    *   **Superheat:** How much extra heat the gas picks up *after* it has finished boiling. (Healthy = ~1-2°C; very low, because tubes are wet).

---

## 1. The Fault: A High-Side Gas Leak

**What "Moderate" means.** This is a leak rate. "Moderate" is sized so that the machine loses about **5 percent of its total mass every hour**. It’s like a slow puncture in a tire—the machine still runs for hours, but it is slowly "starving."

**What this file actually does.** At midnight on 22 August, a hole opens on the **discharge side** (the pipe carrying hot gas from the compressor to the condenser). 
*   **The Knob:** The simulation opens the `vapour_leak_area`.
*   **Why Gas Leaks are "Sneaky":** Because gas is 30x less dense than liquid, the machine loses mass much slower than a liquid leak. This makes it harder for operators to notice until it's too late.

**The "Starvation" Chain (How the machine dies):**
1.  **Stage 1: The Condenser Pool Drains (0-4 hours).** The leak vents gas from the high side. The first thing to suffer is the **Condenser Pool**. This pool is the "storage tank" that feeds the evaporator. As it drains:
    *   **Subcooling falls to zero:** Without a deep pool, the liquid cannot be extra-cooled. The liquid going back to the evaporator is now "relatively hotter," which makes it boil faster and starves the system even more.
    *   **Supply Line Sags:** With the pool empty, the machine can't send enough liquid refrigerant back to the evaporator.
2.  **Stage 2: The Lift Paradox (4-11 hours).** You might think that if the condenser leaks, the pressure drops and the compressor’s job gets "easier." **This is a trap.** While the condenser pressure (the "ceiling") sags a little, the evaporator pressure (the "floor") collapses much faster because it is empty. 
    *   **Result:** The "hill" the compressor has to climb (the **Pressure Lift**) actually gets **steeper**. 
    *   **Power and Current rise** (+43 kW peak) because the compressor is working harder to "suck" what little gas is left from a starved evaporator and push it into a still-high-pressure condenser.
3.  **Stage 3: The Evaporator Tubes Go Dry (11-14 hours).** The condenser pool is gone. Now the **Evaporator Pool** starts to empty. The liquid level drops until the copper tubes are no longer submerged. 
4.  **Stage 4: Overheating (Superheat).** Refrigerant is supposed to boil *on* the tubes. Now, gas flows past *dry* tubes and picks up massive amounts of heat from the building water. This is **Superheat**. Instead of a healthy 1°C, it climbs toward 25°C.
5.  **Stage 5: Flow Collapse (14-17 hours).** Once the evaporator is mostly dry, there is no liquid left to boil. The compressor has no gas left to suck. The "conveyor belt" of refrigerant slows down—falling from 20 kg/s to about **8 kg/s**. Cooling capacity collapses.
6.  **Stage 6: TRIP (17.6 hours).** The safety system sees the "bone-dry" evaporator (High Superheat) and shuts the chiller down to prevent the compressor from burning out.

---

## 2. What you gave, and what you get back

**The Background:** A real operating day (21 August 2026).

**The Result:** You get `sensors.csv` (~41.8 hours total):
*   **Day 1 (21 Aug):** A perfectly healthy day.
*   **Day 2 (22 Aug):** The "Run-to-Failure." The hole opens at midnight, and the data **stops at trip (~17:36)**. 

Unlike fouling, this pack **ends with a dead machine**.

---

## 3. The Telemetry: Key Signs

*   **Truth-Only (The early warnings):** 
    *   `subcooling_K`: Falls first (+59 min). This is the "smoking gun" but Keppel has no meter for it.
    *   `charge_kg`: Total mass is falling.
*   **Keppel Tags (What the operator sees):**
    *   **Early:** `CH-KW_A` (Power) and `CH-RLA` (Amps) rise as the machine struggles.
    *   **Mid-Run:** Evaporator pressure and temperature drop as the barrel starves.
    *   **Late:** Capacity (`CH-CHW-RTON`) collapses and leaving water temperature rises. The building gets hot.

---

## 4. The "Boundary Profile"

Simulation id: `site_day_80`.
*   Uses the real water/weather conditions of **21 August 2026**.
*   Shows the leak happening while the building load changes throughout the day.

---

## 5. The Twin Model: The Brains

High-fidelity physics model of HT-CH-01.
*   **Charge on this run:** Starts at **1150 kg**, ends at **144 kg** (~87.5% lost) by the time it trips.
*   **Equations:** The model calculates how the loss of mass changes every single pressure and temperature in the system.

---

## 6. Mapping the Names

*   **83 Keppel Tags:** Dashboard view.
*   **116 Truth Columns:** Model internals (Mass, Subcooling, Valve Position).
*   **20 Measured Tags:** Where model physics meets site sensors.

## 7. Four types of data columns

1.  **Measured:** Direct results from the model (Power, Pressure).
2.  **Derived:** Calculated formulas (Approach, Efficiency).
3.  **Replay:** Data copied from the real day (Tank pH).
4.  **Total:** Plant-wide sums updated for this chiller.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The hole starts to open (takes 1.2 hours to reach full size).
2.  **+59 min:** **Subcooling falls.** The condenser liquid pool is shrinking. (Internal only: `subcooling_K`).
3.  **+69 min:** **Power rises.** Compressor feels the strain. This is the first Keppel sign (**Tag: `CH-KW_A`**).
4.  **~4 hours:** **Evaporator pressure falls.** Liquid level is getting dangerously low (**Tag: `CH-EVA-RFT-PRES`**).
5.  **~11 hours:** **Capacity fails.** The machine can no longer keep the building water cold (**Tags: `CH-CHW-RTON`** falls, **`CH-CHWST`** rises).
6.  **~14.7 hours:** **Superheat Alarm.** The gas is getting too hot. (Internal: `superheat_K`).
7.  **~17.6 hours:** **TRIP.** The machine shuts down. (Safety trip on **`superheat_K`**).

---

## 9. The Big Picture

```
Real Water Day (Input)  -->  Physics Model (Brain)  -->  116 Truth Values (Internal)
                                     |                   (Mass & Subcooling fall)
                                     v
                          One Knob: Gas Leak Area (Ramp)
                                     |
                                     v
                          83 Keppel Tags (Output)
                          (Power up -> Capacity down -> TRIP)
```

**Summary:** This is a "Run-to-Failure" case. The machine starts by using more electricity and ends by failing to cool the building. By the time the trip happens, nearly 90% of the refrigerant is gone.
