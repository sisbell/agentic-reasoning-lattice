# Review of ASN-0133

I checked the mathematics first, since an anti-bloat pass on a wrong proof is wasted effort. The core results hold: Q0's view-rebuild argument is sound (the four view-parameterized constituents plus the four UV-rewritten fixed-view collections do exhaust the view-sensitive vocabulary, and each rebuilds); Q-EXT correctly composes X-DEF with PD0 ⊥-stability; the Q5/Q5a/Q6 separation of H-W, bounded-domain-growth, and H-RF is correct, including the subtle obstruction (3) in Q6 and the H-SFAIR satisfiability limit; the worked trace verifies. The starvation analysis (H-RF strictly weaker than H-W) is correct. I found no correctness defect.

What I did find, against the `review-mode.anti-bloat` classifier, is that the note's load-bearing observations are re-derived in place rather than stated once and referenced. These compound.

## REVISE

### Issue 1: The starvation-separation argument is re-derived in five places

**ASN-0133, W/H-W, Q5, Q5a, H-RF, Q6**: The single argument — *a starved trigger-true argument keeps `(ρ,x,k) ∈ W(σ)` at every step (`|W(σ)| = ∞`) while contributing no real fire, so H-RF holds where H-W fails* — appears, fully spelled, at five sites:

- W/H-W: "an unfair scheduler that starves a persistently-true trigger drives `|W(σ)| = ∞` … so these conditions supply at most the weaker H-RF, never H-W itself."
- Q5: "it does not discharge H-W, which a starved SF trigger-true argument violates while real fires stay finite."
- Q5a: "under an unfair scheduler a starved trigger-true argument can still drive `|W(σ)| = ∞` … while the real-fire count stays bounded."
- H-RF: "The two come apart precisely at starvation: an SF trigger-true argument the scheduler never fires keeps its triple `(ρ, x, k) ∈ W(σ)` at every step (`|W(σ)| = ∞`) while contributing no real fire."
- Q6: "The starvation mode is exactly why the hypothesis is H-RF rather than H-W: a starved SF trigger-true argument drives `|W(σ)| = ∞` yet contributes no fire."

**Problem**: This is one fact stated five times. Its definitional home is H-RF (which exists to name the distinction) and its motivating home is W/H-W (which declares H-W a foil). The re-statements in Q5, Q5a, and Q6 are asides that re-derive what those two sites already establish — exactly the "two paragraphs say the same thing in different words" pattern, multiplied.

**Required**: State the separation once (H-RF, with W/H-W's foil framing), and at Q5/Q5a/Q6 reference it ("H-RF, not H-W; see the starvation separation") rather than re-walking `|W(σ)| = ∞`-with-zero-fires each time.

### Issue 2: Q0's closing parenthetical restates the body's view partition, and Q7 re-inventories it

**ASN-0133, Q0**: The body works through the partition — "rebuild each of its *exactly four* view-parameterized constituents — `members`, `targets_of`, `is_K`, `M_K`"; "UV … rewrites *six* collection atoms … *and* the four *fixed-view* behavior collections `succs`, `sources_to`, the sequence `chain` returns, and `stale`"; "Everything else … *is* genuinely view-stable" — and then the closing parenthetical re-states the whole thing: "the four view-parameterized constituents together with the four UV-rewritten fixed-view collections `succs`/`sources_to`/`chain`/`stale` exhaust the view-sensitive forms, and each rebuilds: the set-valued ones by a fixed-view filter, `chain` through `elems` or the view-stable `is_in_chain`."

**Problem**: The parenthetical is a defensive recap — same partition, same rebuild method, reframed as a contrapositive ("a non-unifiable trigger would require … the vocabulary of ASN-0129 has none"). The exhaustiveness was already carried by the body's "everything else is view-stable." Q7 then re-lists the same `succs`/`sources_to`/`chain`/`stale` inventory ("the UV-rewritten fixed-view collections `succs`/`sources_to`/`chain`/`stale` alike — to the rebuild Q0 already performs"). The four-element inventory thus appears three times across two claims.

**Required**: Drop the Q0 closing parenthetical (the body proves it); in Q7 reference Q0's rebuild rather than re-enumerating the four collections.

### Issue 3: H-SFAIR is offered as a second route, then argued to be barely one, at length and in two sections

**ASN-0133, H-SFAIR and Q6**: H-SFAIR is introduced as an alternative to regime (i) for non-grow-only reaching, and Q6 presents the disjunction "regime (i) for the rule … or *strong* fairness (H-SFAIR)." The H-SFAIR paragraph then spends a long passage retracting the independence: "This also tempers H-SFAIR's standing as an independent alternative to regime (i) … The 'or' is thus nearer a restatement than a genuinely disjoint second route: H-SFAIR relocates the environmental concession into a fairness premise rather than dispensing with it." Q6 re-opens the same relationship ("H-SFAIR is exactly the closing hypothesis …").

**Problem**: Two things degrade the argument here. (a) If, for the only registries H-SFAIR is invoked on (all-SF, Q6 case 3), H-SFAIR-satisfiability *requires* regime (i)'s own condition, then presenting them as a genuine disjunction and then conceding it "nearer a restatement" is an establish-then-retract that leaves the reader to reconcile the two. (b) The H-SFAIR ⟹ H-FAIR sub-proof — with its finite-σ counterexample and infinite-σ scoping — establishes a "genuinely stronger" positioning claim that no downstream theorem consumes (Q6 invokes H-SFAIR's own statement, never the implication). That is depth doing no work.

**Required**: Either present one route with two framings (eventual local idleness = regime (i), spelled as strong fairness for all-SF rules) instead of a disjunction the note then collapses, or keep H-SFAIR but cut the "tempers its standing"/"nearer a restatement" commentary to the one sentence that records the near-coincidence. If the H-SFAIR ⟹ H-FAIR positioning is kept, compress it to the claim plus the finite-σ caveat in a line, since it is not a lemma.

### Issue 4: Multiple deferrals to one downstream section, and a premature forward-result in RG

**ASN-0133, RG and H-SFAIR**: Two sections defer the same scheduler/serialization material to the same place — RG: "a scheduler obligation (deferred — see *What this note doesn't cover*)"; H-SFAIR: "That full turn/serialization model is the scheduler layer's to fix (deferred — see *What this note doesn't cover*)." Separately, RG previews a Q5a result: "the *closed*, environment-free special case collapses them to restatements of their own conclusions (Q5a)."

**Problem**: Repeated "deferred — see X" pointers are the cross-section-deferral pattern; once the section exists, a single deferral suffices. The RG forward-pointer to Q5a's open/closed collapse states a downstream conclusion in the model-definition slot before the machinery to support it exists — the open/closed point is then made again at Q5a (proved) and in the worked example (instantiated).

**Required**: Defer the scheduler obligation once (at H-ATOM's first mention) and let "What this note doesn't cover" own it; remove the RG preview of Q5a's collapse, leaving the result to Q5a where it is earned.

## OUT_OF_SCOPE

The five Open Questions (SF certificate / `pd_extinct`, a PL surrogate for H-W, per-scope vs global work, cross-scope oscillation, contract necessity) are correctly placed as future work and need no action here.

VERDICT: REVISE
