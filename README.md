# TESS-FFI Asteroid Rotation Catalog

Rotation periods of numbered main-belt asteroids derived from TESS Full-Frame Image (FFI)
moving-target photometry. The program targets objects with **no reliable prior rotation
period** (LCDB quality U <= 1 or no entry), so most entries are first determinations.

This repository is the open **data + reasoning** companion to the accompanying Minor Planet
Bulletin paper(s). The processing code is not distributed; the method is fully specified in
[`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md).

## What's here
| path | contents |
|--|--|
| `catalog/catalog.csv` | adopted periods (CONFIRMED + CANDIDATE + MARGINAL) with shape and reliability code |
| `catalog/rejected.csv` | detections rejected as instrumental (e.g. momentum-dump comb aliases), with reasons |
| `catalog/data_dictionary.md` | column definitions |
| `lightcurves_alcdef/` | light curves in ALCDEF v2.3 format, one file per object |
| `objects/<number>.md` | per-object reasoning (one file per asteroid needing a judgment call: doublings, comb-vs-real, contamination, instrument conflicts); index in `objects/README.md` |
| `methodology/METHODOLOGY.md` | how the periods are derived: gates, thresholds, systematics handling |
| `plots/` | phase-fold montage(s) |

## Current contents
See `catalog/catalog.csv`. Status breakdown and per-object reasoning are versioned; consult
the file for the authoritative counts (this README is not the source of truth for numbers).

## How the periods should be read
- `shape` = 1P or 2P. Asteroid light curves are usually double-peaked (2P): an elongated
  body shows two brightness maxima per rotation, so the rotation period is twice the
  photometric period. See METHODOLOGY §3.
- `quality_U`: 2 = secure (multi-sector, systematics-checked), 1 = provisional candidate,
  1- = marginal. Candidates rest on a single sector and are not yet independently confirmed.
- Rejected detections are published deliberately (`rejected.csv`): the momentum-dump comb
  produces convincing-but-false periods, and documenting what was rejected, and why, is part
  of the method.

## Relationship to LCDB / ALCDEF
This is a supplement, not a replacement, for the canonical infrastructure. The periods are
also being submitted through the standard channels (Minor Planet Bulletin -> ALCDEF ->
Asteroid Lightcurve Database) where the community discovers and cites asteroid periods. This
repository adds the full per-object reasoning and the method description that a journal paper
cannot fully carry.

## Citing
See `CITATION.cff`. Please also cite the accompanying paper(s) and the upstream data
(TESS: NASA/MIT; ZTF: Palomar/IPAC via the Fink broker) and tools (`tess-asteroids`,
`lightkurve`).

## Integrity check
`python3 validate_repo.py` verifies that every `objects/<n>.md` matches `catalog.csv` /
`rejected.csv` on period, shape, and status (and that there are no orphan or missing
files). Exit 0 = consistent. The catalog and the per-object reasoning cannot silently
diverge.

## License
Data and documentation: CC BY 4.0 (see `LICENSE`).
