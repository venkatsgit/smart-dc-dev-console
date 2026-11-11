# Evaporator fouling, severity level 2 — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `evap_fouling_SL2_80pct`.  
This guide explains how scale buildup on the building-side (evaporator) differs from condenser fouling, creating a "starved" state for the refrigerant loop.

---

## 0. The Healthy State: How it should work

Before the evaporator gets dirty, we must understand its job. The evaporator is the "Heat Sponge" of the building.

1.  **The Chilled Water Loop:** Your building's heat is carried into the chiller by **Chilled Water** (the blue loop). 
2.  **The Boiling Action:** Inside the evaporator, liquid refrigerant touches the copper tubes. Heat from the building water jumps across the metal wall, causing the refrigerant to **boil** into a gas.
3.  **Clean Tubes are Key:** In a healthy machine, the tubes are clean. Heat transfers easily, so the refrigerant only needs to be a few degrees colder than the water to "pull" the heat out.
4.  **Key Terms in Health:**
    *   **Evaporator Approach:** The temperature "gap" between the leaving chilled water and the boiling refrigerant. (Healthy = very small, ~1-2°C).
    *   **Suction Pressure:** The pressure at which the refrigerant boils. In a healthy machine at 80% load, this is steady and high enough to maintain efficiency.

---

## 1. The Fault: Evaporator Fouling (Scale)

**What "Fouling" means.** Just like the condenser, the evaporator tubes can build up a thin crust of minerals or biofilm. This crust acts like a **thermal insulator**.

**What SL2 means.** Severity Level 2. In this scenario, exactly **20 percent** of the evaporator tube conductance (**`evap_UA_W_K`**) is lost. The "Heat Sponge" is becoming less effective.

**The "Starvation" Chain (How it hurts):**
1.  **Stage 1: Insulation.** 20% of the tube surface is now blocked by scale. Heat can no longer enter the refrigerant easily.
2.  **Stage 2: Temperature Drop.** To keep pulling the same amount of heat from the building through the scale, the chiller computer forces the refrigerant to get **colder**.
3.  **Stage 3: Pressure Collapse.** Because the refrigerant is colder, its **boiling pressure (Suction Pressure) drops**. You will see **Tag: `CH-EVA-RFT-PRES`** fall.
4.  **Stage 4: Thin Gas.** Colder, lower-pressure gas is "thinner" (less dense). The compressor heart is still beating at the same speed, but it is sucking in less mass with every stroke.
5.  **Outcome: Capacity Loss.** The machine struggles to meet building demand. **Approach (`CH-EVA-APP-TEMP`) rises** (the widening gap between water and refrigerant) and **Efficiency (`CH-KW/RTON`) degrades**.

---

## 3. The Telemetry: Key Signs

Only a few tags show this specific sickness:

*   **Approach:** **`CH-EVA-APP-TEMP`**. This is the "Smoking Gun." A wider gap means the heat exchange is failing on the building side.
*   **Pressure:** **`CH-EVA-RFT-PRES`**. This **falls** because the machine is "digging deeper" into its pressure range to find cooling.
*   **Temperature:** **`CH-EVA-RFT-TEMP`**. This **falls** along with the pressure, moving down the saturation line.
*   **Efficiency:** **`CH-KW/RTON`**. This **rises** because the compressor has to "lift" the gas from a much lower floor (evaporator) to reach the same ceiling (condenser).

---

## 8. What happens after the fault (The Timeline)

1.  **+1 min:** Tube conductance (`evap_UA_W_K`) drops immediately by 20%. (Internal only).
2.  **+Order 2:** **Approach (`CH-EVA-APP-TEMP`) rises.** The gap between water and refrigerant widens immediately.
3.  **+Order 3:** **Refrigerant Pressure (`CH-EVA-RFT-PRES`) falls.** The "floor" of the machine collapses as it tries to compensate.
4.  **+Order 4:** **Capacity (`CH-CHW-RTON`) declines.** The machine can no longer keep up with the building's heat load.
5.  **+Order 4:** **Efficiency degrades.** Power usage stays high while cooling delivery drops.

---

## 9. The Big Picture

```
Real Water Day (Input)  -->  Physics Model (Brain)  -->  Approach Widen
                                     |                   (Heat can't get in)
                                     v
                          One Knob: 20% Evap Dirt Step
                                     |
                                     v
                          83 Keppel Tags (Output)
                          (Suction Pressure down -> Capacity down -> $ up)
```

**Summary:** Evaporator fouling is a "hidden" capacity killer. Unlike condenser fouling (which raises the ceiling), this **drops the floor**. It makes the building harder to cool and the machine more expensive to run.
