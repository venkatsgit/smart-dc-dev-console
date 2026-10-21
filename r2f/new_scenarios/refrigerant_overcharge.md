# Refrigerant overcharge

Primary root cause: **too much refrigerant was charged into the closed loop.**  
This is the opposite of the gas and liquid leaks already in the pack.

**Evidence:** From **ASHRAE RP-1043** (fault RO, +10/+20/+30/+40% extra charge). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane high discharge warning: high subcooling with high head indicates overcharge or non-condensables. Carrier 19XR high condenser pressure list (with fouling / flow / air). York high discharge with air or dirty tubes — overcharge sits in the same high-head family.

---

## 0. The Healthy State

1. **A fixed charge.** The machine is a closed loop. On the current HT-CH-01 packs that mass is about **1150 kg**. Most of it sits as liquid in the evaporator so the tubes stay wet. A smaller pool sits in the condenser.
2. **Subcooling is the condenser-pool thermometer.** After the gas turns back into liquid, that liquid is cooled a few degrees below its boiling point. Healthy subcooling is about **4–5 °C**. It exists because there is enough — not too much — liquid sitting in the condenser.
3. **The compressor climb.** Gas is lifted from about 92 kPa to about 185 kPa. Power is the cost of that climb at the circulating flow (about 20 kg/s on those packs).
4. **What “healthy” looks like.** Charge is at the nameplate fill. Subcooling is a few degrees, not double. Condenser pressure is normal for the tower water of that day. The expansion valve is not fighting a flooded high side.

---

## 1. The Fault

**The knob.** Add refrigerant mass above the design charge (ASHRAE steps +10% to +40%) and hold it. There is no hole. Kilograms do **not** fall.

**The chain.**

1. **The condenser pool grows.** Extra liquid has to sit somewhere. It stacks in the condenser. The pool gets deeper.
2. **Subcooling rises — the opposite of a leak.** A deeper pool can be cooled farther below boiling. **Subcooling goes up.** On a leak, subcooling is the first thing that **falls**. That single direction splits the two families.
3. **Less useful condenser surface for gas.** Liquid occupies tube area that should be condensing vapour. Effective condensing area shrinks. Condenser pressure and temperature rise.
4. **Harder lift, more power.** The ceiling of the climb is higher. Compressor power and kW/ton rise. The machine still cools, often for a long time.
5. **Trip.** Typical end is **high condenser / discharge pressure**, the same cutout fouling and low condenser-water flow use. Trane’s diagnostic note: high subcooling **plus** high head points to overcharge (or air), not to a leak.

**Easy mix-up.** A leak also changes charge and later trips. Leak: mass and subcooling **down**. Overcharge: mass and subcooling **up**.
