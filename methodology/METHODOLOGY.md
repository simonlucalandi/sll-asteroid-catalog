# Methodology: TESS-FFI asteroid rotation periods

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
- **REVISED 2026-08-30, see 3d below.** Odd-harmonic significance at the long period is now
  the primary criterion; the amplitude cut is retained only as a second, independent trigger.
- Folded (phase-binned) amplitude > 0.40 mag -> 2P (P_rot = 2 x P_phot). Hard cut.
- Amplitude < 0.40 mag -> 1P ONLY IF the odd-harmonic test of 3d also fails; a significant
  odd harmonic doubles the period regardless of amplitude.
- Spin-barrier physics override: a strengthless (rubble-pile) body larger than ~150 m
  cannot rotate faster than ~2.3 h. A sub-2.3 h photometric period on a multi-km body is
  therefore necessarily the 2nd harmonic, and P_rot = 2 x P_phot regardless of amplitude.

### 3d. The amplitude cut was biased, and what replaced it (2026-08-30)

**The evidence.** Rotation periods published in the Minor Planet Bulletin between 2024 and
2026 became available for comparison (the publicly distributed LCDB has not been revised
since 2023 October, so three years of ground-based work were invisible to every novelty and
validation test in this repo). On the 36 catalog entries the new comparison reaches, 16
periods agree within 2 per cent and 9 disagree by exactly a factor of two. **All nine
disagreements run the same way, with the independent observer adopting the longer period**,
which has probability 0.002 under a rule that errs symmetrically. The amplitudes of the
affected entries are 0.03 to 0.35 mag here and 0.14 to 0.31 mag from the ground, i.e. below
0.40 in BOTH datasets: the ground observers were not applying an amplitude rule at all, they
were seeing two distinct extrema in a well-sampled curve.

**Why the amplitude cut could not have caught it.** Amplitude is a proxy for the question
("is the body elongated enough that one hump per rotation is implausible?"); the odd harmonic
is a measurement of the question ("do the two halves of the long cycle differ?"). And the
error is invisible to every other diagnostic, because under-doubling IMPROVES them: folding a
two-cycle curve onto one cycle averages away the asymmetry and strengthens the even-harmonic
periodogram peak. No FAP, power, fold-coherence or residual statistic can reveal it.

**The statistic now used.** Two-harmonic Fourier fit at the long period; A1 is the odd
(asymmetry) term; sigma_A1 from a block bootstrap of the residuals (blocks 1/10 of the span,
200 resamples); z1 = A1/sigma_A1, combined across sectors by inverse variance.
**Doubling requires z1 >= 3.0 AND a margin of at least 2 over the same statistic evaluated at
the non-harmonic multiples 1.7x and 2.3x.** The margin exists because a slow amplitude
modulation (changing aspect along a sector, trend residual, comb) raises A1 at ANY long
period; requiring the excess to be specific to 2x removes it. Measured: on the reference
group of 38 entries whose 1P reading the test confirms, the margin exceeds 2 in **0 of 38**;
on a second null, A1 at 2x a period an external observer confirms is already correct, no
object reaches z1 >= 3 in **0 of 17**, while the same statistic at the CORRECT period is
significant for 12 of 17.

**Result of the sweep on the whole catalog.** 113 of the 196 single-peaked entries fire on
z1 alone; **67 also clear the margin and were doubled** (40 CONFIRMED, 27 CANDIDATE). A blind
rerun recovered all five cases the external comparison had established independently, but two
of those five sit below the margin, so **67 is a LOWER BOUND** and the plausible range runs to
113. Effect on the slow tail of the confirmed non-Hungaria set: above 100 h 34 -> 37, above
200 h 5 -> 6. The error runs one way only, so slow counts remain lower limits for this reason
as well. Ledger: docs/results/corrections_20260830.csv.

**Relationship to the 2026-08-02 odd-harmonic audit (section 3b), which used 8 sigma.**
The two are not the same statistic and the thresholds are not comparable. The 2026-08-02 test
measures the combined odd power (k=1,3,5) against a synthetic null in which the even component
is reinjected and the odd signal is absent, so its sigma counts standard deviations above a
no-signal null distribution. The present test measures A1 against its own bootstrap spread,
and because A1 is the magnitude of a two-vector it has a positive floor even with no signal:
the observed null median is 1.60, so z1 = 3 is roughly two of those floors, not three
standard deviations above zero. The present test is also more sensitive by design, combining
sectors by inverse variance where the 2026-08-02 rule required EVERY detecting sector to fire
independently. It therefore overturns 1P readings that the earlier audit had left standing.
Both calibrations rest on comparable null sizes (0/60 there, 0/38 and 0/17 here). **A direct
head-to-head of the two statistics on the same objects has NOT been run and is the obvious
next check.**

