# Review of ASN-0091

## REVISE

### Issue 1: RE-disc proof quantifies over all documents but only handles the target
**ASN-0091, "Discoverability Is Preserved" section**: "Combining RE-cov and RE-ran: ... discoverable_from(a, d, Σ') ⟺ ... ⟺ discoverable_from(a, d, Σ)"
**Problem**: The RE-disc claim quantifies over all `d ∈ dom(Σ.M)` (target *and* non-target documents). The proof cites RE-ran for the equality `ran(Σ'.M(d)) = ran(Σ.M(d))`, but RE-ran as stated and derived in the ASN is parameterised by the *target* document — the one whose arrangement is being permuted by π. For `d' ≠ target`, the range equality follows from RE-other (which gives `Σ'.M(d') = Σ.M(d')` entirely), not from RE-ran. The table's provenance entry "abstract (from RE-cov + RE-ran via LP12)" similarly omits RE-other.
**Required**: Either split the proof into target/non-target cases (citing RE-ran for the former, RE-other for the latter) or update RE-ran's claim to cover all `d ∈ dom(Σ.M)` by combining the bijection argument with RE-other.

### Issue 2: RE-trans proof emphasises target d without addressing non-target d
**ASN-0091, "Cross-Document Transclusion Preserved" section**: "By RE-ran, the *set* of foreign addresses `{a ∈ ran(Σ.M(d)) : origin(a) ≠ d}` is preserved; by RE-μ, each such address appears in d's arrangement with the same multiplicity at Σ' as at Σ"
**Problem**: RE-trans quantifies over every pair `(a, d)` with `a ∈ ran(Σ.M(d))` and `origin(a) ≠ d`. The `d` here can be the REARRANGE target or any other registered document. The proof cites RE-ran and RE-μ — both target-specific — without acknowledging that for non-target `d`, preservation of `ran(M(d))` and the per-address multiplicities follows trivially from RE-other (which preserves the entire arrangement of `d`). The home-document clause `(origin(a)'s arrangement is unchanged)` is correctly addressed via RE-other at `d' = origin(a) ≠ d`, but the per-`d` clauses are not.
**Required**: Explicitly handle both cases — for target `d`, RE-ran and RE-μ apply; for non-target `d`, RE-other gives `Σ'.M(d) = Σ.M(d)` and the range/multiplicity preservation is trivial.

### Issue 3: Range equality for non-target documents is never stated as a lemma
**ASN-0091, RE-ran statement**: "Range Invariance: ran(Σ'.M(d)) = ran(Σ.M(d))"
**Problem**: As written, the RE-* claims that depend on `ran(M(d))` (notably RE-disc and RE-trans) want range invariance for every `d ∈ dom(Σ.M)`. RE-ran as derived (via the π-bijection computation) and as listed in the claims table is for the target. RE-other supplies the non-target case, but the composition "RE-ran for target + RE-other for non-target = uniform range invariance for all d" is implicit throughout — never stated as a separately citable consequence. This forces every downstream proof to perform the same case split, which the text omits.
**Required**: Either generalise RE-ran's statement to cover all `d ∈ dom(Σ.M)` with a two-line proof (target by π-bijection, non-target by RE-other), or add a derived intermediate "uniform range invariance" lemma that the discoverability and transclusion proofs can cite cleanly.

## OUT_OF_SCOPE

(none — the existing Open Questions section identifies the right boundary topics for follow-on ASNs)

VERDICT: REVISE
