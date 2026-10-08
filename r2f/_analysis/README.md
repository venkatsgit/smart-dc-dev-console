# R2F analysis workspace

Data packs live next to this folder:

| Folder | Contents |
| --- | --- |
| `../58/` | All `*_58pct_*` export files |
| `../80/` | All `*_80pct_*` export files |

## Notes by load

| Load | Folder | Scenario write-ups |
| --- | --- | --- |
| 80 percent | [80/](80/) | [cond_fouling_SL1_80pct_detail.md](80/cond_fouling_SL1_80pct_detail.md) |
| 58 percent | [58/](58/) | (add scenario `*_detail.md` files here as you analyse them) |

## Inspect scripts

```powershell
cd poc\smart-dc-dev-console\r2f\_analysis
python inspect_manifest.py cond_fouling_SL1_80pct
python inspect_csv.py cond_fouling_SL1_80pct cascade
```

Scripts resolve `../80` or `../58` from the case id suffix.
