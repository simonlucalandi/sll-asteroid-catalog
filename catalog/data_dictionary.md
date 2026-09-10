# catalog.csv, data dictionary

| column | description |
|--|--|
| number | IAU minor-planet number |
| family | dynamical family / processing batch label |
| P_rot_h | adopted sidereal-approximate rotation period, hours |
| shape | `1P` (single-peaked light curve), `2P` (double-peaked, elongated body), or `ambiguous` (see below). A few Hungaria entries carry LCDB-style shape codes (`S`, `Sq`, `D`, `Dd`) inherited from that lot. |
| quality_U | reliability code: 2 = secure (multi-sector, systematics-checked), 1 = provisional (candidate), 1- = marginal (LCDB-style) |
| status | CONFIRMED / CANDIDATE / MARGINAL |

`shape: ambiguous` means the factor of two is undecided: the published `P_rot_h` is the
photometric period and **twice it is equally allowed**, because neither the calibrated test of
METHODOLOGY 3b-bis, nor the depth difference between the two minima, nor the topology of the fold
prefers one reading over the other. It is not a synonym for `1P`: `1P` asserts that no doubling
applies, `ambiguous` asserts that the question is open. Introduced 2026-09-10 as an explicit
value; four earlier entries already used it.

Rotation periods are TESS-FFI photometric determinations. Per-object reasoning for any
non-trivial call is in `objects/<number>.md`. Rejected detections and the reason
for rejection are in `rejected.csv`. Light curves are provided in ALCDEF v2.3 format under
`lightcurves_alcdef/`.

# evidence.csv, data dictionary

One row per catalog object with the quantities a sceptic would recompute anyway.

| column | description |
|--|--|
| num, family, P_adopted_h, shape, status | as in `catalog.csv` |
| n_sectors | detecting sectors the adopted period rests on |
| n_cycles_best | cycles of the adopted period covered by the best **single** sector. Where the detecting sectors are consecutive and the period was derived on their joint contiguous baseline, the object sheet states that second number too. |
| peak_width_frac | measured half-power full width of the Lomb-Scargle peak at the adopted photometric period, as a fraction of that period, from the narrowest sector |
| P_sigma_h | that width expressed as an approximate 1-sigma uncertainty in hours |
| doubling | what supports the factor of two, strongest first: `EXTERNAL`, `MEASURED`, `PHYSICS`, `CONVENTION`, `UNCONFIRMED`, `AMBIGUOUS`, `NONE(1P)`, `UNSTATED`. See METHODOLOGY 3b. |
| decomb | de-comb verdict: `survived`, `inconclusive`, `outofrange_v2(...)`, `NOT-RUN`, or empty where the test does not apply |
| chunked | whether the period rests on chunk-extracted photometry |
| quarantine | whether the entry's own note requires a re-extraction before the period can be claimed |

`doubling: AMBIGUOUS` is the tier that goes with `shape: ambiguous`: the alias is open, and
reporting it as `NONE(1P)` would claim the question had been settled in favour of the short
period. Added 2026-09-10.

# novelty.csv, data dictionary

| column | description |
|--|--|
| num, family, status, P_ours, shape | as in `catalog.csv` |
| lit_period, lit_sources | the published period used for the comparison, and where it comes from |
| lit_status | `VIRGIN` (no published period on either novelty gate), `PUBLISHED_SINGLE`, `PUBLISHED_AGREEING`, `CONTESTED`, `TWOX_AMBIG` |
| sbdb_period | the JPL Small-Body Database period, where one exists |
| novelty | `FIRST-DETERMINATION`, `CONFIRMATION`, `HARMONIC-RESOLUTION`, `SUPERSEDES-LIT`, `SUPERSEDES-LIT(artifact)`, `ARBITRATION(contested-lit)` |

Novelty is checked on two gates together, the LCDB 2023 summary and the SsODNet `ssoCard`
spins field. Either one alone is incomplete: neither is a superset of the other.
