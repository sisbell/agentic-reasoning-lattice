# Review of ASN-0108

This is a meticulous note. The W2 weakest-precondition analysis (identity vs. offset cursor, with the genuinely-weakest formula `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` and the strict three-way nesting), the W9b cumulative-inflow multiplicity bound, and the dozen concrete walks are all sound and I verified them in detail. The findings below are a real depth gap in the central guarantee plus three precision/bloat items.

## REVISE

### Issue 1: W5's sufficiency argument for the central coherence guarantee is a sketch
**ASN-0108, W5 (OrderStability)**: "Chaining these stable cuts across the pass delivers every both-states tail matcher exactly once: no skip, no re-delivery."

**Problem**: The paragraph establishes the *per-transition* cut-stability cleanly (no both-states link crosses the cut at `c`), then asserts the *whole-pass* conclusion — delivery, exactly once — in a single "chaining" sentence that presents itself as the proof. But neither half of that conclusion follows from cut-stability alone:

- *No-skip* (delivery) is not a property of cut-stability per se. Clause 1 keeps a both-states tail matcher *in* `After`; it does not by itself deliver it. Delivery is forced only by the short-window completion that makes `After(final cursor) = ∅` — i.e. W9's local fact + global guarantee. In a non-terminating pass (infinite inflow) a both-states tail matcher can sit in `After` forever, never delivered, yet not "skipped" (no completion event) — a contingency W5's phrasing obscures. So "no skip" is *conditional on termination*, and that dependence is invisible in W5.
- *No-re-delivery* (exactly once) at the pass level is the cross-call induction "a delivered link stays at or below every later cursor" — which is actually carried out in W9b ("By induction along the cursor sequence, applying clause 1 at each held cursor `c_n` ... that link stays at or below every later cursor"). W5 only states the per-transition version ("no already-delivered both-states link ... has risen into it") and chains it informally.

So the proof of the central law is in fact distributed across W9 (termination → delivery) and W9b (induction → no re-delivery), but W5 routes through neither — it reads as self-contained when it is not.

**Required**: Either complete the argument in W5 (state that no-re-delivery is the cursor-advance induction and no-skip follows because clause 1 keeps each surviving both-states tail matcher in `After` until the short-window signal forces `After = ∅`, hence it must have exited by delivery), or signpost explicitly to W9b's induction and W9's `After(final) = ∅` step. A two-clause pointer suffices — this is a precision fix, not a request for prose.

### Issue 2: Forward-preview accretion in the `Match` definition
**ASN-0108, "State, the Matching Set..."**: "one further structural fact — the `K.λ`-increment shape of `Match`, by which link creation grows the matching set by a single disjoint element — enters once, in W6a's set-level bridge, and is introduced there:"

**Problem**: This previews a fact's content here and then derives it in W6a — double-handling. The clause "enters once, in W6a's set-level bridge, and is introduced there" is document-organization meta-prose (where a fact lives, that it has a single use site), exactly the forward-reference accretion the anti-bloat classifier targets. The two genuine standing handles are M-fin and M-mut; the K.λ-increment is used once and is properly introduced (with the F-V/F-LAMBDA bridge) at W6a.

**Required**: List M-fin and M-mut as the standing handles; drop the preview clause and let W6a introduce the K.λ-increment at its sole use site.

### Issue 3: W6 restates the injectivity caveat as an orthogonal digression
**ASN-0108, W6**: "Allocation-monotonicity is their only *behavioural* divergence on the windowing laws; it is not their only difference, however — the matched-content key is not injective on `Match` unaided and must be composed with the address tiebreaker to satisfy W0/W1, where the link-address key satisfies them alone."

**Problem**: W6's claim is about allocation-monotonicity. The injectivity point was already established in the "What `κ` is" / W1 discussion ("the bare content key is **not injective on `Match`** ... must be composed with a permanent tiebreaker"). Re-raising it here — only to bound the divergence claim — does not advance W6's reasoning; a reader following the append-at-tail argument has to recognize and skip a restated earlier point.

**Required**: Drop the second half of the sentence; "Allocation-monotonicity is their ... divergence on the windowing laws" stands without re-litigating injectivity.

### Issue 4: W6a's functional characterization excludes a key it claims to cover
**ASN-0108, W6a**: "under *any* key that is a function of `(address, matched-content boundary)` — which covers the address key `κ(a) = a`, Gregory's matched-content I-address key, and the content-position key alike"

**Problem**: The note uses "boundary" throughout to mean a content *I-address* (e.g. "the least I-address covered," "the bare boundary-only key"). The content-position key is keyed on the *current V-position*, which is a function of the arrangement `Σ.M(d_q)`, not of any I-address boundary — so it is not "a function of `(address, matched-content boundary)`," yet it is listed as covered. The *conclusion* (creation disturbs nothing) does hold for it, but via the M-frame, as the justification ("no matched endpoint moves" because M and C are framed) correctly notes. The stated functional form and the justification disagree on whether the position key qualifies.

**Required**: Either broaden the functional form to "(address, matched-content boundary or position)" or state the form as "any key reading only `(address, Σ.M(d_q), Σ.C)`," so the content-position key is genuinely subsumed.

## OUT_OF_SCOPE

### Topic 1: Type-refinement of the matching set
**Why out of scope**: The note adopts `Match = findlinks_V(W, d_q, Σ)` (the full discoverability reading) and explicitly delegates "any refinement by the query's type part (ASN-0086) — to query construction, outside this note." Whether a type-class intersection (which grows monotonically by R3) interacts with M-mut/the K.λ-increment is a query-construction matter, correctly left out. The W6a bridge is exact for the in-scope `Match`.

### Topic 2: Cross-call completeness over a mutating set, and multi-document keying
**Why out of scope**: The stitched-completeness invariant across successive windowed states, eventual delivery under a non-allocation-monotone key, the empty-vs-irrecoverable distinction for non-permanent keys, and a globally-monotone key across independent per-document allocators are all genuinely new territory — and the note already enumerates them as Open Questions 1–4. Not errors here.

VERDICT: REVISE
