# Review of ASN-0082

## REVISE

### Issue 1: Subspace preservation argument depends on unestablished depth equality between p and V-positions

**ASN-0082, The Ordinal Shift**: "By VD, all V-positions in the subspace share p's depth, so m ≥ 2 holds throughout."

**Problem**: VD guarantees uniform depth *among* V-positions: `(A v₁, v₂ ∈ dom(M(d)) : subspace(v₁) = subspace(v₂) = S ⟹ #v₁ = #v₂)`. This says every V-position in subspace S has the same depth d. It does not say d = #p. The insertion point p is not required to be in dom(M(d)), so VD's guarantee does not reach it. Without #v = #p, the inference "m ≥ 2 holds throughout" has no basis — the uniform depth d could be anything, and #p ≥ 2 tells us nothing about d.

Concretely: if V-positions have depth 5 and p has depth 2, the comparison v ≥ p crosses depth boundaries (T1 prefix rule), and δₙ = δ(n, #v) acts at depth 5 while p lives at depth 2. The postcondition I3 is still formally well-defined (shift uses #v, not #p), but the subspace preservation argument — which is the ASN's central structural claim — is unsound.

**Required**: Add a precondition to I3 requiring that #p equals the uniform depth of V-positions in subspace S when dom(M(d)) ∩ {v : subspace(v) = S} is non-empty. This simultaneously grounds the subspace preservation argument (d = #p ≥ 2 implies m ≥ 2) and ensures the v ≥ p comparison is between equal-length tumblers, giving it the clean "at or to the right of p" semantics the ASN assumes.

---

### Issue 2: VD's informal justification overstates T10a.1

**ASN-0082, Local Axioms**: "This is a structural consequence of how V-positions are allocated within a subspace: each subspace uses a single allocator whose sibling outputs have uniform length (T10a.1, ASN-0034)."

**Problem**: T10a.1 guarantees uniform length for one allocator's sibling stream. VD claims all V-positions in a subspace share the same depth — a stronger claim that requires the additional assumption that no child-spawning occurs within the element field for V-positions (i.e., the subspace uses a flat allocator with no `inc(·, k')` for k' > 0). If a child allocator were spawned within a subspace's element field, its outputs would have depth d + k' > d (by T10a.3), violating VD while satisfying T10a.1.

**Required**: Either (a) state VD purely as a modeling axiom without claiming it follows from T10a.1 alone, or (b) add the missing premise: "each subspace's element field uses a single flat allocator (sibling production by `inc(·, 0)` only, no child-spawning)." The citation "(T10a.1, ASN-0034)" should reflect which premises are actually used.

---

### Issue 3: VP cited for insertion point p, which is not a V-position

**ASN-0082, Post-Insertion Shift**: "p ∈ T with #p ≥ 2 and subspace(p) = S ≥ 1 (VP)"

**Problem**: VP states `(A v ∈ dom(M(d)) : subspace(v) = v₁ ≥ 1)` — a property of existing V-positions in the arrangement's domain. The insertion point p is not required to be in dom(M(d)). Citing VP to justify S ≥ 1 for p is incorrect; S ≥ 1 should stand as a direct precondition.

**Required**: Drop the "(VP)" citation. State "subspace(p) = S ≥ 1" as an independent precondition. VP is correctly applicable to V-positions v ∈ dom(M(d)) but not to the insertion point.

---

### Issue 4: Worked example omits mandatory boundary cases

**ASN-0082, Worked Example**: Only middle-insertion (p = [1, 3] into a five-element document) is verified.

**Problem**: Three boundary cases are not checked:
- *Insert at start*: p = [1, 1] (all content shifts; left region is empty; I3-L is vacuously true). Verify the shift covers all five positions.
- *Insert past end*: p = [1, 6] (no content shifts; shifted region is empty; I3 is vacuously true). Verify I3-L preserves all five positions.
- *Empty document*: dom(M(d)) = ∅ (both I3 and I3-L are vacuously true). Verify the postcondition is consistent.

Each is trivial to verify but confirms the universal quantifiers in I3 and I3-L handle degenerate domains correctly.

**Required**: Add at least one-line verifications for the insert-at-start and insert-past-end cases. Empty document can be noted in a sentence.

---

### Issue 5: Positivity attribution conflates VP and T4

**ASN-0082, The Ordinal Shift**: "since vₘ + n > 0 whenever vₘ ≥ 1 — the positivity required by VP"

**Problem**: VP concerns the subspace identifier v₁, not arbitrary components. The positivity of vₘ (the last component) follows from T4's positive-component constraint on element-field tumblers, not from VP. VP's preservation under shift follows from a different part of the argument: position 1 is copied from v (when m ≥ 2), and v₁ ≥ 1 by VP. The sentence conflates two distinct positivity guarantees — T4 for component vₘ, VP for the subspace identifier v₁.

**Required**: Replace "the positivity required by VP" with "the positive-component constraint (T4)" for the vₘ + n > 0 claim. Note separately that VP is preserved because shift copies position 1 from v when m ≥ 2.


## OUT_OF_SCOPE

### Topic 1: Span-level displacement properties
**Why out of scope**: The ASN specifies how individual V-position mappings change under insertion (I3). The derived question — how a V-space span (s, ℓ) transforms — is a new property. In particular, width preservation holds only when the width's action point equals the tumbler depth (ordinal displacements); for shallower action points, the width changes (its last component increases by n). This is a genuine span algebra extension, but it requires its own analysis and belongs in a follow-up.

### Topic 2: Vacated positions, new content, and domain closure
**Why out of scope**: I3 specifies where existing content goes but does not characterize what occupies the gap between p and shift(p, n) in M'(d), nor does it fully constrain dom(M'(d)). The new content placement and the biconditional form of frame conditions (nothing new appears in the left region) belong to the full insertion operation specification, not this ASN's shift property.

VERDICT: REVISE
