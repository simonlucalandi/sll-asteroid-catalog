# Paper 3 (MPB, deadline 2026 Oct 15): contents, adversarial review, and the correction plan

Four hostile referees were run in parallel on 2026-08-15 against the proposed
contents, each tasked with destroying one pillar. Every finding below carries the
number that supports it. Where a finding contradicted a decision taken earlier the
same day, the earlier decision loses.

## 1. What we proposed to publish

220 CONFIRMED rotation periods not yet published by us (the catalog holds 378; 209
went into papers 1-2), of which 213 were claimed as first determinations.

| evidence channel | n |
|---|---|
| TESS multi-sector | 143 |
| TESS single sector + independent ZTF blind recovery | 77 |

| period band | n | of which ZTF-dependent |
|---|---|---|
| < 4 h | 32 | 0 |
| 4-50 h | 129 | 56 |
| 50-100 h | 30 | 13 |
| 100-200 h | 21 | 7 |
| >= 200 h | 8 | 1 |

Plus three methodological claims: the crowded-field campaign (|b| 5-15), the
null-calibrated detection gate, and the TESS+ZTF joint confirmation channel.

## 2. What survives, and what does not

### 2.1 Novelty: 213 -> 209 first determinations

(7251) and (9609) have published K2 periods (Sergeyev+ 2025) agreeing with ours 1:1;
they are confirmations. (8378) and (17923) have LCDB U=1 entries, so "first reliable
determination" is defensible but "first determination" is not.

ROOT CAUSE, measured: SsODNet carries **zero** references dated 2025 across the 213
live cards, and LCDB's public release is still the 2023 October snapshot. The oracle
is structurally blind to recent literature. FIXED: `build_ledger.py` gained a fourth
static arm (K2 / Gowanlock+2024 / Cellino+2024 / Euclid 2026 VizieR dumps, 10,482
periods); candidate pool 4,883 -> 4,219. See `novelty_sources.md`.

Six further pool objects have literature values needing explicit framing: (4163)
confirms Cellino+2024 to 0.1%; (1255) and (3631) are our halvings of Gowanlock+2024
values; (27396) conflicts with a published 976 h; (1473) and (2705) reproduce LCDB
U=3 values to 0.11% and 0.33% and are `Npa-ext` positive controls, so they must be
presented as method validation, not discovery.

### 2.2 Slow rotators: 10 of 29 withdrawn, nothing survives above 200 h

| object | P (h) | killer number |
|---|---|---|
| (25880) | 433.59 | 1.35 cycles; a degree-4 polynomial beats the rotation model at equal DoF (R2 0.71 vs 0.25) |
| (28257) | 391.13 | 1.52 cycles; doubling at 3.08 sigma. The 195.6 h photometric period IS solid: publish that |
| (8508) | 275.67 | 2.26 cycles max, doubling never tested |
| (2211) | 227.79 | s98 fails the CANONICAL unweighted gate (0.0957); its chunk length 101.7 h < P_phot 113.9 h, so the extraction suppresses the very signal claimed |
| (73689) | 216.41 | null-calibration 0.120, identical to the (19763) value we withdrew this morning; half-split fails 2/3 |
| (5910) | 200.59 | doubling: poly4 beats rotation (R2 0.56 vs 0.22). ZTF confirms 100.3 h. Publish 100.3 h |
| (9449) | 194.51 | doubled on the minima-asymmetry branch our own notes declare inadmissible |
| (5844) | 148.10 | s70 fails the canonical gate; amplitude 0.31 vs 0.72 between sectors |
| (15286) | 118.76 | poly4 beats rotation on s51; amplitude 0.40-0.44 contradicts the declared 1P |
| (8513) | 107.54 | amplitude 0.41 in both sectors contradicts 1P; 1.9% from the 328.8/3 comb line |

Above 200 h, none of the eight objects has its factor-of-2 established by the
criterion the manuscript itself declares valid (odd-harmonic >= 8 sigma reproduced
across sectors). Seven of the eight never close 3 cycles in any sector.

### 2.3 Doubling and amplitudes: the deepest methodological problem

The declared amplitude estimator (fold, 50 phase bins, max-min of binned medians) is
**biased**, and I verified it independently: on real light curves with the phases
randomised, i.e. no coherent signal at all, it returns up to **0.314 mag**. Median
noise floor across the sample 0.121 mag, 90th percentile 0.242 mag, against decision
thresholds at 0.25 and 0.40 mag.

