# Review of ASN-0085

## REVISE

### Issue 1: TA7a corollary stops one step short of the strand-model consequence

**ASN-0085, Arithmetic Homomorphism (Corollary)**: "ord(v) ⊕ w_ord ∈ S when all components of w_ord after its action point are positive. By the homomorphism, this governs the left-hand side — ord(v ⊕ w) ∈ S under the same condition."

**Problem**: The corollary establishes when `ord(v ⊕ w) ∈ S` but does not derive the equivalent statement about S8a-preservation of `v ⊕ w` — the property downstream ASNs actually need. The derivation is one step: components 1 through k of `v ⊕ w` are always positive (`r₁ = v₁ ≥ 1` by S8a and `w₁ = 0`; `r₂..r_{k-1} = v₂..v_{k-1} ≥ 1` by S8a; `r_k = v_k + w_k ≥ 2`), so the only components that can fail positivity are `r_{k+1}..r_m = w_{k+1}..w_m` — exactly the tail components tested for S-membership. Therefore `ord(v ⊕ w) ∈ S ⟺ v ⊕ w` satisfies S8a, under the given preconditions. This equivalence is the bridge from ordinal-domain results back to the strand model's invariants. The ASN's own stated purpose — "derive from this that TA7a's closure guarantees on S govern the S-membership of the result" — calls for this step.

**Required**: (a) Derive the equivalence `ord(v ⊕ w) ∈ S ⟺ v ⊕ w satisfies S8a` explicitly within the corollary, showing which components of `v ⊕ w` are unconditionally positive and which depend on the tail condition. (b) Promote the corollary to a named, labeled property (e.g., `OrdAddS8a`) with its own formal contract and an entry in the properties table — it has independent semantic content that downstream ASNs will cite.

### Issue 2: OrdShiftHom does not note S8a-preservation as a consequence

**ASN-0085, OrdShiftHom**: "ord(shift(v, n)) = shift(ord(v), n)"

**Problem**: For ordinal shifts, the displacement `δ(n, m) = [0, ..., 0, n]` has its action point at position m (the last component), so there are no tail components after the action point. The TA7a S-membership condition is vacuously satisfied: `ord(shift(v, n)) ∈ S` always holds (and therefore `shift(v, n)` always satisfies S8a). This is a free consequence of OrdShiftHom + the TA7a corollary, and it confirms that ordinal shifts unconditionally preserve V-position well-formedness — a fact the strand model relies on throughout. The ASN should state it rather than leave readers to derive it.

**Required**: Add a remark or postcondition to OrdShiftHom noting that the S-membership / S8a condition is vacuously satisfied for ordinal shifts, so `shift(v, n)` always satisfies S8a when `v` does.

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism
**Why out of scope**: The ASN acknowledges this in its Open Questions section. TA7a's conditional S-membership results for subtraction make this genuinely harder — the conditions under which `ord(v ⊖ w) = ord(v) ⊖ w_ord` holds and the S-membership of the result require a separate analysis.

### Topic 2: Order preservation through ord
**Why out of scope**: The property that `v₁ < v₂ ⟹ ord(v₁) < ord(v₂)` within the same subspace (and its converse) is a natural companion result, but it concerns the ordering structure of the decomposition rather than its arithmetic compatibility. This would be new territory.

VERDICT: REVISE