### 3b. Decision hierarchy for 1P vs 2P (revised 2026-08-01)
The amplitude convention is the WEAKEST rung, not the strongest. The order is:

1. **Measured fold shape** -- odd-harmonic power or unequal minima at the doubled period,
   significant against a block bootstrap. When present, it decides regardless of amplitude.
   **Per-sector requirement (added 2026-08-22):** the fold-shape comparison must be made in
   each sector INDEPENDENTLY, never on a pooled multi-apparition fold. When sectors are
   years apart, the relative phase at the doubled period is effectively arbitrary, and
   pooling can manufacture (or erase) alternating minima. Case in point: (92227) was
   wrongly re-doubled to 93.12 h in July 2026 from a pooled fold showing 0.17 mag fake
   alternation; per-sector even/odd nested Fourier tests (block bootstrap p = 0.89/0.97)
   showed no odd structure, and the original 46.587 h stands. The doubling ladder does not
   recurse: the amplitude rule takes P_phot -> 2 x P_phot once; any FURTHER doubling
   requires per-sector significant odd structure at the quadrupled period.
   **Mutual-event exception (added 2026-08-27):** for a candidate eclipsing binary the
   rung works in one direction only. Unequal minima half a phase apart still force a
   doubled PHOTOMETRIC PATTERN period, because a signal that truly repeats every P must
   look identical on successive cycles; for minima confirmed to be mutual events, that
   doubled pattern is also the doubled orbital period. EQUAL minima, however, prove
   nothing: in the idealized model where the two components have the same uniform
   surface brightness (the usual equal-albedo idealization), a mutual event removes the
   light of the projected overlap area whichever body is in front, so primary and
   secondary events have the same depth for ANY size ratio. Equal depths are therefore
   predicted under both the P and the 2P reading, and neither break the degeneracy nor
   constrain the component size ratio. An upper limit on the depth alternation is not
   evidence for near-twin components, and must not be recorded as MEASURED doubling.
   Case in point: (46992) carried doubling=MEASURED on exactly this argument from
   2026-08-01 until the error was found on 2026-08-27; it is now CONVENTION, with the
   adopted 53.8038 h read as a photometric period and the orbital period left
   unresolved between 26.88 and 53.77 h. What the depth does constrain is the size
   ratio through its ABSOLUTE value (a fractional deficit delta needs a projected area
   ratio of at least delta/(1-delta)), and only when the depth is not inflated by
   background over-subtraction.
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

