# Review of ASN-0093

The proof architecture (simultaneous induction over K.σ/K.α/K.λ, the FirstEmissionFreshness/ChainMembershipForOrigin/StoreT4Validity triad, the Cross-document disjointness lemma) is sound and the worked example genuinely exercises both emission branches and both cross-document prefix cases. My findings are concentrated in the residual meta-prose the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: "Forward allocation, derivable" derives an unconsumed property and defends its non-inclusion
**ASN-0093, K.λ, final paragraph**: "*Forward allocation, derivable.* The within-document forward-allocation property `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)` is not stated as a precondition because it is a derivable consequence of the emission rules — symmetrically with K.α. ... neither operator carries the clause as a precondition."
**Problem**: Forward allocation (the strict-ordering direction `ℓ' < ℓ`) is consumed by no invariant in the substrate (M0–L-fin) and by no freshness discharge — freshness uses ChainEnumerationInjectivity's *distinctness*, never the `<` direction; ChainMembershipForOrigin uses injectivity to locate `max`, not this lemma. The paragraph derives an unused property and then justifies *why it is not a precondition*. That is exactly the "defensive justification / prose explaining the absence of a clause" pattern. The first-emit sentence ("the universal antecedent ... is vacuous") imagines a case the predicate already empties.
**Required**: Delete the paragraph. If forward allocation is needed by a downstream ASN, state it there as a derived consequence; the substrate has no consumer.

### Issue 2: "(cited downstream)" forward-pointer annotation
**ASN-0093, FirstEmission lemma**: "*Anchor-construction admissibility (cited downstream).* The increment steps that build the anchors and first emissions ... are each TA5a-admissible..."
**Problem**: The parenthetical "(cited downstream)" is a use-site inventory marker announcing that the sub-result will be referenced later (it is, in the C1c/L1c chain exhibitions). The admissibility content is fine; the annotation that catalogues its consumers is meta-prose.
**Required**: Drop the "(cited downstream)" annotation; keep the admissibility statement under a neutral label.

### Issue 3: Defensive "not parallel chains" paragraph
**ASN-0093, L1c chain exhibition (first-emit)**: "Note that the C1c first-emit chain has *two* inc steps ... while the L1c first-emit chain has *three* ... they are not parallel chains differing only in a single-step substitution. The link chain must traverse the additional `inc(b_C(d), 0) = b_L(d)` step because the link subspace anchor sits one sibling-component beyond the content subspace anchor."
**Problem**: The two chains are exhibited in full immediately above; the step-count difference is self-evident from reading them. The sentence "they are not parallel chains differing only in a single-step substitution" is a defensive disclaimer anticipating a misreading, not a step that advances the proof. This compounds across cycles — it reads like a relocated prior finding rather than load-bearing argument.
**Required**: Remove the paragraph. The exhibited chains already show the structure; at most retain the one-clause structural fact ("the link anchor sits one sibling-component beyond the content anchor") if it is not already clear from `b_L(d) = inc(b_C(d), 0)`.

### Issue 4: K.σ "anchor-disjointness" discharges an excluded non-case
**ASN-0093, K.σ, "Freshness from zeros"**: "d collides with neither store entry nor anchor: `d ∉ dom(C) ∪ dom(L)` and `d ≠ b_C(d'), b_L(d')` for every `d' ∈ dom(M)` are both forced..."
**Problem**: The substrate states explicitly that anchors "inhabit the foundation carrier set `T` as structural witnesses without occupying any state component." No invariant or operation references `d = b_·(d')` as a hazard, and the `zeros = 2` vs `zeros = 3` gap excludes it trivially. Proving `d ≠ anchor` addresses a case already excluded by the carrier's own structure and consumed by nothing. The store-side clause `d ∉ dom(C) ∪ dom(L)` is likewise tied to no stated obligation (registration extends `dom(M)`, and no invariant requires `dom(M)` disjoint from the stores).
**Required**: Cut the anchor-disjointness clause. If `d ∉ dom(C) ∪ dom(L)` is genuinely required by some discharge, name the invariant it serves; otherwise drop the paragraph to the single fact actually used.

### Issue 5: Discharge matrix attributes derived facts to "precondition"
**ASN-0093, discharge matrix, C1/C1b (K.α) and L1/L1b (K.λ) rows**: "Discharged at new key: precondition pins `zeros(a) = 3`" / "precondition pins `#E(a) ≥ 2`".
**Problem**: In the *subsequent-emission* branch the precondition only fixes `a = inc(a_prev, 0)`; `zeros(a) = 3` is then a consequence of B5a (zero-count preserved under `inc(·,0)`) plus the inductive hypothesis, and `#E(a) ≥ 2` follows from length preservation (TA5(c)), not from any precondition conjunct. The blanket "precondition pins" collapses two structurally different discharge routes into one and hides the deriving lemma from the precise reader. (The first-emit branch is also derived-from-form rather than a standalone conjunct, but is at least immediate.)
**Required**: Split the entry or name the deriving discipline for the subsequent-emit branch (B5a / ChainUniformZeroCount for `zeros`; length preservation for `#E`), so the matrix matches the actual proof.

## OUT_OF_SCOPE

### Topic 1: Disjointness of `dom(M)` from `dom(C) ∪ dom(L)`
**Why out of scope**: Whether registered document addresses must be globally disjoint from content/link addresses (beyond the `zeros`-level separation) is a cross-store structural invariant that no substrate obligation currently needs; if a higher-layer ASN requires it, that is where it belongs — not a defect here. (This is the principled home for the material trimmed in Issue 4.)

VERDICT: REVISE
