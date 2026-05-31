# Review of ASN-0043

I checked the link-store invariants (L0–L14a), the local lemmas (CPP, FSP, FSE, PrefixSpanCoverage), the L9/L11a/L11b derivations, and the six-step worked example against the foundation contracts. The mathematics is sound: the allocator-chain reconstruction in L11a, the freshness/conformance factoring through FSP+FSE, and the coverage arguments in L8/L10/L13 all hold, and the worked example exercises each non-trivial L8 facet (reflexive, equal-coverage/equal-span, disjoint, equal-coverage/distinct-decomposition) and the L5 multi-span case. The findings below are accretion, per the `review-mode.anti-bloat` classifier — prose the precise reader must work around.

## REVISE

### Issue 1: L0a derives content-side T4-validity twice within one section
**ASN-0043, L0a (ContentSubspaceScope)**: First — "By ASN-0036's S7b, every `b ∈ dom(Σ.C)` has `zeros(b) = 3` and well-defined T4b projections; since T4b's definitional domain (UniqueParse, ASN-0034) is precisely the T4-valid subset of `T`, every `b ∈ dom(Σ.C)` is T4-valid." Then, in the disjointness paragraph — "for `b ∈ dom(Σ.C)`, by the content-side T4-validity established two sentences above (S7b gives `zeros(b) = 3` with well-defined T4b projections, and T4b's domain is precisely the T4-valid subset of `T`)."
**Problem**: The parenthetical fully restates the derivation given two sentences earlier — the same S7b → T4b-domain → T4-validity chain, verbatim in substance. The precise reader reads the identical argument twice in one section, and the "established two sentences above" self-pointer adds nothing.
**Required**: State the content-side T4-validity once; in the disjointness paragraph cite it by name only ("for `b`, by the content-side T4-validity above"), dropping the restated parenthetical.

### Issue 2: L11a carries meta-commentary about its own proof method
**ASN-0043, L11a (LinkUniqueness)**: "We derive this embedding rather than assert it, in two cases."
**Problem**: This sentence describes the proof's method rather than advancing the argument; the two-case derivation that follows speaks for itself. (The preceding sentence — "What L1c supplies … is only the existence … GlobalUniqueness needs the stronger fact that `a₁` and `a₂` are genuine allocation events of the one tree 𝒯 …" — is load-bearing because it names the precise gap being closed, and should stay.) The flagged sentence is removable with no loss to the reasoning.
**Required**: Delete the method-announcing sentence; let the case split begin directly.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant
The scoping of disjointness (L0a, L14, L14a) to `dom(Σ.C)|_{s_C}` rather than all of `dom(Σ.C)` is already disclosed as the first Open Question. Extending it requires a content-side invariant that belongs in ASN-0036, not here — correctly left open rather than assumed.

VERDICT: REVISE
