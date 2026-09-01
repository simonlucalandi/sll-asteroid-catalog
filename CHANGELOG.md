# Changelog

All released versions are archived on Zenodo under the concept DOI
[10.5281/zenodo.21446076](https://doi.org/10.5281/zenodo.21446076).

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
