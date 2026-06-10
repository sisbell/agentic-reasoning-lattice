# Channel Assignment — ASN-0126 review-108

**Date:** 2026-06-10 14:11

## Issue 1: The projected-path R6c transfer is proven twice, and the earlier occurrence cites the later one as its license
Reason: The fix is purely structural — extract the duplicated argument into a named bridge clause (B3) and cite it from both sites. The proof material already exists verbatim in the ASN's two inline derivations, built only from ProjectionBridge and B1; no design intent or implementation evidence bears on where a lemma is stated.

## Issue 2: Forward-deferral accretion onto Range sterilization, plus contract-internal meta-prose
Reason: The fix is editorial — deleting meta-prose, trimming forward pointers to a single site, and restricting a postcondition to what the ASN already proves holds at Σ'. Every retained claim is already established elsewhere in the note; nothing new must be sourced from design intent or the implementation.

## Issue 3: P6's inductive step establishes the fresh tuple's conjuncts at the wrong state
Reason: The half-step gap closes using propositions the ASN already proves — P1 (or the step's own registry frame condition) carries registration from Σ to Σ', and P4 carries the Sh-conf verdict, exactly as the proof already does for persisting tuples. The fix is internal application of existing results.

## Issue 4: The "strictly stronger" wp claim is unscoped and contradicted per-substrate by the note's own configuration sweep
Reason: The scoping fix is derivable from the ASN's own configuration sweep in Range sterilization, which already establishes that C2 and C3 hold at every emit under the unregistered and Unary configurations and that both strictness witnesses presuppose Binary/Multi registration. No external channel is needed to restate the claim with its correct quantification domain.
