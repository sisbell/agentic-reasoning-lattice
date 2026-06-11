# Review of ASN-0111

## REVISE

### Issue 1: RL5's caching discipline contradicts the permanence families the same paragraph establishes

**ASN-0111, "Determinacy and the immutability of the recorded relationship" (and the RL5 claims-table row)**: "⊥ at a screen-passing address must not be cached — not because every such address can later be allocated, but because its permanence is not derivable from the address alone."

**Problem**: The paragraph immediately preceding this sentence derives permanent absence for two families of screen-passing addresses *from the address alone*. The depth family is characterized by the address-computable test `#E(a) > 2` (via ChainMembershipForOrigin plus length preservation along the chain), and the lineage family by the address-computable test `¬(n₀ ≼ N(a))` — with `n₀ = [1]` fixed by ASN-0047's Σ₀, this is just `N(a)₁ ≠ 1`. Both derivations consume only the address's structure plus state-independent invariants over reachable states; that is exactly "derivable from the address alone." The claims table contains the contradiction within a single cell: "permanence of ⊥ is not derivable from the address alone — … while off-chain (element-field depth > 2) and off-lineage (node field outside the n₀ lineage) screen-passing addresses are permanently absent." What the preceding text actually proves is that permanence is not derivable from the *screen* alone — the screen-passing class is heterogeneous, and a finer address-computable test splits it.

**Required**: Restate the caching discipline three ways: (i) success-branch results cache permanently; (ii) ⊥ caches permanently wherever an address-computable permanence proof applies — screen failure, element-field depth ≠ 2, or node field off the `n₀` lineage; (iii) ⊥ must not be cached at the residual class (screen-passing, depth-2, lineage-valid), whose members are exactly the addresses a future K.λ can allocate. Correct the body sentence and the RL5 table row to say "not derivable from the screen alone" (or the refined formulation), eliminating the internal contradiction.

### Issue 2: The depth-family argument derives "element-field depth exactly 2" from length preservation alone

**ASN-0111, same section**: "every element of such a chain has element-field depth exactly 2 — the first emission `[d.0.s_L.1]` has `#E = 2`, and each subsequent emission is `inc(·, 0)`, which preserves length (TA5(c), with `sig = #` on T4-valid addresses by TA5-SigValid)".

**Problem**: Length preservation does not by itself fix `#E`. The element-field boundary is determined by the zero positions, so the step needs: `inc(·, 0)` modifies *only* position `sig(t)` (TA5(b), k = 0 case, together with TA5(c)), that position is the terminal one (TA5-SigValid), and its value goes from a nonzero natural to its successor (`t_{sig} + 1 ≥ 2`), so the zero count and zero positions are unchanged and the element-field boundary — hence `#E` — is preserved. As written, the citation chain discharges length but leaves the zeros-invariance step implicit, which is the load-bearing half for a claim about `#E`. The foundation's per-step citation convention (cf. how TA5 itself discharges every ℕ-fact to T0) makes this a gap, and the claim is load-bearing — RL5's permanent-absence conclusion for `[1.0.1.0.1.0.2.1.1]` rests on it.

**Required**: Add the zeros-preservation clause with its citations: single-position modification at `sig(t) = #t` (TA5(b)/(c), TA5-SigValid), nonzero-to-nonzero at that position, therefore `zeros` unchanged and `#E` preserved along the chain.

### Issue 3: The worked read stipulates an allocated-but-unarranged state without exhibiting its reachability

**ASN-0111, "A worked read"**: "three `dom(C)` members that host content and are unarranged."

**Problem**: The standing precondition restricts every claim to reachable, invariant-satisfying states, and J0 (AllocationPlacementCoupling, ASN-0047) requires every freshly allocated I-address to appear in some arrangement at its allocating composite's boundary. A state with allocated-but-unarranged content therefore cannot arise at allocation; it requires a subsequent K.μ⁻ contraction. The state *is* reachable (J0-coupled K.α + K.μ⁺ composite, then K.μ⁻ with content-subspace retention 0), but the example never says so — it stipulates the configuration bare. This matters because the orphaned-instance check of RL6 is built on this very stipulation; if the state were unreachable, that check would be vacuous. The ASN holds itself to the higher standard elsewhere — RL4's witness pair is constructed from Σ₀ precisely because "the exclusion has force only if the state pair … actually exists" — so the asymmetry is a gap, not a style choice.

**Required**: One or two sentences exhibiting the route: the three I-addresses enter `dom(C)` inside J0-satisfying composites (arranged at allocation), and a later K.μ⁻ on each document contracts the content subspace to empty, yielding the stipulated state; the three K.λ steps allocate `a`, `a'`, `c` on `A_L(d₁)`'s chain. This makes the worked state, and the orphan hypothesis built on it, demonstrably within the spec's domain.

## OUT_OF_SCOPE

### Topic 1: An address-status operation exposing the three-way classification RL5 uncovers

RL5's analysis implicitly defines a three-way, address-computable classification (permanently absent / currently absent but allocatable / allocated) that callers performing caching would want as a first-class query rather than re-deriving from screen + depth + lineage tests. **Why out of scope**: this is a new operation with its own contract, not a defect in the read; ASN-0111 only needs the classification to state its caching discipline correctly (Issue 1).

### Topic 2: Reader-side identity disclosure for value-identical links

The third Open Question (distinguishing two links with identical recorded structure) points at whether a read result should carry its key. **Why out of scope**: the ASN correctly scopes `readlink` to value disclosure with identity carried by the caller-held address; any key-bearing result shape is a design decision for a future ASN.

VERDICT: REVISE
