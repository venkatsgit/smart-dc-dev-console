# Refrigerant leak (high-side liquid), moderate rate — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `leak_liquid_moderate_80pct`.  
This guide explains a "Fast Failure" scenario. A liquid leak is much more aggressive than a gas leak because liquid is 30x denser than gas.

---

## 0. The Healthy State: How it should work

A healthy chiller maintains two essential pools of liquid refrigerant:

1.  **The Condenser Pool:** A reservoir of liquid sits at the bottom of the condenser. It acts as a "seal" to keep high-pressure gas from rushing into the expansion valve.
2.  **Subcooling:** In a healthy machine, this pool allows the liquid to be cooled below its boiling point. This "extra cold" liquid is more efficient when it reaches the evaporator.
3.  **The Evaporator Pool:** This pool covers the building-side tubes. As long as the tubes are submerged, they can boil refrigerant and cool the building.

---

## 1. The Fault: A High-Side Liquid Leak

**What "Moderate" means.** This leak rate is sized so that the machine loses mass rapidly. Unlike a gas leak (which vents slowly from the top), a liquid leak at the bottom of the condenser vents the densest part of the charge. 

**What this file actually does.** At midnight on 22 August, a hole opens in the **high-pressure liquid line** (between the condenser and the expansion valve). 
*   **The Knob:** The simulation opens the `leak_area` to a final equivalent orifice of ~20 mm².
*   **The Aggression:** Because the hole is on the high-pressure side and venting liquid, the machine empties much faster than a Low-Side leak. By the time it trips, the machine has lost significant mass (Charge falls from **1150 kg to ~1008 kg** in just 3 hours).

**The "Crash" Chain (How the machine dies):**
1.  **Stage 1: The Seal Breaks (0-1 hour).** The liquid pool in the condenser is the first thing to go. 
    *   **Subcooling collapses:** As the pool uncovers the tubes, **`subcooling_K`** falls to zero almost immediately.
    *   **Gas "Bypass":** Once the liquid is gone, high-pressure gas starts rushing through the expansion valve. This is extremely inefficient.
2.  **Stage 2: Evaporator Starvation (1-3 hours).** The condenser reservoir is empty. The expansion valve now has nothing but foam and gas to feed the evaporator. 
3.  **Stage 3: Thermal Runaway.** The evaporator pool starts to empty. The tubes go dry. Refrigerant is no longer boiling *on* the tubes; instead, gas is flowing past dry tubes and getting **superheated**.
4.  **Stage 4: TRIP.** The safety system sees the "bone-dry" state (**High Superheat above 25 K**) and shuts the chiller down to prevent the compressor from melting.

---

## 3. The Telemetry: Key Signs

*   **Subcooling:** **`subcooling_K`** (Truth-Only). This falls to zero almost immediately. It is the "Smoking Gun."
*   **Superheat:** **`CH-DISCT`** (Discharge Temp). This rises rapidly as the machine starves.
*   **Capacity:** **`CH-CHW-RTON`**. This **collapses** because there is no liquid left to boil.
*   **Power:** **`CH-KW_A`**. This may rise initially as the machine struggles, then fall as the compressor has no mass left to move.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The liquid hole opens.
2.  **+Order 1:** **Condenser Level falls.** The reservoir begins to empty. (Internal: `cond_level_fraction`).
3.  **+Order 1:** **Subcooling falls.** The "extra coldness" disappears as the subcooler tubes are uncovered. (Internal: `subcooling_K`).
4.  **+Order 3:** **Superheat rises.** The evaporator is now starving. The gas picks up too much heat.
5.  **+Order 4:** **Capacity collapses.** The machine can no longer cool the building.
6.  **Terminal:** **TRIP.** Safety shutdown on High Superheat.

---

## 9. The Big Picture

```
Condenser Pool (High Side)  -->  Evaporator Pool (Low Side)
            |                            |
            v                            v
      ONE KNOB: Leak Area          ONE RESULT: Starvation
            |                            |
            v                            v
      83 Keppel Tags (Output)      Final Trip: High Superheat
      (Subcooling -> 0 | Superheat -> Max | Capacity -> 0)
```

**Summary:** A high-side liquid leak is a "heart attack" for the chiller. It is much more violent and faster than a gas leak. Within hours, the machine moves from perfectly healthy to a total safety shutdown.
