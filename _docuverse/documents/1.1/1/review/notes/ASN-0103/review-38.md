# Review of ASN-0103

This is a careful, well-structured note. The allocation proof (Effect One) is genuinely rigorous: the `D_A = E ∩ S(A,2)` argument proves both inclusions, the length-filter rationale is load-bearing (the worked example demonstrates the concrete B8 collision it averts), and the freshness/distinctness split (same-chain by S0 injectivity, cross-chain by a single universal B7 instantiation) is sound. The frame enumeration and invariant discharge are complete. My findings are residual prose accretion, consistent with the `anti-bloat` classifier on this cycle.

## REVISE

### Issue 1: Out-of-scope contrast occupies a proof slot in Effect Two
**ASN-0103, Effect Two**: "This empty range is also exactly what distinguishes a created document from a forked one: CREATENEWVERSION begins its new document with a *populated* arrangement inherited from the source ('creates a new document with the contents of document `<doc id>`', 4/66 — out of scope here), whereas creation begins with `ran(M'(d)) = ∅`. Empty versus inherited is the whole distinction, and it is visible in the post-state."
**Problem**: The claim being proved is `M'(d) = ∅`, established directly one paragraph earlier. This paragraph adds nothing to that proof — it elaborates on CREATENEWVERSION (explicitly out of scope: forking) and ends with essay content ("Empty versus inherited is the whole distinction"). A precise reader must skip past a contrast with a different, out-of-scope operation to follow the empty-arrangement argument. The earlier phrase in the same section — "no inherent starting state, no default text, no placeholder the user can rely on" — is the same elaborative register.
**Required**: Cut the CREATENEWVERSION paragraph. If a contrast is wanted, reduce to a single clause stating that creation produces an empty range, with no comparison to out-of-scope operations.

### Issue 2: Exhaustiveness/inventory sentence restates what the universal B7 step already covers
**ASN-0103, Effect One (cross-chain distinctness)**: "This one step subsumes all other accounts' document chains, all version chains, and version-of-version chains at any depth, present and future."
**Problem**: The preceding sentence already discharges distinctness with a single B7 instantiation universally quantified over *every* B6-valid `(p', d') ≠ (A, 2)`. That universal *is* the proof; the inventory sentence then lists the instances the universal covers and tags them "present and future." This is the flagged exhaustiveness-claim pattern — prose enumerating what a universal quantifier already subsumes, which the skeptical reader does not need and the careful reader works around.
**Required**: Delete the sentence. The universal B7 step stands on its own; the inventory adds no inferential content.

## OUT_OF_SCOPE

### Topic 1: Effective-owner derivation, concurrency ordering, failure recovery
**Why out of scope**: The Open Questions correctly defer the effective-owner reading (requires entity-set/baptismal-registry coupling), concurrent same-account allocation ordering, and partial-failure recovery. These are future-ASN territory, not gaps in this note; CND.own appropriately delivers only the structural (prefix) ownership guarantee derivable from the post-state.

VERDICT: REVISE
