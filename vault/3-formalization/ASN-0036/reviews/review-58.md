# Cross-cutting Review — ASN-0036 (cycle 1)

*2026-04-12 21:38*

I've read the foundation statements and ASN-0036 in full. Here are the cross-property issues I found.

### S8a precondition chain cites S3/S7b but derives nothing from them

**Foundation**: S3 (Referential integrity), S7b (Element-level I-addresses), T4 (HierarchicalParsing)
**ASN**: S8a (V-position well-formedness), formal contract and proof — "by S3 (Referential integrity), every V-reference resolves — M(d)(v) ∈ dom(Σ.C) — and by S7b (Element-level I-addresses), every address in dom(Σ.C) is element-level — zeros(M(d)(v)) = 3 — so the target address has all four fields present. A V-position v is the element field E extracted from the document-scoped address"
**Issue**: The proof chains through S3 → S7b → T4 to establish that the *I-address* M(d)(v) is element-level with positive field components. It then asserts "A V-position v is the element field E extracted from the document-scoped address" — but this identity is the axiom itself, not a consequence of S3/S7b/T4. S3 and S7b constrain the *codomain* of M(d) (the I-addresses V-positions map to), not the *domain* (the V-positions themselves). The V-position [1, 3] and the I-address it maps to, say [N, 0, U, 0, D, 0, 1, 42], are different mathematical objects in different parts of the tumbler space. The postconditions (zeros(v) = 0, v₁ ≥ 1, v > 0) follow from the axiom + T4 alone — S3 and S7b are non-load-bearing. Listing them as preconditions creates a phantom dependency chain: downstream properties citing S8a (D-MIN, D-SEQ, S8, ValidInsertionPosition) would transitively depend on S3/S7b through S8a, when no such dependency exists.
**What needs resolving**: S8a's formal contract should remove S3 and S7b from its precondition list (retaining only T4), or the proof should clearly separate the motivational narrative (why the axiom is reasonable) from the formal derivation (axiom + T4 → postconditions).

---

### S9 frame condition is strictly stronger than the established invariant

**Foundation**: S0 (Content immutability)
**ASN**: S9 (Two-stream separation), frame condition — "Frame: Σ.C is preserved across all state transitions; in particular, arrangement-modifying transitions cannot alter C."
**Issue**: The invariant establishes that *existing entries* of C survive: `(A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`. The frame condition says "Σ.C is preserved across all state transitions," which under T8's own convention ("Read-only operations preserve the allocated set *exactly*; allocation transitions *extend* the set") means dom(Σ'.C) = dom(Σ.C) and all values unchanged — i.e., C is completely invariant. But INSERT-type transitions simultaneously create content (extending dom(C)) and modify arrangements (adding V-positions to dom(M(d))). Under INSERT, dom(Σ'.C) ⊃ dom(Σ.C) while the S9 invariant holds. The frame's claim "arrangement-modifying transitions cannot alter C" is false for these transitions: INSERT is arrangement-modifying and does alter C (by extending its domain). A TLA+ formalizer following the frame would write `UNCHANGED C`, which prevents content creation — an incorrect formalization. The invariant itself is S0 with a vacuous antecedent (the proof acknowledges this), so the frame should match S0's scope: existing entries are preserved, but dom(C) may grow.
**What needs resolving**: The frame condition should distinguish between preserving existing entries (what S9 establishes) and preserving C entirely (what the frame claims). Following T8's convention: "Arrangement-only transitions preserve Σ.C exactly; transitions that also create content extend dom(Σ.C) while preserving all existing entries."

---

### D-MIN postconditions cite dependencies absent from preconditions

**Foundation**: D-CTG (VContiguity), S8-fin (FiniteArrangement), S8-vdepth (MinimalVPositionDepth)
**ASN**: D-MIN (VMinimumPosition), formal contract — "Postconditions: Combined with D-CTG, S8-fin, S8-depth, and S8-vdepth (for m ≥ 2), V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n} for some finite n ≥ 1."
**Issue**: D-MIN's preconditions list V_S(d) ≠ ∅, S8-depth, and S8a. The postcondition brings in D-CTG, S8-fin, and S8-vdepth — three properties not in the precondition list — to derive the full sequential characterization V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}. This characterization is exactly D-SEQ's statement, which D-SEQ derives separately with a clean precondition list that includes all five dependencies. D-MIN's contract violates the convention that postconditions follow from the stated preconditions: a formalizer verifying D-MIN's preconditions (S8-depth, S8a) without also verifying D-CTG and S8-fin would not be able to derive the "combined" postcondition, yet the contract structure implies they could. The "Combined with" qualifier documents the additional dependencies inline, but the formal contract's precondition/postcondition split is inconsistent.
**What needs resolving**: Either add D-CTG, S8-fin, and S8-vdepth to D-MIN's precondition list, or remove the sequential characterization from D-MIN's postconditions and let D-SEQ own it exclusively. The latter is cleaner — D-MIN's own contribution is the minimum-position axiom, not the full characterization.
