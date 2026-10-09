# Run-to-failure with Red Dot Analytics

CEO briefing. Chiller failure scenarios, what we can detect today, and what we are building next.

---

## Slide 1. Purpose

We engaged **Red Dot Analytics (RDA)** to turn healthy chiller history into **run-to-failure** cases: a fault is introduced and the machine is followed until it is dirty and still running, or until it trips.

We want one answer operations can use:

**What failure is coming, and when will it happen?**

We are building that proof of concept on our side. This briefing covers the data we have, the models, how we will check them, and what we still need from RDA and from our own subject-matter experts.

---

## Slide 2. What we exchanged

**What we shared.** Two weeks of **healthy, steady** chiller telemetry. The machine was not failing. We sent it at two loads: about **80%** (higher load) and about **58%** (part load).

**What we received.** The same **13 scenarios** at each load. One healthy day, then faults RDA’s physics model ran on top of that day. The proof of concept starts on the **80%** set.

Each scenario is a pack of files: the recipe, the site-style sensor trace, and the model’s internal record of what the fault did. We do not need those internals to run a live detector. We need them to know what the correct answer was.

---

## Slide 3. The scenarios, in four families

Thirteen runs. Four failure families, plus a healthy baseline. Severity is how hard or how fast the fault is. It is not a separate kind of failure.

| Family | What it is | How hard / how fast | What the run ends as |
| --- | --- | --- | --- |
| Healthy | No fault | — | Machine keeps running |
| Condenser fouling | Scale on the condenser tubes. Heat cannot leave as easily. The compressor works harder. | SL1 (mild) through SL4 (severe) | Dirty, still running. No trip in this set. |
| Evaporator fouling | Scale on the evaporator tubes. Cooling of the building water gets worse. | SL1 through SL4 | Dirty, still running. No trip in this set. |
| Refrigerant gas leak | Hot discharge gas escapes on the condenser side. Charge drains until the evaporator tubes go dry. | Slow, or moderate | Protection trip (loss of charge) |
| Refrigerant liquid leak | Liquid refrigerant escapes on the high side. Charge is lost faster than in the gas case for the same size hole. | Slow, or moderate | Protection trip (loss of charge) |

**80% pack, by name**

- Healthy baseline
- Condenser fouling SL1, SL2, SL3, SL4
- Evaporator fouling SL1, SL2, SL3, SL4
- Gas leak, slow and moderate
- Liquid leak, slow and moderate

The 58% pack repeats this list at part load.

Two write-ups are done on the 80% set: mild condenser fouling, and the moderate gas leak. The moderate gas leak trips about **18 hours** after the hole opens. Mild condenser fouling never trips. It sits a little worse than a clean day for the rest of the fault day.

---

## Slide 4. What we can do today

| Today | What it tells us | What it does not tell us |
| --- | --- | --- |
| Anomaly detection | Something looks unlike normal operation. | Which failure it is. |
| Time to threshold | We forecast a sensor forward and see when that forecast crosses a limit. | Which failure will cause the crossing, or that a trip is coming when no single limit is the real end. |

A fouling case may never cross a trip limit. A leak case ends in a trip, but the early hours can look almost healthy. Thresholds on one tag do not answer “gas leak, about 12 hours left.”

---

## Slide 5. What we want

Two questions, in order.

1. **Which failure** is this window? Healthy, condenser fouling, evaporator fouling, gas leak, or liquid leak.
2. **When** will the named event happen? For the leaks in this set, the event is the protection trip. That time remaining is **remaining useful life**.

Fouling in this set has no trip. The honest answer there is: the fault is visible, the machine is in a dirty running state, and this data does not contain a trip time.

---

## Slide 6. How we will get there

One proof of concept. Two models. Both learn from the RDA scenarios. Live input is the same kind of chiller telemetry we already collect.

**Classification (one model).**  
It reads a short window of site tags and names the family. Severity stays out of the label: SL1 and SL4 are both condenser fouling. Slow and moderate are both a gas leak, or both a liquid leak. A separate label, used only in training, marks minutes where we must not name a family yet: the fault has started but the meters still look normal, or the machine has already tripped.

**Remaining useful life (one model, leaks only).**  
If the classifier says gas leak or liquid leak, and the machine is still running, a second model reads the same window and estimates time left until trip. Slow and moderate leaks train that same model. The sensors show how far the leak has gone. Healthy and fouling rows are not given a trip time, because this pack has no trip for them.

We are developing this proof of concept ourselves, on the scenarios RDA has already produced.

---

## Slide 7. The validation gap

Training and hold-out tests on these files will tell us whether the models fit the **simulated** faults. They will not tell us whether the same models recognise a **real** failure in a hall.

The physics runs are the right material for building the models. They are not a substitute for a check against plant behaviour, instrumentation, and how operators see the event.

---

## Slide 8. Where that check should happen

Older data centres are a poor place to learn this. They are not on Athena. A trial there is likely to become a data-collection and wiring exercise, not a test of the failure models.

**Ask.** Our subject-matter experts help **simulate the same failure families in SGP7 or SGP8**, on a site we already operate and can instrument. The RDA physics data stays the training set. SGP7 or SGP8 is the check that the models still make sense outside that set.

---

## Slide 9. What we do with RDA next

**Near term.** Continue the engagement for more scenarios, after this proof of concept shows we can name the family and, for leaks, estimate time to trip.

**Long term.** Learn their tooling and configuration: how a scenario is defined and how a run-to-failure case is produced. The aim is to create cases ourselves, at a scale we choose.

That scale is not one chiller only. The same method should reach a **subsystem** and, later, the **whole cooling system**.

---

## Slide 10. Commercials

Scope, price, and who owns the tooling are not settled.

What has to be costed:

- More scenarios from RDA while we finish this proof of concept
- Knowledge transfer so we can configure scenarios and run-to-failure cases ourselves
- The right to use that method beyond a single chiller

Budget for that second stage is still to be worked out. It should be separate from the cost of the SME simulation in SGP7 or SGP8, which is our plant and our people.

---

## Slide 11. Decisions needed

1. Confirm the proof of concept stays on the **80%** scenarios first, with the **58%** set as the second load.
2. Accept that the deliverable is **failure family plus time to trip for leaks**, not another anomaly or threshold alarm.
3. Nominate **SGP7 or SGP8**, and the SMEs, for a simulated check once the models exist.
4. Keep the older, non-Athena halls out of this validation.
5. Ask RDA for a proposal on **further scenarios** and on **teaching us to build scenarios**, with commercials split from the SGP7 / SGP8 work.
