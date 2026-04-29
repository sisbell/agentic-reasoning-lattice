# Review of ASN-0036

## REVISE

### Issue 1: S5 within-document sharing claim unproven
**ASN-0036, S5 (Unrestricted sharing)**: "The same I-address may appear in the ranges of multiple arrangements, and at multiple V-positions within a single arrangement."
**Problem**: The formal proof constructs a witness with N+1 documents, each mapping one V-position to the shared address. This demonstrates unbounded cross-document sharing but does not address the separate English claim about within-document sharing — that a single `M(d)` can map arbitrarily many distinct V-positions to the same I-address. The formal statement's `(d,v)` pair count subsumes both types, but the proof only exercises the cross-document case (one pair per document, N+1 documents). No witness shows `M(d) = {v₁ ↦ a, v₂ ↦ a, ..., v_{N+1} ↦ a}`.
**Required**: Add a within-document witness. For any N, construct `M(d) = {v₁ ↦ a, ..., v_{N+1} ↦ a}` for distinct V-positions `vᵢ` with `a ∈ dom(C)`. S2 holds — each `vᵢ` maps to exactly one address (they all map to `a`). S3 holds — `a ∈ dom(C)`. This takes two sentences and completes the proof for both claims in the English preamble.

### Issue 2: S8 partition proof restricted to depth 2
**ASN-0036, S8 (Finite span decomposition)**: "by S8-depth, all V-positions in a subspace share the same tumbler depth, so positions are of the form `s.x` for varying ordinal `x`. For distinct ordinals `x₁ < x₂`, the intervals `[s.x₁, s.(x₁+1))` and `[s.x₂, s.(x₂+1))` are disjoint because `s.(x₁+1) ≤ s.x₂` (since `x₁ + 1 ≤ x₂`)."
**Problem**: S8-depth states that V-positions within a subspace share the same tumbler depth but does not fix that depth to 2. The phrasing "positions are of the form `s.x` for varying ordinal `x`" commits to depth 2, and the disjointness argument (`x₁ + 1 ≤ x₂`) depends on positions differing at a single ordinal component. For uniform depth `d > 2`, V-positions can differ at any of the `d − 1` non-subspace components, and the single-ordinal argument does not apply. The counterexample (mixed depths `s.3` and `s.3.1`) correctly shows why S8-depth is *needed*, but the positive argument only covers the `d = 2` case.
**Required**: Either (a) generalize the disjointness argument: for uniform depth `d`, the interval `[v, v+1)` — where `+1` increments only position `d` — contains no depth-`d` tumbler other than `v` itself (any depth-`d` tumbler in the interval must agree with `v` on positions `1` through `d−1`, since divergence at any earlier position would place it outside the interval; at position `d`, the natural-number constraint `v_d ≤ t_d < v_d + 1` forces `t_d = v_d`); or (b) strengthen S8-depth to commit to depth 2 for the text subspace, consistent with the implementation evidence already cited.

## OUT_OF_SCOPE

### Topic 1: Contiguity of dom(M(d))
**Why out of scope**: S8 proves that runs partition `dom(M(d))`, but whether `dom(M(d))` must be gap-free — every V-position between the minimum and maximum occupied — is not addressed. Gaps may arise after deletion. Whether re-numbering is required, and what that implies for V-position stability, is an operation-level concern belonging to a future ASN.

### Topic 2: Link-subspace reconciliation with T4 and S7b
**Why out of scope**: The S8a remark correctly identifies that link-subspace V-positions (`v₁ = 0`) produce adjacent zeros in full addresses, violating T4's syntactic constraints. S7b's universal claim `(A a ∈ dom(C) :: zeros(a) = 3)` will also need qualification when link content enters `dom(C)`. Both tensions are properly deferred to a future ASN on links.

VERDICT: REVISE
