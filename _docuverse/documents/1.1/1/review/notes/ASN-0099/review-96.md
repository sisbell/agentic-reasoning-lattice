# Review of ASN-0099

I checked the proofs and worked example for rigor, and ran the additional anti-bloat pass the note's classifier requests. The core mathematics is sound: the two-phase factoring (F12), the match-predicate algebra (F1, F13, F20–F20a), the wp analyses (F21–F23), and the six-query worked example all check out against their cited foundations, and the depth standards (non-trivial wp, concrete example, derived consequences) are met. The findings below are confined to redundant prose/structure the anti-bloat pass targets.

## REVISE

### Issue 1: F22 carries a redundant parallel citation for range invariance
**ASN-0099, F22 (ReorderingDiscoverabilityInvariance), derivation**: "LP11 (ReorderingBijection, ASN-0098) gives `ran(Σ'.M(d)) = ran(Σ.M(d))` for *every* such π, so range invariance is independent of which π is chosen. Equivalently J3/K.μ~-RANGE (ASN-0047) supplies the same range equality, and A1a gives `Σ'.L = Σ.L`."

**Problem**: LP11 has already established the exact fact the derivation uses (range invariance under every admissible π). The clause "Equivalently J3/K.μ~-RANGE (ASN-0047) supplies the same range equality" is a second route to a fact already in hand; the word "Equivalently" flags it as non-advancing. This is the redundant-citation pattern the anti-bloat pass names — the reader must skip the aside to follow the derivation. (A1a's `Σ'.L = Σ.L` in the same sentence is load-bearing and should stay.)

**Required**: Drop the "Equivalently J3/K.μ~-RANGE…" clause, keeping the single LP11 citation and the A1a clause.

### Issue 2: `findlinks_V` is entered twice in the Claims-Introduced table
**ASN-0099, Claims Introduced table**: row `findlinks_V(R, d, Σ)` — "Two-phase composite `findlinks(image(R, d, Σ), Σ)` (operation, defined by F12)" — and row `F12` — "TwoPhaseFactoring: `findlinks_V(R, d, Σ) ≡ findlinks(image(R, d, Σ), Σ)`".

**Problem**: Both rows state the same definition in the same words, and the first even cross-references the second ("defined by F12"). This is the same-thing-twice pattern. Other operation definitions in the table (e.g. `findlinks`, `image`) get a single row; only `findlinks_V` is duplicated.

**Required**: Collapse to one entry — either keep the `findlinks_V` object row and drop the F12 row, or keep F12 as the defining-claim row and drop the standalone object row.

## OUT_OF_SCOPE

### Topic 1: Type-endset-only matches as backlinks
F1's slot-uniform existential means a link whose *only* overlap with the query is at its type endset (slot 3) is reported as "found here." Whether that is the desired reader semantics for backlink discovery is a design question the ASN defers to L7 (directional significance lives in the type). This is a semantics refinement, not an error in this ASN.

VERDICT: REVISE
