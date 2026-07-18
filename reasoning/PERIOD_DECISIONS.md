# Period-decision log — reasoning for contested / doubtful objects

Purpose: for every asteroid where the adopted period required a judgment call (doubling,
comb-vs-real, contamination, instrument conflict), record WHY we adopted it and HOW to
justify it to a referee. The catalog (`verified_catalog.csv`) holds the decision; this
file holds the reasoning. Append a new entry whenever an object needs more than a
mechanical pipeline pass. Format per entry: adopted value, the doubt, the evidence, the
verdict + confidence, caveats.

Standing conventions this log applies (see PIPELINE.md for the code):
- 1P vs 2P by FOLDED amplitude: > 0.40 mag -> 2P (elongated body, two humps/rotation).
- SPIN-BARRIER physics override: a rubble pile (D > ~150 m) cannot spin faster than
  ~2.3 h; a sub-2.3 h photometric period on a multi-km body MUST be the 2nd harmonic
  -> P_rot = 2 x P_phot. This overrides a low folded amplitude.
- Momentum-dump comb: periods within ~3% of 328.8/n h are suspect; the SysRem de-comb
  (DIA) is the tool that separates comb from real (a real period survives, a comb
  artifact collapses). ZTF (no shared TESS systematics) recovering the same period is
  independent proof of reality.
- Slow rotators: the de-comb over-subtracts them (their signal overlaps the systematics
  band), so an inconclusive de-comb drop is NOT a kill; the decisive test is multi-sector
  phase-fold COHERENCE (real rotation folds to one shape across epochs; systematics do not).

---

## (5793) Ringuelet — Beltwide6 — CONFIRMED, 3.0396 h, 2P
**Doubt:** the photometric period is 1.52 h (huge power 0.34-0.36, FAP 1e-113 / ~0, over
47 and 393 cycles in s70/s71). 1.52 h looks alarming.
**Reasoning:** SBDB gives D = 8.068 km (H=12.62, albedo 0.306). An 8 km rubble pile has a
cohesionless spin barrier at ~2.3 h; 1.52 h is far below it and is physically impossible
for a body this size (centrifugal > self-gravity -> disruption). Therefore 1.52 h is the
2nd harmonic (two brightness maxima per rotation) and the true rotation is 2 x 1.52 =
3.0396 h. Folded amp 0.19 (mildly elongated, near-symmetric minima) is consistent with a
low-elongation 2P body seen near-equator; the doubling here is forced by PHYSICS, not
amplitude.
**Verdict:** 2P / 3.0396 h, high confidence. **This is not a 1.52 h fast rotator** — do
not revert to the photometric value.

## (2024) — Beltwide2 — CONFIRMED, 167.52 h, 2P  [promoted from CANDIDATE 2026-07-18]
**Doubt:** base period ~83.3 h is robust, but 1P (83.3 h) vs 2P (166.6 h) looked
unresolved because TESS folded amp (~0.56) argues 2P while ZTF shows ZERO power at 166.6 h
(read as 1P). Both candidates also sit ~1.3% from comb teeth (82.2 h = 328.8/4,
164.4 h = 328.8/2).
**Reasoning:** (a) 83.3 h SURVIVES the de-comb in both sectors (drop 10-16%, far below the
50% kill line) and is independently recovered by ZTF -> real rotation, NOT a comb artifact
near n=4. (b) Folded amp is 0.55-0.73 mag in all 8 measurements (raw/decomb x 2 sectors x
2 periods) -> categorical 2P by the amplitude rule. (c) KEY: for a symmetric double-humped
(180-deg-periodic) curve, Fourier power at the FUNDAMENTAL 1/166.6 h is ZERO by symmetry
-- all power is at the 2nd harmonic 1/83.3 h. So "ZTF sees zero power at 166.6 h" is the
EXPECTED signature of a near-symmetric 2P body, NOT 1P evidence; the original TESS-vs-ZTF
"conflict" was a misread. TESS's own clean sector (s71) shows the same (near-symmetric
minima, weak fundamental power). s70 shows genuine decomb-stable minima asymmetry (20-26%)
that actively confirms 2P.
**Verdict:** CONFIRMED 2P / 167.52 h (user-approved promotion 2026-07-18). Precise value
from combined fine LS: fundamental 83.76 h (pw 0.51) x 2 = 167.52 h; the 2P region itself
is near-zero power (0.04), the symmetric-double-hump signature. Moderate-high confidence.
Caveats: only ~3.5 cycles of 167.5 h per sector (few-cycle); asymmetry evidence leans on
the contaminated s70. NEW super-slow rotator (>100 h).

