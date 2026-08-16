# Novelty sources and how to refresh them (2026-08-15)

An adversarial novelty review found two objects in the paper-3 pool with published
rotation periods that the ledger could not see **by construction**: (7251) Kuwabara
and (9609) Ponomarevalya, both from Sergeyev et al. 2025 (Kepler K2, A&A 703, A302).

Root cause, measured: SsODNet's own bibliographic ingest thins out sharply after
2024 (across 213 live ssoCards: 801 references dated 2023, 558 dated 2024, **0 dated
2025**, 1 dated 2026). The oracle arm of the ledger is therefore blind to 2025+
literature, and LCDB's public release is still the October 2023 snapshot, so the
static arm cannot cover it either.

## Fix applied

`scripts/build_ledger.py` gained `load_vizier_periods()`, a fourth static arm reading
TSV dumps in `scripts/refcat_cache/`. Objects with a period in any of them are dropped
from the candidate pool before the SsODNet stage. Effect: 10,482 known periods added,
candidate pool 4,883 -> 4,219.

| file | catalogue | VizieR source | number col | period col |
|---|---|---|---|---|
| `sergeyev_k2.tsv` | Sergeyev+ 2025, Kepler K2 | J/A+A/703/A302 | `Number` | `Per` |
| `gowanlock24.tsv` | Gowanlock+ 2024 | J/AJ/168/181 | `MPC` | `Prot` |
| `cellino24.tsv` | Cellino+ 2024, Gaia DR3 inversion | J/A+A/687/A277 | `Name` | `Prot` (signed, use abs) |
| `euclid_prot.tsv` | Irureta-Goyena+ 2026, Euclid | J/A+A/710/A27 | `Name` | `P1h` |

## Refresh before any submission

```bash
cd ~/projects/astro/ng/scripts/refcat_cache
for c in "J/A%2BA/703/A302:sergeyev_k2" "J/AJ/168/181:gowanlock24" \
         "J/A%2BA/710/A27:euclid_prot" "J/A%2BA/687/A277:cellino24"; do
  curl -sL "https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=${c%%:*}&-out.max=unlimited&-out.all" \
       -o "${c##*:}.tsv"
done
```

Then re-run the SsODNet census **live, not from cache** (the cached path silently
returns the state of the day it was frozen), one query per second:
`https://ssp.imcce.fr/webservices/ssodnet/api/ssocard.php?q=<number>`, field
`parameters.physical.spins[].period.value`. Note `spins` is plural and an entry can
exist with no period value; ~half of a typical pool has exactly that shape and must
NOT be scored as known.

## Remaining blind spot

MPB issues from 2024 to 2026 are reachable through neither LCDB (2023 snapshot) nor
SsODNet (2025+ gap). Before submission, sweep VizieR for period catalogues registered
after the last ledger build:
`https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=METAcat&-out=name,title&-out.max=200&title=*asteroid*`

## Cross-match result on the paper-3 pool (220 objects)

| object | ours (h) | published (h) | source | relation |
|---|---|---|---|---|
| (7251) | 4.7866 | 4.9153 | Sergeyev+2025 K2 | 1:1 (-2.6%) — CONFIRMATION, not first |
| (9609) | 8.0790 | 7.8840 | Sergeyev+2025 K2 | 1:1 (+2.5%) — CONFIRMATION, not first |
| (4163) | 26.3520 | 26.3266 | Cellino+2024 | 1:1 (+0.1%) — confirmation |
| (1255) | 38.2758 | 76.6240 | Gowanlock+2024 | 1:2 — our halving, must be declared |
| (3631) | 22.3630 | 47.8410 | Gowanlock+2024 | 1:2 — our halving, must be declared |
| (27396) | 129.7912 | 976.2151 | Cellino+2024 | conflict, must be discussed |

Two further objects sit in the LCDB U=1 grey zone, where "first *reliable*
determination" is defensible but "first determination" is not: (8378) 11.794 h
against an LCDB U=1 value of 12.0 h, and (17923) 84.65 h against 20.0 h.
