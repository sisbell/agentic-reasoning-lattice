This is a strong, unusually faithful digest. I checked every "forced/conventional" label, every Green claim against the evidence, and the load-bearing chains (I0/I1/I1a, AD/AM, DR/C2-C3, S3/P-tgt, BH4), and found no misreads, no ungrounded source-level claims, no altitude slips, and no missing load-bearing commitment. A few sections deserve explicit credit because they do work the note itself doesn't:

- The **Q8 pushback** is correct and valuable: it sides with the code-exploration half of the evidence (no backend type registry; QUOTE_TYPE/MARGIN_TYPE are client-side VSpecs) over the KB-synthesis half, and honestly labels the registry-subspace isolation as the digest's own invention. It correctly downgrades the note's "precedent is exact" overclaim.
- The **dedup-cannot-be-sharded-by-home** insight (partition by I0-class, never by home, or I1a breaks across homes) and the **K-surface-emitted ∧ atomic-check-deposit** decomposition of the idem-uniqueness guarantee are sound additions beyond the note.
- The **C2/C3 born-nullified precision** (DR vacates only C3; self-emit retraction still self-nullifies via C2) is exactly right and resists the easy "no born-nullified tuples" overstatement.
- **Forced/conventional** discipline checks out throughout (registry pre-seeding forced, names/slot-direction conventional, "fix *a* direction" forced / "*which*" conventional, BH4 idem=⊥ forced).

Revision list (both non-blocking):

1. **[SHARPENING]** *Implementation approaches → Age-staleness (BH4):* "Age is the home chain's frontier minus the tuple's chain index" is off by one. The note's `age(a) = f_d^Σ − 1 − j` (the count of deposits that *postdate* the event), so "frontier − index" overstates age by one. Either give the exact formula or phrase it conceptually ("how far the frontier has advanced past the tuple's slot") so the prose doesn't assert a wrong equation. The surrounding design content — ordinal, home-relative, no clock, read straight off per-home append order — is correct, which is why this is a precision fix, not a build error.

2. **[SHARPENING]** *Implementation approaches (nullification) / Decisions for the builder:* The digest rightly says don't build a separate sterilization-avoidance/born-nullified *check* (it falls out of `A_K = L_K \ nullified`). Add a one-line pointer that this is distinct from OQ3 — whether to *also* harden the shape gate (make non-unit `G` non-conformant for R specifically) as defense-in-depth — which the note leaves genuinely open to a successor. A builder weighing belt-and-suspenders gate hardening should know that lever is deferred, not settled, and is not the same as the dead born-nullified check.

VERDICT: CONVERGED
