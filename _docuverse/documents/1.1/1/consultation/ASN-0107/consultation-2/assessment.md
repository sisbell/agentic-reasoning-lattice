# Channel Assignment — ASN-0107 review-2

**Date:** 2026-06-07 21:44

## Issue 1: `Q = (T, T, T)` does not count every stored link
Reason: The fix is internal — the same paragraph already states the correct rule ("satisfied by any link with a *non-empty* i-th endset"), and the algebra it cites (L3, `Endset = 𝒫_fin(Span)`) is already in the dependency base. Striking the contradictory clause and stating the e₁/e₂-non-empty restriction is pure self-consistency repair derivable from the ASN's own definitions.

## Issue 2: A1's justification is false
Reason: The fix is internal — the correct reasoning (K.α adds no link to `dom(Σ.L)`, leaves `coverage` and fixed `Q` unchanged, so this is just E3) is already present in the ASN, and the orphan/resurrection mechanism (LP17/LP18/L9) the reviewer invokes is in the cited ASN-0098. No design intent or implementation evidence is needed to swap a false parenthetical for the E3 argument the ASN already proves.

## Issue 3: The reordering worked instance is incompletely computed and inconsistent
Reason: The fix is a pure recomputation of the worked example under the ASN's own `sat` definition and D2-reordering clause; both correction options (set `W₂,W₃ = T`, or carry the three-slot count to `num_disc = 0`) are mechanical arithmetic over claims already stated. Fully internal.

## Issue 4: R1's minimal-decrement case omits a precondition
Reason: The fix is internal — adding the "last consulted V-position mapping to that I-address" precondition follows directly from content-sharing (M13/S5, cited from ASN-0058/0036) and the ASN's own `Qᵢ(Σ)` resolution definition. No new design intent or code evidence is required to tighten R1 into the genuine `k=1` floor of R2.
