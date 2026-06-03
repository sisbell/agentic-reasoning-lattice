# Review of ASN-0098

## REVISE

### Issue 1: Forward/backward reference loop between LP-Fin and the `tight` definition
**ASN-0098, "Boundary and Width Behaviour"**: LP-Fin's hypothesis reads "ℓ = δ(n, #s) for some n ≥ 1 (the displacement-shape condition shared with the tight definition below)", and the `tight` definition — stated *after* LP-Fin and LP12b — reciprocates with "together with the canonical shape ... this discharges LP-Fin's hypotheses."
**Problem**: The canonical condition `ℓ = δ(n, #s)` is fully self-contained in LP-Fin; the parenthetical "(the displacement-shape condition shared with the tight definition below)" adds no reasoning and only cross-links to a definition placed downstream, which then links back. This is exactly the "multiple paragraphs deferring to the same location" / forward-reference accretion pattern this review mode targets. A reader hitting LP-Fin must jump ahead to a definition that depends on LP-Fin.
**Required**: Either move the `tight` definition above LP-Fin (so the motivating notion precedes the lemma it relies on), or delete the parenthetical cross-link. The canonical shape needs no annotation about its reuse elsewhere.

### Issue 2: Claims-table entries carry derivation prose instead of statements
**ASN-0098, "Claims Introduced" table**: The LP12b row's Statement column contains "derived via LP-Fin Corollary applied at X = s_C to give coverage(Σ.L(a).eᵢ) ∩ dom(Σ.L) = ∅", and the LP-Fin row contains "Covers only the canonical case (the tightness domain, per the tight definition's canonical-form requirement)."
**Problem**: The table's Statement column is a structural slot for the claim itself; these entries instead embed a mini-derivation (LP12b) and a scope-justification deferral (LP-Fin). Essay content in a structural slot is the noise pattern flagged for this note. The derivation belongs in the LP12b body (where it already appears); the scope caveat belongs in the LP-Fin prose.
**Required**: Reduce both rows to a bare statement plus status, matching the terseness of rows like LP2, LP9, LP10.

## OUT_OF_SCOPE

### Topic 1: Interval finitude for non-canonical spans
LP-Fin and the tightness machinery cover only canonical spans (`ℓ = δ(n, #s)`); general well-formed spans with `#ℓ ≠ #s` are not addressed. The table already marks this explicitly, so it is a deliberate boundary, not an error — finitude/discoverability for non-canonical endsets is future territory.

VERDICT: REVISE
