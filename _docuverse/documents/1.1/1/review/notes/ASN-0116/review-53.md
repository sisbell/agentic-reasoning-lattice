# Review of ASN-0116

I checked the operation as a valid composite, the per-step precondition discharge, every boundary case (empty subspace, append, front-insertion at `n'_{s_C}=0`, block extending past `N`), the four coupling constraints, and each named claim (IP0–IP6, PROV). **The technical content is sound** — the composite `K.α(×n) → K.μ⁻ → K.μ⁺ → K.ρ(×n)` is correctly exhibited, the gapped-vs-filled `M'₀` distinction is handled, the wp derivation (IP6) is genuinely non-trivial and correctly distinguishes containment from emptiness, and the link-survival decomposition (IP4) is complete. The remaining issues are prose accretion of the kind the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: IP1 is discussed — with its maximality caveat — several paragraphs before it is stated
**ASN-0116, "The document remains one coherent sequence"**: the paragraph "IP1 records the narrower fact that the inserted material forms a correspondence run in S8's sense … though not necessarily a *maximal* one: when the left-adjacent slot `q_{J-1}` holds the current greatest origin-`d` address `a_prev` … the block I-merges backward into it…" appears, then PROV, then "Two finer points remain", and only after all that: "We record the connected-region fact as a claim: **IP1 (InsertedRun).**"
**Problem**: A reader meets IP1's *limitation* (non-maximality, backward I-merge) before meeting IP1 itself, separated from the formal statement by an unrelated provenance claim and the "finer points" paragraph. The caveat is the load-bearing observation, but it floats detached from the claim it qualifies.
**Required**: State IP1 first, then attach the maximality discussion directly beneath it. Remove the forward reference.

### Issue 2: The post-state dense-run domain is stated a third time, under the banner "worth stating once"
**ASN-0116, "The document remains one coherent sequence"**: "One concrete shape is worth stating once … The post-state text domain `V_S(d')` is the canonical dense run `{q_1, …, q_{N+n}}` … this is I-DOM, **which the Effect already establishes** from the block-disjointness fact, and is exactly the contiguity K.μ⁺'s clause (iii) discharged…"
**Problem**: `V_S(d') = {q_1,…,q_{N+n}}` is now stated three times — I-DOM (Effect), K.μ⁺ clause (iii) (valid-composite section), and here — and the paragraph itself concedes "the Effect already establishes" it while reasserting it under "worth stating once." The only genuinely new content is the Q10 reading-order connection.
**Required**: Reduce to a one-line pointer: I-DOM, restricted to the whole text subspace, is the Q10 "read end-to-end" guarantee. Drop the re-derivation.

### Issue 3: Restatement accretion — "Two finer points" and the per-clause gapped/filled bridge
**ASN-0116, "The document remains one coherent sequence"**: "First, inserting a *span* rather than a single byte is, at the V-layer, no different in kind — the same uniform shift opens a block of exactly the right size…"
**Problem**: The first finer point adds nothing — the entire note treats general `n`, so "a span is no different from a byte" is established by every claim already. It is a restatement with implementation color (Q5), not a step in any argument. Separately, in the Effect, the gapped/filled bridge ("I3 fixes values on `M'₀(d)`; INSERT's post-state is `M'(d) = M'₀(d) ∪ {block fill}`; the union adds no entry at [region]") is re-explained in each of I-SHIFT, I-LEFT, I-NEW, and I-DOM, with only the disjoint region changing.
**Required**: Drop the first finer point. State the `M'(d) = M'₀(d) ∪ {block}` bridge once (alongside the block-disjointness fact in the Effect preamble) and let each clause cite it, rather than re-narrating it four times.

## OUT_OF_SCOPE

The Open Questions correctly defer transclusion at a shared position, concurrent unsynchronized insertions, transclusion provenance, and post-edit fragmentation — these are raised as questions, not claimed, so nothing here is a scope violation. No action needed.

VERDICT: REVISE