Since 2026-08-08 the evidence columns surface rung 2 as its own provenance tier, `PHYSICS`,
sitting between MEASURED and CONVENTION in the `doubling` column; earlier releases lumped
those objects under the amplitude convention or left them unstated, which understated the
strength of their doubling. The same pass closed every remaining UNSTATED entry in the
catalog (52 objects, all outside the slow tail, which had been cleaned on 2026-08-05).

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
- De-comb (tess-decomb v2, re-scored 2026-08-23): for objects that are comb-adjacent, slow
  (>= 30 h), or rest on a contamination-flagged sector, an eigen-systematics basis is built
  from the full sector pool of field stars (~1600 stars, rows weighted 1/sigma^2 with sigma
  from the first differences, SVD, top 5 components) and projected out of the cubic-detrended
  target light curve; the verdict statistic is the RETAINED AMPLITUDE, the ratio of the
  sinusoid semi-amplitude fitted at the candidate period after and before the projection,
  quoted as the median over the full-pool basis plus 7 bootstrap resamples of the pool
  (10-90 band as uncertainty). Object sheets show it as `<verdict>_v2(ret=...[p10-p90],
  sNN@P)` per sector. The thresholds are calibrated operating points on the V12 ROC of the
  public tess-decomb repository (568 published periods as controls, 63 comb artefacts; AUC
  0.632): retained < 0.60 = `reject` (artefact-like; 1.2% of true periods fall here),
  0.60-0.85 = `flag` (suspect, not a rejection), >= 0.85 = `survived`. The test is an
  ASYMMETRIC SCREEN: a rejection is reliable, a non-rejection is not evidence of a real period.
  **Operating point superseded 2026-08-28 (tess-decomb V15).** Those thresholds are global,
  and a global threshold does not deliver one false-rejection rate: measured on the 468
  controls it delivers 0.7% below 55 h, 3.2% between 55 and 150 h and 31% above 150 h. The
  screen was therefore about ten times too conservative in the band where the comb is
  physical flux rather than a spectral-window alias, and was issuing verdicts beyond 150 h
  where the score is ANTI-discriminating (AUC 0.326, controls suppressed more than
  artefacts because a signal completing barely one cycle is absorbed by the basis). The
  calibrated replacement sets the threshold per period band at a true fixed false-rejection
  rate: reject at retained <= 0.908 below 55 h and <= 0.613 between 55 and 150 h (FR 5%),
  flag up to 0.957 and 0.797 respectively (FR 15%), no verdict above 150 h. Catch inside
  the domain rises from 5.1% to 27.1% with no change to the estimator, and
  leave-one-sector-out gives 5.6% out-of-sample false rejection against the 5% nominal.
  **The catalog's decomb column has NOT been re-scored under the new operating point yet**;
  it still carries the global-threshold verdicts, which are conservative, so no published
  period was wrongly rejected by them.
  About a quarter of the comb artefacts are pure spectral-window aliases that no flux-based
  basis can remove (V13), and parallel-aperture "ghost" regressors add nothing beyond the
  star basis (V13, pre-registered pilot). The earlier power-drop metric (drop <= 15% kept,
  >= 50% collapsed) was retracted on 2026-08-18 and no sheet quotes it any more. Slow
  rotators remain a caveat -- their signal overlaps the systematics band, so a `flag` on a
  slow rotator is deferred to a multi-sector phase-coherence test (real rotation folds to
  one shape across epochs; systematics do not).
