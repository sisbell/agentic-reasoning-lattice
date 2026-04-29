# Revision Categorization — ASN-0067 review-1

**Date:** 2026-03-21 15:50

## Issue 1: ContentReference span denotation is unsatisfiable over fixed-depth V-positions
Category: INTERNAL
Reason: The fix replaces ⟦σ⟧ ⊆ dom(M(d_s)) with a depth-restricted containment using definitions already present in ASN-0034 (T12, shift) and ASN-0036 (S8-depth). The review even suggests the exact reformulation.

## Issue 2: D-MIN not verified; ValidInsertionPosition for empty documents is incomplete
Category: INTERNAL
Reason: D-MIN is defined in ASN-0036 and the constraint v = [S, 1, ..., 1] follows directly from it. The non-empty preservation argument follows from the COPY construction (C4) and existing D-MIN definition.

## Issue 3: C3 claims "every foundational invariant" but verifies a subset
Category: INTERNAL
Reason: Each missing invariant (P6, P7, P7a, P8, J1', D-CTG, D-MIN) is defined in ASN-0036/ASN-0047, and the one-line derivations follow trivially from C0 (C'=C), E'=E, R'⊇R, and C2. No external evidence needed.

## Issue 4: No elementary decomposition for ValidComposite
Category: INTERNAL
Reason: The elementary transitions K.μ⁺, K.μ~, K.ρ and their preconditions are defined in ASN-0047. Constructing the decomposition and verifying intermediate preconditions is a proof exercise over existing definitions.

## Issue 5: C13 makes an unsupported concurrency claim
Category: INTERNAL
Reason: The fix is editorial: separate the derivable sequential-correctness claim (from ValidComposite) from the concurrency/visibility claim, and flag the latter as requiring a concurrency model not yet in the foundation. No design-intent or implementation evidence needed for this restructuring.

## Issue 6: Resolution applies M11/M12 to a restriction without justification
Category: INTERNAL
Reason: The step-down argument — that restrictions of M(d_s) inherit S2, S8-fin, and S8-depth, which are the only properties M11/M12 depend on — is derivable entirely from ASN-0058's proof structure and ASN-0036's invariant definitions.
