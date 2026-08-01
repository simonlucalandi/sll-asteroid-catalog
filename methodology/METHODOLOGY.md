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

### 3b. Decision hierarchy for 1P vs 2P (revised 2026-08-01)
The amplitude convention is the WEAKEST rung, not the strongest. The order is:

1. **Measured fold shape** -- odd-harmonic power or unequal minima at the doubled period,
   significant against a block bootstrap. When present, it decides regardless of amplitude.
2. **Spin-barrier physics** -- a rubble pile larger than ~1 km cannot rotate faster than
   ~2.2 h. A sub-barrier photometric period on a km-sized body is therefore double-peaked
   whatever its amplitude: the single-peaked reading is physically excluded, not merely
   unlikely. This rung was added after a systematic sweep found 49 catalog entries below
   2.2 h, all on 5-16 km bodies and all shape 1P by the amplitude rule; a fresh
   odd-harmonic audit then found MEASURED double-peak evidence in 44 of the 49 (up to
   23.7 sigma), confirming that the amplitude rule fails systematically at the fast end,
   where geometric foreshortening keeps folded amplitudes small. All 49 were doubled onto
   3.0-4.4 h, the ordinary main-belt range.
3. **Amplitude convention** (folded amp > 0.40 -> 2P) -- only where neither measurement nor
   physics constrains the answer.

The odd-harmonic audit itself is CALIBRATED, not trusted: a null test re-runs the identical
machinery asking whether the already-doubled period should double again (2P vs 4P), where a
fire is false by construction. Measured on 60 real curves: the raw verdict fires falsely 27%
of the time, almost entirely through the minima-asymmetry branch (false z up to 34), which is
therefore NOT accepted on its own. Requiring odd-harmonic >= 8 sigma with EVERY detecting
sector significant gives 0/60 false fires; that is the bar a measured doubling must clear.
Applied to all 228 single-peaked entries on 2026-08-02: 45 cleared it and were doubled; the
71 symmetric and 41 sub-threshold cases keep their 1P reading.

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

## 5b. Chunked extraction and the quarantine (added 2026-08-01)
A crossing whose pixel stack exceeds memory is re-extracted in N time chunks and the chunks
are stitched. Each chunk's MEDIAN magnitude is normalised to a common reference, which
removes the inter-chunk zero-point steps that stitching would otherwise leave, but that
normalisation is a HIGH-PASS FILTER with its corner at the chunk length: it cannot separate an
instrumental step from real variation slower than one chunk, so it removes both. Measured over
the three ledger lots, 37% of crossings were chunked, with a median chunk span of ~155 h.

Consequently a long period recovered from a chunked curve is a lower bound, not a measurement,
and each such object carries one or more labels:

- **SUPPRESSED** the adopted period is at least half the chunk span, so amplitude is damped
  and the period can be biased short.
- **BROKEN_CHUNK** a chunk returned under 10% of the points its siblings did (its median is
  noise), or the applied offsets are large and not a smooth monotonic ramp. A monotonic ramp
  is instead a real slow trend across the sector and only affects periods near the chunk span.
- **AMP_DOMINATED** the non-monotonic stitching steps exceed the object's own folded
  amplitude, so any fold SHAPE from that curve may be an artefact of the stitching.

An object escapes the labels if a DIRECTLY extracted sector carries the adopted period; that
test is harmonic-aware, since under the doubling convention a direct sector at P/2 supports
rather than contradicts the claim. An object whose period rests only on quarantined curves is
recorded as CANDIDATE rather than CONFIRMED, and its object file says so.

Starved chunks are dropped rather than aligned as of 2026-07-30; curves extracted before that
date can contain a few points displaced by up to ~3 mag, which the census clipping removes.

## 5c. Field-wide (common-mode) events
Deep faint excursions in DIFFERENT asteroids coincide in absolute time 2.13x more often than
chance (5269 cross-object coincidences within 6 h against 2472 expected, over 294 objects and
38 sectors). At those times scattered light and background-subtraction failure degrade every
moving target in the field together. A bad-times map is built from every extracted curve on
disk (~3,200 curves, 97 sectors, 519 bad bins covering 1,557 h) and any event landing inside
one is rejected. This matters for transient-like features (dips, brightenings); it does not
affect the rotation periods, which are periodic and survive isolated bad windows.

## 5d. Star proximity
The co-moving aperture passes field stars continuously. A crossing is normally brief, but near
a STATIONARY POINT the target's apparent motion falls to ~8 TESS pixels/day and it lingers
beside a star for days, so the PRF wings draw a broad symmetric brightening that mimics an
astrophysical event. Any transient-like claim is therefore checked against the object's
ephemeris track and a Gaia DR3 cone search before it is retained.