Consequences:
- 26 objects cross the 0.40 threshold and 31 cross 0.25 depending on which estimator
  is used, so for about a quarter of the sample the 1P/2P decision is set by the bin
  count, not by the data;
- the declared 50-bin recipe does not reproduce the tabulated amplitudes (23% within
  0.02 mag; the published table matches a 20-bin fold), a reproducibility failure;
- the quoted odd-harmonic significances are covariance sigmas, inflated by a median
  factor 7.9 against a null calibrated on decoy periods.

Concrete errors found, both verified independently by me:
- **(5024)**: catalog note claims "doubling MEASURED at 15.0 sigma"; the calibrated
  value is z = -0.86, i.e. the odd-harmonic amplitude sits BELOW the decoy median.
  The doubling must be withdrawn (13.0234 h, 1P). This is live in the public catalog.
- **(23444)**, adopted at 2P earlier today on "amp 0.411/0.439 >= 0.40": the unbiased
  Fourier peak-to-peak is 0.329/0.317, inside the ambiguous band. The doubling is not
  supported; the object must be declared ambiguous.

Nine 1P objects must instead become 2P (9955, 16650, 4728, 24362, 6640, 8593, 12011,
9174, 19932): reproduced odd harmonics and/or the elongation-corrected spin barrier
P_crit = 3.3 h sqrt(a/b) / sqrt(rho), which the flat 2.2 h cut under-applies.

Amplitude correlates with per-sector photometric error even under the unbiased
estimator (Spearman 0.226, p = 2.6e-5), and 11 of 13 discordant objects have their
larger amplitude in the noisier sector: variable dilution or a field star is present.

No period uncertainty is quoted anywhere. dP = P^2/(2T) gives dP/P > 10% for 26
objects and > 15% for 11; seven of those have no independent realization and can only
be published as lower limits.

### 2.4 ZTF channel: acceptable with restrictions

The strongest attack failed, and the refutation is worth publishing. The claim that
ZTF determines frequency only modulo 1 cycle/day was withdrawn by the referee after
calibration: injecting a known signal at f_det +- 1 c/d into the real residuals
(block-permuted by night, so correlated noise is preserved) gives a confusion rate of
**14/1680 = 0.83%**, with correct recovery in 97.7-98.6% of trials. Under the maximally
hostile prior that all 84 frequencies are daily aliases, ZTF would have produced the
claimed value for 0.70 objects out of 84.

What stands and must be fixed before submission:
1. **Baluev's premise is violated.** Nightly-binned chi2_red has median 2.45, above
   1.5 in 77/84 objects. The noise is correlated on the nightly scale, so the
   "FAP < 1e-8" bar is not the guarantee we present it as. Publish `nightly_chi2_red`
   per object and stop leading with Baluev FAP.
2. **The quoted FAP does not refer to the printed period.** 40/84 objects have
   FAP > 0.05 at the exact published value: ZTF detects a period *near* ours, and on a
   6.4 yr baseline a 0.5% offset is many peak widths. The honest sentence is "ZTF
   independently detects a period agreeing with ours to X%", not "FAP = Y at our period".
3. **(9891)** has TESS power 0.0577, below the canonical gate: promoted without a real
   TESS detection. Withdraw.
4. Nine objects retain a 5-20% alias-flip probability (3520, 6873, 6914, 8367, 9146,
   17725, 26161, 59522, 86402): publishable, but stating that the alias-family member
   is fixed by TESS, not by ZTF.
5. Comb candidates were never tested for 24/84 objects.

## 3. Correction plan

**Applied immediately to the public catalog** (these are live errors, not paper-only):
withdraw the (5024) doubling; withdraw (9891); re-declare (23444) ambiguous.

**Before writing the paper**: apply the 9 shape corrections; recompute every amplitude
with the unbiased Fourier estimator and publish it with its sigma; adopt the rule "the
amplitude rule fires only when A - 2 sigma_A exceeds the threshold"; add a period
uncertainty column; add a three-state novelty column (FIRST / FIRST RELIABLE /
CONFIRMATION) with the literature value; withdraw the 10 slow rotators, republishing
(28257) at 195.6 h and (5910) at 100.3 h.

**Resulting content**: about 209 objects, of which ~199 first determinations, 19 slow
rotators above 100 h and none above 200 h claimed as measured periods, plus the
methodological section on the crowded-field campaign, the null-calibrated gate, and
the TESS+ZTF channel with its measured limitations. That is a smaller paper than the
one we proposed, and one that survives review.
