# Review of ASN-0082

## REVISE

### Issue 1: I3 formalizes arrival but not departure — shift semantics incomplete

**ASN-0082, Post-Insertion Shift**: "Content at or beyond p shifts forward by n ordinal positions."

**Problem**: The prose says "shifts" but the formal postcondition I3 only establishes that content *arrives* at shifted positions — it does not establish that content *departs* from original positions. The postconditions I3, I3-L, I3-X, and I3-D collectively leave original positions `v ≥ p` in subspace S unconstrained: no clause assigns them a value, but no clause excludes them from `dom(M'(d))` either.

For contiguous arrangements this is harmless — every original position is either in the gap or coincides with a shifted output from below. But the ASN defines `M(d)` as a partial function (`T ⇀ T`), permitting sparse arrangements. In the sparse case, an original position `v ≥ p` can exist with no `u ∈ dom(M(d))` satisfying `shift(u, n) = v`, leaving `v` unaddressed by any clause. An implementation that retains `M'(d)(v) = M(d)(v)` alongside `M'(d)(shift(v, n)) = M(d)(v)` would satisfy all four postconditions while duplicating content — violating the shift semantics.

Concrete example: `dom(M(d)) = {[1,3], [1,7]}`, insert at `p = [1,3]`, `n = 2`. I3 gives `M'(d)([1,5]) = M(d)([1,3])` and `M'(d)([1,9]) = M(d)([1,7])`. Position `[1,7]` is not `< p`, not a shifted output (since `shift⁻¹([1,7]) = [1,5] ∉ dom(M(d))`), not in the gap `[[1,3], [1,5])`, and not in another subspace. No clause constrains it. Retaining `M'(d)([1,7]) = M(d)([1,7])` duplicates content at both `[1,7]` and `[1,9]`.

The gap analysis compounds this: it identifies only `[p, shift(p, n))` as "unaddressed," missing the broader class of original positions outside the gap that are not shifted outputs.

**Required**: Add a vacating postcondition. For example:

> **I3-V** (vacating): `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d)))`

This states that original positions in the shifted region are removed from `dom(M'(d))` unless they happen to coincide with a shifted output of another position. The gap analysis should then identify *all* unspecified positions — both the gap and the vacated originals — not only `[p, shift(p, n))`.

### Issue 2: Cited foundations missing from Statement Registry

**ASN-0082, Statement Registry**

**Problem**: Two foundation properties are directly cited in arguments but absent from the registry:

- **T12 (SpanWellDefinedness, ASN-0034)**: cited in "We verify that σ' is a well-formed span (T12, ASN-0034)" when checking the shifted span's well-formedness.
- **T4 (HierarchicalParsing, ASN-0034)**: cited in "the positive-component constraint (T4) is maintained because vₘ + n > 0 whenever vₘ ≥ 1 (T4 guarantees all element-field components are positive)."

**Required**: Add both to the registry as cited dependencies from ASN-0034.

## OUT_OF_SCOPE

### Topic 1: Span behavior when a span straddles the insertion point
**Why out of scope**: A span with `start(σ) < p < reach(σ)` is split by the insertion — the left part preserved by I3-L, the right part shifted by I3. Characterizing this split (via S4) and reassembly is an operation-level concern for the INSERT ASN, not for the displacement property itself.

### Topic 2: Injectivity preservation of M(d)
**Why out of scope**: Whether `M(d)` being injective (each I-address mapped at most once) implies `M'(d)` is also injective is an arrangement-level invariant. The shift property preserves values and uses an injective relocation (TS2), so the pieces are in place, but the full injectivity argument requires the gap-filling postcondition from the INSERT ASN.

VERDICT: REVISE
