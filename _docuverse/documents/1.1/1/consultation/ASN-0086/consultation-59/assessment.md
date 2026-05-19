# Channel Assignment — ASN-0086 review-59

**Date:** 2026-05-19 09:29

## Issue 1: R7a proof's confused content-store monotonicity reference
Reason: The reviewer has specified the exact replacement text; the correct citation is established in ASN-0036's own invariant catalog and the ASN already cites S0/S1 elsewhere. Derivable from the ASN alone.

## Issue 2: R7a's conformance scope is incomplete
Reason: The reviewer has specified the broadened scope text; S0/S1 are the content-store invariants already cited in the Frame conditions, and the conformance scope's extension is mechanical. Derivable from the ASN alone.

## Issue 3: Reference to non-foundation ASN-0047
Reason: The reviewer has specified the exact replacement text; removing the disclaimer-style mention and substituting positive scoping is purely editorial. Derivable from the ASN alone.

## Issue 4: Substrate emission primitive lacks formal status
Reason: The fix is structural — assign labels, add table rows, update internal citations. The content of both the emission primitive and the witness-only L1c reading is already fully articulated in the Setup section. Derivable from the ASN alone.

## Issue 5: R7a lacks concrete example
Reason: Constructing an illustrative composite ↝-step (document allocation + link emission) uses only mechanics already established in R0, R7a, and the Worked Sketch's existing setup. Derivable from the ASN alone.

## Issue 6: Inconsistent variable naming in R0a Stage 2 induction
Reason: Pure variable renaming to unify naming conventions within a single induction step. Derivable from the ASN alone.

## Issue 7: R6c-Corollary's induction is too brief
Reason: The two-case decomposition (→-step covered by R6c; arrangement-modifying step preserving A_K pointwise) is already justified in the Definition of BroadExtension and the surrounding text; expansion is mechanical. Derivable from the ASN alone.

## Issue 8: Definition of nullified — implicit `a ∈ A_rel^Σ` constraint
Reason: The motivation is already present in R4 Consequence (b) (retraction is well-typed; only A_rel addresses are valid Nullify arguments) and R5 Consequence (a) (classifier-tuple pattern for document removal). The fix transcribes existing rationale into the Definition's neighborhood. Derivable from the ASN alone.

## Issue 9: R6b is essentially "by definition" — claim status unclear
Reason: The simpler resolution (re-label as "Consequence of Definition (Nullified)") is purely a status correction reflecting the proof's tautological structure already visible in the proof body. Derivable from the ASN alone.

## Issue 10: T_ghost referenced but not formally defined
Reason: The reviewer specifies both options (formal Definition or explicit phrase substitution); either is a self-contained editorial fix using terminology already in scope (`dom(Σ.C)`, `dom(Σ.L)`, tumbler space `T`). Derivable from the ASN alone.

## Issue 11: Emit_K signature missing K parameter
Reason: The reviewer offers two clear resolutions (make K explicit, or declare K a type-index); both are signature-presentation fixes consistent with how Nullify already reads `Emit_R` as type-indexed. Derivable from the ASN alone.
