# Non-condensable gas in the refrigerant

Primary root cause: **air or nitrogen in the refrigerant circuit** (poor evacuation after service, or a failed purge on a low-pressure machine).  
Not dirt. Not extra refrigerant. A gas that **will not condense** at condenser temperature is occupying space.

**Evidence:** From **ASHRAE RP-1043** (fault NC, +1/+2/+3/+5% non-condensable). Official report is sold; local open evidence: [`references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf`](references/ASHRAE_RP-1043_evidence_JSTAGE_AIUE_2019.pdf).  
**Sources (same trip names in OEM manuals):** Trane high head: non-condensable gases in the circuit. Carrier 19XR **235** — check for non-condensables. York YK: high discharge with condensing-to-water difference high → “Air is in the condenser”; purging removes foul gas and reveals whether fouling remains.

---

## 0. The Healthy State

1. **Only refrigerant should be in the shells.** After a correct vacuum, the condenser and evaporator contain refrigerant and oil, not air.
2. **Condensing means the gas can become liquid.** Tower water cools refrigerant vapour until it condenses. Pressure then sits on the refrigerant’s saturation line for that temperature.
3. **Purge (where the machine has one).** Low-pressure chillers (for example older R-123 machines) run a purge to pull air out. High-pressure machines (R-134a / R-513A / R-1233zd class) still suffer if air was left in at charging.
4. **What “healthy” looks like.** Condenser pressure matches the saturation pressure of the refrigerant at the observed condenser temperature. Subcooling is the usual few degrees. There is no “mystery extra” pressure above that saturation line.

---

## 1. The Fault

**The knob.** Introduce a small mass fraction of air (or nitrogen) into the condenser / high side and hold it. ASHRAE’s mildest step is only **1 percent**.

**The chain.**

1. **Air takes volume in the condenser.** Air does not turn into liquid at these temperatures. It sits in the vapour space and **adds partial pressure**.
2. **Head pressure rises first.** The compressor now discharges against refrigerant pressure **plus** air pressure. Condenser pressure on the gauges goes up even when the water and the tubes are still clean.
3. **The climb gets taller.** Power and current rise. Surge margin shrinks. This looks like fouling or overcharge on a single pressure tag.
4. **Why York tells you to purge.** If you purge the air, head pressure falls back. If the tubes were dirty, head pressure **stays** high after purge. That is the field split: air is removable gas; fouling is not.
5. **Versus overcharge.** Overcharge raises **subcooling** (deeper liquid pool). Air mainly raises **pressure above saturation** without a matching extra liquid inventory. Trane groups “high subcooling + high head” as overcharge **or** non-condensables — both must be in the training set so a classifier can see the difference.
6. **Trip.** **High condenser / discharge pressure**, same family as low condenser-water flow and severe fouling.

**Easy mix-up.** Condenser fouling and overcharge. Split them with flow (normal here), subcooling (not a leak-like fall), and whether purge would clear the extra pressure.