## 6. Verification and catalog
Every confirmed/candidate period passes an independent, refutation-first re-analysis
(re-derive the period from the raw light curves; apply the alias, comb, and contamination
checks; enforce the shape conventions above; single-sector photometric detections above 100 h are treated as dead-on-arrival (trend-indistinguishable); an amplitude-forced doubling of a well-sampled fundamental across the 100 h line is retained as a provisional candidate with the doubling explicitly marked unconfirmed). Adopted values, shapes, and per-object reasoning for every non-trivial
call are recorded per object in `objects/` (one file each), including whether a 1P/2P doubling
was MEASURED (odd-harmonic power or unequal minima at the long period, significant against a
block bootstrap and reproduced per sector) or adopted BY CONVENTION (symmetric fold above the
amplitude cut, where photometry cannot decide). Where a fold-shape measurement contradicts the
amplitude rule the measurement wins and the override is recorded with its evidence; (2211) is
the worked example (odd-harmonic 4.3 sigma at 227.79 h in a directly extracted sector, against
an amplitude of 0.256 mag that the rule would have halved).

## 6b. Curve-quality audit and human review (standing gate, added 2026-08-01)
The signal gates above test the detection; none of them asks whether the CURVE is clean
enough to carry the claim it carries. That gap let a curve with day-long brightening bursts
hold a CONFIRMED 379 h entry until a human spotted it in the published montage. Two measures
now close it:

- `curve_quality_audit` ranks every catalog object by (a) its worst sector's outlier rate
  relative to THAT SECTOR's own norm (extended-mission sectors run 2-4x noisier than early
  ones, so absolute rates mislead), (b) the spread of folded amplitude across sectors,
  (c) the cycle count in the poorest sector, and (d) whether the 1P/2P call is measured or
  conventional. Objects with two or more flags go to human review.
- Every flagged object is REVIEWED BY EYE on the published fold before release, with three
  possible verdicts per object (holds / downgrade / kill) recorded alongside the audit. The
  2026-08-01 pass reviewed 86 flagged objects: 83 held, one was downgraded (its doubling had
  no shape evidence and its curve carries unexplained bursts), one had a sub-cycle 24 h data
  fragment removed from its display, one gained a documented eclipsing-binary reading.

Display rule from the same pass: a sector fragment covering less than ~3/4 of one cycle of
the adopted period is excluded from published folds; it cannot phase-fold meaningfully and
only smears the figure.

## 7. Published fold displays
The phase-fold plots in `plots/` show the photometry the periods were derived from, with
two display-side contamination excisions (both disclosed here and in figure captions):
- Error-gated dips: faint excursions > 0.75 mag below the sector median whose photometric
  error exceeds 4x the sector median error (PRF failures and resolved field-star crossings);
  this is the same rule applied in the period analysis.
- Non-recurrent transients: brief (< 3 h) faint excursions deeper than max(0.5 mag, 1.5x the
  folded amplitude) whose rotational phase is covered by at least three other observed cycles
  and never recurs in the cycle-binned light curve. These are field-star crossings and
  track-start scattered-light ramps that carry normal photometric errors. A real minimum or
  eclipse recurs every cycle and is retained by the recurrence test; excision is capped at
  1.5% of a sector's cadences. Sectors are phase-aligned by best circular shift (the relative
  rotational phase between epochs separated by months is not measurable at catalog period
  precision).

## Quality flags in the catalog
- `quality_U = 2` -- secure (CONFIRMED): multi-sector, systematics-checked.
- `quality_U = 1` -- provisional (CANDIDATE): single-sector or unresolved shape.
- `quality_U = 1-` -- MARGINAL.
Rejected detections (instrumental artifacts, e.g. comb aliases) are listed with reasons in
`catalog/rejected.csv` for transparency.

## Provenance lots
Objects carry the lot they were extracted in. `Ledger-v16/v17/v18` are the novelty-selected
belt-wide lots (V_opp <= 16.0, 16.0-16.25, 16.25-16.50), built by joining AstDyS against LCDB
2023, Vavilov & Carry 2025, McNeill 2023 and the SsODNet ssoCard aggregator, so every target
had no published period in any of those sources at selection time; the SsODNet query is
repeated live before publication. Named families (Themis, Koronis, Phocaea, ...) are
dynamically selected lots. `main belt` in the public tables covers the belt-wide batches.

## Data provenance and attribution
Derived from public TESS FFIs (NASA/MIT/TESS) and ZTF (Palomar/IPAC, via the Fink broker).
Built on the open `tess-asteroids` and `lightkurve` packages. Please cite those upstream
resources and the accompanying paper(s) when using this catalog.
