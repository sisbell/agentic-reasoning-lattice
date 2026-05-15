# Review of ASN-0082

## REVISE

### Issue 1: Incomplete NAT citation for the strict inequality `1 + c > c`
**ASN-0082, D-BJ proof of (a)**: "Since p ∈ V_1(d), S8a gives p₂ ≥ 1, hence p₂ + c ≥ 1 + c > c (NAT-addcompat, ASN-0034)."
**Problem**: The first inequality `p₂ + c ≥ 1 + c` follows from NAT-addcompat's right order compatibility on `1 ≤ p₂`, but the strict inequality `1 + c > c` does not. NAT-addcompat provides weak order compatibility plus the strict successor `n < n + 1` — giving only `c < c + 1`, not `c < 1 + c`. The step from `c < c + 1` to `1 + c > c` requires commutativity of natural addition (not a foundation axiom) or a separate derivation via NAT-addbound's right dominance (`1 + c ≥ c`) combined with NAT-cancel's summand absorption (`1 + c = c ⟹ 1 = 0`) and NAT-closure's Consequence `0 < 1` to rule out equality.

The same hand-waved citation recurs in D-S's "Derivation of (a)" (within the `s₂ ≥ p₂ + c ≥ 1 + c > c` chain), in D-SHIFT's well-definedness derivation, and in S8a-post's argument ("vₘ − c ≥ p₂ ≥ 1"). Each instance needs the full chain.

**Required**: Either spell out the chain explicitly at each site (NAT-addcompat + NAT-addbound + NAT-cancel + NAT-closure Consequence), or introduce a derived strict order compatibility lemma once and cite it consistently. The conclusion is correct; the citation chain is not.

### Issue 2: "Necessity from TA4" argument suppresses TA4's `k = #a` clause
**ASN-0082, Scoping axioms, "Necessity from TA4 (mathematical)"**: "TA4's zero-prefix precondition `(A i : 1 ≤ i < k : aᵢ = 0)` — where a = ord(p) and k = actionPoint(w_ord) — requires zeros in ord(p) at positions before the action point. But S8a's componentwise positivity gives ord(p)ᵢ > 0 for all i, so the zero-prefix precondition is *only* vacuous when k = 1, i.e., when #ord(p) = 1, i.e., when #p = 2."
**Problem**: TA4's full preconditions are `Pos(w) ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0)` with k being simultaneously the action point of w, the length of a, and the length of w. The argument names "k = actionPoint(w_ord)" and then leaps from "k = 1" to "#ord(p) = 1" via *i.e.* — but this leap silently uses TA4's `k = #a` clause (with a = ord(p)). Without that suppressed clause, k could be the action point of w_ord without coinciding with #ord(p), and the necessity conclusion does not follow.

Additionally, the obstruction depends jointly on three TA4 constraints, not just the zero-prefix: at depth #p > 2, both (a) `k = #a = #ord(p) > 1` (forcing the zero-prefix range to be non-empty) and (b) `k = action point of w_ord` (forcing w to have action point at its last position) interact with S8a positivity to fail TA4. The argument conflates these.

**Required**: Restate the necessity argument to make all three TA4 constraints explicit, then derive the obstruction from their joint interaction with S8a positivity. Show that depth #p = 2 satisfies all three vacuously (k = 1, zero-prefix range empty, w_ord has action point 1 = #w_ord), and that #p > 2 fails the zero-prefix specifically because TA4's `k = #a > 1` forces a non-empty range that S8a's positivity contradicts.

### Issue 3: I3-V's stated necessity is unsupported — it is a corollary of I3-CS
**ASN-0082, Post-Insertion Shift, prose after the postcondition list**: "The vacating postcondition (I3-V) completes the shift semantics: original positions at or beyond p that are not the destination of any shifted content are removed from dom(M'(d)), preventing content duplication in sparse arrangements. Without I3-V, an implementation could retain M'(d)(v) = M(d)(v) alongside M'(d)(shift(v, n)) = M(d)(v), duplicating content at both the original and shifted positions."
**Problem**: I3-CS already closes dom(M'(d)) ∩ subspace S to (left-region ∪ shifted-images). For any v ∈ dom(M(d)) with subspace S and v ≥ p that is not a shifted image, I3-CS's contrapositive directly excludes v from dom(M'(d)) — without I3-V. The "duplicating content" scenario the prose describes (retaining M'(d)(v) = M(d)(v) at an original position) is already ruled out by I3-CS alone, because such a v is neither left-region (v ≥ p) nor a shifted image (by hypothesis), and I3-CS forbids any other membership.

So I3-V is a corollary of I3-CS, not an independent constraint. The prose claims it is doing essential work that it is not.

**Required**: Either (a) drop I3-V and let I3-CS carry the closure obligation; (b) keep I3-V for narrative explicitness but rewrite the justification — note that I3-V is the corollary of I3-CS restricted to v ∈ dom(M(d)), retained for readability rather than as an independent specification clause.

## OUT_OF_SCOPE

### Topic 1: Generalization of contraction to ordinal depths greater than two
**Why out of scope**: The depth-2 restriction is mathematically forced by TA4 at this stratum. Lifting it would require either a strengthened TA4 in the foundation or a separate derivation of the partial-inverse identity from TumblerAdd and TumblerSub directly. The Open Questions section already names this as future work.

### Topic 2: Full INSERT operation composing the shift sub-operation with content placement
**Why out of scope**: I3 is explicitly scoped to the arrangement-shift sub-operation. A composing INSERT would extend dom(C) with n new I-addresses, populate the gap [p, shift(p, n)), and re-derive D-CTG/D-MIN/D-SEQ for the complete post-state. That belongs in a downstream operation ASN.

### Topic 3: Link-subspace operations (MAKELINK, link contraction by tombstoning)
**Why out of scope**: Contraction is scoped to S = 1 by the subspace axiom. Link-subspace mutation uses tombstoning rather than shift-to-close-gap; MAKELINK allocates new link content. Both are deferred to future ASNs and rely on different mutation disciplines than those characterized here.

VERDICT: REVISE
