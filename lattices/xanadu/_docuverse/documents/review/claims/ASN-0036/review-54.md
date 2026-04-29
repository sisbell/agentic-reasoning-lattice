# Cone Review — ASN-0036/ValidInsertionPosition (cycle 3)

*2026-04-13 18:12*

### S8-depth postcondition 3 presupposes field-structure preservation by OrdinalShift without establishing it

**Foundation**: OrdinalShift (ShiftDefinition, ASN-0034) — prefix rule `shift(a, k)ᵢ = aᵢ` for `i < #a`; T4 (HierarchicalParsing, ASN-0034) — field structure determined by zero-valued separator positions
**ASN**: S8-depth postcondition 3 — "E₁(a + k) = E₁(a) — … S7c then gives δ ≥ 2, so E₁ is at a position less than #a; OrdinalShift's prefix rule copies it unchanged."
**Issue**: The notation `E₁(a + k)` denotes the first component of `(a + k)`'s element field — the fourth field as parsed by T4. This requires `a + k` to be a four-field element-level address with the element field starting at the same absolute position as in `a`. The proof establishes that `a` is element-level (via S3 → S7b at k = 0), and that the value at E₁'s absolute position p is preserved by OrdinalShift (since p < #a). But `E₁(a + k)` refers to position p only if `a + k` has the same field structure as `a` — i.e., the three zero-valued field separators occupy the same positions. This follows from OrdinalShift: the separators are at positions < #a and are preserved by the prefix rule; the last position goes from `a_{#a} > 0` to `a_{#a} + k > 0`, so no zero is introduced or removed; therefore `zeros(a + k) = zeros(a) = 3` and the field decomposition is structurally identical. This intermediate step — OrdinalShift preserves T4 field-separator positions, hence four-field parseability — is never stated, yet it is the bridge that makes `E₁(a + k)` well-defined. (An alternative route exists: by the run definition, `a + k = M(d)(v + k)`, so S3 gives `a + k ∈ dom(Σ.C)`, S7b gives `zeros(a + k) = 3` independently; but this route is also not stated for k ≥ 1.)
**What needs resolving**: The proof must establish that `a + k` is parseable as a four-field address before using `E₁(a + k)`. Either state the field-structure preservation lemma (OrdinalShift on an element-level address preserves zero positions and hence T4 parseability), or apply the S3 → S7b chain at each k in the run (using `a + k = M(d)(v + k)` and S3's applicability to every `v + k ∈ dom(M(d))`).

---

### ValidInsertionPosition S8a-consistency proof narrows scope to "text-subspace" when argument and preconditions are subspace-universal

**Foundation**: S8a (V-position well-formedness) — postcondition `zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0` for all V-positions; remark: "Link-subspace V-positions satisfy the same `zeros(v) = 0` and `v > 0` constraints as text-subspace positions"
**ASN**: ValidInsertionPosition S8a consistency — "For text-subspace positions (S ≥ 1), every valid position [S, 1, ..., 1 + j] has all components strictly positive (S ≥ 1, intermediate components are 1, last component is 1 + j ≥ 1), so zeros(v) = 0 and v > 0 — satisfying S8a."
**Issue**: The proof's label says "For text-subspace positions (S ≥ 1)," but S ≥ 1 is the universal condition on all subspace identifiers — it is the precondition stated in ValidInsertionPosition's own formal contract ("S is a subspace identifier (S ≥ 1)"), not a text-subspace-specific condition. The text subspace has S = 1; the link subspace has S = 2; both satisfy S ≥ 1. The mathematical argument is correct for all subspaces — it uses only S ≥ 1 and the structure [S, 1, ..., 1 + j]. But the label "text-subspace" creates an apparent scope restriction that contradicts both the formal contract's universal precondition and S8a's explicit remark that link-subspace positions satisfy the same constraints. A formalizer reading the label might believe link-subspace positions require a separate consistency proof.
**What needs resolving**: The S8a consistency section should either drop the "text-subspace" qualifier (the argument is universal over S ≥ 1) or explicitly note that the same argument covers all subspaces including the link subspace.

## Result

Cone not converged after 3 cycles.

*Elapsed: 5118s*
