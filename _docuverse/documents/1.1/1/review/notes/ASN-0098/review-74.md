# Review of ASN-0098

I checked the major proofs in detail — LP-Fin (the interval-finitude argument, sub-cases A and B), LP9–LP11, LP12a/LP12b (the wp derivations), LP19a/LP19, LP20's partition, and the two worked traces. The technical content holds up: the case splits are exhaustive, the boundary cases (empty arrangement, empty retention R = ∅) are handled, and the trace's bijection arithmetic checks out. The findings below are residual-noise and precision items, consistent with the `review-mode.anti-bloat` classifier on this note.

## REVISE

### Issue 1: Post-LP19 remark restates the "Achievability" paragraph
**ASN-0098, after LP19 / "tight" definition section**: "Tightness is a construction discipline, not a structural invariant the system enforces. The canonical construction — selecting span endpoints among I-addresses resident at construction time, with reach at or before the chain's next emission point — produces tight endsets."
**Problem**: This duplicates the *Achievability* paragraph attached to the `tight` definition, which already establishes constructively that canonical construction yields tight endsets ("Choose `ℓ = δ(n, #s)` with `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` … discharging tightness"). The post-LP19 prose is the same fact in words: "reach at or before the chain's next emission point" = the frontier bound `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)`; "endpoints among I-addresses resident at construction time" = the residency conjunct. This is the "two paragraphs in the same document say the same thing" pattern — the second adds no new reasoning and sits as an essayistic aside between two lemmas.
**Required**: Drop the post-LP19 remark; the *Achievability* paragraph carries it. If the "construction discipline, not enforced invariant" point is wanted, fold that single clause into the `tight` definition rather than re-deriving the achievability conclusion.

### Issue 2: LP13 misattributes arity-fixing to LP2★
**ASN-0098, LP13 proof**: "LP2★ gives `a ∈ dom(Σ'.L)` and `Σ'.L(a).eᵢ = Σ.L(a).eᵢ` for every slot `i`, and fixes the arity `|Σ'.L(a)| = |Σ.L(a)|` (value preservation under L12 forces equal-length sequences)."
**Problem**: LP2★'s schema `P(Σ, Σ') ≡ a ∈ dom(Σ'.L) ∧ Σ'.L(a).eᵢ = Σ.L(a).eᵢ` is quantified over `i ∈ {1, …, |Σ.L(a)|}` and says nothing about arity; it cannot "fix the arity." The parenthetical correctly credits L12's value preservation, contradicting the clause's subject. The slot-by-slot reconstruction is also a roundabout route to a conclusion (`Σ'.L(a) = Σ.L(a)`) that is just L12's full-value equality lifted by the same closure schema.
**Required**: Attribute arity to L12 directly (or derive LP13 as the schema-(★) closure of L12's full value equality `Σ'.L(a) = Σ.L(a)`), instead of routing through LP2★'s slot equality and then patching arity in.

## OUT_OF_SCOPE

### Topic 1: Reverse discovery, V-order preservation, link-to-link induction, fork link-subspace transclusion
**Why out of scope**: These are correctly deferred to the Open Questions and name new state/operations (a reverse-discovery primitive, V-order invariants under K.μ~, link-referencing-link discovery induction) not within this note's remit. No error here.

VERDICT: REVISE
