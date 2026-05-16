# Channel Assignment — ASN-0086 review-1

**Date:** 2026-05-16 14:06

## Issue 1: R0 proof has substantive gaps
Reason: The fix is internal — walk through the L-invariant chain explicitly using ASN-0043 invariants (L0, L1a, L1b, L1c, L3, L4 etc.), add the `dom(Σ.M) ≠ ∅` precondition inherited from L1a, and verify each invariant against the arbitrary `(F, G, K)` emission. All cited material is already present in ASN-0043's content.

## Issue 2: R4 proof overstates L14's actual content
Reason: The fix is internal — either restate R4 as scoped disjointness matching L14's actual form, or add an explicit setup hypothesis about s_C-residence and derive from L0 + T7. Both options use only existing ASN-0043 and ASN-0034 content.

## Issue 3: T7 cited by incorrect name
Reason: Pure citation correction — rename to `T7 (FirstElementFieldDistinction, ASN-0034)`. No external input needed.

## Issue 4: T_cat bootstrap problem in Emit_K precondition
Reason: The fix is internal — relaxing Emit_K's precondition to `K ∈ Endset` with `K ≠ ∅` is directly supported by L9 (TypeGhostPermission), which already establishes type endsets need not refer to stored content. The structural inconsistency can be resolved from existing foundation content; the deeper design question about dynamic catalog extension remains in the Open Questions section.

## Issue 5: R ∈ T_cat fails at empty initial state
Reason: The fix is internal — define `L_R` independently of T_cat membership (it is well-defined as ∅ when no retraction exists). The ASN already states R is "a name chosen by convention" via L9, and R6 is explicitly the substrate's own contribution, so design intent is not in question.

## Issue 6: L_K silently restricts to arity exactly 3, not arity ≥ 3
Reason: Pure notational correction — change `≥ 3` to `= 3` and clarify in prose. The set-comprehension pattern match already enforces arity 3; the fix is editorial.

## Issue 7: State-dependence of A, A_doc, A_rel not made explicit
Reason: Pure notational fix — add Σ subscripts or a single clarifying note. No external input needed.

## Issue 8: Worked sketch does not address coverage-extension nullification
Reason: The fix is internal — cite T10a.5 (CrossAllocatorIncomparability) from ASN-0034 to justify that no two distinct link addresses are in prefix relationship, or revise the example to use a span with coverage exactly `{a₁}`. Both options use existing foundation content.

## Issue 9: R6a proof treats coverage as state-dependent
Reason: Pure proof rewording — `coverage` is by definition a pure function on endset values; the proof simply needs to state that R2 preserves the endset value `G'` and `coverage(G')` is therefore the same set in both states. Internal editorial fix.

## Issue 10: Emit_K signature omits state transition
Reason: Pure signature notation — annotate Emit_K's signature to reflect state effect. No external input needed.

## Issue 11: Implicit assumption of s_C-resident content not stated as hypothesis
Reason: The fix is internal — add an explicit setup assumption that `(A a ∈ dom(Σ.C) :: subspace_I(a) = s_C)` at the top of the ASN. The hypothesis can be stated as a scoping condition for ASN-0086 without requiring external validation of its global truth.

## Issue 12: R5's META status and the gap from "no derived constraint" to permission
Reason: The fix is internal — replace the absence-of-constraint argument with positive citation of L4(c) (cross-subspace endsets permitted) and L13 (link addresses are valid span targets), both already present in ASN-0043. The positive-permission framing is stronger and entirely derivable.
