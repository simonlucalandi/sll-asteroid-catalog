# Methodology — TESS-FFI asteroid rotation periods

This describes how the periods in `catalog/catalog.csv` are derived. The processing code
is not distributed; this document specifies the method, gates, and thresholds in enough
detail to assess and reproduce the results independently.

## 1. Photometry
Rotation light curves are extracted from TESS Full-Frame Images (FFIs) using moving-target
aperture (PRF) photometry that tracks each asteroid across the FFI stack (built on the
open `tess-asteroids` / `lightkurve` stack). Each asteroid x sector crossing yields a
time series of (time, magnitude, uncertainty). Targets are numbered main-belt asteroids
with no reliable prior rotation period (LCDB quality U <= 1 or no entry), selected to be
bright enough at their in-sector epoch and away from the galactic plane to limit crowding.

## 2. Period detection (per sector)
- Cleaning: reject points with formal error >= 1.0 mag, then a 3x iterated bright-side clip
  at median - 4*MAD to remove field-star crossings (a co-moving aperture periodically
  overlaps background stars). Faint excursions are kept unless independently flagged.
- Detrending: a cubic polynomial is subtracted to remove the slow phase-angle/opposition
  brightness trend over the ~27-day sector.
- Periodogram: Lomb-Scargle from 1.5 h to min(400 h, half the baseline), with the analytic
  Baluev false-alarm probability (FAP).
- Detection gate: a sector "detects" only if FAP < 1e-3 AND normalized power >= 0.10 AND the
  peak is not at the search-grid edge. A single-sector peak longer than 0.35x the baseline
  is flagged as possible phase-curve geometry rather than rotation.

## 3. Shape: 1P vs 2P
A rotation light curve usually shows two brightness maxima per rotation (an elongated body),
so the photometric period is half the rotation period. The rotation period P_rot is adopted
as follows:
- Folded (phase-binned) amplitude > 0.40 mag -> 2P (P_rot = 2 x P_phot). Hard cut.
- Amplitude < 0.40 mag -> 1P, unless there is clear phase-locked minima asymmetry at the
  doubled period (two distinct, unequal minima), which forces 2P.
- Spin-barrier physics override: a strengthless (rubble-pile) body larger than ~150 m
  cannot rotate faster than ~2.3 h. A sub-2.3 h photometric period on a multi-km body is
  therefore necessarily the 2nd harmonic, and P_rot = 2 x P_phot regardless of amplitude.

## 4. Confirmation across sectors
- CONFIRMED: two or more sectors independently detect the same period (harmonic-aware, i.e.
  agreeing to within 5% at P, P/2, or 2P), with the multi-sector agreement significant at
  Baluev FAP < 1e-6.
- CANDIDATE: a single strong sector (power >= 0.30, >= 5 cycles, no phase-curve/grid-edge
  flag). A candidate cannot be promoted to confirmed without a second independent epoch.

## 5. Systematics rejection
Two families of instrumental signal are addressed explicitly:
- Momentum-dump / scattered-light comb: TESS reaction-wheel desaturations recur on the
  ~13.7-day orbit, producing a comb of alias periods at 328.8/n h. Periods within ~3% of a
  comb line are flagged and scrutinized.
- Difference-imaging / de-comb (DIA): for objects that are comb-adjacent, slow (>= 30 h), or
  rest on a contamination-flagged sector, an eigen-systematics model built from ~200 field
  stars in the same sector (SVD, top 5 components) is projected out of the target light curve,
  and the period power is re-measured harmonic-aware. A real rotation signal is preserved
  (power drop <= 15%); a purely instrumental one collapses (drop >= 50% with a high
  systematics-model R^2). Slow rotators are a known caveat -- their signal overlaps the
  systematics band, so an inconclusive de-comb result is deferred to a multi-sector
  phase-coherence test (real rotation folds to one shape across epochs; systematics do not).
- Independent instrument: where available, ZTF ground-based photometry (which shares none of
  TESS's systematics) is used as an independent check. A blind recovery of the TESS period
  over ZTF's multi-year baseline is decisive evidence the period is astrophysical.

## 6. Verification and catalog
Every confirmed/candidate period passes an independent, refutation-first re-analysis
(re-derive the period from the raw light curves; apply the alias, comb, and contamination
checks; enforce the shape conventions above; single-sector photometric detections above 100 h are treated as dead-on-arrival (trend-indistinguishable); an amplitude-forced doubling of a well-sampled fundamental across the 100 h line is retained as a provisional candidate with the doubling explicitly marked unconfirmed). Adopted values, shapes, and per-object reasoning for every non-trivial
call are recorded per object in `objects/` (one file each).

## Quality flags in the catalog
- `quality_U = 2` -- secure (CONFIRMED): multi-sector, systematics-checked.
- `quality_U = 1` -- provisional (CANDIDATE): single-sector or unresolved shape.
- `quality_U = 1-` -- MARGINAL.
Rejected detections (instrumental artifacts, e.g. comb aliases) are listed with reasons in
`catalog/rejected.csv` for transparency.

## Data provenance and attribution
Derived from public TESS FFIs (NASA/MIT/TESS) and ZTF (Palomar/IPAC, via the Fink broker).
Built on the open `tess-asteroids` and `lightkurve` packages. Please cite those upstream
resources and the accompanying paper(s) when using this catalog.
