# Review of ASN-0093

I checked the three primitives, the sub-allocator chain machinery, the freshness lemmas, the simultaneous-induction discharge matrix, and the nine-step worked example. The mathematics is sound: the anchor construction (`b_C(d) = inc(d,2)`, `b_L(d) = inc(b_C(d),0)`), the B6/B7/S0/S1-based chain disciplines, the cross-document (T10) and cross-subspace (T7) freshness splits, and the contiguous-prefix induction all check out, including boundary branches (first-emit/subsequent-emit) and both prefix-comparable and prefix-incomparable document pairs. My findings are confined to the forward-reference/anti-bloat patterns the note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: FirstEmissionFreshness link case is unreadable double-transposition prose
**ASN-0093, "Lemma (FirstEmissionFreshness)", Link case**: "the against-`dom(L)` argument transposes the content against-`dom(C)` argument (...), and the against-`dom(C)` argument transposes the content against-`dom(L)` argument (...)"
**Problem**: The symmetry is genuine (content↔link), so "by symmetry" is legitimate — but the cross-wiring ("against-L transposes against-C, against-C transposes against-L") plus the substitution list "(`ℓ`, `A_L(d)`, `b_L(d)`, `s_L`, L1a, C1 ↦ `a`, `A_C(d)`, `b_C(d)`, `s_C`, C2, L1)" forces the reader to mentally swap two arguments crosswise to follow it. This is meta-prose one must skip past, not reasoning that advances.
**Required**: Replace with a single clean statement: "By symmetry under content↔link (swap `A_C(d)↔A_L(d)`, `s_C↔s_L`, C2↔L1a), the link first emission is fresh against `dom(L)` by the cross-document/T10 argument and against `dom(C)` by the T7 argument." Drop the transposition narration.

### Issue 2: Redundant alternative justifications ("equivalently …") for single facts
**ASN-0093, discharge matrix, C2 (K.α subsequent-emit)**: "hence `origin(inc(a_prev, 0)) = origin(a_prev) = d` by the IH on `a_prev` (equivalently from `b_C(d) ≼ a` via the chain's prefix preservation)" — and the identical parenthetical in L1a; also ChainUniformZeroCount's source line "ASN-0040 SiblingStream postcondition (...), equivalently *B5a (SiblingZerosPreservation)*".
**Problem**: Each gives two derivation routes / two sources for one conclusion. This is the "two paragraphs say the same thing in different words" pattern compressed into a cell. One justification carries the proof; the second is accreted noise.
**Required**: Keep one route per fact (the IH route for origin; one ASN-0040 citation for the zero count), delete the "equivalently …" alternatives.

### Issue 3: K.σ definition closes with a downstream-consumer inventory
**ASN-0093, K.σ (DocumentRegistration)**: "K.σ opens the content and link sub-allocator frontiers `A_C(d)` and `A_L(d)` under `d` — available once `d ∈ dom(M)` — for subsequent K.α and K.λ emissions."
**Problem**: This sentence is a use-site inventory ("for subsequent K.α and K.λ") appended to an operation definition — it names downstream consumers rather than stating what the operation does. The operation's effect clause (`dom(M') = dom(M) ∪ {d}`, `M'(d) = ∅`) already says everything load-bearing; chain availability is a definitional consequence of `d ∈ dom(M)` established under "Address sub-allocators under documents."
**Required**: Delete the sentence, or reduce to "Chains `A_C(d)`, `A_L(d)` are active once `d ∈ dom(M)` (per Address sub-allocators)" without the K.α/K.λ forward inventory.

## OUT_OF_SCOPE

### Topic 1: Disjointness of `dom(M)` from `dom(C) ∪ dom(L)`
**Why out of scope**: The substrate states SD (`dom(C) ∩ dom(L) = ∅`) but not that document tumblers (`zeros = 2`) are disjoint from content/link addresses (`zeros = 3`). This is trivially forced by T3 on differing zero counts and is never needed by any freshness argument (which target `dom(C) ∪ dom(L)` only), so its absence is not an error — if a future layer ever lets the stores interact it can state it then.

VERDICT: REVISE
