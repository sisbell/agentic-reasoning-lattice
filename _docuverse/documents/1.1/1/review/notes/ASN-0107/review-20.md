# Review of ASN-0107

## REVISE

### Issue 1: P0a cites LP21 for a fact about raw request sets, where it does not apply

**ASN-0107, "What Is Counted" (P0a / RequestRepresentationInvariance)**: "If `Q` and `Q'` have `Qᵢ = Q'ᵢ` as address sets for every `i` — in particular if their parts are re-decomposed into different spans of the same coverage (LP21, ASN-0098) — then `match(Q, Σ) = match(Q', Σ)`..."

**Problem**: A counting request is defined as "a triple of address sets `Q = (Q₁, Q₂, Q₃)` with each `Qᵢ ⊆ T`" — the parts are raw sets, not endsets, and `sat` consults them only through `coverage(Σ.L(a).eᵢ) ∩ Qᵢ`. LP21 is a statement about *endset → projection* invariance (the stored endset side), not about a request part's span decomposition. The "in particular" clause imagines the request supplied as spans and re-decomposed, but (a) that is outside the formal definition of `Q`, and (b) even for that case the relevant fact is equality of coverage under different span decompositions (the `coverage` definition / PrefixSpanCoverage), not LP21. The claim's actual justification — "immediate from `sat`, which consults `Qᵢ` only set-wise" — is correct and self-sufficient.

**Required**: Drop the LP21 parenthetical, or replace it with the correct ground (set-wise use of `Qᵢ` in `sat`; coverage equality of span re-decompositions). Do not borrow an endset-projection lemma for a raw-set fact.

### Issue 2: Essay-content closers in structural slots (anti-bloat)

**ASN-0107, "What the Count Does Not Say"**: "W1 and W2 are the disciplined statement of why the count is useful despite being lossy... The loss of identity is the price and the point. A count that revealed identity would not be a count."

**ASN-0107, R3**: "Survivability is a guarantee that endset breadth is a reserve: a link clings to whatever bytes remain."

**ASN-0107, A2 (closing)**: "A2 is the precise reconciliation of [Nelson quote] with the fact that copying content adds no entry to the link store..."

**Problem**: These are rhetorical/meta restatements appended after the claims they follow. They position or re-justify a claim rather than advance its reasoning. The W1/W2 closing paragraph adds no reasoning past the claim bodies; "the price and the point" / "would not be a count" is pure flourish. R3's "a link clings to whatever bytes remain" and A2's "precise reconciliation of Nelson..." are essay flourishes in claim slots. (Note: the substantive middle sentences of A2 — "The link population does not grow; what grows is the set of documents from which the unchanged population is reachable" — are statements of what happens and should stay.)

**Required**: Remove the meta-commentary sentences; retain only prose that states what the operation/claim does. Keep concrete statements and the Nelson quotation where it grounds the satisfaction rule; cut the "X is the disciplined statement of why..." framing.

## OUT_OF_SCOPE

### Topic 1: Interaction with the retraction layer (ASN-0086 active subsets)

The note declares store-residence semantics ("`num` is blind to any notion of link nullification or retraction"). Whether a separate count over the *active subset* `A_K` (excluding nullified links) is wanted is a distinct operation belonging to a future ASN, not a defect here. The note's stance is internally consistent.

### Topic 2: Multi-document independently-anchored request parts

Raised in the note's own Open Questions — the count when the three parts resolve through three separately-evolving arrangements is new territory, correctly deferred.

VERDICT: REVISE
