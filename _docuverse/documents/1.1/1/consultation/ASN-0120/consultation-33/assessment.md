# Channel Assignment — ASN-0120 review-33

**Date:** 2026-06-11 19:09

## Issue 1: "names a vacuous interval" contradicts T12
Reason: Internal fix — the contradiction is between the ASN's own boundary enumeration and T12(b)'s guarantee that intervals contain their start, both already cited in the ASN. The reword ("contains no active position") follows from `ρ`'s active-position filter as defined in ML1; no design intent or implementation evidence is involved.

## Issue 2: The composite is written with the atomic-transition arrow
Reason: Internal fix — a pure notation correction governed by conventions the ASN already invokes (SequentialTransitionAxiom for `→`, ValidCompositeAmended for `→*`, both ASN-0047). The intermediate state is already reasoned about explicitly; only the arrow needs changing.

## Issue 3: The ρ/resolve agreement is asserted, not derived
Reason: Internal fix — the missing derivation rests entirely on ASN-0058's decomposition conditions (B1, B3) and the definition of `ρ`, all formal material already in the dependency cone; the review even sketches both inclusions. Neither Nelson's intent nor udanax-green behavior bears on a proof-obligation discharge between two abstract definitions.