- Independent instrument: where available, ZTF ground-based photometry (which shares none of
  TESS's systematics) is used as an independent check. A blind recovery of the TESS period
  over ZTF's multi-year baseline is decisive evidence the period is astrophysical.
- Calibrated ZTF admission (added 2026-08-27). The ZTF joint-fit verdict CLASSES alone are
  not sufficient for admission: in cadence-preserving null realizations (whole observing
  nights of residuals permuted over the real observation times, so gaps, filters and
  within-night correlations are preserved) 5-23% of pure-noise datasets still reach the
  SUPPORT class, and the analytic Lomb-Scargle FAPs are inflated by orders of magnitude
  (empirical floor of the nulls: 1e-4 to 1e-9, never the nominal 1e-20 and beyond). An
  object is therefore admitted through this pathway only when (a) its observed continuous
  statistic (the analytic FAP at the TESS-family period, used purely as a ranking number)
  is reached by fewer than 5 in 100 null realizations, and (b) signal injections at the
  proposed period into the same null base are recovered by the full decision rule in more
  than half of the realizations. A daily-alias ambiguity (comparable power at the +-1
  cycle/day alias of the half-period) is resolved by bidirectional injections before
  admission; if the alias is preferred, the object is not admitted at the long period.
  First admissions under this rule: (15631) and (43173), 2026-08-27.

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

## 5b-bis. Resolving the chunk quarantine (2026-08-05)

Section 5b quarantines a period that rests on chunk-extracted photometry, because median-matching
the chunks is a high-pass filter that removes variation slower than one chunk. Sixteen crossings
carried that flag, and their entries said the period could not be claimed until a direct
extraction existed. Rather than leave the caveat standing, all sixteen were re-extracted without
chunking and the Lomb-Scargle power AT THE ADOPTED PERIOD was compared before and after. That is
the right comparison: the global peak of a trend-dominated sector legitimately differs between
the two reductions, but the power supporting the published period must not.

Fifteen of sixteen retained or improved it (ratios 0.79 to 1.61, most above 1 because removing
the filter returns power to the signal), so twelve objects left quarantine on a measurement.
One did not. **(10824)**, adopted at 224.91 h, lost 76 per cent of its power in the sector that
carried it (0.263 to 0.063) and fell from being that sector's global peak to a third of it; its
second sector never supported the period strongly in either reduction. It is now rejected.

The programme was then extended (2026-08-06) to every remaining catalog object resting on
chunked photometry, quarantined or not, because leaving the test unrun on the rest of the
exposed population after it had refuted one member would have been indefensible. Final balance
over the full chunked-dependent set: **37 crossings targeted, 36 direct extractions obtained,
35 of 36 retained or improved the power at the adopted period** (ratios 0.75 to 1.61, most
above 1 because removing the high-pass filter returns power to the signal). The survivors
include the catalog's four longest periods, whose power ratios are 0.91 to 1.02 and which
remain the global peak of their sectors in both reductions. The one collapse is (10824),
rejected. The one crossing that could not be directly extracted is (2211) sector 98, the
57-day double-length sector, whose pixel track exceeds available memory as a single
allocation; that object is verified on its other, directly re-extracted sector, and the s98
curve remains chunk-extracted and flagged.

Two things follow for the method. Chunk stitching does not generally manufacture or destroy long
periods, which an indirect test on synthetic curves had already suggested and this direct test
on real curves confirms at 35 of 36. But the exception was real and it sat in the P > 200 h bin,
the most fragile part of the catalog, so a chunk-dependence is resolved by re-extraction and not
by argument. The direct curves are now the published ones.

## 5b-ter. Crowding rescue of |b| 5-15 degree crossings (2026-08-08)

The extraction queues historically discarded any crossing within 15 degrees of the galactic
plane. A ground-truth test on the tumbler lot (114 rescued objects against LCDB) measured the
real cost of crowding at these latitudes: agreement with published periods is 72 per cent for
|b| 5-15 against 77 per cent above, a 5-point penalty and not a cliff. The cut was therefore
relaxed to |b| >= 5 for catalog objects, with the other queue criteria unchanged
(median TESS magnitude <= 16.8, fraction on silicon >= 0.5).

The rescued crossings earn their place under the SAME per-sector gates as every other
detecting sector (FAP < 1e-3 and power >= 0.10 at the adopted photometric period), and
promotions to CONFIRMED follow section 4 unchanged; every promoted second sector in this
pass in fact supports the adopted period at FAP <= 1e-22. First application: 48 crossings
targeted on 42 catalog objects, 43 extracted, 25 passed the gates, 9 single-sector
candidates gained a second independent sector and were promoted.

Near-comb candidates from these crowded fields get one additional test that the rest of the
catalog rarely needs: a FIELD CONTROL. The Lomb-Scargle power at the candidate's exact
frequency is measured on at least 15 unknown objects extracted from the same sector; a real
rotation stands 39x to 5000x above the field median, while a frame-level systematic would
appear in the field too. This is now part of the standard verification for any candidate
within 3 per cent of a 328.8/n or 24/n line, motivated by the measured comb excess in
|b| 5-15 fields (47 per cent of census peaks near a line against 26 per cent expected).

A rescued curve in which the adopted period does NOT pass the gates is renamed to
`lc_<num>_s<sector>.csv.nodetect` and drops out of every downstream count: n_sectors in the
evidence columns means DETECTING sectors, and a curve that does not detect the period must
not inflate it. The file is kept on disk because a non-detection at one apparition is still
information (aspect changes can null the lightcurve of an elongated body seen pole-on).

## 5b-quater. Crowded-field campaign over the full ledger tiers (2026-08-15)

The 5b-ter relaxation was extended from targeted rescues to the ENTIRE |b| 5-15 tier of the
consumed extraction queues (ledger v16/v17/v18 and the batch lots): 118 crossings, 106
extracted (2026-08-13/14). Two pipeline changes made the unattended campaign reliable and
are now permanent: a camera/CCD auto-locate fallback when the queue's predicted chip is
stale (the "was not observed in sector/camera/ccd" class of failures proved to be mostly
wrong-chip predictions with real data, not missing data), and per-job wall-clock caps in
the extraction driver (2h single / 4h chunked) after a hung download idled a worker for 8h.

Adoptions and promotions from this harvest passed a three-way ADVERSARIAL review beyond the
standard gates (docs/results/adversarial_review_20260815.md in the working repo):

- NULL-CALIBRATED GATE: on each evidence sector, 200 random periods (log-uniform, excluding
  +-25 per cent of P_phot and 2 P_phot) are pushed through the same gate; if more than ~5
  per cent pass, the gate has no discriminating power on that curve (red noise) and the
  object cannot be CONFIRMED from it. This test alone rejected three census-CONFIRMED slow
  rotators (2125, 3372, 19763), including a 279h claim whose curve passes 22 per cent of
  random periods.
- HALF-SPLIT stability, cross-sector spread judged against the peak width dP/P ~ P/baseline
  (agreement inside the width is NOT independent evidence), and the spectral window at 1/P.
- The folded-amplitude doubling rule applied adversarially: a census 1P with folded
  amplitude >= 0.40 mag is refuted, and the object is adopted at 2x the census period
  (23444, 25064 — the latter also below the ~2.2h spin barrier).
- FIELD CONTROLS (5b-ter) for any survivor within ~3 per cent of a 24/n or 328.8/n line.

GATE DEFINITION CLARIFIED: the per-sector gate is UNWEIGHTED Lomb-Scargle power (the
implementation of rescue_sector_verdicts.py). Error-weighted LS can move a marginal sector
across the 0.10 bar in either direction (three cases in this pass, spread 0.008-0.126 vs
0.083-0.121); reviews must therefore be re-verified with the canonical tool before any
catalog change, and two weighted-only promotions were rolled back on exactly this ground.

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

## 6c. Phase anchors: T0 and per-apparition amplitude (2026-08-08)

A period without an epoch says how often, not since when: it cannot propagate a rotational
phase to an external instrument's observing time. `catalog/phase_anchors.csv` therefore ships,
for every object, an absolute epoch and the amplitude information a joint fit needs:

- `T0_jd`: the JD of the deepest minimum of the Fourier model, evaluated inside the
  best-covered apparition (not the first), so the anchor sits where the data constrain it
  most. The model is a least-squares Fourier series at the adopted photometric period,
  order chosen by BIC between 2 and 6.
- `amp_folded_mag` and `amp_per_apparition`: apparitions are clusters of epochs separated
  by gaps longer than 90 days; the per-apparition fit holds the period and relative harmonic
  shape fixed and rescales amplitude and phase offset, because viewing aspect changes
  between apparitions and a single global amplitude would average over geometry.
- Declared limitation, half-cycle ambiguity: for a 2P object whose two minima are nearly
  equal, "deepest minimum" is decided by noise, and independent reductions can land half a
  cycle apart. A consistency check against the public ALCDEF exports found exactly this in
  49 of 116 overlapping objects (median offset 0.495 cycles, amplitudes agreeing); a
  downstream fit should treat T0 as defined modulo half a cycle unless the minima depths
  differ by more than the noise.
- The sigma_P column of the evidence table is reported to four significant figures since
  2026-08-08; the previous two-decimal rounding quantized 103 fast rotators to a
  meaningless 0.00 h.

These anchors exist because phase PREDICTION over survey timescales is impossible at
catalog precision (median sigma_P/P of 3.8e-3 accumulates to ~6 cycles of phase error over
two years): an external epoch series must be fit JOINTLY with the period, with the catalog
value as the alias-breaking prior, and T0 plus per-apparition amplitude are the parameters
that fit needs seeded.

## 6d. Cross-checking periods against SPHEREx QR2 (2026-08-09, revised same day after adversarial review)

SPHEREx observes every asteroid near quadrature and releases calibrated spectral images
weekly; forced PSF photometry at the ephemeris position yields an epoch series that is
instrument-independent of TESS. The photometry is validated on catalog stars
across all six detectors and multiple PSF zones (247 stars, 2MASS for D1-D3 and AllWISE
for D4-D6): on the reflected-band detectors D1-D3, which carry all the science below
2.6 um, the median offset is -0.01 to -0.05 mag (scatter 0.27-0.34 mag, dominated by
unmodelled star colors); the thermal detectors D4-D6 show color-systematic offsets up to
+0.3 mag and are excluded from the reflected-band fits. Epochs with a contaminating star
are dropped by a two-tier, per-band screen matched to the estimator footprint (Gaia for
D1-D2, 2MASS for D3-D4, AllWISE for D5-D6), with a background-ring rule that respects the
median's robustness (only a bright star or a crowd can bias it). Two FLAGS-mask subtleties are documented in the code: bit 21
marks pixels of known sources, and bit 19 is the outlier detector, which fires on the
moving target itself.

What this cross-check can and cannot claim was settled by an adversarial review the same
day the first version of this section was published, and the corrected standard is:

- significance is quoted ONLY from empirical nulls matched to the claim structure (rigid
  phase rotation for an anchored phase; visit-block shuffling for phase coherence), never
  from sqrt(delta chi-square), because the spectral baseline is misspecified
  (chi-square/dof 15-22) and per-epoch systematics of 0.2-0.7 mag dominate the formal
  errors;
- a leverage audit is mandatory: if removing one epoch or visit removes most of the
  signal, the claim is about that epoch, not the dataset.

First applications, restated at their null-calibrated value:

- **(2451)**, P = 138.36 h: the TESS-shape model at the adopted period, with phase
  ANCHORED to the contemporaneous TESS sector (36 of 37 SPHEREx epochs fall inside that
  sector's time window, so this is a same-window cross-instrument consistency check, not
  an out-of-sample prediction), is consistent with the SPHEREx epochs at about the
  2-sigma level (rigid-phase null p ~ 0.10 on the contamination-cleaned set; permutation
  null p ~ 0.013). The de-rotated reflectance is consistent with its published S class.
- **(2869)**, P = 310.5 h: inter-visit brightness modulation is present at about 3 sigma
  with amplitude compatible with TESS, but phase coherence across the 172-day span is NOT
  established: 37 of 38 clean epochs span 1.5 rotations and the long baseline rests on a
  single later epoch (visit-block null p ~ 0.15). The period's external support remains
  the LCDB 311.3 h agreement.

Neither object's adopted value changes. A verification CLAIM from SPHEREx awaits the
corrected contamination screen (footprint-matched radius, red-star handling), photometric
validation across detectors, and the null-calibrated fleet analysis.

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

## 8. Non-principal-axis (tumbling) screening
Objects are also screened for a second, non-harmonic rotation frequency (tumbling) with a
two-frequency Fourier fit in the Pravec et al. (2005) formulation: harmonics of f1 and f2
plus the combination terms (j f1 +/- k f2) that distinguish genuine two-axis rotation from
two unrelated periodicities. Detection is NOT taken from analytic statistics: the F statistic
of the second frequency is judged against the empirical distribution of the same statistic
over the non-control population of the same run (red noise makes analytic thresholds
meaningless), the operating point is chosen on a measured ROC built with LCDB-listed tumblers
as positive controls run through the identical pipeline, and every candidate must survive
(a) a common-fundamental veto (the two frequencies must not be harmonics of one base), 
(b) momentum-dump comb separation, and (c) reproduction of f2 across sectors where a second
sector exists. Candidates from this screen are reported separately from the rotation catalog
and are not catalog rows until independently confirmed.

The screen's SELECTION FUNCTION is measured, not assumed (injection-recovery, 2026-08-03:
3,264 two-frequency injections with combination-term power into 12 real single-period light
curves, the full decision chain as run, plus 12 clean nulls). Three measured facts constrain
what this screen can and cannot claim:

