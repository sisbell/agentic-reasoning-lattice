# Channel Assignment — ASN-0047 review-79

**Date:** 2026-05-17 13:56

## Issue 1: Broken reference to "rejection model fixed in the preamble above"
Reason: Internal fix. The intended semantics (transitions with unsatisfied preconditions do not enter the transition set) is standard operational semantics and can be added as an explicit subsection or the references rephrased to cite preconditions directly — no design intent or implementation evidence needed.

## Issue 2: Broken reference to "Scope and base-liveness analysis above"
Reason: Internal fix. The substantive content (ghost-base versioning admissibility) already exists inline in the K.δ table; only the section heading or cross-reference text needs adjustment.

## Issue 3: Broken reference to "Reconciliation with ASN-0043's L1c"
Reason: Internal fix. The reconciliation content (L1c as structural producibility, not state) is already discussed in the Allocator hierarchy section; only the named paragraph header or rephrased pointer is needed.

## Issue 4: Broken reference to "Per-state arrangement shape (D-SEQ★)"
Reason: Internal fix. The forward-reference structure exists; only the named pointer needs to be added at the Elementary transitions section or removed from the D-SEQ★ derivation.

## Issue 5: T_link undefined
Reason: Internal fix. T_link can be defined symmetrically to T_elem (e.g., `{a ∈ T : IsElement(a) ∧ fields(a).E₁ = s_L}`) or the reference rephrased — no external evidence required.

## Issue 6: K.μ~ Case 2 labeling misleads — it is a sub-argument, not a third case
Reason: Internal fix. The decomposition logic is fully present in the ASN; only the case-numbering organization needs restructuring (fold Case 2 into Case 1's justification, or relabel as a sub-argument).

## Issue 7: P3 retained as "orienting prose only" with no proof obligation
Reason: Internal fix. The choice of whether to remove P3 entirely (P3★ suffices) or reduce it to a single inline sentence is an authorial organizational decision; no external evidence needed.

## Issue 8: K.μ⁻ amendment paragraph is redundant with K.μ⁻'s own postcondition
Reason: Internal fix. Removing the redundant prose or folding it into K.μ⁻'s definition is purely an editorial decision; the per-subspace structure is already explicit in K.μ⁻'s effect clause and case analysis.

## Issue 9: SubAllocatorAxiom's "namespace property" obscures the freshness chain
Reason: Internal fix. The substantive content of the axiom is already justified in Design provenance; the restructuring (split into three sub-axioms vs. add a dispatch table) is purely about formal presentation of derivation paths in K.α and K.λ.

## Issue 10: The "Two scopes of T10a's domain" predicate definitions are load-bearing but tucked inside K.δ
Reason: Internal fix. The predicate definitions exist and are correct; only their placement in the document structure needs adjustment (promote to top-level notation section).

## Issue 11: Cross-document disjointness lemma Case B sub-case enumeration is informal
Reason: Internal fix. The proof can be reworked using T10a's allocator structure (from ASN-0034) plus S7d's allocator discipline; the partition or coverage lemma is derivable from the foundation invariants already invoked.

## Issue 12: Notational inconsistency — dom_C(M(d)) vs V_{s_C}(d)
Reason: Internal fix. Pure notation choice — either unify on one symbol or add an explicit equivalence note.

## Issue 13: "Three discharge paths" is referenced as a named catalogue but not headlined
Reason: Internal fix. The three paths are already enumerated in the K.δ table; only a headlined paragraph naming the catalogue is needed to resolve downstream citations.

## Issue 14: K.μ~ contract's bijection equation under-determines π without explicit acknowledgement of consequence
Reason: Internal fix. When two V-positions v₁, v₂ share an I-address `a` (under S5), any π satisfying the bijection equation produces M'(d) with the same function values (both witnesses yield M'(d)(v₁) = M'(d)(v₂) = a). The proof that all valid π yield identical M'(d) is derivable from the equation `M'(d)(π(v)) = M(d)(v)` plus the bijectivity of π — no external evidence required.

## Issue 15: P7a derivation's "fresh-content branch" leans on J0 but J0's introduction lacks proof of P7a sufficiency
Reason: Internal fix. P7a is an existential `(E d :: (a, d) ∈ R)`; J0 supplies some d and J1★ records the pair. The clarification is purely textual — one sentence acknowledging that the existential is closed regardless of which d J0 selects.
