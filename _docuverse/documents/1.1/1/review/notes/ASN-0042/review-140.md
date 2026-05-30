# Review of ASN-0042

The formal apparatus is sound. I checked the load-bearing operations (O3, O7, O8, O10) and the inductions (NestingByDelegation, O4, PrefixBaptismCoupling, the shared O1a/O1b/T4 induction) case-by-case — including the O10 fork construction in both the `zeros(pfx(π)) = 0` and `= 1` branches, the Form-A/Form-B non-coverage split, and the worked example's milestone trajectory. I found no skipped case or false claim in the proofs. The remaining issues are meta-prose accretion and one precision gap.

## REVISE

### Issue 1: Factoring narration in StrictLongestCover preamble
**ASN-0042, StrictLongestCover (lemma)**: "The same covering-chain three-case contradiction recurs whenever we ask which principal achieves the longest matching prefix of a covered address. We isolate it once."
**Problem**: This is meta-prose about *why the lemma is factored out*, not content that advances the lemma. The precise reader must skip it to reach the actual statement ("General form: let `χ ∈ Π_{Σ'}` cover..."). It narrates document structure rather than reasoning.
**Required**: Delete the two-sentence preamble and open with the general-form statement. The lemma stands on its own; its reuse at O3/O7/O10/NestingByDelegation is evident from the citations there.

### Issue 2: Content-model deferral repeated, duplicating the Scope declaration
**ASN-0042, O10(b), O10 closing, and the final fork paragraph**: O10(b) — "any content effects are governed by the content model, which lies outside this ASN's ownership state `Σ`"; closing — "a relationship that belongs to the content model, not the ownership model"; final — "whose content identity may relate to `a₃`'s content (through the content model)".
**Problem**: Three in-body paragraphs in the same section defer the same fact to the same out-of-scope location. The Scope section already declares "content storage and retrieval" and "operation-specific effects" out of scope. This is the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: State the content-model boundary once (in O10(b)), and drop the two restatements.

### Issue 3: O17's statement omits the reachability qualifier its derivation requires
**ASN-0042, O17 (AllocatedAddressValidity)**: "`(A Σ, a : a ∈ Σ.B ⟹ T4(a))`" — proven "By RegistryReachability (derived above), in every reachable state `Σ`..."
**Problem**: The derivation routes through RegistryReachability and B10, both of which hold only over *reachable* registries; the literal `(A Σ, ...)` quantifies over all configurations. The note leans on the global "all states discussed are reachable" convention, but O17 is a derived lemma consumed by O6 and O9 and should be self-contained in its own contract. Other claims (O4, O6, O9) carry "Σ reachable from Σ₀" inline; O17 does not — an inconsistency.
**Required**: Write the statement as `(A Σ reachable from Σ₀, a : a ∈ Σ.B ⟹ T4(a))`, matching the inline convention used by the claims that cite it.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
**Why out of scope**: The note correctly restricts to the refinement regime (O3) and records transfer as an Open Question. The relationship between inalienable provenance (O6) and a transferred effective owner (O2) is genuinely new territory, not a gap in this ASN.

VERDICT: REVISE
