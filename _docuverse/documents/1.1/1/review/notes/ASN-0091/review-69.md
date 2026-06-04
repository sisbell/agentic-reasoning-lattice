# Review of ASN-0091

The mathematics is sound. I verified the abstract class derivations (RE-C, RE-ran, RE-μ, RE-proj transport, S2-at-abstract-level), the ChainDisjointAdjacency inline lemma, and all four worked examples at the value level — the run-cardinality witnesses (frag 1→2, coal 3→2, eq 2→2) and the bijection-non-uniqueness trace all check out, and the RA-adm reachability discharge (K.μ~-valid composite / empty-composite split) is correct. The findings below are anti-bloat, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Over-determination commentary that does not advance the claim
**ASN-0091, "Subspace Frame (REARRANGE_K-specific)"**: "The two conjuncts are mutually reinforcing under RA-π: substituting π(v) = v into Σ'.M(d)(π(v)) = Σ.M(d)(v) gives Σ'.M(d)(v) = Σ.M(d)(v), so the first conjunct alone (sourced from R-PPERM/R-SPERM) implies the second, which R-FRAME-P/S(a) records independently."
**Problem**: This paragraph establishes that one source of RE-sub makes the other redundant — pure provenance commentary about the robustness of the dual sourcing. It does not advance RE-sub; the claim is already fully stated and sourced in the preceding two sentences. The same over-determination style appears in the abstract S2 derivation, where "π's surjectivity supplies the existence of v and its injectivity supplies the uniqueness" is immediately followed by the redundant restatement "the inverse π⁻¹ is itself well-defined only because π is a bijection."
**Required**: Delete the "mutually reinforcing" paragraph (the dual sourcing in the two preceding sentences stands on its own) and the trailing inverse-well-definedness clause in the S2 paragraph.

### Issue 2: Defensive asides stating what a discharge does *not* need
**ASN-0091, "REARRANGE_K Realises..."**: "(S5/UnrestrictedSharing is a state-independent existential theorem of the model class, not a per-state predicate, so it holds at Σ' for the same reason it holds at every state, with no appeal to RA-π.)" — and "Standing premise...": "Under this premise we extend reachability across the REARRANGE_K step rather than assume it of Σ'."
**Problem**: Both passages spend their force describing what the argument avoids ("with no appeal to RA-π", "rather than assume it of Σ'") rather than what it establishes. The positive content (S5 holds at every state; reachability extends one step) is complete without the negative aside, which is the defensive-justification pattern this classifier targets.
**Required**: Trim to the positive statements — "S5 holds at Σ' as a state-independent theorem of the model class"; "we extend reachability across the REARRANGE_K step."

## OUT_OF_SCOPE

### Topic 1: Whether two fragments jointly reconstitute a same-source transcluded span
**Why out of scope**: The ASN correctly flags this in RE-trans ("Whether the two fragments jointly reconstitute the original source span... is not established here") and routes it to the Open Questions. It is genuinely new territory, not a gap in this ASN's claims.

VERDICT: REVISE
