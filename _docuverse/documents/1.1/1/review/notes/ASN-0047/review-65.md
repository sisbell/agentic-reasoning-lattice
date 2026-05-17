# Review of ASN-0047

## REVISE

### Issue 1: Cross-document disjointness chain proof gap (version pairs not covered)

**ASN-0047, *Allocator hierarchy under documents***: "The prefix-incomparability `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` splits by parent-account relationship. *Same-account sibling case:* ... T10a.2 ... *Different-account case:* ... T10a.5 ..."

**Problem**: The case split is incomplete. Two distinct documents under the same parent account can stand in a *version* relationship (`d₂ = inc(d₁, 1)`), which is neither a k=0 sibling case nor a different-account case. For this case, `d₁ ≼ d₂` (d₁ is a tumbler prefix of d₂), so the proof's premise `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` is *false*. The lemma's conclusion (anchor prefix-incomparability) happens to hold because `b_L(d₁) = [d₁, 0, s_L]` and `b_L(d₂) = [d₁, 1, 0, s_L]` diverge at position `#d₁+1` (0 vs 1) — but for a different structural reason than the proof states.

**Required**: Add a third case to the case split — same-account version pair — and exhibit the divergence at position `#d₁+1` between `b_L`'s zero separator and the version's positive increment. The K.δ k=1 sub-case admits version allocation (and ghost-base versioning), so this case is reachable.

### Issue 2: K.μ⁻ exhaustiveness lemma's mutual exclusion claim is incorrect

**ASN-0047, *Elementary transitions* (K.μ⁻ exhaustiveness lemma)**: "The three cases are mutually exclusive: ... (b) and (c) each exhibit a removed index that prevents that initial-segment shape, and they themselves are disjoint because (c) asserts `1 ∈ K\K'` whereas (b) asserts an interior hole strictly above a retained minimum."

**Problem**: As stated, definitions (b) and (c) overlap. Take K = {1, 2, 3, 4, 5} and K' = {3, 5}: this satisfies (b) (k_lo=3, k_hi=5, k₀=4 ∈ K\K') AND satisfies (c) (1 ∈ K\K' and K' ≠ ∅). The proof's *partition algorithm* uses contiguity as the distinguishing criterion (non-overlapping), but the *lemma's stated definitions* admit overlap. The disjointness argument in the proof is therefore unsound on its own terms.

**Required**: Tighten the lemma's definition of (c) to also require contiguity of K' (e.g., "K' is contiguous and 1 ∈ K\K' and K' ≠ ∅"), or refactor (b) and (c) to be definitionally disjoint by using the contiguity criterion explicitly. Either fix matches what the partition algorithm in the proof actually does.

### Issue 3: S4 derivation for K.λ first-link case incorrectly invokes T10a

**ASN-0047, *Foundation invariants previously implicit* (S4)**: "*K.λ — first-link case:* ... The structural form falls under the inc-chain hypothesis of T10a: SubAllocatorAxiom's emission is a length-3 inc step from the document prefix, so T10a's GlobalUniqueness applies and gives `ℓ ∉ dom(L)` within origin(ℓ) = d's link store."

**Problem**: This contradicts the K.λ definition's explicit statement that T10a does *not* apply to first-link emissions ("SubAllocatorAxiom's link namespace property gives `ℓ ∉ dom(L) ∪ dom(C)` directly; no inc derivation from a previously allocated `t` is invoked, because the axiom underwrites the first allocation by structural construction rather than by T10a's per-owner inc discipline"). SubAllocatorAxiom is needed precisely because T10a's at-most-once spawning constraint does not admit two distinct sub-allocator frontiers via one inc operation. The S4 derivation cannot simultaneously rely on T10a's GlobalUniqueness for first-link freshness.

**Required**: Rewrite the S4 first-link case to cite SubAllocatorAxiom's namespace property as the underwriter of `ℓ ∉ dom(L)` (combined with the precondition `V_{s_L}(d) = ∅`), parallel to how the K.λ definition discharges the same precondition. The T10a invocation belongs only in the subsequent-link case.

### Issue 4: "S8-scope in the extended state" note attributes link-subspace decomposition to wrong invariants

**ASN-0047, *Extended reachable-state invariants* (S8-scope note)**: "The link subspace's analogue of S8 — that the link-subspace V-positions also decompose into a finite span — is established separately by L1 + L1b (link-subspace contiguity and depth) discharged through the K.μ⁺_L analysis in the Link-subspace extension section, and does not require re-invoking ASN-0036's S8."

**Problem**: L1 (`zeros(ℓ) = 3`) and L1b (`#E(ℓ) ≥ 2`) are address-level properties of link addresses, not arrangement-level decomposition invariants. The parenthetical "(link-subspace contiguity and depth)" is therefore misattributed — contiguity at the arrangement level is D-CTG★, and uniform depth is S8-depth. The K.μ⁺_L section itself cites the right invariants ("S8 is derived from S8-fin, S8a, S2, and S8-depth"); the S8-scope note should match.

**Required**: Replace "L1 + L1b (link-subspace contiguity and depth)" with "D-CTG★, D-MIN★, S8-fin, S8-depth, and S8a applied per subspace" — the arrangement-level invariants that actually establish the link-subspace finite-span decomposition.

## OUT_OF_SCOPE

None — the ASN explicitly enumerates and defers each known gap (tombstone-style withdrawal, version-management semantics, account-level k=1, non-T10a allocators) under the *Structural sufficiency and known gaps* section and in the Open Questions list.

VERDICT: REVISE
