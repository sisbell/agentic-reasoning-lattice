# Review of ASN-0121

## REVISE

### Issue 1: FL-DEC proves `sat` decidable but not the addressability filter
**ASN-0121, FL-DEC**: "Hence sat — a conjunction of four decidable tests — is decidable, and findlinks(q, Σ) ⊆ dom(Σ.L) is finite by L-fin … so it is computed by deciding sat over the finitely many addressable links."
**Problem**: The proof establishes only that `sat` is decidable per link and that the result is finite. But `findlinks(q, Σ) = { a ∈ addressable(Σ) : sat(a, q, Σ) }` and `addressable(Σ) = dom(Σ.L) \ nullified(Σ)`. "Deciding sat over the finitely many addressable links" presupposes the addressable filter is itself computable — i.e. that `nullified(Σ)` membership is decidable. That step is never stated or derived. Computability of the *filter* is load-bearing for the "computable set" claim and is distinct from `sat`-decidability.
**Required**: Add the missing step. It is dischargeable directly: `L_R^Σ` is selected by CoverageEqualityDecidable (type-coverage matching the retraction class), each retraction tuple's to-coverage `G'` is a finite span-set, and `a ∈ coverage(G')` is decidable by T2 — so `nullified(Σ)` is computable and `addressable(Σ)` enumerable. This is exactly the computability ASN-0086 already records for its ActiveSubset/`nullified`; cite it rather than leaving the filter implicit.

### Issue 2: FL-WP claims K.λ is "the unique result-changing transition" then omits the fresh-retraction-link entry case
**ASN-0121, FL-WP / "The only result-changing transition"**: "K.λ is the unique result-changing transition. We compute its weakest precondition in the two cases that matter — the entry of a newly created link, and the survival of an existing match under a retraction-bearing K.λ."
**Problem**: The framing promises "the entry of a newly created link," but case (a) explicitly restricts to a *fresh ordinary* link (`coverage(Θ) ∉ [coverage(R)]`), precisely to obtain `L_R^{Σ'} = L_R^Σ`. The entry of a fresh *retraction* link (non-ordinary, type-coverage in `[coverage(R)]`) into the answer is therefore covered by neither (a) nor (b), yet it is a genuine K.λ result-changing scenario: such a link can satisfy a type-`R` query and enter `addressable(Σ')` unless it self-nullifies. Its wp differs from (a) because that same K.λ grows `nullified` (and may self-retract), so the addressability conjunct unfolds as `ℓ ∉ coverage(G_own') ∧ ℓ ∉ nullified(Σ)` rather than the (a) form. Asserting K.λ is the *unique* result-changing transition and then leaving one of its result-changing sub-cases unanalyzed is an incompleteness.
**Required**: Either generalize case (a) (or add a case (c)) to compute the wp for a fresh retraction-typed link's entry — carrying the self-retraction term — or narrow the framing from "the entry of a newly created link" to "the entry of a newly created *ordinary* link" and explicitly scope the retraction-link entry case out with a one-line justification (e.g. that a retraction link's own discoverability is not a target guarantee).

## OUT_OF_SCOPE

(none beyond the Scope list; the ASN correctly confines itself to FINDLINKSFROMTOTHREE and raises version/time-scoped and federation reach as Open Questions rather than claims.)

VERDICT: REVISE
