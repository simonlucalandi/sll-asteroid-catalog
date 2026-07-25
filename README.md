# TESS-FFI Asteroid Rotation Catalog

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21446076.svg)](https://doi.org/10.5281/zenodo.21446076)

**Citing this catalog.** The badge above is the *concept* DOI
([10.5281/zenodo.21446076](https://doi.org/10.5281/zenodo.21446076)): it never changes and
always resolves to the newest release, so use it to point people at the current data.
When citing the catalog **in a paper**, cite the *version* DOI of the release you actually
used instead, so the numbers behind your results stay retrievable. The current release is
**v1.1.0**, [10.5281/zenodo.21567084](https://doi.org/10.5281/zenodo.21567084); every
version is listed on the
[Zenodo versions page](https://zenodo.org/search?q=conceptdoi:%2210.5281/zenodo.21446076%22&f=allversions%3Atrue).

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
| `plots/<number>.png` | per-object phase-fold at the adopted period (sectors phase-aligned); `plots/MONTAGE_<family>.png` are per-family contact sheets |

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
