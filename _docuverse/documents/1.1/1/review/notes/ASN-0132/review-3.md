# Review of ASN-0132

## REVISE

### Issue 1: CN-MONO cites the wrong increment lemma — and does so inconsistently with its own E-INV correction

**ASN-0132, CN-MONO**: "This is the cardinality of FL-MON (ASN-0121) together with the K.λ increment (F-LAMBDA, ASN-0127): link creation is the only transition that can add to the satisfying set, and it adds at most one address, which by freshness was not already present."

**Problem**: F-LAMBDA (ASN-0127) is the increment lemma for the *slot-agnostic, addressability-unaware* operation `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}` — quantified over `dom(Σ.L)`, not `addressable(Σ)`, and using `matches` (some slot meets an I-set), not the four-slot `sat`. The count `countlinks_FTT` is built on `findlinks_FTT`/`sat` over `addressable(Σ)`. F-LAMBDA therefore cannot deliver the count's increment: it has no nullification filter, so it cannot express the load-bearing subtlety the ASN itself then derives — that a *fresh ordinary* link may be born already covered by a standing retraction tuple (`¬(E (b, F', G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`). That conjunct comes from FL-WP(a) (ASN-0121), which the ASN correctly cites three sentences later.

This is the *same* defect the ASN explicitly disavows for the parallel pre-existing-link-stability step two sentences on: "an earlier draft mis-attributed [it] to E-INV, ASN-0127 — which speaks of the slot-agnostic `matches(a, I, ·)` predicate, not the four-slot `sat`, and which says nothing of addressability at all, so it delivers neither half of what the step needs." F-LAMBDA shares both disqualifying properties (slot-agnostic, addressability-silent). The E-INV citation was fixed; the structurally identical F-LAMBDA citation was left standing in the same argument.

The underlying facts the gloss actually needs are: (i) "K.λ is the only transition that grows the satisfying set" — from F-PRES + CN-STAB; (ii) "K.λ adds at most one fresh address" — from K.λ's effect clause (ASN-0093); (iii) the four-slot increment with the retraction-coverage condition — from FL-MON / FL-WP(a) (ASN-0121). None of these is F-LAMBDA. The detailed derivation that follows is correct and self-contained; only this supporting citation is misattributed.

**Required**: Replace "the K.λ increment (F-LAMBDA, ASN-0127)" with the correct basis — K.λ's single-fresh-address effect (ASN-0093) for "adds at most one address," and FL-MON / FL-WP(a) (ASN-0121) for the four-slot increment — so the citation is consistent with the E-INV correction and with the FL-WP(a) appeal already made in the same paragraph.

## OUT_OF_SCOPE

No additional out-of-scope items. The ASN's own Open Questions correctly defer the content-identity-vs-arrangement-position invariant, the cross-inquiry concurrency discipline behind CN-ENUM's "single state" qualifier, count caching, fragmented-endset deduplication, the count-vs-enumeration cost relationship, and federated counting (BEBE). Each is genuinely future territory, not an error here, and the ASN cites rather than rebuilds ASN-0121's match semantics and ASN-0127's existence/discovery taxonomy.

VERDICT: REVISE