## (3396) — Beltwide6 — CONFIRMED, 61.963 h, 1P
**Doubt:** flags gap-alias-risk:62 h (s42 has a 62 h data gap = the period) and
incoherent-sectors; and the de-comb drops power 25-41% at 62 h with high systematics R2
(0.76 in s27) -- looked partly instrumental.
**Reasoning:** (a) NOT a gap alias: window-function power at 61.96 h is ~0.002 (~zero) in
all sectors, so the sampling/gap does not manufacture the period. (b) NOT a comb tooth
(5.8% from the nearest, n=5 at 65.76 h). (c) DECISIVE: the 4 sectors phase-fold COHERENTLY
at 62 h -- all 6 pair correlations are +0.82 to +0.93 -- proving body-fixed rotation
(systematics are not phase-coherent across epochs). (d) The 25-41% de-comb drop is the
known slow-rotator artifact: a 62 h signal overlaps the scattered-light systematics band,
so the de-comb over-subtracts real signal (a validated clean slow rotator like 14720 loses
<1%, but that one sits away from the band). Amp 0.041 -> 1P.
**Verdict:** 1P / 61.963 h, confirmed. The de-comb "inconclusive" is a slow-rotator
artifact, overruled by 4-sector phase coherence. FAP 1e-108 to 1e-120.

## (3127) — Beltwide3 — KILLED (was CONFIRMED)
**Doubt:** adopted 15.6536 h, 2 sectors, but heavily comb-adjacent and previously killed.
**Reasoning:** (a) 15.6536 h sits on the momentum-dump comb tooth n=21 (328.8/21 =
15.657 h, 0.02% off). (b) The DIA collapses the s17 (confirming-sector) peak 63% (R2=0.47)
-> the period IS the systematics. (c) The 2nd sector s70 is contaminated and weak, no
independent confirm. (d) Removing 15.65 h and re-searching finds only noise (s17 residual
FAP 0.63) or the NEXT comb tooth (s70 hops 9.42 h=n34, 22.21 h=n15) -- there is no real
period underneath, it is comb all the way down. (e) Prior ZTF "support" cannot separate
real-vs-comb when the period sits exactly on a tooth.
**Verdict:** KILLED (user decision 2026-07-18). Momentum-dump artifact, not rotation.
Plot: review_3127.png.

## (1285) — Beltwide1 — CONFIRMED, 15.24 h, 1P
**Doubt:** user flagged S91 as contaminated (mag-7 star-crossing spike + faint dips to
-2.5 mag); the DIA had never run on it (it fell through the old comb/slow-only trigger and
the range>3 mag sector-skip).
**Reasoning:** (a) S91 contamination is real but localized; the census bright-clip removes
the 62 bad points and S91 still detects 7.62 h = P/2 (FAP ~0 over 69 cycles) -- a
star-crossing is a 1-2 day event, it cannot fake a 69-cycle coherent period. (b) S42 is
clean: 15.24 h, FAP 1e-123, 0 contamination. (c) The SysRem DIA (run after this case
prompted the new contamination trigger): S42 survives at 15.24 h (drop -2%), S91 survives
at 7.62 h (drop +13%) -> astrophysical, not systematics. (d) Folded amp 0.09 (S42) / 0.24
(S91), both < 0.40 -> 1P.
**Verdict:** 1P / 15.24 h, confirmed, 2-sector (S42 fundamental + S91 harmonic).
Disagrees with the published LCDB 20.3 h (a genuine literature disagreement, not a
confirmation). This case motivated the contamination-triggered DIA rule (see PIPELINE.md).

---
# Backfill: batch review-flags and resolved conflicts (2026-07-18)

## Spin-barrier physics-forced 2P (sub-2.3h photometric period on a multi-km body)
- **(50545) Beltwide8 — CONFIRMED 2P/3.182h.** P_phot=1.591h in 2 sectors (FAP 6e-55,
  1.5e-231), not a comb tooth. Body ~8-17km (H=12.72) -> 1.591h sub-barrier -> P_rot=2x=3.182h.
  Folded amp 0.138 low (mildly elongated); doubling forced by physics not amplitude. Same
  logic as 5793.
- **(2124) Beltwide8 — CANDIDATE 2P/3.1227h.** Single sector s22 (-> CANDIDATE ceiling),
  P_phot=1.5613h (FAP 5e-153), ~15km body sub-barrier -> 2P/3.1227h. Single-sector so not
  promotable without a 2nd epoch.
- **(4671) Beltwide7 — CANDIDATE 2P/3.833h.** Single sector s70, LS 1.916h strong, H=13.03
  (D~5-15km) sub-barrier -> physics-forced 2P/3.833h. Single-sector cap.

## 1P/2P amplitude calls
- **(15991) Beltwide8 — CONFIRMED 2P/61.02h.** 3 sectors agree fundamental ~30.5h, folded
  amp 0.60>0.40 -> 2P. Slow-ish. CAVEAT: s70 heavily contaminated (raw range 5 mag); split-
  half + amplitude checks hold up but eyeball s70 fold before publishing.
