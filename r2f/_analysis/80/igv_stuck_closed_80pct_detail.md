# Inlet guide vanes stuck closed — Zero to Hero Guide

Chiller **HT-CH-01**. Files start with `igv_stuck_closed_80pct`.  
This guide explains what happens when the "Throttle" of the compressor is stuck at idle, even when the building needs more cooling.

---

## 0. The Healthy State: How it should work

The **Inlet Guide Vanes (IGV)** act like the "Throttle" of your car engine.

1.  **Capacity Control:** When the building gets hotter, the chiller computer opens the vanes (e.g., to 90%) to let more gas into the compressor.
2.  **Efficiency:** When the building is cool, the vanes close (e.g., to 20%) to save electricity.
3.  **Smooth Flow:** The vanes also help direct the gas into the spinning impeller smoothly.

---

## 1. The Fault: IGV Stuck Closed

**What it means.** A mechanical failure of the linkage or actuator. The building is asking for cooling, but the compressor vanes are physically stuck at **10% open (90% closure fraction)**.

**The "Suffocation" Chain (How it hurts):**
1.  **Stage 1: Throttled.** The compressor is "suffocated." It wants to suck in gas to cool the building, but the path is blocked by the stuck vanes (**Tag: `CH-IGV1-POS`**).
2.  **Stage 2: Capacity Shortfall.** The machine can only move a small fraction of the refrigerant it needs. Even if the motor spins fast, the flow is physically restricted.
3.  **Stage 3: Building Heat-Up.** Because the machine can't "sponge up" enough heat, the **Leaving Chilled Water Temperature (`CH-CHWST`)** begins to rise above the setpoint.
4.  **Outcome: Inability to Cool.** The machine stays running and doesn't trip, but it fails its primary job. It is like driving a high-performance car with a brick under the gas pedal.

---

## 3. The Telemetry: Key Signs

*   **Vane Position:** **`CH-IGV1-POS`**. This is the "Smoking Gun." It will flatline at a low value while the building load remains high.
*   **Leaving Water:** **`CH-CHWST`**. This **rises** above the setpoint (e.g., 6.5°C -> 12°C) because the machine can't meet the load.
*   **Capacity:** **`CH-CHW-RTON`**. This is capped at a low value (~40% of normal capacity).
*   **Power:** **`CH-KW_A`**. Electricity usage is **lower** than normal for the time of day because the "throttled" compressor is doing less work.

---

## 8. What happens after the fault (The Timeline)

1.  **00:00:** The IGVs stick at 10% open.
2.  **+Order 1:** **Vane Position (`CH-IGV1-POS`) flatlines.**
3.  **+Order 2:** **Capacity (`CH-CHW-RTON`) drops** and stays capped.
4.  **+Order 3:** **Leaving Water Temperature (`CH-CHWST`) rises.** The building starts to warm up.
5.  **Outcome:** No trip, but the chiller is effectively "useless" for meeting the site's cooling demand.

---

## 9. The Big Picture

```
Building Demand (Input)  --| THROTTLE STUCK |--  Compressor Work
            |                                       |
            v                                       v
      ONE KNOB: IGV = 10%                     ONE RESULT: Suffocation
            |                                       |
            v                                       v
      83 Keppel Tags (Output)                 Final Outcome: Hot Building
      (IGV flat | Capacity cap | CHWST up)
```

**Summary:** Stuck IGVs are a "Performance Killer." The machine is mechanically healthy but physically restricted. You catch it by seeing **high leaving water temperatures** even though the chiller says it is "running."
