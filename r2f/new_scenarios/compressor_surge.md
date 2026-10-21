# Compressor surge

Primary root cause: **the centrifugal compressor is driven across its surge line** — too much lift, too little flow through the impeller.  
Surge is the **stall**. High condenser pressure, a dead tower fan, stuck-closed vanes, or severe fouling are the usual reasons the map point walks there.

**Evidence:** Taken from the **Trane**, **York / JCI**, and **Daikin** OEM manuals in [`references/`](references/): [`Trane_CVHE-SVU01E-EN_CH530.pdf`](references/Trane_CVHE-SVU01E-EN_CH530.pdf), [`York_YK_Style_G_160.75.pdf`](references/York_YK_Style_G_160.75.pdf), [`Daikin_IOM1210_Magnitude_WMC-D.pdf`](references/Daikin_IOM1210_Magnitude_WMC-D.pdf), [`Daikin_IOM1372_Magnitude_WME-D.pdf`](references/Daikin_IOM1372_Magnitude_WME-D.pdf).  
**Sources:** Trane CH530 condenser-limit / surge mode; head-relief request when in surge. York YK hot-gas bypass “to eliminate compressor surge during light load or high head.” Daikin Magnitude: `Surge High Suct SH-Running` — compressor stop. The current HT-CH-01 twin already stores `surge_margin`, `surge_active`, `surge_count`.

---

## 0. The Healthy State

1. **A centrifugal impeller is a high-speed fan with a stall line.** As long as enough gas flows through it, flow is smooth. If the pressure it must climb is too tall for the flow it has, flow breaks down. That breakdown is **surge**: gas slugs backward, then forward, again and again.
2. **Surge margin is the gap to that line.** High = safe. Falling = closer to the cliff. On the mild condenser-fouling pack, margin dips a little and stays safe. The machine never surges.
3. **Healthy map point.** Design water, design charge, vanes following load: lift about 2:1 on these packs (~92 kPa to ~185 kPa), flow about 20 kg/s. Far from stall.
4. **What “healthy” looks like.** `surge_margin` is comfortable. No surge count. No abnormal suction swing. Power is steady, not pulsing.

---

## 1. The Fault

**The knob.** Do **not** invent a “surge switch.” Drive a physical cause until `surge_margin` hits the twin’s trip:

- raise condenser pressure (hotter CW-in, lower CW flow, or non-condensables), **or**
- cut compressor flow (IGV stuck closed at high lift).

Ask RDA for one clean pack whose **terminal_event is surge**, not “dirty but still running.”

**The chain.**

1. **Lift grows or flow shrinks.** The operating point slides toward the stall line. `surge_margin` falls. This can take minutes (fan fail) or hours (slow fouling). For R2F, pick a cause that reaches the line in the 18-hour window.
2. **First symptoms before the bang.** Condenser pressure up and/or vanes too closed. Power may rise (harder lift) or become **unstable**. Suction pressure can swing.
3. **Surge.** Flow reverses in pulses. Vibration jumps. Discharge and suction temperatures / superheat can spike (Daikin’s “surge high suction superheat” running trip). Oil and bearings see the shock.
4. **Why this is its own class.** High head from fouling or low CW flow can **end** in high-pressure cutout **without** crossing surge. Surge is a different protect path. If you only train high-pressure trips, a surge trip looks like an unknown class.
5. **Trip.** `surge_active` / surge count / OEM surge stop. Machine unavailable. Residual risk: seal and bearing damage (York shaft-seal note: extended surge overheats the seal).

**Easy mix-up.** Any high-head case. State the terminal in the brief: this pack must **stop on surge**, with the driving cause named in the manifest (`cooling_tower_fan_failed` or `igv_stuck_closed` at high lift). The class for the classifier can still be `surge` if the live signature is the stall, not the upstream cause.
