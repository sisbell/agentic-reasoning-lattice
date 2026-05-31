# Review of ASN-0043

I checked the L1c chain construction and its two-CPP-invocation `s = home(a)` argument, the FSP/FSE conformance lemmas, the PrefixSpanCoverage interval reasoning, and the six-step worked example's arithmetic and coverage claims. The mathematics is sound — the L1c T4-validity induction closes correctly (the unstated `k=1` side-condition `zeros ≤ 3` follows from the inductive T4-validity hypothesis, so it is not a gap), the coverage-equality of `Θ_split`/`Θ_single` is exact, and the sibling-disjointness discrimination in Step 4 is correct. The remaining issues are anti-bloat, which this note's classifier asks me to surface.

## REVISE

### Issue 1: Motivating preamble recurs in worked-example extension steps 4, 5, 6
**ASN-0043, Worked Example — Extension, Steps 4–6**:
- Step 4: "Steps 1-3 share a single ghost type at `g`, so the only L8 check available across that history is the reflexive one ... We add a fifth link `a₄` ..."
- Step 5: "Steps 1–4 use only singleton endsets, so L5 holds there only in its trivial form. We add a link `a₅` ..."
- Step 6: "Steps 1–4 compare only same-singleton (match) and disjoint-singleton (no match) endsets, never the crux case. We add `a₆` ..."

**Problem**: Each step opens with a "prior steps did only X, so we add Y to exercise W" justification — navigational/motivational essay content, not advancing a claim. The recent history (`revise(asn-43): trim motivating preamble from steps 3, 4, and 6`) shows this exact pattern was already targeted for removal elsewhere; the same construction recurs here and will compound across cycles. A step that constructs `a₅` with a two-span type endset and verifies L5 needs only that statement, not a recap of what steps 1–4 omitted.
**Required**: Drop the "Steps 1–X only do Y" recap clauses; open each step with what it constructs and which invariant it exercises.

### Issue 2: Closing interpretive commentary after the verification checkmarks
**ASN-0043, Worked Example — Extension, Steps 4 and 6**:
- Step 4: "The discrimination is structural: `g` and `g'` differ only at the tail (position 8), but that single divergence forces their prefix-cone coverages to be disjoint — sibling ghost addresses generate sibling type cones, neither containing the other."
- Step 6: "This is precisely the case that distinguishes L8's coverage criterion from a span-set-identity criterion: a span-set test would (wrongly) report these as different types, since `Θ_split ≠ Θ_single`."

**Problem**: These sentences sit after the `✓` and restate the significance of a check already discharged — essay content in a verification slot. The check itself (coverage disjointness; coverage equality across distinct decompositions) is the substance; the gloss re-narrates it.
**Required**: Remove the trailing significance restatements, or fold the single load-bearing fact (Step 6: span-set identity would over-discriminate) into one clause inside the check.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace invariant
The `s_C`-resident scoping of L0a/L1d(b)/L14/L14a leaves disjointness conditional rather than universal over `dom(Σ.C)`. The ASN's own Open Questions flag this; fixing it requires a content-side invariant that belongs in the content model, not here.

VERDICT: REVISE
