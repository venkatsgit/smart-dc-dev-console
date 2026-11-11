# Expansion valve stuck closed — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `exv_stuck_closed_80pct`.  
This guide explains what happens when the "Gate" that feeds the building-side of the machine is stuck shut.

---

## 0. The Healthy State: How it should work

The **Expansion Valve (EXV)** is the "Gatekeeper" of the chiller.

1.  **The Feeding Job:** Liquid refrigerant from the condenser must pass through the EXV to reach the evaporator. 
2.  **The Level Control:** A computer adjusts the EXV's opening (0-100%) to keep the liquid level in the evaporator just high enough to cover the tubes.
3.  **Pressure Drop:** The EXV is also where the pressure "drops" from high (Condenser) to low (Evaporator), allowing the refrigerant to get cold and boil.

---

## 1. The Fault: EXV Stuck Closed

**What it means.** A mechanical failure of the valve actuator or linkage. The building is asking for cooling, but the valve is physically stuck at **0% (fully closed)**.

**The "Starvation" Chain (How the machine dies):**
1.  **Stage 1: The Gate is Shut (Midnight).** No new liquid can enter the building-side of the machine. (Internal: **`mdot_exv_kg_s`** drops to zero).
2.  **Stage 2: Evaporator Drainage.** The compressor is still sucking gas out of the evaporator, but no new liquid is coming in to replace it. The liquid level drops rapidly (**Tag: `evap_level_fraction`** collapse).
3.  **Stage 3: Bundle Exposure.** The copper tubes in the evaporator are no longer submerged. They "go dry" within minutes.
4.  **Stage 4: Thermal Spike.** Building heat can no longer boil liquid. Instead, it just heats up the gas. **Discharge Temperature (`CH-DISCT`)** rises vertically as the gas is superheated.
5.  **Outcome: FAST TRIP.** Within 154 seconds of the fault, the safety system sees the "bone-dry" evaporator (High Superheat above 25 K) and shuts the machine down.

---

## 3. The Telemetry: Key Signs

*   **Valve Command vs Position:** The Tag **`CH-EXV`** might show the computer asking the valve to open, but the machine's "starving" behavior proves it is physically closed.
*   **Superheat:** **`CH-DISCT`** (Discharge Temp). This **rises vertically**. This is the most distinctive sign of a stuck valve.
*   **Evaporator Level:** **`evap_level_fraction`** (Truth-Only). This collapses to near zero in seconds.
*   **Capacity:** **`CH-CHW-RTON`**. This **falls** to zero as the boiling process stops.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The EXV sticks fully closed.
2.  **+Order 1:** **Feed flow stops.** (Internal: `mdot_exv_kg_s` -> 0).
3.  **+Order 2:** **Evaporator level falls.** The "Pool" is sucked dry by the compressor.
4.  **+Order 3:** **Superheat rises.** The gas is getting dangerously hot.
5.  **Terminal:** **TRIP.** The machine shuts down within minutes.

---

## 9. The Big Picture

```
Condenser (High Side)  --| GATE CLOSED |--  Evaporator (Low Side)
            |                                       |
            v                                       v
      ONE KNOB: EXV = 0%                      ONE RESULT: Bone Dry
            |                                       |
            v                                       v
      83 Keppel Tags (Output)                 Final Outcome: Fast Trip
      (Superheat up | Capacity down | TRIP)
```

**Summary:** A stuck EXV is a "Sudden Death" scenario. Unlike a leak (which takes hours), a stuck-closed valve starves the machine in minutes. It mimics a total loss of charge, but the refrigerant is still there—it’s just trapped on the High Side.