1. Amplitude floor: recovery is zero for second components below half the primary's
   amplitude, and 17-29% (hunt operating point) at equal-to-1.5x amplitude. The screen only
   detects tumblers whose second mode is comparable to the primary.
2. Blind zones at low-order period ratios: within 4% of a rational p/q (p, q <= 4),
   recovery drops to 11-14% against 34-54% outside, because the common-fundamental veto
   (correctly) kills pairs that a single harmonic-rich period could explain. A genuine
   tumbler at such a ratio is indistinguishable from a shaped single rotator in frequency
   content alone and cannot be claimed from this screen.
3. Null false-positive rate at the operating points: 0/12.

Consequently: reported tumbler candidates are required to sit at non-rational period ratios;
and no population-level tumbling fraction is quoted from raw candidate counts, since the
effective completeness is of order 10-20% and ratio-dependent. Full numbers and the map:
docs/results/NPA_SELECTION_FUNCTION.md and npa_blind_zones_v2.* in the working repository.

CONTROL-SET VALIDATION (2026-08-03, extended run). The positive-control set was doubled by
extracting 40 additional LCDB NPA-flagged objects that had never been observed by this survey
(selection dropped the original P >= 30 h and U >= 2 requirements: a control is a control
regardless of its period). Blind re-run over 1,024 objects / 134 controls / 1,748 sector fits:

