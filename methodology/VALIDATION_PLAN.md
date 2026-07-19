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

## V2. Injection campaign at scale -- **DONE 2026-07-19**
Substrates: several hundred NONE-tier real moving-target light curves (real noise, no
detection). Inject sinusoids on a grid: P in 2-300 h including points ON and BESIDE each
momentum-dump comb tooth (328.8/n, n=2..15); amplitudes 0.05-1.0 mag; across sectors
spanning crowding levels. Measure recovery fraction, amplitude bias, and false-kill rate
vs (P, amplitude, crowding). Deliverable: completeness/reliability maps.

## V3. Null test (false-survive rate) -- **DONE 2026-07-19**
Run the verdict machinery on pure comb power in NONE-tier tracks: how often does a known
artifact SURVIVE? Publishes the method's false-save rate alongside its false-kill rate.
**RESULT (2026-07-19; 120 tracks, 17372 injections, 46 null tests):** V2 false-kill <=3.0%
at amp 0.05 falling to ~0% at amp 0.4 (on-tooth included); median recovery 94-98%.
V3 false-survive ~61% (upper bound; impure ground truth): the projection removes the
ensemble-SHARED comb only. **Asymmetry: high-confidence killer, conservative clearer;
survival alone never certifies an on-tooth period.** Files: v2_injections.csv,
v3_null_test.csv, V2_RESULTS.md.

## V4. Threshold calibration -- **DONE 2026-07-19**
Using V2+V3 distributions, place the survive (<=15% drop) and kill (>=50% drop, R2>=0.3)
thresholds on an ROC curve with quantified error rates; recalibrate if warranted.
**RESULT (2026-07-19):** kill operating point (0.50) sits near the ROC knee: 1.13%
false-kill on real signals vs 6.5% artifact recall; tightening to 0.70 halves false-kills
but costs a third of the recall; retained. NO survive threshold separates real from null
(gap ~15pp at every X): quantifies the killer-strong/clearer-weak asymmetry across the
full sweep. Table: V4_V5_RESULTS.md.

## V5. Ensemble robustness -- **DONE 2026-07-19** (bootstrap + disjoint halves; local-vs-track variant deferred to PASP)
Bootstrap the 200-star ensembles (resampling, reseeding): verdict stability fraction.
One targeted local-vs-global ensemble comparison in a crowded field (scattered light is
position-dependent; test whether track-local star selection changes verdicts).
**RESULT (2026-07-19; 384 object-sector tests, B=6):** 77.3% of verdicts identical across
all 6 bootstrap-resampled bases; 88.5% agreement between two DISJOINT ~110-star half
ensembles. Of 87 unstable cases, 81 are benign survived<->inconclusive crossings; all 6
KILLED-involved cases are already-rejected artifacts wobbling killed<->inconclusive.
ZERO confirmed catalog objects flip under ensemble resampling. (Note: run with a
simplified single-period verdict reimplementation; production harmonic-aware verdicts
differ in detail, robustness statistics are the point. Track-local ensembles deferred.)
Files: v5_bootstrap.csv, V4_V5_RESULTS.md.

## V6. Validity domain -- **DONE 2026-07-19**
From V2: signal-loss curve vs P/baseline. Publish the domain statement, turning the
known slow-rotator over-subtraction into a characterized limit.
**RESULT (2026-07-19; 17.7k injections + long-P extension to 0.85x baseline):** the
domain is BETTER than the conservative guess: retention >= 88% and false-kill <= 3% out
to P = 0.45x baseline (~290 h in a 27-d sector); beyond it retention drops to ~70% and
false-kill to 6-8%. Curve: v6_validity_curve.png, v6_validity.csv.

## V7. Joint-fit upgrade -- **PROTOTYPED 2026-07-19 (mixed result, architecture decided)**
Replace sequential project-then-measure with simultaneous fitting of the eigen-basis and
a Fourier series at the trial period, so the basis cannot absorb the signal.
**RESULT (2026-07-19, 376 comparisons + 46 nulls + real slow rotators):** the joint fit
ELIMINATES the slow-rotator over-subtraction in-domain (recovery ~1.0-1.2 up to
P/baseline ~0.7 where sequential degrades to 0.49) and decisively recovers the real
over-subtracted cases (3396, 2869: dBIC 223-1298) -- but it is NOT an artifact
discriminator (96% false-clear on comb nulls) and overshoots in the few-cycle limit.
ARCHITECTURE DECISION: "sequential kills; joint measures" -- keep projection as the
calibrated KILL test, add the joint fit as the slow-rotator amplitude/significance
estimator. Centerpiece result for the PASP paper. Files: V7_RESULTS.md,
v7_joint_injections.csv.

## Publication mapping
- RNAAS note (now): method + current evidence, scoped claims.
- PASP paper (after V1-V7): full validation + (decision pending) release of the
  standalone de-comb module.
