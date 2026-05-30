# Review of ASN-0084

This note carries the `review-mode.anti-bloat` classifier. The mathematics is sound — I traced all five worked examples and checked the well-definedness, permutation, and run-decomposition proofs; the displacement arithmetic, tiling, and merge computations all hold. My findings are accumulated meta-prose and dead derivations that the precise reader must work around.

## REVISE

### Issue 1: Multiset-of-I-addresses preservation is a dead derivation
**ASN-0084, "Definition — ArrangementRearrangement" and "S5-multiplicity"**: "The multiset of I-addresses is also preserved: since π is a bijection, for each I-address a, the preimage {v : M(d)(v) = a} ... *Forward inclusion* ... *Backward inclusion* ... The multiplicity of a is therefore identical in M(d) and M'(d)." Then later: "S5 (unrestricted sharing) is a permission rather than an obligation; the multiset-of-I-addresses preservation derived above ... preserves any pre-existing sharing pattern."

**Problem**: This two-paragraph forward/backward-inclusion proof establishes multiplicity preservation, but its sole consumer is S5, which the note itself classifies as "a permission rather than an obligation." No invariant requires multiplicity preservation: R-RI uses only the *set* equality `ran(M'(d)) = ran(M(d))`, and R-BLK uses only bijectivity. The derivation advances no proof obligation.

**Required**: Delete the multiset/multiplicity derivation and the S5-multiplicity paragraph. Retain only the set-level `ran(M'(d)) = ran(M(d))` derivation that R-RI consumes. If S5-preservation must be mentioned, one sentence ("S5 is a permission; bijectivity of π preserves any sharing pattern") suffices.

### Issue 2: R-NS proof re-derives what the frame condition already supplies
**ASN-0084, R-NS proof**: "the non-S clause of the bijection definition ... stipulates π(v) = v on this domain; combined with the frame condition, this stipulation is consistent with the rearrangement defining equation M'(d)(π(v)) = M(d)(v) — substituting π(v) = v yields M'(d)(v) = M(d)(v), already supplied by the frame condition."

**Problem**: The clause after the em-dash proves nothing — it substitutes `π(v) = v` to recover an equation it concedes is "already supplied by the frame condition." This is a consistency check on a definitional stipulation, presented as proof content. The first sentence ("R-FRAME-P(a)/R-FRAME-S(a) gives `M'(d)(v) = M(d)(v)` directly") already discharges the lemma.

**Required**: Stop the proof after "the non-S clause ... stipulates π(v) = v on this domain." Drop the redundant substitution sentence.

### Issue 3: R-PPERM "Remark (uniqueness scope)" is a non-advancing aside
**ASN-0084, R-PPERM Remark**: "When the pre-state arrangement M(d) is injective on V_S(d) ... π is the unique bijection ... When M(d) has repeated I-addresses (S5 ...) bijections that permute positions within each fibre ... π is then unique only up to that equivalence class of fibre-permutations. ... This scope depends only on the fibre structure of M(d), not on the cut count."

**Problem**: The ASN never claims or uses uniqueness of π — the arrangement-rearrangement definition and every consumer (R-RI, R-BLK) require only that *a* bijection with the defining property exists, and R-PPERM exhibits the canonical one. This remark is an essay on a property the specification does not need; the closing sentence ("depends only on the fibre structure ... not on the cut count") is filler. It is the kind of prose the reader must skip to follow the argument.

**Required**: Delete the remark, or compress to one sentence if the canonical-choice point genuinely matters downstream (it does not appear to).

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
Correctly deferred to the Open Questions. The 3/4-cut restriction (CS1) is a deliberate scope boundary, not a gap.

### Topic 2: Operational recovery of the canonical (maximal) partition from B'
The note defers the merge-to-maximal procedure and its confluence to a future ASN (CanonicalRunDecomposition, Open Questions). Appropriate — B' validity is established; canonicalization is new territory.

VERDICT: REVISE
