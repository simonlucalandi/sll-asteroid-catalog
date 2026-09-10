# Changelog

All released versions are archived on Zenodo under the concept DOI
[10.5281/zenodo.21446076](https://doi.org/10.5281/zenodo.21446076).

## v1.5.0 (2026-09-10)

### Fourteen periods from the unadjudicated ledger stock

The catalog was frozen on 2026-08-24 for the method and catalog paper. The ledger lots v16,
v17 and v18, plus one Agnia crossing, had been extracted for a separate slow-rotator rate
study and were never adjudicated object by object, so a stock of measured but unarbitrated
periods sat outside the catalog. Eighteen of those objects were clean on both novelty gates
and carried a measured period; fourteen survived verification and enter here, four were set
aside as not measurable with the data in hand.

Each of the fourteen was re-derived rather than promoted from the census output:

- **Physical reduction instead of a per-sector polynomial.** JPL Horizons ephemerides from
  the TESS viewpoint, then reduced magnitude through the HG phase function at G = 0.15, so
  distance and phase angle are removed physically rather than absorbed by a detrending fit.
- **One global cubic trend** over the whole baseline with the period search capped at
  baseline/8, and the same search repeated at polynomial degree 2, 3 and 4; a period that
  moves with the trend degree is rejected. Independent time halves (or quarters, where the
  halves are too thin) must return the period, its double or its half within 5 per cent.
- **De-comb.** Eleven survived, three were inconclusive on the power-drop metric and were
  resolved individually: none was killed and none was downgraded. Two entries, (45880) and
  (12323), sit 1.0 and 2.1 per cent from a momentum-dump tooth, where survival of the
  de-comb does not certify by construction, and they are labelled as the most fragile of
  the batch.

Twelve of the fourteen rest on a single sector and are CANDIDATE. (3136) Anshan (three
consecutive sectors) and (4460) Bihoro (two) are CONFIRMED. (3136) at 463.822 h becomes the
longest period in the catalog, with the factor of two adopted **by convention and not
measured**.

| object | P_rot (h) | doubling class |
|--|--|--|
| (3136) Anshan | 463.822 | by convention, not established |
| (12323) Haeckel | 80.4884 | by convention, not established |
| (45880) 2000 WG49 | 55.355 | ambiguous, alias 110.710 h open |
| (8578) Shojikato | 30.8287 | ambiguous, alias 61.6574 h open |
| (6390) Hirabayashi | 24.6588 | ambiguous, alias 49.3176 h open |
| (13556) 1992 OY7 | 21.9454 | by convention, not established |
| (18405) 1993 FY12 | 15.5581 | ambiguous, alias 31.1162 h open |
| (17871) 1998 RD58 | 10.6016 | ambiguous, alias 21.2032 h open |
| (4460) Bihoro | 9.9302 | ambiguous, alias 19.8604 h open |
| (21691) 1999 RC42 | 7.597 | by convention, not established |
| (3430) Bradfield | 5.3088 | by convention, not established |
| (26649) 2000 ML6 | 4.2842 | **measured** |
| (6216) San Jose | 3.2648 | **measured** |
| (8067) Helfenstein | 3.0117 | ambiguous, alias 6.0234 h open |

Counts: 569 to **583** objects, 368 to **370** CONFIRMED, 200 to **212** CANDIDATE,
1 MARGINAL unchanged. Above 100 h 57 to **58**, above 200 h 13 to **14**. Period range
2.2942 h to **463.822 h**.

### Extraction completeness measured at pixel level, for the first time

Until now the extraction chain itself was assumed sound. It has now been measured: synthetic
moving sources with a known rotation signal are injected into the real FFI pixel cube before
any photometry touches the data, with the real TESS PRF, trailed inside each exposure, with
Poisson noise and the real distance and phase-angle terms, against an empty control track on
the same field. The design was pre-registered before execution. METHODOLOGY section 1b.

| apparent speed (px per 30 min) | recovered flux | period error | folded amplitude error |
|--|--|--|--|
| 0.15, near a stationary point | **0.86** | < 0.1 per cent | +9 to -14 per cent |
| 1.00, typical main belt | **0.986** | < 0.01 per cent | within 2.6 per cent |
| 2.05, fast | 0.993 | < 0.02 per cent | within 2.8 per cent |

At typical apparent speed the chain is sound and neither periods nor folded amplitudes are
measurably degraded. At slow apparent speed the photometry is systematically 12 to 14 per
cent faint, uniformly in time, because the per-pixel star model uses knots every 0.5 days
while a source at 0.15 px per 30 min needs 1.53 days to cross the window: 11.0 per cent of
the source flux ends up inside the background model, against 1.15 per cent at typical speed.
Absolute magnitudes from slow-track crossings carry that bias; rotation periods and folded
amplitudes do not. (3136) Anshan is affected in sectors 45 and 46 and its entry says so.

These numbers come from one sector, one camera, one CCD and one field: treat 0.86 as a
conditional single-field response, not a calibrated completeness correction. The same pass
also measured the de-comb projection, which preserves folded amplitude (median change 1.6 per
cent) but removes about half of a linear ramp across a sector, so no slow slope and in
particular no phase curve may be read off a de-combed light curve. METHODOLOGY 5d now carries
the measured size of the star-proximity effect as well.

### The odd-harmonic doubling test was not calibrated, and the catalog says so

The F test on the odd harmonics at twice the photometric period was validated against 174
external labels built from LCDB 2023 entries with U in {3, 3-}: 112 objects whose published
period is twice ours, 62 whose published period equals ours. Read with its nominal p-value the
test has **specificity 0.290**: it declares a doubling for 44 of the 62 non-doublings. Its two
added odd harmonics are low-frequency sinusoids that absorb red noise, while the F test assumes
independent residuals. **Nominal p-values from that test are no longer quoted anywhere.**

Recalibrated with a block bootstrap under the single-peaked hypothesis (residual and quoted
error permuted together within each sector, two block lengths, 20,000 realisations), the same
statistic reaches specificity 0.984 at sensitivity 0.196: when it speaks it is almost always
right, and it rarely speaks. The criterion that separates the two classes best is neither of
the pre-registered ones: it is the **topology of the fold**, one prominent maximum at the
photometric period stable in more than 90 per cent of bootstraps, at sensitivity 0.759 and
specificity 1.000. That criterion is **post-hoc** and has no prospective test yet; it is the
project's doubling convention made quantitative and stable, not independent physical evidence.

| criterion | sensitivity | specificity |
|--|--|--|
| nominal F test, p < 1e-3 | 0.964 | **0.290** |
| calibrated p_emp < 1e-3 at both block lengths | 0.196 | **0.984** |
| folded amplitude at P1 > 0.40 mag | 0.473 | 0.871 |
| unequal minima, z > 3 above the null mean | 0.179 | 0.984 |
| one prominent maximum in the fold at P1 | 0.759 | **1.000** |

What this changes in the catalog:

- **The catalog keeps deciding the factor of two on amplitude and topology**, which is what it
  already did, but now with measured sensitivity and specificity attached (METHODOLOGY 3b-bis).
- **The fourteen new entries carry an explicit doubling class**: measured, by convention and
  not established, or ambiguous. Where only the convention speaks, both aliases are published.
- **`shape: ambiguous` and `doubling: AMBIGUOUS` are documented values** in
  `catalog/data_dictionary.md`. `ambiguous` is not a synonym for `1P`: `1P` says no doubling
  applies, `ambiguous` says the question is open.
- **Pre-existing catalog entries did not use the F test and none of them changes here.** The
  67 doublings of v1.4.0 rest on the z1 statistic with a non-harmonic margin (METHODOLOGY 3d),
  which is a different test and is unaffected.
- Two statistical traps found in the same pass and now avoided: a non-negative statistic such
  as the depth difference between two minima must never be standardised as D/sd(null), because
  the null has a positive mean; and that difference must be defined invariantly under a phase
  shift, not as first half against second half. Correcting the first withdrew three doublings
  from the fourteen during review.

### Object sheets

- The line that announced an override of the pipeline shape carried a hardcoded justification
  ("folded amplitude >= 0.25 mag", "doubling audit 2026-07-25") that was **false on 144 of the
  215 sheets that printed it**: their amplitude is lower, and many overrides came from later
  passes. It now points at the factor-of-two line and the note on the same page, which are the
  per-object reasons.
- A de-comb verdict produced by a dedicated pass, rather than inside a lot's own refine output,
  is now reported instead of being announced as "not run" or omitted.

### Not released

The version is left unreleased on purpose: no tag, no Zenodo archive, and `CITATION.cff` still
points at v1.4.0.

## v1.4.0 (2026-09-01)

This release supersedes v1.2.0. A v1.3.0 tag exists in git but was never archived, so its
content is folded in here.

### The doubling rule was biased, and 67 periods changed

Rotation periods published in the Minor Planet Bulletin between 2024 and 2026 became
available for comparison. The publicly distributed LCDB has not been revised since
2023 October, so three years of ground-based determinations had been invisible to every
novelty and validation test in this repository.

On the 36 catalog entries the new comparison reaches, 16 periods agree within 2 per cent
and 9 disagree by exactly a factor of two. **All nine disagreements run the same way**, with
the independent observer adopting the longer period: probability 0.002 under a rule that
errs symmetrically. The amplitudes of the affected entries are 0.03 to 0.35 mag here and
0.14 to 0.31 mag from the ground, so below the 0.40-mag threshold in both datasets. The
ground observers had not applied an amplitude rule at all; they had seen two distinct
extrema in a well-sampled curve.

The folded-amplitude criterion has been replaced by a measurement of the asymmetry itself:
the odd-harmonic term A1 at the long period, with sigma from a block bootstrap, doubling
when z1 = A1/sigma >= 3 **and** the same statistic at the non-harmonic multiples 1.7x and
2.3x is smaller by at least 2. The margin excludes a slow amplitude modulation, which would
raise A1 at any long period. Nulls: 0 of 38 in the reference group, 0 of 17 at twice a
period an external observer confirms is already correct, against 12 of 17 at the correct
period. Full derivation in `methodology/METHODOLOGY.md` section 3d.

- **67 entries doubled** (40 CONFIRMED, 27 CANDIDATE). A blind rerun over all 569 rows
  recovered all five cases the external comparison had established independently, and misses
  two of them, so **67 is a lower bound** and the plausible range extends to 113.
- Objects above 100 h: 53 -> 57. Above 200 h: 11 -> 13. The error runs one way only, toward
  periods that are too short, so these counts remain lower limits.
- Twelve entries changed novelty class from first determination to confirmation, eleven
  against the Minor Planet Bulletin and one against Huang et al. (2026, KMTNet).
- The amplitude scale was checked and cleared: the median ratio to the ground-based scale
  is 0.93 over 28 objects, so the defect lay in the decision rule, not the photometry.
- The hand-written reasoning for (4597) is **retracted in place**. It had rejected the
  doubling by asserting an absence of asymmetry that was never measured; measured, it gives
  z1 = 7.42 with a margin of 5.30.

### Also since v1.2.0

- De-comb column re-scored with the calibrated v2 estimator across the catalog.
- (16405) moved to `rejected.csv`: the v2 screen rejects its only detecting sector.
- (15631) and (43173) admitted as CANDIDATE through the calibrated ZTF null pathway.
- (46992): the doubling is recorded as CONVENTION, not MEASURED. Equal mutual-event depths
  carry no information about the size ratio, so the earlier inference was withdrawn.
- Fold plots refreshed against current adopted values; duplicate batch-named plots removed.

## v1.2.0 (2026-08-02)

94 doublings corrected plus a quality audit.
Version DOI [10.5281/zenodo.21755996](https://doi.org/10.5281/zenodo.21755996).

## v1.1.0

26 periods corrected. Version DOI [10.5281/zenodo.21567084](https://doi.org/10.5281/zenodo.21567084).

## v1.0.0

First public release. Version DOI [10.5281/zenodo.21446077](https://doi.org/10.5281/zenodo.21446077).
