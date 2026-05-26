# Review of ASN-0077

## REVISE

### Issue 1: O11' non-empty branch — cross-subspace exclusion implicit
**ASN-0077, Claim O11' derivation, non-empty case**: "the precondition fixes `v_ℓ = shift(max(V_{s_L}(d)), 1)`, which strictly exceeds every existing link-subspace V-position by TA-strict (ASN-0034) and so lies outside `dom(M(d))`."

**Problem**: TA-strict yields `v_ℓ > max(V_{s_L}(d))`, which excludes `v_ℓ` from `V_{s_L}(d)` only. The step "and so lies outside `dom(M(d))`" requires further argument because `dom(M(d)) = V_{s_C}(d) ∪ V_{s_L}(d)` (by S3★-aux), and the TA-strict bound says nothing about `V_{s_C}(d)`. The derivation actually needs: `v_ℓ` has `subspace = s_L` (by OrdShiftHom (b), since shift preserves subspace), every `w ∈ V_{s_C}(d)` has `subspace = s_C` (by S3★-aux's classification combined with S8a), and `s_L ≠ s_C` (by SC-NEQ). The argument is real and the conclusion is correct, but the cross-subspace step is left implicit. Since O11' is a labelled claim whose derivation downstream proofs may cite, the gap should be closed.

**Required**: Either (a) complete the derivation by citing OrdShiftHom (b) + SC-NEQ + S3★-aux to discharge `v_ℓ ∉ V_{s_C}(d)`; or (b) simplify by citing K.μ⁺_L's effect axiom directly — `dom(M'(d)) = dom(M(d)) ∪ {v_ℓ} ⊃ dom(M(d))` asserts strict containment, which is exactly freshness, and obviates the need to re-derive freshness from the V-position construction.

### Issue 2: Summary line omits O0 from required implementation claims
**ASN-0077, Summary**: "Any implementation of Xanadu that claims to support SHOWORIGIN must satisfy O1–O12 (with the O1 corollaries O1.1, O1.2)."

**Problem**: O0 is listed in the Claims Introduced table as a substantive claim (status: "introduced") with a three-part derivation establishing structural well-definedness, semantic correspondence, and totality of `origin` on `dom(L)`. It is load-bearing: the V-span operation over the link subspace returns `{d}` precisely because `origin` is total and semantically correct on `dom(L)` (an output of O0). Omitting O0 from the implementation-required list contradicts treating it as a claim. The exclusion would mean an implementation that supplies S7 (origin on `dom(C)`) but no extension to `dom(L)` could claim full SHOWORIGIN support — which the SHOWORIGIN_V link-subspace edge case shows it cannot.

**Required**: Expand the conclusion to "O0–O12", or re-classify O0 as definitional infrastructure (and remove it from the Claims Introduced table). The current state is internally inconsistent.

## OUT_OF_SCOPE

None — the Open Questions section already correctly defers cross-subspace I-spans, transitive provenance reporting, native-vs-transcluded distinction, unreachable-source behaviour, historical containment, and intra-document sharing under S5 to future ASNs.

VERDICT: REVISE
