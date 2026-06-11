# Channel Assignment — ASN-0120 review-15

**Date:** 2026-06-11 03:41

## Issue 1: The worked example's discoverability check ignores the type endset's residence
Reason: Internal fix. The example is the ASN's own construction; the required repair is to stipulate `θ₁`'s source document (a fourth document `D`) within the example's own state assertions and add the one-line `discoverable_from(a, D, Σ')` check, all using machinery (ML9, coverage, `ran(Σ.M(·))`) already in the ASN.

## Issue 2: The stored link value is underdetermined — "fix the canonical representation" is immediately retracted, and ML2 overstates unobservability
Reason: The choice between a deterministic canonical form and coverage-equivalence should be grounded in what the implementation actually stores; the existing implementation note says one sporgl per contiguous I-region but does not establish whether that decomposition is deterministic. The rewording of ML2 and ML9 Fact (a) is then internal.
Gregory question: When CREATELINK stores an endset via `vspanset2sporglset`/`permute`, is the resulting sporgl decomposition deterministic and canonical (e.g., always maximal contiguous I-runs in a fixed order), or can the same resolved I-address set be stored under different decompositions depending on input span structure?

## Issue 3: J1'★'s vacuity is mis-attributed, and ML10's frame omits E and R
Reason: Internal fix. The review identifies the correct discharge (`R' = R` inherited from K.λ and K.μ⁺_L's ASN-0047 frames), and the ASN already cites those elementary transitions; adding `E' = E ∧ R' = R` to ML10 and rerouting J1'★ is derivable from cited substrate facts.

## Issue 4: The discharge of K.μ⁺_L's `a ∉ ran(M(d))` covers only the link-subspace half of the range
Reason: Internal fix. The missing half (`a ∉ dom(Σ.C)` from K.λ's freshness against `dom(C) ∪ dom(L)`, or SD at the intermediate state) is already available from the substrate the ASN cites; the repair is completing a proof step, not gathering new facts.

## Issue 5: `wf`'s prose asserts a depth condition the predicate does not contain
Reason: Deciding whether to add the depth-match conjunct or weaken the gloss turns on what the implementation actually requires of input V-spans — the ASN's partial-span generalization suggests depth-match is not intended, but that should be confirmed against CREATELINK's actual acceptance behavior before the predicate is settled.
Gregory question: Does CREATELINK (via `vspanset2sporglset`/`permute`) require an input V-span to sit at the document's common content depth, or does it resolve spans at other depths and spans containing inactive/deleted positions, emitting sporgls only for the active positions?

## Issue 6: ML1's covering-surplus argument applies `#E` where it is undefined
Reason: Internal fix. The correct store-membership argument (case split via LP-Sub and `F`'s `#E = 2`) already appears verbatim in ML9 Fact (a); the repair is replicating that careful version at ML1 and in the worked example.

## Issue 7: Meta-prose accretion (anti-bloat)
Reason: Internal fix. Purely editorial: deleting/folding the flagged sentences, correcting the claim count to eleven, and relocating the Gregory CREATELINK divergence into a blockquoted implementation note require no facts beyond the ASN's own text.
