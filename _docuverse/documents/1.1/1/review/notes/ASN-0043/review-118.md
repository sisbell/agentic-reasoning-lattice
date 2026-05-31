# Review of ASN-0043

I checked the proofs (L0a/T7 disjointness, L1c chain + CPP, FSP/FSE, PrefixSpanCoverage by mutual inclusion, L9 Cases A/B, L11a single-tree discharge, and the six-step worked example) and found the mathematical content sound — the chains are T10a-consistent, the prefix-cone identity is correctly derived, and the worked example exercises each invariant non-vacuously. The remaining issues are forward-reference accretion and meta-prose, flagged per the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: L11a closes with use-site meta-prose that does not advance the claim
**ASN-0043, L11a — LinkUniqueness (final sentence)**: "Fresh-sibling extensions (FSP) preserve L1c and S7d, so L11a's premises — and hence its conclusion — carry to any FSP-extended state automatically."
**Problem**: L11a's claim is "distinct T10a-conforming allocation events produce distinct link addresses." Its proof is complete at the single-tree 𝒯 discharge two sentences earlier. This trailing sentence is a note about how a *different* lemma (FSP) interacts with L11a's premises across state extensions — a downstream-preservation remark, not a step in L11a's argument. The reader must skip it to stay on the claim. This is the "use-site inventory / forward note" pattern.
**Required**: Delete the sentence. FSP's own preservation of L1c and S7d is already established where FSP is proved; it does not need a back-pointer planted inside L11a.

### Issue 2: T4-validity of link addresses is deferred forward from three separate sites to L1c
**ASN-0043, L0a, Definition — home, and L1a**: L0a (stated before L1) reads "By L1 (below)… T4-validity… for `a ∈ dom(Σ.L)`, by L1c's T4-validity postcondition"; the `home` definition reads "T4-validity by L1c (LinkAllocatorConformance)"; L1a reads "T4-validity by L1c."
**Problem**: Three consumers — the L0a disjointness discharge, the `home` well-definedness clause, and L1a — each forward-defer to L1c for the same fact (link addresses are T4-valid), and L1c is stated *after* all three. L1c's own statement in turn uses `home(a)`. This is the "multiple paragraphs in different sections defer to the same downstream location" pattern, and it forces the reader to hold an unproven T4-validity obligation across four properties. The interleaving is avoidable: the T4-validity-of-link-addresses fact (the CPP/T10a.4 postcondition) is a single result that could be stated once, before its consumers.
**Required**: Lift the "every link address is T4-valid" postcondition to a standalone statement preceding L0a (or fold it into L1 as a companion), and have L0a, `home`, and L1a cite that single prior result rather than forward-referencing L1c three times.

### Issue 3: L0a refers to itself by name for a discharge stated within the same property
**ASN-0043, L0a — ContentSubspaceScope**: "T4-validity is discharged on each side… for `b ∈ dom(Σ.C)`, by the content-side T4-validity discharge established in L0a above."
**Problem**: L0a citing "the content-side T4-validity discharge established in L0a above" is a property pointing at itself by name a few lines up. The self-citation reads as a cross-reference but resolves to the immediately preceding sentence of the same paragraph, which the reader must reconcile before continuing.
**Required**: Replace with a direct phrasing ("by the content-side T4-validity established two sentences above" or simply restate the one-clause justification inline), dropping the named self-reference.

### Issue 4: The `s_C`-residence hypothesis is spelled out in full at four sites
**ASN-0043, L9, L11b, L14a, and FSP**: the quantified hypothesis `(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)` ("`s_C`-resident content") is written out verbatim in each.
**Problem**: This is a single recurring precondition reproduced in full across four properties plus the "state-local invariants" preamble. It is genuine precision, but the repeated long-form quantifier is exactly the kind of phrase that should be named once and cited, to keep the statements scannable.
**Required**: Introduce a one-line named predicate (e.g., "`Σ` is `s_C`-resident iff `(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)`") at first use and reference it by name in L9, L11b, L14a, and FSP.

## OUT_OF_SCOPE

None. The Open Questions correctly route content-subspace globalization (Q1), transclusion consistency, and compound-link well-formedness to future ASNs; no in-scope claim is misfiled.

VERDICT: REVISE
