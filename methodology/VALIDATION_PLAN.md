# De-comb method: validation and hardening plan (V1-V7)

Status ledger for the systematic validation of the ensemble eigen-systematics removal
("de-comb", METHODOLOGY.md section 5). Purpose: replace every ad-hoc choice with a
measured one, and publish the method's completeness, reliability, and validity domain.
Current published evidence (RNAAS-scope): injection recovery 91-97% of synthetic 90 h
signals, <=1% power loss on a validated real rotator, real kill/save case studies.

## V1. Data-driven K (holdout cross-validation) -- **DONE 2026-07-19**
Every cached sector ensemble stores 20 holdout field stars never used in the SVD basis.
For each sector: sweep K=1..8, project the basis out of each holdout star, and pick K*
minimizing the holdout residual RMS (penalizing variance absorption). Deliverables:
- K* per sector across all ~58 cached sectors; median and spread.
- K* vs galactic latitude / field crowding.
- Verdict-stability check: re-run the catalog decomb verdicts at K in {3,4,5,6,7};
  report the fraction of verdicts that flip.
**RESULT (2026-07-19, 71 sectors, 224 verdict re-runs):** holdout residual plateau spans
K~2-8 (no overfit through rank 8); 84% of catalog verdicts identical for K in [3,7], the
rest almost all benign survived<->inconclusive crossings; ground-truth bracket: K=3 fails
to kill a known artifact (4942), K>=6 kills an independently ZTF-confirmed real signal
(3477). **K=5 is the conservative top of the data-bracketed range [4,5]: a derived
operating point, no longer an assumption.** Files: v1_holdout_k_sectors.csv,
v1_verdict_stability.csv, V1_RESULTS.md (working dir).

## V2. Injection campaign at scale
Substrates: several hundred NONE-tier real moving-target light curves (real noise, no
detection). Inject sinusoids on a grid: P in 2-300 h including points ON and BESIDE each
momentum-dump comb tooth (328.8/n, n=2..15); amplitudes 0.05-1.0 mag; across sectors
spanning crowding levels. Measure recovery fraction, amplitude bias, and false-kill rate
vs (P, amplitude, crowding). Deliverable: completeness/reliability maps.

## V3. Null test (false-survive rate)
Run the verdict machinery on pure comb power in NONE-tier tracks: how often does a known
artifact SURVIVE? Publishes the method's false-save rate alongside its false-kill rate.

## V4. Threshold calibration
Using V2+V3 distributions, place the survive (<=15% drop) and kill (>=50% drop, R2>=0.3)
thresholds on an ROC curve with quantified error rates; recalibrate if warranted.

## V5. Ensemble robustness
Bootstrap the 200-star ensembles (resampling, reseeding): verdict stability fraction.
One targeted local-vs-global ensemble comparison in a crowded field (scattered light is
position-dependent; test whether track-local star selection changes verdicts).

## V6. Validity domain
From V2: signal-loss curve vs P/baseline. Publish the domain statement (e.g. "reliable
for P below ~0.3x the sector baseline; beyond it, defer to multi-sector phase-fold
coherence"), turning the known slow-rotator over-subtraction into a characterized limit.

## V7. Joint-fit upgrade (methodological, optional)
Replace sequential project-then-measure with simultaneous fitting of the eigen-basis and
a Fourier series at the trial period, so the basis cannot absorb the signal. Expected to
largely remove the slow-rotator over-subtraction. If it works, becomes the centerpiece
of the full methods paper (PASP), with V1-V6 as its validation.

## Publication mapping
- RNAAS note (now): method + current evidence, scoped claims.
- PASP paper (after V1-V7): full validation + (decision pending) release of the
  standalone de-comb module.
