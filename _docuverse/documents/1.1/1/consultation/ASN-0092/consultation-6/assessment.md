# Revision Categorization — ASN-0067 review-6

**Date:** 2026-03-21 18:01

## Issue 1: C4 (Displacement) applies shift to non-target subspaces
Category: INTERNAL
Reason: The construction (B') is correct — B_other leaves non-target subspaces unchanged. The fix is restricting C4's quantifier and updating C5/C7a derivations to match the existing construction. All needed information is in the ASN.

## Issue 2: Effects frame condition too narrow and ambiguously scoped
Category: INTERNAL
Reason: B_other already handles all non-S subspaces correctly in the composition. The fix is editorial — making the effects summary match B' by broadening the frame condition from `p₁ < 1` to `subspace(p) ≠ S`.

## Issue 3: ValidInsertionPosition undefined when N = 0
Category: INTERNAL
Reason: The ASN already contains both cases (N > 0 and N = 0) in separate sentences. The fix is restructuring the definition to avoid referencing undefined v₀, using information already present.

## Issue 4: Resolution applies M11/M12 to a restriction without justification
Category: INTERNAL
Reason: The ASN already identifies the inherited properties (S2, S8-fin, S8-depth). The fix adds an explicit argument that M11/M12 proofs depend only on these properties, which is derivable from the proof structure in ASN-0058.

## Issue 5: Inconsistent property labels (INV vs POST)
Category: INTERNAL
Reason: The foundation ASNs establish the INV/POST labeling convention. C0, C6, C11, C13 are COPY-specific postconditions, not universal state invariants. The fix is a relabeling using conventions already defined in the foundation.
