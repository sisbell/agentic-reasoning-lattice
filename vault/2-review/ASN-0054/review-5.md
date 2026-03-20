# Review of ASN-0054

## REVISE

### Issue 1: A1a formal statement admits an incorrect reading

**ASN-0054, Depth Fixity (A1a):** "While V(d) ≠ ∅, the depth L(d) is fixed: no valid composite transition can change it."

**Problem**: "While V(d) ≠ ∅" is ambiguous between two readings:

(a) *Pre-state condition*: "If V(d) ≠ ∅ in the pre-state, no valid composite can change L(d)." This is **false**. A composite that first empties V(d) via K.μ⁻ (removing all positions), then repopulates via K.μ⁺ at a different depth, is valid — A0 holds in the post-state (the new V(d) is contiguous), S8-depth holds at every intermediate state (V(d) = ∅ satisfies S8-depth vacuously, then the new positions have uniform depth). Yet L(d) changes across the composite.

(b) *Continuous condition*: "If V(d) ≠ ∅ at every intermediate state within the composite, then L(d) is unchanged." This is **correct**: each K.μ⁺ into a non-empty V(d) must match the existing depth (S8-depth precondition), K.μ⁻ of a subset preserves the remaining depth, and K.μ~ preserves the domain.

The follow-up sentence ("Only after complete deletion...") resolves the ambiguity in favor of reading (b), but the formal claim taken alone admits reading (a). Since A1a is a named property that downstream ASNs will cite, the standalone statement must be unambiguous.

**Required**: Restate A1a as a formal proposition making the continuous-non-emptiness condition explicit:

"For any valid composite transition Σ = Σ₀ → Σ₁ → ··· → Σₙ = Σ′, if V(d) ≠ ∅ at every intermediate state Σᵢ, then L(Σ′, d) = L(Σ, d)."

The corollary — that depth can only change by passing through V(d) = ∅ — then follows directly rather than hanging as a prose caveat.

## OUT_OF_SCOPE

### Topic 1: Canonical decomposition–enfilade correspondence

The canonical decomposition (a finite sequence of span pairs) is the abstract characterization of what the enfilade stores concretely. A future ASN should establish when and how an enfilade faithfully represents the canonical decomposition — particularly the correspondence between tree structure and run boundaries, and whether the enfilade's merging/splitting invariants enforce A0 as a byproduct.

**Why out of scope**: The enfilade is a data-structure concern; this ASN establishes abstract arrangement properties independent of representation.

### Topic 2: Incremental decomposition maintenance

The operation-effect sections describe structural changes qualitatively ("at most one run splits," "at most three runs split") but do not establish whether these local descriptions are sufficient for O(affected runs) incremental update of the canonical decomposition, or whether global recomputation is needed.

**Why out of scope**: This is an algorithmic concern beyond the specification-level structural properties established here.

VERDICT: REVISE
