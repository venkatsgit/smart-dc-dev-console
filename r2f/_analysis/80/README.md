# 80 percent load — scenario analysis index

Unique scenarios under [`../../80/`](../../80/): **13**.

Work through them one by one. Tick a row when its detail note exists.

| # | Scenario id | Name | Status | Detail note |
| --- | --- | --- | --- | --- |
| 1 | `healthy_80pct` | Healthy baseline (no fault) | pending | — |
| 2 | `cond_fouling_SL1_80pct` | Condenser fouling, severity SL1 | done | [cond_fouling_SL1_80pct_detail.md](cond_fouling_SL1_80pct_detail.md) |
| 3 | `cond_fouling_SL2_80pct` | Condenser fouling, severity SL2 | pending | — |
| 4 | `cond_fouling_SL3_80pct` | Condenser fouling, severity SL3 | pending | — |
| 5 | `cond_fouling_SL4_80pct` | Condenser fouling, severity SL4 | pending | — |
| 6 | `evap_fouling_SL1_80pct` | Evaporator fouling, severity SL1 | pending | — |
| 7 | `evap_fouling_SL2_80pct` | Evaporator fouling, severity SL2 | pending | — |
| 8 | `evap_fouling_SL3_80pct` | Evaporator fouling, severity SL3 | pending | — |
| 9 | `evap_fouling_SL4_80pct` | Evaporator fouling, severity SL4 | pending | — |
| 10 | `leak_gas_slow_80pct` | Refrigerant gas leak, slow | pending | — |
| 11 | `leak_gas_moderate_80pct` | Refrigerant gas leak, moderate | done | [leak_gas_moderate_80pct_detail.md](leak_gas_moderate_80pct_detail.md) |
| 12 | `leak_liquid_slow_80pct` | Refrigerant liquid leak, slow | pending | — |
| 13 | `leak_liquid_moderate_80pct` | Refrigerant liquid leak, moderate | pending | — |

## Suggested order

1. Healthy baseline (reference for every fault pack)
2. Condenser fouling SL1 → SL4
3. Evaporator fouling SL1 → SL4
4. Gas leak slow → moderate
5. Liquid leak slow → moderate

## Per-scenario files in `../../80/`

For each id above, the data pack has:

- `*_manifest.json` — recipe and metadata
- `*_sensors.csv` — site-tag time series
- `*_cascade.csv` — departure / signature analysis (not on healthy)
- `*_truth.csv` — twin physics ground truth
- `*_twin_sensors.csv` — generic twin sensor tags

## Progress

- Done: **2 / 13**
- Remaining: **11**
