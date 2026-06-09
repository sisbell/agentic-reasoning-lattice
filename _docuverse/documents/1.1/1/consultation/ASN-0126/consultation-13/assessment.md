# Channel Assignment — ASN-0126 review-13

**Date:** 2026-06-08 23:43

## Issue 1: Gate soundness (P4) proven, gate completeness never stated
Reason: The realizability lemma is a structural assembly of facts the note already imports — R0 (fresh-address emission) and `a_emit` totality transfer to `π(Σ)` via the projection argument, and gate satisfaction `(0)∧(i)∧(ii)` for a conforming triple holds by the definition of `Sh-conf` and `K.λ_sh`. Showing the ungated `K.λ` step is in fact a `K.λ_sh` step for conforming triples is pure internal reasoning over the note's own definitions and inherited lemmas; no design-intent or implementation evidence is required.
