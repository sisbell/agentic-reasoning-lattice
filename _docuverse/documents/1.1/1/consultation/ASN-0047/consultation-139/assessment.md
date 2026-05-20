# Channel Assignment — ASN-0047 review-139

**Date:** 2026-05-20 00:09

## Issue 1: P4 → P4★ supersession status under "stale" usage in coupling section
Reason: The wp-style derivation pattern is established in the ASN, P4★'s definition and J1★'s scoping are already present, and the design choice "preserve P4★" is documented. Re-running the wp computation mechanically yields J1★ — derivable internally.

## Issue 2: K.μ⁺_L's omitted strict-extension verification
Reason: The verification `v_ℓ ∉ dom(M(d))` is already in the body prose with its full subspace-decomposition argument; the fix is just lifting it into the effect clause or citing it there. Internal.

## Issue 3: K.μ~ existence condition's circular-looking dependency
Reason: The inductive separation between CL-UNIQ at Σ (hypothesis) and CL-UNIQ at Σ' (preserved) is already correct in the proof body; the fix is exposing it at the definition site. Internal.

## Issue 4: K.μ⁻ precondition `dom(M(d)) ≠ ∅` placement
Reason: The explicit precondition and the "Per-subspace consequence" derivation are both in the ASN; the fix is clarifying which is load-bearing. Internal.

## Issue 5: J0 transient-failure handling vs J0's "design intent" framing
Reason: ValidComposite★ already scopes coupling constraints to composite boundaries; the fix is making J0's temporal scope as explicit as P4★/P4a/P7a's Class (b) treatment. Internal.

## Issue 6: Worked example traces don't verify L11a explicitly
Reason: Both discharge routes (SubAllocatorAxiom.FirstEmission and T10a GlobalUniqueness on the inc chain) are already specified in the ASN; the fix is applying them explicitly in the worked example steps. Internal.

## Issue 7: K.μ~ singleton case necessity argument leaves a gap
Reason: The argument is correct; the fix is restructuring the quantifier order ("for any admissible π" rather than "the identity permutation"). The required premises (Step D, CL-UNIQ, subspace preservation) are all in the ASN. Internal.
