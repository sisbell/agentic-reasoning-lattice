# Channel Assignment — ASN-0058 review-25

**Date:** 2026-05-14 20:03

## Issue 1: M7 necessity proof opens with OrdShiftHom but does not establish #v₁ ≥ 2
Reason: The fix is a citation chain entirely within ASN-0036 (β₁ ∈ B → v₁ ∈ dom(M(d)) → S8a → #v₁ ≥ 2). All required axioms are already present and cited elsewhere in this ASN.

## Issue 2: M12 partition argument relies on the same implicit S8a chain
Reason: Same internal citation chain as Issue 1, plus a textual note distinguishing OrdinalShiftBase (k=0) from OrdShiftHom (k≥1). All material is in ASN-0036 and the OrdinalShiftBase convention already established here.

## Issue 3: M6(d) forward-references M16 instead of the cleaner M16a
Reason: Pure reorganization — move M16a before M6 and have M6(d)/M16 cite it. The proof of M16a is already written into M16's body; only ordering changes.

## Issue 4: C0a's handling of the partial-projection case is scattered and confusing
Reason: Restructuring an existing proof into two explicit cases (#t ≥ m, #t < m). All mathematical content (T1(i), T1(ii)) is already cited in the proof.

## Issue 5: B1's `v₁ ≥ 1` guard is redundant under standing preconditions
Reason: Definition cleanup using S8a (already a standing precondition for M2). No external evidence needed.

## Issue 6: M11 termination phrasing "bounded below by 1 for non-empty M(d)" is misleading
Reason: Pure phrasing correction — replace lower-bound argument with well-foundedness on the strictly-decreasing |B|.

## Issue 7: M16's transitive T10a conformance for element-level allocators relies on an implicit system assumption
Reason: The fix requires checking what ASN-0034's T10a allocator-tree clause and ASN-0036's S7d formally establish about descendant allocators, then either citing precisely or adding a precondition. This is a cross-ASN foundational question — neither design intent (Nelson) nor implementation evidence (Gregory) decides which formal axiom carries the obligation.

## Issue 8: Notation `t + k` overloads tumbler-shift with the integer `c + j` inside M-aux
Reason: One-sentence notational clarification to the OrdinalShiftBase convention. Self-contained.

## Issue 9: C1a's "extension of M11/M12" reuses M7f, which is stated for M(d) rather than arbitrary partial functions
Reason: Adding a clarifying sentence noting M7f's proof depends only on B1–B3 (already established structurally in this ASN). No external evidence needed.
