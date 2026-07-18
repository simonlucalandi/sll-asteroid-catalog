# catalog.csv — data dictionary

| column | description |
|--|--|
| number | IAU minor-planet number |
| family | dynamical family / processing batch label |
| P_rot_h | adopted sidereal-approximate rotation period, hours |
| shape | 1P (single-peaked light curve) or 2P (double-peaked, elongated body) |
| quality_U | reliability code: 2 = secure (multi-sector, systematics-checked), 1 = provisional (candidate), 1- = marginal (LCDB-style) |
| status | CONFIRMED / CANDIDATE / MARGINAL |

Rotation periods are TESS-FFI photometric determinations. Per-object reasoning for any
non-trivial call is in `reasoning/PERIOD_DECISIONS.md`. Rejected detections and the reason
for rejection are in `rejected.csv`. Light curves are provided in ALCDEF v2.3 format under
`lightcurves_alcdef/`.
