# Walrus and Athena — four slides

Companion to `polymathic-walrus-failure-prediction.md`. Slide text only.

Assets in scope: **chiller** (primary chilled-water plant, HT/LT) and **FWU** (fan wall unit, hall-side secondary cooling).

---

## Slide 1 — Athena today

We are not starting from scratch. Several capabilities are already in production. A few are still experimental.

| Capability | Stage | What it does |
| --- | --- | --- |
| Anomaly detection | Production | Autoencoder + regression early warning for cooling and electrical |
| Time-to-threshold | Production | When a parameter is likely to hit a set operating limit |
| Physics-embedded models | Experimental | Physics equations inside the loss |
| Graph attention / topology | Experimental | Upstream and downstream relationships, root-cause context |
| Digital twin / run-to-failure | Experimental | Physics failure scenarios, such as condenser fouling |
| Survival / failure prediction | Experimental | Failure mode and time-to-failure |
| SME agent | Partial production | Agentic RAG and tools for investigation |

**Objective:** say **what** will fail, and **when**.

---

## Slide 2 — Two problems still open

Everything on slide 1 supports this. These two outputs are the gap.

**1. Classification — what will fail**

Which mode, on which asset.

- Condenser fouling, evaporator fouling, refrigerant leak
- Same question on the hall side: FWU coil heat-transfer collapse, valve or flow blockage

**2. ETF — estimated time to failure**

How long until that mode reaches a limit.

- Days, not the next minute
- Distinct from time-to-threshold, which watches one tag against a fixed limit

A useful answer is a pair: **mode + ETF**. A residual or a short forecast is not that pair.

---

## Slide 3 — LLM, Walrus, and the link back to slide 2

| | LLM (Llama, Qwen) | Walrus |
| --- | --- | --- |
| What it is | Transformer trained on text | Transformer trained on physical fields |
| One step of the sequence | A word piece | A patch of a grid |
| Input | A sentence | 6 snapshots of a 2D or 3D field |
| Output | The next word | The next physical state |

**Walrus in one line.** Give it the recent physical state. It returns the next physical state.

```text
6 grids  →  Δu  →  next grid = last grid + Δu
```

Call it again for the step after that. It does not return two steps in one call.

**Field types it already knows.** One `temperature` map, one `pressure` map, velocity in x/y/z, density, energy. About 63 names, slots 0–66. They are generic simulation channels. They are not `CH-CHWST`, `CH-CON-RFT-PRES`, FWU supply-air temperature, kilowatts, or amps.

**How this connects to slide 2.**

| Slide 2 question | Walrus |
| --- | --- |
| Which failure mode? | No. It does not classify. |
| Estimated time to failure? | No. It does not emit an ETF. |
| What can it do? | Continue the physical state. The weights were learned from many physics simulations (fluids, heat, acoustics, plasma), not by fitting a chiller or FWU tag table the way a time-series model does. |

No equation is typed into the model. The training movies came from physics solvers. The network learned “given these grids, the next grid moves like this.”

---

## Slide 4 — Use as-is? No. Fine-tune, and none exists for us

**Can we drop it onto the chiller, the FWU, or the primary and secondary cooling loops as released?**

No.

| System | Why the released checkpoint does not apply |
| --- | --- |
| Chiller (primary) | Minute-level point tags: supply, return, refrigerant pressure, power. Walrus wants a spatial grid and 6 frames. |
| FWU (secondary / hall) | Point tags: air temperatures, valve, water temperatures. Same mismatch. |
| Either loop, electrical side | No voltage, current, or power channel in the pretrained list. |

**Is there already a data-centre fine-tune?**

No. Public fine-tunes are other physics grids: incompressible Navier–Stokes, turbulent flow, neutron-star merger, stellar convection, FlowBench, and BubbleML pool boiling. BubbleML is the nearest thermal neighbour. It is a boiling-research grid, not a chiller and not an FWU.

**What a fine-tune would actually be**

1. Start from the public Walrus weights. Keep the pattern their own fine-tunes use: 6 frames in, 1 next frame out, predict the change.
2. Training data has to be spatial fields (a grid of temperature, pressure, velocity), in The Well layout or the same tensor. The sensor CSV is not that file.
3. Chiller and FWU tag names are new vocabulary slots. Those slots start untrained. The backbone only helps after the new fields are trained on our trajectories.
4. Realistic source of those grids: the digital twin or a CFD run of one fault, for example condenser fouling, written out as fields over time. Not the 2,880-row tag export alone.
5. After the rollout, Athena still does slide 2. Engineering indicators from the predicted state go into the existing classifier and ETF model. Walrus does not replace them.

**Practical split**

- Tag tables and ETF on chillers and FWUs: stay on the current Athena models.
- Walrus: only worth a pilot if the twin can emit a real spatial trajectory for one asset and one fault.
