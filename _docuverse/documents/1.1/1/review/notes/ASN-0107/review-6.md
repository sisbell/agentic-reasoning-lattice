# Review of ASN-0107

## REVISE

### Issue 1: Worked-example R2 attribution contradicts the link table

**ASN-0107, A Worked Instance (discovery contraction paragraph)**: "the two-unit drop is R2 with `k = 2` — the I-address `a₁` was reached in the from-slot by exactly `ℓ₁` and `ℓ₂` (each only through `a₁`), while `ℓ₃` clung to the surviving `a₂` (R3)."

**Problem**: The claim "`a₁` was reached in the from-slot by exactly `ℓ₁` and `ℓ₂`" is false given the example's own table. `ℓ₃`'s from-endset is `{a₁, a₂}` (two spans), so `a₁ ∈ coverage(Σ.L(ℓ₃).e₁)` — `ℓ₃` *also* reaches `a₁` in the from-slot. Three links reach `a₁`, not two. What distinguishes `ℓ₁`, `ℓ₂` is that their from-coverage is *only* `{a₁}`, whereas `ℓ₃` has an alternate reach `a₂`. The word "exactly" is wrong.

**Required**: Restate as "`a₁` was reached in the from-slot by `ℓ₁`, `ℓ₂`, and `ℓ₃`, but only `ℓ₁` and `ℓ₂` reach it *exclusively*; `ℓ₃` clung to the surviving `a₂` (R3)." Then reconcile the `k` label with Issue 2.

### Issue 2: R2 defines `k` two incompatible ways

**ASN-0107, R2 (ContentDeletionUnbounded)**: "Contracting an arrangement so as to remove an endpoint that `k` distinct links reach can drop up to `k` links from the discovery count... The per-operation bound is *not* one; it is the number of links whose only consulted reach ran through the deleted entry."

**Problem**: The first clause sets `k` = number of links that *reach* the endpoint (correct as an upper bound: drop ≤ reaching-links). The gloss then equates the bound with "links whose *only* consulted reach ran through the deleted entry" — a different, smaller quantity that is the *exact* drop, not the bound. The two readings of `k` diverge precisely in the worked example: reaching-links for `a₁` is 3, only-reach-links is 2, actual drop is 2. The example's "`k = 2`" silently adopts the second reading while R2's headline adopts the first.

**Required**: Pick one definition of `k` and use it consistently. Either keep `k` = reaching-links and state the bound as "drop ≤ k, with equality iff each reaching link's only consulted reach is the deleted entry," or define `k` = exclusively-reaching links and state "drop = k exactly." Then label the worked example to match.

### Issue 3: A2 conflates discoverability (one-slot) with the count (three-slot conjunction)

**ASN-0107, A2 (TransclusionDiscoverability)**: "makes every link whose coverage includes those I-addresses discoverable from `d_new` (LP16)... The discovery count of a query against `d_new` rises by the links thus shared."

**Problem**: Discoverability requires only one slot's coverage to meet the query (`discoverable_from` is an existential over slots). But `sat` — and therefore the count — is *conjunctive* across all three slots (this is the ASN's own P1/`sat` definition). A link made discoverable through one transcluded slot need not be *counted*, because its other two slots may not be satisfied by the query against `d_new`. The sentence asserts the count rises by all shared links, which does not follow from LP16. This is exactly the count-vs-discoverability distinction the ASN is built to police, so the slippage is load-bearing.

**Required**: Either qualify the query (e.g., "for a query whose to- and type-parts are unconstrained, `Q₂ = Q₃ = T`"), restate the claim as a discoverability claim with a count *lower bound* conditioned on the other slots, or derive precisely which shared links become counted.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored per-slot requests across separately-evolving documents
**Why out of scope**: The first Open Question already names this as future territory; the ASN correctly fixes a single resolution document for the discovery anchoring and a single fixed `Q` for the existence anchoring.

### Topic 2: Agreement between `num` and the cardinality returned by the retrieval operation
**Why out of scope**: This belongs to FINDLINKS / ASN-0099 (returning the links), explicitly excluded by the scope note and flagged as an Open Question.

VERDICT: REVISE
