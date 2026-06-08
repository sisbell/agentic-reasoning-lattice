# Review of ASN-0112

## REVISE

### Issue 1: Design-rationale meta-prose in the result-type definition
**ASN-0112, "What the caller must be handed" (V0)**: "Returning a span-set uniformly puts both results in one ASN-0053 type — we choose this over a heterogeneous `Span ⊎ SpanSet` union precisely so the empty and non-empty cases inhabit the same codomain."
**Problem**: This sentence justifies a design decision (why this codomain rather than a sum type) rather than advancing what V0 states. The reader must skip it to reach the substantive content — the denotational distinguishability of `⟨⟩` vs `⟨σ_d⟩`, which immediately follows and is the real claim. This is exactly the forward-reference/justification accretion the anti-bloat pass targets.
**Required**: Drop the `Span ⊎ SpanSet` comparison sentence. State the codomain (`SpanSet`) and the two cases, then the denotational distinguishability. The "why not the alternative" rationale belongs in a design note, not the claim.

### Issue 2: The reach property is referenced at four sites under two names without a single label
**ASN-0112, V2 / V3 / worked variant / wp section**: the property `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d` is named "the V2 reach biconditional" in V2 and V3, but "ReachTight" in the worked variant ("what lapses is the V2 reach biconditional") and in the wp analysis ("`ReachTight ≡ reach(σ_d) = reach_d`").
**Problem**: A property load-bearing enough to be cross-pointed from four locations and to anchor a non-trivial wp ("`wp(…, ReachTight) = (O(d) = ∅ ∨ #origin_d ≤ #reach_d)`") is carried as un-numbered prose buried inside V2, referenced under two different names. This is naming drift plus deferral accretion — each site re-explains the same sub-property.
**Required**: Promote it to a single labeled claim (e.g. `V-ReachTight`) stated once, and reference that label uniformly. Then V3, the worked variant, and the wp section can point to one place instead of re-narrating it.

### Issue 3: V6 strict inclusion proved only by example, not by a general witness
**ASN-0112, V6**: "When occupied positions span more than one subspace, `O(d) ⊊ ⟦σ_d⟧` strictly … includes the unoccupied void separating the two subspaces."
**Problem**: The strictness (`⊊`) requires exhibiting an *unoccupied* position inside `⟦σ_d⟧`. The body gives this only verbally ("the unoccupied void") and concretely only in the worked example (`[1,4],[1,5]`). The general witness is not named, so the universal claim rests on an example.
**Required**: Name the general witness — e.g. `[s_C,1,…,1,n_C+1]`, which satisfies `origin_d ≤ [s_C,…,n_C+1] < reach_d` (it is a content position, hence below any `s_L` reach by T1) and lies outside the dense content run `{[s_C,…,k] : k ≤ n_C}` (D-SEQ★), so it is covered yet unoccupied. One line discharges the strictness universally.

### Issue 4: V12 is a thin upstream inventory, not a claim that advances reasoning
**ASN-0112, "What the caller learns beyond the name" (V12)**: "The span discloses the *live origin* (the addressing anchor of V1/V8) and the *current extent* (the present bounds of V2)."
**Problem**: V12 restates V1/V8/V2 by reference without adding content — it enumerates upstream claims rather than establishing anything new. This is the use-site-inventory pattern the anti-bloat pass flags.
**Required**: Either fold the genuine residue ("neither derivable from `d`'s identity") into V8/V2 as a corollary, or strengthen V12 into an actual information-gain statement (e.g. a precise characterization of what `σ_d` determines that `d` alone does not). As written it is a label over a cross-reference list.

## OUT_OF_SCOPE

### Topic 1: Multi-subspace extent-vs-count invariant
The first Open Question (relating reported extent to occupied-position count in the cross-subspace case) is correctly deferred — it is genuinely new territory, and a span "does not designate a number of anything" (4/24), so any count relation needs its own development. Properly scoped.

### Topic 2: Historical-version faithfulness and correspondence-run composition
The third and fourth Open Questions (version-report faithfulness; composing the whole-document span from per-run bounding spans) belong to future operations and are appropriately left out. Per-subspace reporting is correctly routed to ASN-0113.

VERDICT: REVISE
