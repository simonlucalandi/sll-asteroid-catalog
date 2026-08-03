# Tumbling asteroids (non-principal-axis rotation)

Most asteroids spin like a wheel, around one fixed axis. A **tumbler** rotates around an axis
that itself precesses: the light curve is the product of two incommensurate periods and never
repeats exactly. Tumbling is where an asteroid's collision and spin-down history is written,
and it is structurally invisible to sparse ground-based photometry, which is why TESS's
uninterrupted 27-day stare is the right instrument and why so few tumblers are known.

**Method** (METHODOLOGY §8): a two-frequency Fourier fit in the Pravec et al. (2005)
formulation, with the combination terms (j·f1 ± k·f2) that separate genuine two-axis rotation
from two unrelated signals. Thresholds are calibrated empirically with LCDB-listed tumblers as
positive controls run through the identical pipeline; every candidate must survive a
common-fundamental (harmonic) veto, momentum-dump comb separation, an eigen-systematics
de-comb test, and reproduction of the second frequency across independent sectors. The
screen's selection function is measured by injection-recovery, not assumed: it only detects
second components comparable in amplitude to the primary, and it is deliberately blind near
low-order period ratios, where a real tumbler cannot be told apart from a harmonic-rich
single rotator (the full map is in METHODOLOGY §8).

## Proof that the pipeline works: recovered known tumblers

Run blind over 1,024 objects containing 134 LCDB-listed tumblers as positive controls, the
screen flags known tumblers at 2.9x the rate of everything else (13.4% vs 5.1%, Fisher exact
p = 0.0006). The cleanest recovery is **(2000) Herschel**, which carries the highest-confidence
tumbling code LCDB assigns (T+): our rotation period matches the published 133.6 h to 1%, and
the second period reproduces across two independent sectors to 0.3%. The chart below is the
whole argument in one figure: a generous single-period model (4 harmonics) cannot follow the
curve, the two-period Pravec fit can, and the residual of the single-period fit folds
coherently at the second period while the two-period residual folds flat.

<img src="figs/tumbler_known_2000.png" width="100%">

Two more recoveries, same test, same bars:

- **(2045) Peking**, LCDB code T: the only object in the whole run that survives the strictest
  operating point (1% false-positive rate) in both blind runs.
  <img src="figs/tumbler_known_2045.png" width="100%">
- **(1839) Ragazza**, LCDB code T: the strongest combination-term signature of the run
  (F_comb 616), the physical fingerprint Pravec's method relies on.
  <img src="figs/tumbler_known_1839.png" width="100%">

## New candidates

### (3345), rotation 187.7 h + precession 264.9 h
The published LCDB rotation (~187 h) plus a NEW second frequency at 264.9 h (ratio 0.71,
non-harmonic). Beat-envelope modulation is visible by eye; a single-period fit leaves 137 mmag
of coherent residual, the two-period fit drops it to 65 mmag and leaves nothing folding at
either period. In the 2026-08-03 re-run of the full chain with a doubled control set, (3345)
was the only object outside the controls to re-emerge past every bar, without being looked for.

<img src="figs/tumbler_3345.png" width="100%">

### (7887), rotation 111.7 h + second period 87.2 h
A rotation period first determined by this survey ([reasoning](objects/7887.md)). The second
frequency reproduces to **0.7%** across two independent sectors (87.24 / 86.67 h), passes the
harmonic veto in both, and survives the de-comb with a 1-5% power change.

<img src="figs/tumbler_7887.png" width="100%">

### (6162), rotation 167.7 h + second period 135.3 h
Also a first-determination rotator of this survey ([reasoning](objects/6162.md)). Second
frequency reproduced to **0.9%** (136.63 / 135.34 h), harmonic veto passed in both sectors,
de-comb survived.

<img src="figs/tumbler_6162.png" width="100%">

## Status

These are **candidates**, reported separately from the rotation catalog (they become catalog
claims only after independent confirmation, e.g. a physical two-axis model fit or a second
epoch). The falling residual rms is necessary but not sufficient: a two-period model has more
freedom, which is why the bars above lean on reproduction across sectors and on the
combination terms, not on the fit improvement alone. All three candidates sit at non-rational
period ratios (0.71, 0.78, 0.81), inside the sensitive part of the measured selection
function; a candidate at a low-order rational ratio would not be claimable at all.
