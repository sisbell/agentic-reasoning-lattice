# Review of ASN-0077

## REVISE

### Issue 1: Tangential parenthetical referencing an unused foundation operation
**ASN-0077, "Lifting origin to a V-span"**: "(C1a covers both subspaces, where `resolve` would confine I-targets to `dom(C)` by C1.)"
**Problem**: This parenthetical references ASN-0058's `resolve` and C1, neither of which is used anywhere in this ASN. It describes a contrast the V-span lift does not depend on, so the reader must skip past it to follow the definition. This is meta-prose, not an advance of the argument.
**Required**: Delete the parenthetical. The preceding sentence ("C1a's preconditions … are subspace-agnostic; the decomposition is well-defined whether the V-positions … lie in the content subspace … or the link subspace") already carries the load.

### Issue 2: Summary closing paragraphs duplicate the bullet list and the introduction
**ASN-0077, Summary**: "Span-level answers are derived from this pointwise invariant rather than sharing it: an I-span's reported set grows monotonically under content allocation (O6/O6★) and is stable only under fixed or extended arrangements (O7, O11/O11′), while a V-span's answer is arrangement-dependent and can shift to an incomparable set under reordering (O14)."
**Problem**: This restates (a) the numbered list (1)(2)(3) immediately above it, and (b) the opening sentence of the note: "Span-level results are derived from this pointwise guarantee rather than inheriting it unchanged." Three sites assert the same proposition. The trailing paragraph adds no claim not already stated.
**Required**: Keep one statement of the pointwise-vs-span distinction (the intro sentence suffices) and drop the duplicated summary restatement, or collapse the two closing paragraphs into a single sentence of forward-looking consequence.

### Issue 3: "Why the foundation is needed" glosses in O0(b)/O1(c)
**ASN-0077, O1 derivation (c)**: "S7d alone delivers *one document*; the further identification with *one allocator* requires the sub-allocator structure of ASN-0047."
**ASN-0077, O0 derivation (b)**: "…and SubAllocatorBundle (ASN-0047) — whose cross-subspace disjointness delta gives domain disjointness across all of a document's sub-allocators and across documents — makes this attribution unambiguous."
**Problem**: Both passages explain *why a foundation citation is needed* rather than stating what it delivers — the explicit reviser-drift pattern flagged for anti-bloat mode. The em-dash clause in O0(b) is a use-site gloss on SubAllocatorBundle's content; the O1(c) sentence narrates the division of labor between S7d and ASN-0047 instead of carrying the proof.
**Required**: Cite the lemma and state the consequence directly (e.g., "by SubAllocatorBundle, `dom(A_C(d)) ∩ dom(A_L(d)) = ∅` and the cross-document disjointness clauses, so the attribution is unambiguous"). Drop the meta-commentary on what each foundation "alone delivers."

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation
The Open Questions correctly defer a single operation reporting both content and link origins over an I-stream range. The cross-subspace edge case settling that the I-span lift drops link addresses is in scope; the unified operation is future territory.

### Topic 2: Historical containment from Σ.R
"What SHOWORIGIN does not promise" correctly excludes historical containment as a separate operation over the provenance relation. Stating the exclusion is in scope; specifying that operation is not.

Note on re-review targets: O0, O3, and O10 (carried forward from the prior cycle for re-check against ASN-0040 and ASN-0098) are sound as written — O0's codomain conjuncts are discharged by P6/L1a, O3's structural-derivation claim consults no 0040/0098 machinery, and O10's read-only frame is definitional. No new issue arises from the added foundations.

VERDICT: REVISE
