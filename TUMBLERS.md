# Tumbling asteroids (non-principal-axis rotation)

Most asteroids spin like a wheel, around one fixed axis. A **tumbler** rotates around an axis
that itself precesses: the light curve is the product of two incommensurate periods and never
repeats exactly. Tumbling is where an asteroid's collision and spin-down history is written,
and it is structurally invisible to sparse ground-based photometry -- which is why TESS's
uninterrupted 27-day stare is the right instrument and why so few tumblers are known.

**Method** (METHODOLOGY §8): a two-frequency Fourier fit in the Pravec et al. (2005)
formulation, with the combination terms (j·f1 ± k·f2) that separate genuine two-axis rotation
from two unrelated signals. Thresholds are calibrated empirically with LCDB-listed tumblers as
positive controls run through the identical pipeline; every candidate must survive a
common-fundamental (harmonic) veto, momentum-dump comb separation, an eigen-systematics
de-comb test, and reproduction of the second frequency across independent sectors.

The same calibrated run recovered **4 known LCDB tumblers** — (1839), (1506), (2045) Peking,
(2000) — which validates the pipeline on the very dataset that produced the candidates below.

## New candidates

### (3345) — rotation 187.7 h + precession 264.9 h
The published LCDB rotation (~187 h) plus a NEW second frequency at 264.9 h (ratio 0.71,
non-harmonic). Beat-envelope modulation is visible by eye; a single-period fit leaves 137 mmag
of coherent residual, the two-period fit drops it to 65 mmag and leaves nothing folding at
either period.

<img src="figs/tumbler_3345.png" width="100%">

### (7887) — rotation 111.7 h + second period 87.2 h
A rotation period first determined by this survey ([reasoning](objects/7887.md)). The second
frequency reproduces to **0.7%** across two independent sectors (87.24 / 86.67 h), passes the
harmonic veto in both, and survives the de-comb with a 1-5% power change.

<img src="figs/tumbler_7887.png" width="100%">

### (6162) — rotation 167.7 h + second period 135.3 h
Also a first-determination rotator of this survey ([reasoning](objects/6162.md)). Second
frequency reproduced to **0.9%** (136.63 / 135.34 h), harmonic veto passed in both sectors,
de-comb survived.

<img src="figs/tumbler_6162.png" width="100%">

## Status

These are **candidates**, reported separately from the rotation catalog (they become catalog
claims only after independent confirmation, e.g. a physical two-axis model fit or a second
epoch). The falling residual rms is necessary but not sufficient: a two-period model has more
freedom, which is why the bars above lean on reproduction across sectors and on the
combination terms, not on the fit improvement alone.
