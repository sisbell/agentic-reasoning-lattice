# Review of ASN-0068

This is a mathematically strong note — CV-MAX's existence/uniqueness proof is genuinely rigorous (the non-global-finiteness left-walk bound via D-SEQ★/S8a is a nice touch), the four worked examples all check out, and CV-PRED's five-clause predecessor machinery is sound. The deps are foundation-only; no cross-ASN violation. The findings below are the forward-reference/anti-bloat accretion the classifier asks me to surface, plus one substantive duplication.

## REVISE

### Issue 1: CV-PROV-FORGOTTEN is stated twice
**ASN-0068, "The Correspondence Relation" and "What the Result Cannot Express" (iii)**: CV-PROV-FORGOTTEN says "the relation provides no information about how `a` came to be referenced by both documents." Then (iii) repeats: "Per CV-PROV-FORGOTTEN, the result reports correspondence without explaining how the shared I-address came to be referenced by both documents."
**Problem**: Two paragraphs in different sections asserting the same fact in different words — the exact accretion pattern flagged. (iii) adds nothing CV-PROV-FORGOTTEN did not already establish.
**Required**: Drop (iii)'s body to a bare cross-pointer or remove it; let CV-PROV-FORGOTTEN carry the claim once.

### Issue 2: Document-ordering prose in definition/corollary introductions
**ASN-0068, CV-PRED intro**: "The maximality conditions reference *valid V-predecessors* ... which we lift to iterated form as a separate labeled definition before stating maximality."
**ASN-0068, CV-SPAN-VIEW intro**: "The set of maximal correspondence runs admits a natural presentational view ... which we record as a labeled corollary before the example that exercises it."
**ASN-0068, CV-LINK intro**: "the `s_L` case is structurally constrained, as the following two corollaries record."
**Problem**: These sentences justify *where* a definition/corollary sits in the document rather than advancing its content. The reader does not need to be told a labeled definition is coming before the place it is used.
**Required**: State CV-PRED, CV-SPAN-VIEW, and the link corollaries directly. Delete the ordering announcements.

### Issue 3: Defensive justifications of why a clause exists
**ASN-0068, CV-PROV-FORGOTTEN**: "CV-PROV-FORGOTTEN is necessary for the operation to be definable on any pair of documents regardless of their derivation history."
**ASN-0068, common-subspace paragraph**: "The common-subspace restriction is not optional."
**Problem**: Both are "why this clause is needed" framing rather than what the clause says or does. CV-IDENT/CV-PROV-FORGOTTEN already say what is and isn't witnessed; the necessity editorializing is meta.
**Required**: Keep the object-level content (subspace mismatch ⇒ disjoint storage ⇒ empty relation, which is a real consequence). Remove the "is not optional"/"is necessary for the operation to be definable" defensive sentences.

### Issue 4: Use-site preview attached to CV-PRED
**ASN-0068, CV-PRED**: "The two inverse forms support reductions of the shape `(v ± j) ± k` by signed last-component arithmetic, with M-aux (OrdinalIncrementAssociativity, ASN-0058) absorbing the natural-number addition."
**Problem**: This previews where the inverse forms get consumed downstream rather than advancing the definition. The reductions are exercised explicitly in the CV-MAX proof, which is where the M-aux interaction belongs.
**Required**: Remove the preview sentence; the inverse-property clauses stand on their own.

### Issue 5: CV-IN action-point block carries accretion around a real derivation
**ASN-0068, CV-IN follow-on paragraph**: "The action-point clause `actionPoint(width(σ)) = m_σ` is load-bearing. ... We rule out any weaker constraint `actionPoint(width(σ)) < m_σ` by a unified V-position-capture argument."
**Problem**: The V-position-capture derivation itself is legitimate object-level content (it proves a weaker precondition admits unbounded capture). But it is wrapped in defensive framing ("is load-bearing," "We rule out any weaker constraint... uniformly across the full range") and closes with a cross-reference flourish ("This matches the well-formedness condition for content references (ASN-0058 C0) and produces the bounded ordinal-displacement restriction semantics the operation contracts on") that restates the conclusion as a use-site claim.
**Required**: Keep the capture argument; strip the "load-bearing"/"we rule out"/"matches C0... the operation contracts on" framing so the derivation stands as a derivation, not a justification of itself.

## OUT_OF_SCOPE

### Topic 1: Concurrent modification, replication, and version-history-walk invariants
**Why out of scope**: The Open Questions correctly defer these (concurrent mid-comparison modification, replicated-copy consistency, pairwise history traversal). They are posed as questions, not claimed, so no action is needed — flagging only to confirm they are appropriately left to future ASNs and not smuggled into a claim.

VERDICT: REVISE
