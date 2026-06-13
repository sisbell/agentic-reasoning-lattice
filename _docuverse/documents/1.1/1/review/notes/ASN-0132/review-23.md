# Review of ASN-0132

I checked the mathematics first. The core definition `countlinks_FTT(q, Σ) ≡ |{a ∈ addressable(Σ) : sat(a, q, Σ)}|`, its well-definedness (finite subset of `dom(Σ.L)` by L-fin), CN-LOC, CN-ENUM, CN-ZERO, CN-STAB, CN-MONO (both the ordinary and retraction wp cases, matched against FL-WP(a)/(b)), CN-RETRACT, and CN-ORPHAN all hold. I re-ran the worked example end to end — the five-link store, `nullified(Σ) = {a₂}`, `count = 2` for `q`, `count = 4` for `q*`, the `q_H`/`q_H'` home-slot cases, and the three-step census-in-motion (`2→3→3→2`) — and every step is arithmetically and structurally correct. All cross-references are to foundation ASNs (0034, 0036, 0043, 0047, 0058, 0086, 0093, 0098, 0121, 0127); no Rule-7 violations.

The note is mathematically converged. The remaining items are the forward-reference and meta-prose accretion the `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: CN-UNIT case (d) is presented as an independent fourth multiplicity, then proven to reduce to (c)

**ASN-0132, CN-UNIT**: the postcondition lists the contribution as independent of "(d) the number of versions into which the documents it touches refract," and the case-(d) prose runs: *"One might fear this mints a distinct link per version. It does not. … Versions are therefore not a fourth independent unit but a special case of the third — the link is one address, stored once, counted once, however many versions refract it."*

**Problem**: The note enumerates four co-equal dimensions but establishes only three are independent — (d) is self-admittedly an instance of (c). The genuinely new content in the paragraph is one fact (forking via J4 performs only K.δ + K.μ⁺ over `V_{s_C}` + K.ρ, so `Σ.L` is link-store-inert under versioning); the remainder re-routes to (c)'s already-given CN-LOC argument. The "One might fear this mints a distinct link per version. It does not." framing is the imagined-concern-then-refutation pattern, and presenting version-refraction as a fourth dimension in the postcondition overstates the independence the proof delivers.

**Required**: Fold (d) into a remark under (c): state the J4 link-store-inertness fact (the substantive part) and note that cross-version surfacing is therefore appearance multiplicity. Drop the "one might fear" framing and the co-equal fourth-dimension listing in the CN-UNIT postcondition.

### Issue 2: Final section ("Cost, and the meaning of asking for a number") restates two boundaries multiple times

**ASN-0132, CN-OBT and the surrounding paragraphs**:
- CN-OBT box tail: *"what it does not carry is on-demand delivery of those links, a separate concern across a separate boundary (out of scope here)…"*
- Immediately following: *"The number lives on the discovery side; carrying a per-item retrieval guarantee across the delivery boundary would be a different and stronger claim."*
- Then on cost: *"the specification is silent: … not a correctness obligation, and is not among the claims below,"* followed by *"…is a matter of cost, and does not bear on what the number is,"* and the implementation note's *"an unrealised opportunity with respect to the cost aspiration."*

**Problem**: The delivery boundary is stated twice in adjacent sentences (two phrasings of "count yields handles, not delivery"). The "cost is out of scope / not a claim" point is then asserted three more times in different words. This is duplicate prose around a forward-deferral to out-of-scope/open-questions territory — exactly the meta-prose-around-forward-references the classifier flags. The one substantive item in the cost material is the implementation observation (Gregory's back end pays full enumeration cost); the rest is scope-restating.

**Required**: State the delivery boundary once. Collapse the cost discussion to a single sentence (cost is a quality-of-service concern, not specified here — see open question 5) plus the one implementation observation. The point that the count specifies a *value*, not a *cost*, needs to be made once.

### Issue 3: CN-MONO claims-table cell carries the full wp derivation

**ASN-0132, Claims Introduced table, CN-MONO row**: the "Statement" cell embeds the complete weakest-precondition formula `wp(create ℓ, Δcount = +1) = sat(ℓ, q, Σ') ∧ ¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))` together with three parenthetical caveats (FL-WP(a) identification, R0a collapse under the unit-depth discipline, FL-WP(b) for retraction links).

**Problem**: The claims table is a summary index; this cell reproduces the body's derivation rather than summarizing the claim. Essay content in a structural slot — the precise reader must read the same wp twice.

**Required**: Reduce the cell to the claim ("absent retraction of counted links the count is non-decreasing; a fresh matching addressable link increments it by 1; K.λ is the only count-changing transition"). Leave the wp formula and its FL-WP(a)/(b)/R0a refinements to the body, where they already appear in full.

## OUT_OF_SCOPE

The note's own Open Questions section already defers the future territory correctly — the V-spec-vs-address-set count invariant (Q1), single-state concurrency discipline (Q2), count caching (Q3), fragmentation/dedup cardinality (Q4), cost-as-planning-primitive (Q5), and federated counting/BEBE (Q6). These are appropriately scoped as open questions, not errors in this ASN, and I have nothing to add to them. The upstream V-to-I resolution that produces a "resolved request" is likewise correctly placed outside the operation.

VERDICT: REVISE