- Discrimination: controls flagged at 13.4% vs 5.1% of non-controls (odds ratio 2.9,
  Fisher exact p = 0.0006). The screen separates known tumblers from the field.
- Full-chain recall (F above the empirical bar, F_comb > 20, second frequency reproduced
  to 10% in >= 2 sectors): 3 of 55 multi-sector controls at the 5% operating point,
  1 of 55 at the 1% point. This low number is the amplitude floor of the measured
  selection function at work, not a defect: LCDB tumbling flags come mostly from epochs
  and aspects where the second component was large.
- Recovered: (2045) Peking [T], (2000) Herschel [T+, published rotation matched to 1%,
  second period reproduced to 0.3%], (1839) Ragazza [T, strongest combination terms].
  Two of the newly added controls, (24077) and (6183), light up strongly in their single
  sector and are structurally excluded only by the two-sector reproduction bar.
- The candidate (3345) re-emerged past every bar in this blind re-run, unprompted, as the
  only non-control survivor besides the documented common-fundamental false positive (879),
  which the veto removes.

COVERAGE, AND THE BASELINE-SCALING VETO (2026-08-03). The screen needs a seed period, so it
had only ever run on objects that already had one, which is the population where tumblers are
least likely: the census rejects an object exactly when its sectors disagree on a single
coherent period, and a tumbler's light curve does not repeat. The complement was therefore
swept separately (369 multi-sector objects with no census period, seeded from each sector's own
Lomb-Scargle peak and its double). It produced no candidate, but it did expose a hole in the
bars:

