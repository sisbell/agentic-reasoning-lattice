# Review of ASN-0107

## REVISE

### Issue 1: "Insertion shifts the following positions" contradicts the note's own extension semantics

**ASN-0107, "How the Count Changes: Content Added" (boundary paragraph)**: "If `W` is expressed as raw V-position ranges and an insertion shifts the following positions, then the literally-identical positional query resolves, after the insertion, to *different* I-addresses — a different request in effect, even though it reads the same."

**Problem**: This attributes a fixed-position image change to *insertion*, but the note's formal apparatus does not permit insertion to shift prior positions. The operation that adds content is K.μ⁺ (ArrangementExtension), whose contract preserves every prior position's image: `(A v ∈ dom(Σ.M(d)) : Σ'.M(d)(v) = Σ.M(d)(v))` (ASN-0047; LP9, ASN-0098). The note's own D2 *extension* clause relies on exactly this — "for every `v ∈ Wᵢ ∩ dom(Σ.M(d_q))` the image `Σ'.M(d_q)(v) = Σ.M(d_q)(v)` survives." So under K.μ⁺ a literally-identical positional query resolves the surviving positions to the *same* I-addresses, never different ones. The only transition that moves the image of a *fixed* V-position is K.μ~ (reordering) — which is precisely what D2's reordering clause isolates. A mid-stream insert in this model is realized as extension *plus* reordering (D-SEQ contiguity forbids changing `[1,2]`'s image under pure extension), so the position-image movement belongs to the reordering component, not the insertion.

**Required**: Re-attribute the caution to reordering (K.μ~), or state explicitly that the warning concerns raw positional *notation* at an implementation layer that renumbers — distinct from the K.μ⁺ extension semantics the rest of the note (D2, A1b, LP9) depends on. As written it conflicts with the extension-preserves-prior-images guarantee used elsewhere.

### Issue 2: R2's definition of `D` overstates under intra-document content sharing

**ASN-0107, R2 (ContentDeletionUnbounded)**: "Let `D` be the set of I-addresses that leave the resolved part `Qᵢ` through the contraction — the images of the dropped positions in slot `i`".

**Problem**: The leading clause ("I-addresses that leave the resolved part `Qᵢ`") and the appositive ("the images of the dropped positions") are not the same set when a single I-address is reached by more than one consulted V-position in the same document — admitted here (P2, A2 both rely on shared I-addresses; M13/M14, ASN-0058). If a dropped position's image is also the image of a *retained* consulted position, that address does **not** leave `Qᵢ`, yet it is among "the images of the dropped positions." R1 handles exactly this with its (P-uniq) clause; R2's appositive drops the analogous condition, so `D` — and the derived `k` — can be overstated. The downstream decrement ("whose only slot-`i` reach ran through some removed endpoint") is phrased precisely, but the `D`/`k` definitions feeding the bound are not.

**Required**: Define `D` as the I-addresses with no surviving consulted preimage in slot `i` after contraction (i.e., every consulted position mapping to the address was dropped), matching R1's (P-uniq) treatment, so the appositive agrees with the leading definition.

## OUT_OF_SCOPE

None. The note stays within counting semantics and correctly defers retrieval (FINDLINKS), pagination, creation, and traversal.

VERDICT: REVISE
