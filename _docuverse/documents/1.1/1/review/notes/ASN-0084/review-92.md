# Review of ASN-0084

## REVISE

### Issue 1: Merge asserts a run without establishing S8-cons, while Split proves it

**ASN-0084, Correspondence-Run Decomposition Transformation, "Merge"**: "Two runs `(v₁, a₁, n₁)` and `(v₂, a₂, n₂)` … are *mergeable* when `v₂ = v₁ + n₁` … and `a₂ = a₁ + n₁` …. The merged run is `(v₁, a₁, n₁ + n₂)`."

**Problem**: Calling `(v₁, a₁, n₁ + n₂)` a *run* asserts S8-cons — `M(d)(v₁ + k) = a₁ + k` for all `0 ≤ k < n₁ + n₂` — but no derivation is given. The companion operation **Split** in the immediately preceding paragraph supplies its full S8-cons derivation (using Extended Associativity at the junction). The asymmetry is the gap: the junction index `k = n₁` (where `v₁ + n₁ = v₂` and, by I-adjacency, `a₁ + n₁ = a₂`) is exactly the non-trivial step, and it is the one omitted. The worked examples then promote merged runs into stated canonical partitions (4-cut example: "Merge: `([1,6], B, 3)`" → "Canonical partition: `{… ([1,6], B, 3)}`"), so an unproven operation underwrites a stated result.

**Required**: Either include the one-line junction derivation for Merge (symmetric to Split), or, if the proof is genuinely deferred, stop calling the result "the merged run" and mark the validity claim explicitly deferred/out-of-scope so the examples do not silently rely on it.

### Issue 2: Essay paragraph on maximality coincidence is consumed by no proof

**ASN-0084, "Canonical decomposition"**: "We note that S8's maximality criterion and merge-non-extendability coincide: a forward lockstep extension of `(v, a, n)` to `(v, a, n+1)` requires … Hence a run is non-extendable in S8's sense iff it admits no merge, and the two notions of *maximal* name the same partition."

**Problem**: No lemma or theorem in this ASN consumes this coincidence. The only place it is relevant — recovering the canonical partition from R-BLK's non-maximal `B'` — is explicitly listed as an *Open Question* ("By what operational process is the S8-unique maximal … run partition recovered …"). This is essay content placed in a definition slot, advancing no reasoning the ASN actually uses.

**Required**: Remove the paragraph, or relocate the observation into the Open Question that motivates it.

### Issue 3: Duplicated deferral of the post-state S8 existence/uniqueness discharge

**ASN-0084, "Canonical decomposition"**: "Its existence and uniqueness for M'(d) are discharged in the Invariant-preservation audit above." — and **"Invariant preservation"**: "*Post-state S8 discharge.* Since `dom(M'(d)) = dom(M(d))` and all of foundation S8's preconditions … foundation S8 (ASN-0036) applies to M'(d) directly: it supplies the post-state maximal correspondence-run partition and its uniqueness."

**Problem**: Two paragraphs in different sections establish/point to the same fact (foundation S8 applies to `M'(d)`). One section states the discharge; the other defers back to it. This is the cross-section back-pointer pattern that accretes across cycles.

**Required**: State the discharge once (the Invariant-preservation paragraph is the natural home) and delete the back-reference in Canonical decomposition.

### Issue 4: R-BLK "Outside ⋃ₖ V(bₖ)" re-derives EXT-VAC

**ASN-0084, R-BLK Phase 1, "Outside ⋃_k V(b_k)"**: the three-step argument "(1) Every cᵢ … lies in [c₀, c_{n−1}). … (2) Each such cᵢ lies in V_S(d). … (3) Each such cᵢ lies in some V(bₖ)." followed by "EXT-VAC (Consequences of R-PRE) gives c_{n−1} ∉ dom(M(d))…".

**Problem**: The closing facts (only `c_{n−1}` may fall outside `V_S(d)`; the right exterior is then empty; `c_{n−1} ∉ dom(M(d))`) are already established in the EXT-VAC paragraph and re-cited here, while steps (1)–(3) re-walk CS2/CS3/CS4 + R-PRE(iv) coverage that the reader has just seen. The defensive re-derivation can be replaced by a single sentence citing EXT-VAC for the only-`c_{n−1}` exemption.

**Required**: Compress to: "By CS2–CS4 and R-PRE(iv), `c₀,…,c_{n−2} ∈ V_S(d) ⊆ ⋃ₖ V(bₖ)`; only `c_{n−1}` may fall outside, and EXT-VAC then gives `c_{n−1} ∉ dom(M(d))` with empty right exterior, so no run straddles it."

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 / minimum m₁ = 2

The ASN restricts the text subspace to `m_1 = 2` (CS4: `#cᵢ = 2`) and identifies singleton ordinals with ℕ. But the operative arithmetic only ever touches the *last* ordinal component (via OrdinalShift), and D-SEQ already collapses every `V_1(d)` to a last-component range at any depth. The depth-2 restriction therefore appears stronger than the construction needs. Generalizing the singleton-tumbler identification and width arithmetic to depth-`m` ordinals is real additional work and belongs in a follow-on revision, not this one — but the scope note should acknowledge that the restriction is a presentational convenience, not a structural requirement, so a later reader does not mistake it for an essential constraint.

### Topic 2: Composition and k>4 cut classes

The Open Questions (composition of rearrangements, k-cut generalization for k > 4, run-count growth bounds, canonical-partition recovery process) are correctly identified as future territory; no action needed here.

VERDICT: REVISE