- **(5074) Beltwide8 — CONFIRMED 1P/6.331h.** Pipeline reported 2P/12.662h (amp 0.43) but
  audit-tool recompute gives folded amp 0.24 -> 1P/6.331h; the higher pipeline amp was
  inflated by the noisy sector-dropped s72 (err 0.22-0.27 vs 0.06 in the clean s57). Adopt 1P.
- **(2465) Beltwide8 — CANDIDATE 1P/16.4918h.** Single sector s37 (CANDIDATE ceiling),
  folded amp 0.359 -- BORDERLINE just under 0.40, ridge single-min so 1P held. Watch: a 2nd
  sector could flip it to 2P.
- **(2538) Beltwide5 — CONFIRMED, OPEN 1P/2P.** 2 sectors agree 26.71h. Folded amp 0.55>0.40
  (house rule -> 2P) BUT the verify agent kept 1P because the 2P-fundamental FAP=1.0 and the
  fold is a single asymmetric hump. Genuine amplitude-vs-morphology conflict -- STILL OPEN,
  user's 1P (26.71h) vs 2P (53.4h) call. Currently recorded 1P/26.711h.
- **(5203) Beltwide6 — CONFIRMED 2P/6.934h.** s42+s44 nail P_phot=3.467h (FAP~0, agree
  0.003%), folded amp 0.48>0.40 -> 2P. DIA: survives at 3.467h in s42/s44 (the s43 kill in
  the first rescan was one contaminated sector; survival-first rule keeps it). Real.
- **(6808) Beltwide3 — CONFIRMED 2P/7.996h.** base 4.0h doubled, consecutive s42/s43 agree
  0.44%. DIA: survives at 3.998h=P/2 in both sectors (the 8h-alias "kill" in the first
  rescan was a weak-alias false positive fixed by the survival-first rule). Real.

## Under-called by a pipeline bug (now fixed)
- **(5051) Beltwide8 — CONFIRMED 1P/7.2598h.** 3 sectors (s18/s35/s91) recover ~7.26h at
  extreme FAP (1e-29..1e-55, combined 2e-94). The census flag logic MISLABELED LS power as
  folded amplitude and scored it a weak CANDIDATE; it is a rock-solid 3-sector CONFIRMED.
  (Upstream amp-column bug flagged for fixing.)

## Super-slow rotators (>100h) -- sidereal-anchored, comb-checked
- **(2024) Beltwide2 — 167.52h/2P** (see main entry above).
- **(18070) Phocaea — CONFIRMED 2P/111.7h.** Multi-year sidereal confirmation (PAB epoch,
  c=-1.1 non-zero -> body-fixed, not comb) vs the 109.6h comb line. Re-pass's refine wanted
  216h; sidereal anchor wins -> catalog 111.7h stands.
- **(13388) Beltwide4 — CONFIRMED 2P/305.594h.** Super-slow #3, 3 sectors comb-free, base
  ~152-154h in all three; sidereal P_sid=307.0h Theta<=0.47. Refine wanted 153h(1P); sidereal
  resolves to 305.6h(2P) -> catalog stands.
- **(1887) Beltwide1 — CONFIRMED 2P/70.18h.** Arbitration: matches Durech 70.17h inversion;
  P_sid=70.11h Theta=0.366. Refine wanted 35h(1P); literature+sidereal anchor -> 70.18h stands.
- **(5185) Beltwide7 — CONFIRMED 1P/102.3h.** RECOVERED from a wrong KILL: NOT single-sector
  (3 sectors s42/s43/s62 agree ~101-102h, FAP~0). Prior 204.594h/2P and prior single-sector
  KILL both wrong; folded amp <0.40 and only 1/3 sectors pass minima test -> 1P/102.3h.
- **(16785) Beltwide5 — CANDIDATE 1P/139.885h.** s101 (139.28h) + s38 (140.49h) agree 0.9%,
  decomb survived, not a comb line. Slow-rotator CANDIDATE (2nd sector detrend-dependent);
  needs a 3rd epoch to confirm.

## Comb-alias corrections
- **(2863) Themis — CORRECTED to 1P/5.251h.** Prior 10.501h was a comb-alias artifact from
  the contaminated s72 (164.4h = 328.8/2). 3 clean sectors s43/s44/s91 agree 5.251h (FAP
  1e-140..1e-294). Same failure mode as 3127 but with clean sectors that recover the real period.
- **(4597) Beltwide7 — CONFIRMED 1P/4.44h.** 2 sectors agree 4.44h; the competing 8.873h/2P
  entry was a doubling artifact (folded amp 0.11-0.16<0.40, no asymmetry). Deduped + resolved.
- **(5814) Beltwide7 — CANDIDATE 2P/9.4098h.** Single sector s50, folded amp 0.551>0.40 with a
  real half-cycle asymmetry -> 2P (not the "identical minima" trap). Single-sector cap.
