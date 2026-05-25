# Review of ASN-0098

## REVISE

### Issue 1: LP19 state naming is internally inconsistent
**ASN-0098, LP19**: The claim states "any K.α (or K.λ) transition between `Σ` and `Σ'` allocating a fresh address `a_new`" — fixing Σ' as the post-K.α state. The consequence then says "if a subsequent K.μ⁺ or K.μ⁺_L extends `Σ.M(d)` by a mapping `(v_new, a_new)`, then `v_new ∉ project(e, d, Σ')`." The proof concludes "Then `Σ'.M(d)(v_new) = a_new ∉ coverage(e)`."

**Problem**: Three contradictions:
- "Subsequent K.μ⁺" implies K.μ⁺ fires after Σ', producing a third state, but no state name is introduced for it.
- "Extends `Σ.M(d)`" should be `Σ'.M(d)` (the state K.μ⁺ acts on); K.α does not modify M, so `Σ'.M(d) = Σ.M(d)`, but K.μ⁺ extends whichever state it fires from.
- The proof's `Σ'.M(d)(v_new) = a_new` cannot hold at the post-K.α state — K.α leaves M unchanged, so v_new is not in dom(Σ'.M(d)) until K.μ⁺ fires. If Σ' is post-K.α, the conclusion `v_new ∉ project(e, d, Σ')` is vacuous (v_new not in domain at all), not the intended substantive claim.

**Required**: Introduce a distinct state name (e.g., Σ_post for post-K.α/K.λ, Σ_final for post-K.μ⁺) and rephrase: "if any later K.μ⁺ or K.μ⁺_L transition `Σ_n → Σ_n+1` (with `Σ_post →* Σ_n`) extends `Σ_n.M(d)` by `(v_new, a_new)`, then `v_new ∉ project(e, d, Σ_n+1)`."

### Issue 2: LP9 and LP10 difference characterizations asserted without proof
**ASN-0098, LP9**: "The new V-positions that enter the projection are exactly the new arrangement entries whose I-addresses fall in the coverage: `project(e, d, Σ') ∖ project(e, d, Σ) = {v ∈ dom(Σ'.M(d)) ∖ dom(Σ.M(d)) : Σ'.M(d)(v) ∈ coverage(e)}`"
**ASN-0098, LP10**: analogous set equation for losses.

**Problem**: These are non-trivial set equalities asserted without bidirectional verification. The forward inclusion is direct, but the reverse requires ruling out the case where `v ∈ dom(Σ.M(d))` could enter the projection without being a new mapping — which holds by the agreement clause `Σ'.M(d)(v) = Σ.M(d)(v)` on prior domain, but this step is not shown.

**Required**: Either derive each set equality in two-line form (forward and reverse), or qualify the equation as a direct corollary of the projection definition combined with the K.μ⁺/K.μ⁻ agreement clause.

### Issue 3: Holder summary uses multi-step language but cites single-step claims
**ASN-0098, "What the Link Holder Can Rely On"**: Section opens with "Across any state evolution `Σ →* Σ'`" and lists:
- "The address `a` remains in `dom(Σ'.L)` (L12, ASN-0043)."
- "The endsets `Σ'.L(a).eᵢ` are byte-identical to `Σ.L(a).eᵢ` for every slot (LP2)."

**Problem**: L12 (ASN-0043) and LP2 are both single-step (Σ → Σ'). Their multi-step closures hold by induction, but the ASN states such a closure only for coverage (LP3★) and for store containment (Store Monotonicity★). The holder summary's value-preservation claim relies on a multi-step closure of LP2 that is not stated. LP3★ establishes coverage equality multi-step but not value equality (it could in principle hold with reshaped spans denoting the same coverage), so it does not subsume the byte-identity claim.

**Required**: State LP2★ as the reflexive-transitive closure of LP2 (parallel to LP3★), or fold an explicit multi-step argument into the holder summary's citations. The induction is one line — make it visible.

## OUT_OF_SCOPE

### Topic 1: Reverse discovery
The Open Questions section already flags this. Not an error in this ASN.

### Topic 2: Non-tight endset behavior under subsequent allocation
The ASN acknowledges non-tight endsets ("such endsets are not tight, and an `a_new` allocated within their forward extent would in fact enter the coverage") but does not formalize the consequences. Flagged as an open question — appropriate scope deferral.

### Topic 3: V-order of projected positions
Open question; not a gap in current scope.

### Topic 4: Link-to-link endset induced discovery
Open question; not a gap in current scope.

VERDICT: REVISE
