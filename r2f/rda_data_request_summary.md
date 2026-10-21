# RDA Data Request: Run-to-Failure (R2F) Scenarios for HT-CH-01

This document outlines the request for additional physics-based digital twin data from **Red Dot Analytics (RDA)** for machine **HT-CH-01**. 

### Context: ASHRAE Standards & Carrier OEM Manuals
This request is grounded in two primary technical authorities:

1.  **ASHRAE RP-1043 (The "A" Standard)**: 
    This is the globally recognized research standard for *Fault Detection and Diagnostic (FDD) Requirements and Evaluation Tools for Chillers*. It defines the seven "classic" thermodynamic faults (fouling, leaks, overcharge, etc.) that account for the vast majority of chiller efficiency losses. We use this to ensure our models are scientifically sound.
    
2.  **Carrier 19XR OEM Manuals**: 
    Since **HT-CH-01** is a Carrier machine, we use the official manufacturer's **Operation & Maintenance (O&M)** manuals to define the "red lines." These manuals specify the exact mechanical safety limits—such as the **18–25 psid** oil pressure requirement and **Surge** protection logic—that the digital twin must simulate to represent a real-world trip.

---

### 1. Existing Scenarios (Already Delivered)
We have successfully received and analyzed the following R2F packs for both 80% and 58% load:

- [x] **Healthy Baseline**: Normal operation across standard site days.
- [x] **Condenser Fouling**: Scale buildup on water tubes (Severity Levels 1–4).
- [x] **Evaporator Fouling**: Scale buildup on chilled water tubes (Severity Levels 1–4).
- [x] **Refrigerant Gas Leak**: Discharge-side leak (Slow and Moderate).
- [x] **Refrigerant Liquid Leak**: High-side liquid line leak (Slow and Moderate).

---

### 2. New Scenario Requests (R2F Data Needed)
We are requesting the following **11 new scenarios**. For each case, RDA should ramp the "Root Cause" knob until the machine hits the named "Final Stage" protection trip.

| ID | Scenario ID | Root Cause | Final Stage (Trip) | Chain Effect (Brief) |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `reduced_condenser_water_flow` | Pump degradation or valve blockage. | High Condenser Pressure | Water flow falls, causing the heat exchange to stall. Head pressure rises rapidly as the condenser can no longer reject heat. |
| **02** | `reduced_evaporator_water_flow` | CHW pump failure or strainer clog. | Low Evaporator Pressure / Freeze | Flow through the evaporator drops. The refrigerant "over-cools" the stagnant water, risking a freeze-up trip. |
| **03** | `refrigerant_overcharge` | Maintenance error (too much gas added). | High Condenser Pressure | Excess liquid stacks up in the condenser, reducing available surface area. Subcooling rises while head pressure climbs. |
| **04** | `noncondensable_gas` | Air/moisture leaked into the low side. | High Condenser Pressure | Air creates a "blanket" in the condenser that refrigerant cannot penetrate. Causes high head pressure similar to fouling, but persists after cleaning. |
| **05** | `excess_oil` | Oil migration from the sump to the tubes. | Capacity Loss / Low Evap Pressure | Oil coats the evaporator tubes, creating a thermal barrier. The machine loses cooling capacity even though the refrigerant charge is correct. |
| **06** | `expansion_valve_stuck_closed` | Expansion valve motor/linkage failure. | High Superheat / Low Evap Pressure | The "gate" is closed. Refrigerant piles up in the condenser (starving the evaporator). Superheat spikes and the machine trips to protect the compressor. |
| **07** | `expansion_valve_stuck_open` | Expansion valve failure (full open). | Compressor Slugging / Low Superheat | The "gate" is wide open. Liquid refrigerant floods the evaporator and enters the compressor suction, risking catastrophic "slugging" (liquid hitting the spinning blades). |
| **08** | `igv_stuck_closed` | Inlet Guide Vane actuator failure. | Capacity Shortfall / Surge Risk | The "throttle" is stuck at idle. The building gets hot because the chiller can't ramp up, and the low flow puts the machine at risk of surging. |
| **09** | `cooling_tower_fan_failed` | Tower fan motor or belt failure. | High Entering CW Temperature | The water returning from the tower gets hotter. This forces the condenser pressure up until the compressor can no longer climb the "pressure hill." |
| **10** | `low_oil_pressure` | Oil pump failure or plugged filter. | Low Oil Differential Pressure | The oil pump loses its "pressure fight" against the refrigerant. Without a ΔP of 18–25 psid, the bearings lose their oil film and the machine trips to prevent melting. |
| **11** | `compressor_surge` | High Lift vs. Low Flow imbalance. | Surge Trip (Vibration) | The refrigerant gas loses momentum and falls backward through the impeller. This creates violent vibration shocks and power pulses until the machine trips. |

---

### Request Details for RDA
*   **Load Conditions**: Provide both `site_day_80` and `site_day_58`.
*   **Data Format**: Maintain the same `sensors.csv`, `truth.csv`, and `cascade.csv` structure used in previous deliveries.
*   **Stop Condition**: For all trip-labeled scenarios, the simulation should run until the safety limit is exceeded (`stop_on` trip).
