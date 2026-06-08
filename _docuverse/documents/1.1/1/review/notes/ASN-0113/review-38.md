# Review of ASN-0113

The mathematics is sound. I checked the load-bearing derivations — W4 (T5 prefix-confinement of the half-open extent span), W10 (first-component pinning by T1), W11 (disjointness via SC-NEQ), W3 (T12 well-formedness of `δ(n_S, m_S)`), and the W19 wp computations — and each holds, including the boundary instances (allocated-empty, one-member, and the non-vacuous depth-3 case that exercises T5 where `m_S = 2` does not). The findings below are confined to accreted/redundant prose, per the anti-bloat classifier.

## REVISE

### Issue 1: Open Question 2 re-asks content W14 already settled and duplicates Open Question 6
**ASN-0113, Open Questions (second question)**: "how must a *consumer* interpret an omitted member when comparing reports across documents of differing vintages — under what conditions is 'subspace absent' safely read as 'extent zero'?"
**Problem**: W14 already proves the absent-reads-as-zero question *unconditionally* for documents sharing a kind-list: "by W6/W7 the operation omits kind `S` exactly when `V_S(d) = ∅`, which is exactly when `n_S(d) = |V_S(d)| = 0` … so a missing member can only ever signify an empty subspace." The question's clause "under what conditions is 'subspace absent' safely read as 'extent zero'" is therefore answered, not open. The only genuinely open part — *differing* vintages / changed kind-lists — is exactly the last Open Question ("Should the subspace convention be extended beyond text and links … so the report stays comparable across documents of different vintages"). The question is thus the settled W14 result plus a duplicate of Q6.
**Required**: Remove the question, or fold its non-redundant remainder into the kind-list-extension question.

### Issue 2: D-CTG★'s load-bearing role for W4 is restated in the Open Questions parenthetical
**ASN-0113, Open Questions (first question)**: "(a non-contiguous subspace would, by order-convexity, force a single covering span to admit inactive interior tumblers — so faithful coverage would then require a fragmented span-set)"
**Problem**: This re-derives the W4-prose point ("it is *because* D-CTG★ holds … that a single half-open span can be exact") and the W4 table row ("exactness rests on the standing D-CTG★ contiguity invariant via order-convexity"). The forward question only needs to ask what the operation must guarantee if D-CTG★ is relaxed; the embedded re-justification of why D-CTG★ is load-bearing duplicates the W4 derivation rather than advancing the question.
**Required**: Drop the parenthetical justification; the question stands on its own with a pointer to W4.

### Issue 3: Doubled conclusory prose in "Why text and links must be reported apart"
**ASN-0113, "Why text and links must be reported apart"**: "one is *forced* into a span-set of two members. This is not a representational convenience but a structural necessity: the honest report of two separated regions is two spans."
**Problem**: Three phrasings of one idea in two sentences ("forced into a span-set of two members," "structural necessity," "honest report … is two spans"). The substantive content — W11 disjointness forbids a single contiguous span — is already established; the trailing sentence pair restates the conclusion without adding reasoning.
**Required**: Collapse to a single sentence stating the consequence of W11.

## OUT_OF_SCOPE

The remaining open questions (D-CTG★ relaxation, version-fork permanence, transclusion, consistency with a single overall extent, subspace-convention extension) are appropriately forward-looking and correctly defer to future ASNs rather than overreaching into this note.

VERDICT: REVISE
