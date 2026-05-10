# Review of ASN-0040

## REVISE

### Issue 1: B6 biconditional is false — condition (i) is not necessary for T4 preservation

**ASN-0040, B6 (Valid Depth), necessity proof for condition (i)**: "If p ends in zero, then inc(p, 1) appends component 1, yielding a tumbler [..., 0, 1] where the final zero of p and the appended 1 parse as a field separator followed by a new field — the child inhabits a different hierarchical level than intended, and p's malformed structure propagates."

**Problem**: The claim that a T4 violation in the parent always propagates to the stream is false. Counter-example:

Let `p = [1, 0]`, `d = 1`. The parent violates T4 (ends in zero: T4a requires `t_{#t} ≠ 0`). Yet every element of `S([1, 0], 1)` satisfies T4:

- `c₁ = inc([1, 0], 1) = [1, 0, 1]` — one zero at position 2, no adjacent zeros, `t₁ = 1 > 0`, `t₃ = 1 > 0`. Satisfies T4.
- `c₂ = inc([1, 0, 1], 0) = [1, 0, 2]` — satisfies T4.
- All `cₙ = [1, 0, n]` for `n ≥ 1` satisfy T4.

The formal contract claims `(A n ≥ 1 : cₙ ∈ S(p, d) satisfies T4) ⟺ (i) ∧ (ii) ∧ (iii)`. The counter-example gives LHS = true, RHS = false (since (i) fails). The biconditional is false.

The mechanism: when `p` ends in zero and `d = 1`, the trailing zero of `p` becomes an interior field separator in the stream elements (which append `n > 0` after it), so the T4 violation is "healed" by the stream construction. The proof's claim that "the T4 violation of p is not repaired by the increment; it is transmitted to the output" is incorrect for this case.

Note: condition (i) IS necessary for B7 (namespace disjointness) — `S([1, 0], 1)` is identical to `S([1], 2)`, so allowing baptism under the invalid parent would create overlapping namespaces. But this is a B7 argument, not a T4-preservation argument.

**Required**: Either (a) restate B6 as a sufficient condition, dropping the necessity proof and replacing the biconditional `⟺` with an implication `⟸` in the formal contract, while noting separately that condition (i) is required for B7; or (b) replace the necessity argument for (i) with the correct one: without (i), the stream `S(p, d)` may coincide with a valid stream `S(p', d')`, collapsing namespace disjointness — which makes (i) necessary for the system, though not for T4 preservation of the stream in isolation.

---

### Issue 2: B1 proof invokes B7 without checking its preconditions

**ASN-0040, B1 (Contiguous Prefix), inductive step, "All other namespaces" case**: "By B7 (Namespace Disjointness), S(p₀, d₀) ∩ S(p, d) = ∅, so a ∉ S(p, d)."

**Problem**: B1 is universally quantified over all `(p, d)` with `p ∈ T` and `d ≥ 1`. B7 requires both pairs to satisfy B6 — specifically, both parents must satisfy T4 and both depths must satisfy `d ∈ {1, 2}` with the zeros bound. The "all other namespaces" case invokes B7 for arbitrary `(p, d)`, including invalid pairs where B7's preconditions are not met.

Two sub-cases are unaddressed:

(a) **Streams with no T4-valid elements**: When `(p, d)` violates B6 in a way that makes every stream element violate T4 (e.g., `p` starts with zero, or `d ≥ 3`, or `p` has adjacent zeros), then by B10 no stream element can be in `Σ.B`, so `children(Σ.B, p, d) = ∅` — B1 holds vacuously. This case needs an explicit argument via B10.

(b) **Shadow streams identical to valid streams**: When `p` ends in zero and `d = 1`, the stream `S(p, 1)` can be identical to `S(p', 2)` where `p'` is `p` with the trailing zero removed (and `p'` satisfies T4). In this case `children(B, p, 1) = children(B, p', 2)`, so B1 for the valid namespace implies B1 for the shadow. This case also needs an explicit argument.

The conclusion is almost certainly correct — B1 holds for all `(p, d)` — but the proof as written has a gap where B7 is invoked outside its domain.

**Required**: Add a paragraph to the "all other namespaces" case that handles non-B6 pairs explicitly: either through B10 (no T4-valid elements in the stream, so children is empty) or through stream identity with a valid namespace (B1 inherited).

---

### Issue 3: Finiteness of B₀ not explicitly required

**ASN-0040, Σ.B definition**: "Initially Σ.B contains some non-empty seed set B₀ ⊆ T of root addresses established at system genesis"

**Problem**: The definition does not require `B₀` to be finite. However, the well-definedness proof for `next(B, p, d)` states "B ⊆ T finite" as a precondition. If `B₀` is infinite and every namespace's children set is a contiguous prefix of a stream (B1), `children(B, p, d)` could be infinite (the entire stream) — making `max(children)` undefined (the stream has no maximum element under T1, being strictly increasing without bound).

The next function's formal contract explicitly assumes finiteness: "B ⊆ T finite." Since `B` starts as `B₀` and grows by one element per baptism, `B₀` finite implies `B` finite at every reachable state.

**Required**: Add "B₀ is finite" to the Σ.B definition or to B₀ conf. (SeedConformance). This makes the finiteness precondition of `next` derivable rather than implicit.


## OUT_OF_SCOPE

### Topic 1: Formal bridge between Σ.B and T8's allocated set
**Why out of scope**: The ASN notes that B0 is "the state-level reading of T8 (AllocationPermanence)" but does not formally establish that Σ.B is the allocated set referenced by T8, T9, and T10a. Formalizing this correspondence — and showing that the baptism mechanism is the unique realization of the allocation axioms — would require a bridging argument connecting the algebraic allocator model (ASN-0034) with the state-based registry model (this ASN). This is new connective tissue, not an error in the current ASN.

VERDICT: REVISE
