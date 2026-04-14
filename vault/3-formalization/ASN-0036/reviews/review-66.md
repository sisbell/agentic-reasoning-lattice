# Cone Review — ASN-0036/S8 (cycle 2)

*2026-04-14 16:56*

### T3 and T0 omitted from S8's foundation dependency enumeration

**Foundation**: T3 (CanonicalRepresentation: `a = b ⟺ #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`); T0 (CarrierSetDefinition: components ∈ ℕ)
**ASN**: S8 formal preconditions: `"dom(M(d)) ⊆ T (Σ.M(d)), providing the carrier-set membership required by OrdinalShift, T1, T5, and T10"`
**Issue**: S8's formal preconditions enumerate four foundation properties that require carrier-set membership. S8's proof invokes two additional ASN-0034 properties not in this list. (1) T3 is invoked in the within-subspace uniqueness proof, j=m case: `"t = v by T3 (CanonicalRepresentation, ASN-0034) — contradicting t ≠ v."` T3 characterizes equality on T and requires both arguments to be in T. (2) T0 is invoked for ℕ-discreteness: `"Since tumbler components are natural numbers (T0, ASN-0034), v_m ≤ t_m < v_m + 1 forces t_m = v_m."` Establishing that components are ℕ-valued (and therefore discrete) requires the tumbler to be in T per T0's definition. A consumer checking whether the carrier-set precondition `dom(M(d)) ⊆ T` is sufficient for the proof would see four listed recipients but find six in the proof text.
**What needs resolving**: S8's formal preconditions should enumerate all foundation properties from ASN-0034 that are invoked on V-positions in the proof, including T3 and T0, or use a blanket statement covering all ASN-0034 properties.

---

### S8-depth postcondition 3: separator preservation argument covers only zero-introduction, not zero-removal

**Foundation**: OrdinalShift (last-component increment: `shift(v, n)ₘ = vₘ + n`; prefix preservation: `shift(v, n)ᵢ = vᵢ` for `i < m`)
**ASN**: S8-depth Postcondition 3 proof: `"OrdinalShift's prefix rule preserves all positions before #a — including the three zero-valued field separators — and the last position satisfies a_{#a} + k > 0, so no zero is introduced; the separators of a + k therefore occupy the same positions as those of a"`
**Issue**: The conclusion that `zeros(a + k) = zeros(a) = 3` — and hence that the four-field structure and separator positions are preserved — requires two directions: (i) no zero is introduced at position `#a`, and (ii) no existing zero is removed at position `#a`. The proof explicitly argues direction (i): `a_{#a} + k > 0`. Direction (ii) requires `a_{#a} ≠ 0` in the original address — otherwise OrdinalShift converts a zero at position `#a` to a nonzero value `k`, reducing `zeros(a + k)` from 3 to 2 and destroying the four-field structure. The proof provides the ingredients for establishing `a_{#a} ≠ 0`: the phrase "including the three zero-valued field separators" places all three zeros at positions `< #a`, and `zeros(a) = 3` (from S7b) means these three account for every zero in `a`, so position `#a` cannot be zero. But this implication (`all three zeros at positions < #a` ∧ `zeros(a) = 3` → `a_{#a} ≠ 0`) is never stated. A formalizer tracing the argument would find a gap between S7b's zero count, S7c's depth bound (which places separators before `#a`), and the conclusion that the shift cannot alter the separator count.
**What needs resolving**: The postcondition 3 proof should explicitly establish that `a_{#a} ≠ 0` — i.e., that position `#a` is not among the three separator positions — before concluding that the separator structure is invariant under OrdinalShift. The step is: since `zeros(a) = 3` and all three zeros are at positions `< #a` (by δ ≥ 2 from S7c), position `#a` is non-zero, so the shift neither introduces nor removes a zero.