Cross-sector reproduction of the second frequency was the main defence against systematics, and
against sector-specific artifacts it works. It is NOT evidence against an artifact whose period
is a fixed fraction of the sector length, because TESS sectors all have similar durations, so
such an artifact reproduces trivially. One object, (1826), passed every bar this way: P2 =
137, 248, 335, 338 h in sectors of 320, 495, 598, 586 h, that is P2/baseline = 0.43 to 0.58
throughout. A half-baseline drift, not a period.

The added test asks which quantity is stable across sectors of DIFFERENT length: a real period
holds P2 constant in hours while P2/baseline varies; a drift does the opposite. It targets the
half-baseline family specifically, so an object whose P2/baseline lies outside [0.35, 0.75] in
every sector passes conclusively; inside that band with near-identical baselines the verdict is
INCONCLUSIVE, never a pass. Applied retroactively, all recovered controls and all three
published candidates pass, and for (3345) it is the strongest evidence on record: its sector
baselines span 52% while P2 stays within 3%, where a baseline-scaling artifact would have
varied by the same 52%.

HOW MUCH THE REPRODUCTION BAR IS ACTUALLY WORTH (measured 2026-08-04). The bar requires the
second frequency to agree within 10% across sectors. That tolerance was never compared against
the precision the data can deliver, and it should have been. A Lomb-Scargle peak for a period P
over a baseline T is about P^2/T wide, so for a 175 h period in a 600 h sector (three cycles)
the peak is 30% of the period wide, and for two cycles it is 45%. Two independent draws from a
peak that wide agree within 10% often enough that passing the bar is weak evidence. **The
tolerance is therefore quoted relative to P^2/T from now on, not as a flat 10%, and a
reproduction claim states the peak width beside the agreement.** For the three candidates the
agreements (0.7%, 0.9%, and 3% in hours) are much tighter than their peak widths (13%, 23%,
30%), which is what a real signal detected strongly should give, so this measurement does not
overturn them; it removes an unearned part of their support.

WHAT A PHASE-CONNECTED TEST CAN AND CANNOT ADD. The natural next step, requiring the second
frequency to keep its phase across years rather than merely reappear, was built and calibrated
on the same controls. It does not discriminate: **(2000) Herschel, which carries LCDB's
highest-confidence tumbling code and whose second period the coherent scan recovers to 0.09%,
fails the test at p = 0.27**, and the null distributions sit within about 1% of the observed
scores throughout. With two to five sectors the share of the fit improvement that comes from
cross-sector phase is negligible next to within-sector structure, so no candidate is confirmed
or retracted on this basis. The coherent scan is kept for what it demonstrably does well: it
recovers published second periods to 0.1 to 1.8%, against about 30% per sector, and is used as a
period estimator only. A related correction belongs here: a shared-frequency multi-sector fit
that gives each sector its own harmonic coefficients does NOT constrain phase at all, since free
coefficients are free amplitude and free phase; only a fit with shared coefficients does.
