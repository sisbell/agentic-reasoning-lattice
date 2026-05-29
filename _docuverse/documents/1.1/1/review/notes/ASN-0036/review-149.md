# Review of ASN-0036

This ASN is in strong formal shape — S0–S5, the S7 family, the S8 singleton-partition theorem, the D-CTG/D-CTG-depth/D-SEQ chain, and the insertion-position predicates all carry complete, case-exhaustive proofs (the within/across-subspace split in S8 and the four-step D-SEQ assembly are genuinely rigorous, with boundaries — empty arrangement, depth m=2 vs m≥3, j<m vs j=m — all addressed). The findings below are residual anti-bloat per this cycle's `review-mode.anti-bloat` mandate, not correctness gaps.

## REVISE

### Issue 1: Forward-reference prose occupying a postcondition slot
**ASN-0036, ValidFirstInsertionPosition Formal Contract, postcondition (d)**: "In any state where `V_1(d)` is non-empty at depth `m`, S8-depth fixes the text-subspace depth at `m`, and validity of further insertion positions is governed by `ValidInsertionPosition(d, v)`."
**Problem**: This is not a postcondition of the `ValidFirstInsertionPosition` predicate. It is a remark about a *different* state (after `V_1(d)` becomes non-empty) and a *different* predicate (`ValidInsertionPosition`). It states nothing about what is true of `(d, v, m)` when the predicate holds. This is exactly the flagged pattern — essay/cross-reference content placed in a structural slot, which a precise reader must skip past to read the actual postconditions (a)–(c). Postconditions (a), (b), (c) are genuine; (d) is a transition narrative.
**Required**: Remove (d) from the postcondition list. If the empty→non-empty handoff needs stating, it belongs in surrounding prose, not in the predicate's formal contract.

### Issue 2: Non-derived design-stance essay deferring to out-of-scope material
**ASN-0036, "The document as arrangement," closing Remark**: "This motivates a design stance the strand model adopts but does not formalize here... A formal decidability statement would border on the out-of-scope document-creation-and-lifecycle cluster; we record the stance as motivation rather than a derived guarantee."
**Problem**: This paragraph advances no claim, formal contract, or derivation. It records a stance it explicitly declines to formalize and defers the formalizable content to an out-of-scope cluster — the "essay content + downstream deferral" accretion pattern this cycle is meant to surface. The surrounding section's assertion that identically-rendering documents "remain distinct documents with independent ownership, and independent edit histories" additionally reaches into ownership and versioning, both explicitly out of scope for this ASN.
**Required**: Trim the closing Remark. The legitimate consequence ("a document is its arrangement, not its content"; identically-rendering documents may map to different I-addresses) can stand on the Nelson-grounded statement already given; drop the deferral sentence and the ownership/edit-history overreach.

## OUT_OF_SCOPE

None beyond the ownership/versioning phrasing noted in Issue 2, which the ASN should simply not assert rather than defer.

VERDICT: REVISE
