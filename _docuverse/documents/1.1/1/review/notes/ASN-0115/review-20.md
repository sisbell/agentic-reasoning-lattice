# Review of ASN-0115

## REVISE

### Issue 1: C0a (PrefixConfinement) is applied outside its stated contract

**ASN-0115, "What a spec-set is"**: "C0a routes through C0 (OrdinalDisplacementNecessity) to obtain `actionPoint(ℓ) = #ℓ`, which is the one place its content-reference preconditions enter; the V-spec asserts ordinal-level width directly, and C0a's remaining confinement step consumes only that and depth `#s ≥ 2`, so it transfers to every V-spec span, bound or not."

And **R6**: "We pin the shape of that slice by *prefix confinement* (ASN-0058, C0a), *not* by D-SEQ★ … so C0a gives every `t ∈ ⟦σ⟧` agreement with `s` on positions `1 … m_S − 1`."

**Problem**: C0a's contract requires a *well-formed content reference*, whose well-formedness condition is `{v : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))` — every depth-`m` position in the range is bound. R6's whole point is the *terminal-overrun* case, where the named positions with `k > n_S` are **unbound**; those positions lie in `⟦σ⟧` yet are absent from `dom(Σ.M(d))`, so the span is *not* a well-formed content reference. The note nonetheless invokes C0a's confinement "for every `t ∈ ⟦σ⟧`, bound or not." The licensing for this beyond-contract use is a one-sentence assertion about C0a's *internal proof* ("C0's role is the one place content-reference preconditions enter; the remaining confinement step consumes only ordinal-level + depth"). That is a claim about an un-shown proof, not a derivation; it cannot be checked against C0a's contract, which lists the binding precondition with no separability annotation. This is "X follows from Y+Z" standing in for the steps — and the conclusion is load-bearing for both R6 (no-interior-hole) and R10 (no boundary crossing).

**Required**: Derive the confinement from a foundation whose preconditions are actually met. T5 (ContiguousSubtrees, ASN-0034) gives it directly and within contract: for an ordinal-level `σ`, both `s` and `reach(σ) = s ⊕ ℓ` extend the length-`(m−1)` prefix `p = [s₁,…,s_{m−1}]` (ℓ acts only at position `m`), so `p ≼ s` and `p ≼ reach(σ)`; for any `t` with `s ≤ t < reach(σ)`, `s ≤ t ≤ reach(σ)` and T5 yields `p ≼ t`, i.e. `tⱼ = sⱼ` for `j < m` — for **all** `t ∈ ⟦σ⟧`, bound or not, with no content-reference hypothesis. Cite T5 (or state the confinement as a standalone lemma requiring only ordinal-level width and `#s ≥ 2`, with this proof), rather than applying C0a beyond its envelope.

### Issue 2: The reachability precondition and its use-site inventory are stated three times

**ASN-0115, "The substrate we build on"**: "This scoping is load-bearing, not decorative: nearly every step below cites an invariant that ASN-0047 establishes only of reachable states … among them S3★ and S3★-aux (which make `item` total …), S8-depth and D-SEQ★ (R6's terminal-overrun argument), CL-OWN and CL-UNIQ (R8's link-vacuity argument), and S8a/S8-fin (finiteness …). … At a non-reachable state these may fail — S3★-aux could admit a position in a third subspace, leaving `item` undefined; D-SEQ★ could fail, defeating R6's no-hole claim; CL-OWN/CL-UNIQ could fail, defeating R8's link vacuity…"

**And "What a spec-set is and what delivery is"**: "All definitions and claims in this section and below are stated at a state `Σ` reachable from `Σ₀` … this is what licenses the per-state invariant citations (S3★, S3★-aux, S8-depth, D-SEQ★, CL-OWN, CL-UNIQ, S8a, S8-fin) that the definitions of `act`, `item`, and `deliver`, and the proofs of R1–R11, rely on."

**Problem**: The same downstream-consumer inventory is given three times — once as "among them …", a second time as "At a non-reachable state these may fail …" (the identical list re-keyed to its failure mode), and a third time at the opening of the next section. The substance of the precondition is one sentence (every `Σ` is reachable from `Σ₀` under the sequential order); the rest is why-it's-needed essay plus a thrice-repeated use-site list. The convention-appeal "The project's foundation ASNs scope this the same way (ASN-0086 …; ASN-0098 …)" adds nothing about *this* note's content. This is the accreted forward-reference/use-site bloat the `review-mode.anti-bloat` classifier flags.

**Required**: State the reachability precondition once, saying what it constrains. Delete the duplicate "may fail" enumeration, the third restatement at the section opening, and the foundation-convention appeal. Per-claim invariant citations already appear at their use sites; they do not need an index here.

### Issue 3: The single-boundary-crossing-span deferral is repeated across three sections

**ASN-0115, "What a spec-set is"**: "A single boundary-crossing span is therefore outside this ASN, deferred to the Open Questions…"
**R10 intro**: "(Whether a *single* span's denotation can itself straddle the boundary … we leave to the Open Questions; the V-spec definition restricts `σ` to ordinal-level spans…)"
**Open Questions**: "What must delivery guarantee when a single span's denotation straddles the subspace boundary…"

**Problem**: The same deferral to the same downstream location appears in three places — the pattern "multiple paragraphs in different sections defer to the same downstream location."

**Required**: Keep the substantive restriction where it is load-bearing (the V-spec is ordinal-level, so by confinement it cannot straddle) and let the Open Questions entry carry the deferral. The in-body mentions can state the restriction without repeating the pointer.

### Issue 4: The V-spec definition slot carries forward-reference justifications and a consumer inventory

**ASN-0115, "What a spec-set is"**: "The direct imposition is necessary: S8a is an invariant restricted to the active domain `dom(Σ.M(d))`, and R6 below contemplates named starts absent from the arrangement, so the shape cannot be borrowed …" and "The allocation precondition `d ∈ dom(Σ.M)` is what makes the arrangement `Σ.M(d)` — and hence `act`, `item`, `deliver₁`, and `deliver` below — well-defined; it is the same precondition the substrate's `project` carries … It is a precondition on the *existence* of the named arrangement, and is therefore distinct from R6's silent-gap case, which concerns the *absence of a binding* …"

**Problem**: The definition of a V-spec is interleaved with forward-reference justifications (to R6, to R10), a downstream-consumer inventory (`act, item, deliver₁, deliver`), an appeal to "the same precondition the substrate's `project` carries," and a defensive distinction-from-R6. A reader extracting "what a V-spec is" must skip past these. (The concrete boundary-crossing counterexample `s=[1,5], ℓ=[2,0]` and the Nelson quotations are not bloat — they are a worked example and primary grounding; the issue is the surrounding justification essay, not them.)

**Required**: State the V-spec constraints (allocated `d`, well-formed/level-uniform/ordinal-level `σ`, S8a-shaped start, depth-compatibility). Move the "why imposed directly" and "distinct from R6" rationale to R6's vicinity, or cut it; drop the `act/item/deliver` consumer list and the `project`-parity appeal.

## OUT_OF_SCOPE

### The deferred Open-Question topics are appropriately future work
The single-span subspace-crossing case, inline-provenance-in-the-delivered-stream, channel faithfulness, and the "no entity bound at a resolved reference" case are correctly held out of this ASN. R9 is careful to claim *resolution* provenance-traceability, not inline provenance; R10 confines `σ` to ordinal-level spans so no single span straddles. No revision needed for scope handling itself — the ASN also claims nothing in the forbidden set (R10 delivers a link *reference*, not link structure, explicitly excluding READLINK/FOLLOWLINK territory).

VERDICT: REVISE
