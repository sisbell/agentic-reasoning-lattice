# Review of ASN-0119

This is a strong note: the imported permutation is used correctly, the two worked transpositions (pivot and swap) check out arithmetically against the postconditions, the link-survival cases are genuinely distinct and concretely worked, the wp analysis isolates the one non-trivial property (footprint contiguity), and the implementation critique stays at the spec level (no META). The defining structural fact — REARRANGE rewrites only `M` and never an I-address — is established and propagated cleanly. The findings below are completeness, labeling, and anti-bloat items.

## REVISE

### Issue 1: E and R frames asserted as prose, not as clauses, while load-bearing

**ASN-0119, "The two streams" / "What is preserved"**: "the entity set `E` and the provenance relation `R` are inert under it, so we suppress `E` and `R` from the state-tuple notation" — and later, in the P3 discharge, "`E = E'`, `R = R'` by the inert `E`/`R` frame."

**Problem**: When lifting REARRANGE_K (which specifies only `M` and frames `C`) into ASN-0047's `(C, L, E, M, R)` state, the note recognizes that the foundation's frame "says nothing about the link store `L`" and so "extended that frame at the outset with an explicit clause — RA6, `Σ'.L = Σ.L`". The identical situation holds for `E` and `R` — ASN-0084's frame names neither — yet they get only the prose word "inert," with no labeled clause. These frames are load-bearing: P3's conjuncts `E ⊆ E'` and `R ⊆ R'` are discharged "by the inert `E`/`R` frame"; the frame-closure rule for P6, P7, P8, S7d, NodeLineage, ActivatedEmission, and L1a all rest on `E` and `R` being frozen; and the J1'★ / P7a discharges turn on `R' = R`. By the note's own lifting discipline (which it applied to `L`), `E' = E` and `R' = R` deserve explicit clauses.

**Required**: Add explicit frame clauses `Σ'.E = Σ.E` and `Σ'.R = Σ.R` (parallel to RA6), or a single labeled frame statement covering both, rather than carrying them as the informal word "inert."

### Issue 2: Claim-label sequence skips RA4

**ASN-0119, body and Claims table**: the RA-series runs RA0, RA1, RA2, RA3, **RA5**, RA6, RA7a, RA7b, RA7c, RA8a, RA8b, RA9.

**Problem**: RA4 appears nowhere — neither in the prose nor the Claims Introduced table; the sequence jumps RA3 → RA5. This reads as either a claim removed during revision without renumbering, or a misassignment. The RA-series is cited throughout (RA0–RA9 are the note's working vocabulary), so a precise reader will look for a dangling RA4 reference.

**Required**: Renumber to a contiguous sequence, or state explicitly why the gap is intentional.

### Issue 3: P4a discharge re-derives a foundation result in full (anti-bloat)

**ASN-0119, "What is preserved"**: "We discharge it by induction on the number `n` of valid composites in a trace, over the *extended* vocabulary ... Base (`n = 0`) ... Step (`n → n+1`) ... New entry ... Pre-existing entry ...", closing with "REARRANGE is simply the `Σ⁺.R = Σ⁻.R` instance, in which the new-entry branch is empty and every entry discharges through `U(n)`."

**Problem**: The full base case (`Σ₀`, `R₀ = ∅`), the J1'★ new-entry branch, and the IH old-entry branch reproduce ASN-0047's own trace-length induction for P4a verbatim in structure. The REARRANGE-specific content is a single fact — `R' = R` makes the new-entry branch vacuous — which the note itself states in its closing sentence. Under the active `review-mode.anti-bloat` classifier, a foundation-result re-derivation occupying a structural proof slot is exactly the essay/re-derivation noise to remove: the induction is generic in the final composite, so the delta is the only new content.

**Required**: Cite ASN-0047's P4a induction and add only the REARRANGE case — its step relies on J1'★ for new entries and the IH for old; REARRANGE's `R' = R` empties the new-entry branch, so the induction extends to the augmented vocabulary unchanged. Drop the restated base case and generic branches.

## OUT_OF_SCOPE

The note's six Open Questions already defer the genuinely-future topics (cross-document boundary-hood under shared transclusion, unserialized concurrent rearrangement, the content-discovery-index invariant under footprint fragmentation, three-region footprint run-structure beyond RA7c, prior-arrangement recoverability, and the closed-form-arithmetic boundary guard). These are correctly scoped as future work, not gaps in this ASN; no additional OUT_OF_SCOPE items to raise.

VERDICT: REVISE
