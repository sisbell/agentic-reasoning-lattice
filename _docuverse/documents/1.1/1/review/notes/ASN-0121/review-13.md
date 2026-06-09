# Review of ASN-0121

This is a carefully constructed specification of a pure query operation. The forcing argument for FL-DEF (soundness ∧ completeness leave no slack once the addressability conjunct is added) is sound, the foundation usage is legal (all referenced ASNs — 0034, 0043, 0047, 0086, 0098 — are foundations), the worked instance exercises the principal claims with six concrete traces, and the consequences of each claim are derived rather than asserted. I found one genuine precision gap and one minor table inaccuracy.

## REVISE

### Issue 1: H-component spans cited as denoting subtrees without the unit-depth condition PrefixSpanCoverage requires

**ASN-0121, "What is being matched"**: "its spans are rooted at node-, account-, or document-level addresses, each denoting (PrefixSpanCoverage, ASN-0043) the corresponding subtree `{t : p ≼ t}`, which is order-convex under T5 (ASN-0034)."

**Problem**: PrefixSpanCoverage (ASN-0043) establishes `coverage({(x, δ(1,#x))}) = {t : x ≼ t}` **only for the unit-depth displacement** `δ(1,#x)`. A span `(p, ℓ)` rooted at `p` with any other width denotes the order-convex range `{t : p ≤ t < p ⊕ ℓ}`, which is a proper sub-range of the subtree, not `{t : p ≼ t}`. As written, the ASN applies PrefixSpanCoverage to "spans rooted at p" without establishing its precondition (that the span is the unit-depth prefix span), so the stated subtree denotation does not hold for an arbitrary H endset. The grammar admits `H ∈ Endset = 𝒫_fin(Span)`, so a wide span rooted at a document address is a syntactically legal H whose coverage is *not* the subtree — and the residence semantics `athome(a, H)` for such an H is then unspecified by the prose, even though Trace 6 (correctly) uses only unit-depth spans.

**Required**: State explicitly that H's spans are unit-depth prefix spans (`ℓ = δ(1,#p)`) so the PrefixSpanCoverage citation discharges its precondition; or, if general H span-sets are intended, specify `athome` for them and acknowledge that coverage is then an order-convex range rather than the full subtree (this is the territory open question #3 gestures at). Either way the present blanket "each denoting the corresponding subtree" overstates what the cited foundation delivers.

### Issue 2: FL-WILD table entry says all-wildcard links are "matched on" their endsets

**ASN-0121, Claims Introduced table, FL-WILD**: "all-wildcard returns all addressable links, of every arity `N ≥ 3`, each matched on its first three endsets `e₁, e₂, e₃` (slots `e₄ … eₙ` never enter `sat`)"

**Problem**: Under the all-wildcard request every `lift` is `true` independent of endset content, so no link is "matched on" any endset — the endsets are not consulted at all. The prose in the FL-WILD section states this correctly ("a higher-arity link is admitted by the all-wildcard request like any other, and under a constrained request is matched on its first three endsets alone"), but the table conflates the all-wildcard case with the constrained case.

**Required**: Restate the table entry so the "matched on first three endsets" qualifier attaches to constrained requests, not to the all-wildcard case where no endset enters `sat`.

## OUT_OF_SCOPE

The five open questions — version/time-qualified inquiry, the I-address↔V-spec equivalence invariant, single-test residence reduction, exact subtype-by-containment conditions, and cross-store federation completeness — are correctly identified as future territory rather than defects in this operation. No action needed; flagging only to confirm I did not treat them as gaps.

VERDICT: REVISE
