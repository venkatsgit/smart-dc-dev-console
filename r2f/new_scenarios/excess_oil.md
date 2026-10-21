# Excess oil in the refrigerant loop

Primary root cause: **too much oil circulating with the refrigerant** (overfill, failed oil-return, or oil logged in the evaporator).  
Not evaporator tube scale. The water side can be clean.

**Evidence:** From **ASHRAE RP-1043** (fault EO, +14/+32/+50/+68% extra oil). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** York YK evaporator note: an excessive quantity of oil in the evaporator contributes to erratic performance and can look like fouled tubes or low charge. Carrier / Trane oil systems assume oil stays in the sump and a thin film returns — not a flooded evaporator.

---

## 0. The Healthy State

1. **Oil has one job.** It lubricates bearings and gears. It lives in the **oil tank / sump**. A pump holds a differential of about **18–25 psid** (Trane 18–22; Carrier 18–25).
2. **A little oil always travels.** Some oil leaves with discharge gas. A healthy machine **returns** it (eductor, oil-return line, separator). The evaporator still has a clean liquid pool covering the tubes.
3. **Heat transfer needs wet, clean tubes.** Refrigerant must touch metal to boil. A thick oil film is an insulator, the same way scale is an insulator, but the film is on the **refrigerant** side.
4. **What “healthy” looks like.** Oil level is in the sight-glass band. Oil ΔP is in range. Evaporator approach is small. Capacity matches the load. The machine is not “sluggish” at the same water temperatures.

---

## 1. The Fault

**The knob.** Raise the oil inventory in the refrigerant circuit (ASHRAE starts at **+14%** oil) and hold it. The water flows and the refrigerant charge stay at design.

**The chain.**

1. **Oil coats the evaporator tubes.** Extra oil does not stay in the sump. It logs in the cold evaporator. The boiling surface sees oil instead of clean refrigerant.
2. **Evaporator UA falls.** Heat cannot cross as easily. Evaporator refrigerant temperature drops relative to the water. **Evaporator approach widens.** Capacity falls.
3. **The compressor still tries to meet leaving-water setpoint.** Guide vanes or speed open. Power per ton gets worse. Evaporator pressure may sag.
4. **Why this is not a leak.** Total refrigerant mass is still there. Subcooling does not drain away as the first signature. Oil level / oil circulation is the hidden state (often truth-only unless the site has a reliable oil-level tag).
5. **Why this is not water-side fouling.** Condenser-water and chilled-water flows are normal. Condenser approach is not the first mover. The sick heat exchanger is the **evaporator**, from the refrigerant side.
6. **End state.** The machine may keep running in a weak, inefficient band (like mild fouling) or lose leaving-water control. Severe oil logging can contribute to **low evaporator pressure** or force a shutdown from capacity / oil-temperature limits. York treats “too much oil in the evaporator” as a real performance fault, not a later curiosity.

**Easy mix-up.** Evaporator fouling (already in the pack). Same-looking approach and capacity. The training split is: fouling is a water-side UA knob; excess oil is a refrigerant-side oil-mass knob. Both are needed or the classifier will call every weak evaporator “fouling.”
