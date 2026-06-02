# Review of ASN-0086

This is a mature ASN and the core mathematics holds up: R0a's two-case antichain argument, R0's branch-by-branch freshness discharge, R-Scope, and the wp Case 2 biconditional are all sound, and the Worked Sketch's concrete tumblers check out arithmetically. The remaining issues are accreted meta-prose and forward-reference scaffolding around otherwise-correct claims — exactly what the anti-bloat classifier targets.

## REVISE

### Issue 1: R0 enumerates downstream consumers of its own postconditions
**ASN-0086, R0 (TupleAddressFreshness), prose under the statement**: "The two address conditions `a ∉ dom(Σ.L)` (*freshness*) and `a ∈ A_L(d)` (*on-chain admissibility*) are explicit postconditions of the lemma, established below... **They are the facts downstream operations (Emit_K, Nullify) cite for the home they pass in.**"
**Problem**: The second sentence is a use-site inventory — it names which downstream operations consume the postcondition rather than advancing R0's meaning. A postcondition stands on its own; Emit_K and Nullify cite it where they cite it. This is the "definition's introduction enumerates downstream consumers" pattern.
**Required**: Delete the sentence "They are the facts downstream operations (Emit_K, Nullify) cite for the home they pass in." The preceding sentence already establishes the postconditions.

### Issue 2: wp load-bearingness paragraph defers forward to its own derivation
**ASN-0086, Weakest-Precondition Analysis, "The disjunction is load-bearing"**: "Necessity — that the disjunction cannot be weakened to the home-precondition alone — is the necessary direction of the biconditional proved in *Derivation (both directions)* below."
**Problem**: This opening sentence asserts a claim and immediately defers its proof to a later paragraph in the same section, duplicating the Derivation's content. The paragraph's *concrete example* (`G = ∅`, to-span rooted away from `a`) is genuine and should stay — but the forward-pointing first sentence is pure deferral scaffolding.
**Required**: Drop the deferral sentence; lead the paragraph with the concrete escape-branch example, which is what actually demonstrates load-bearingness.

### Issue 3: Domain restriction (unit-depth-disciplined, →*-reachable) stated three times with a forward-pointer chain
**ASN-0086, Weakest-Precondition Analysis**: The same domain restriction appears in (a) the Result formula's parenthetical "(over →*-reachable, unit-depth-disciplined Σ...)", (b) a dedicated "*Domain restriction.*" paragraph, and (c) the opening of "*Derivation (both directions)*" ("The domain restriction supplies, via (i)..."). The "*Domain restriction.*" paragraph then ends "...the next paragraph shows why it is load-bearing," chaining into "*The unit-depth discipline is load-bearing.*"
**Problem**: Two paragraphs in the same section restate the same restriction, joined by an explicit "the next paragraph shows why" forward pointer — the accretion pattern where adjacent paragraphs defer to one another rather than stating the content once. The parenthetical in the Result line plus the Derivation already carry the restriction; the standalone "*Domain restriction.*" paragraph is redundant except for its load-bearingness claim, which belongs merged with the discipline-load-bearingness paragraph.
**Required**: Collapse the restriction statement to one site (the Result parenthetical) and fold the two load-bearingness paragraphs into a single justification for restriction (ii), removing the inter-paragraph "the next paragraph shows why" pointer.

## OUT_OF_SCOPE

### Topic 1: Cardinality/ratio bounds on nullified(Σ) vs dom(Σ.L)
**Why out of scope**: Already correctly listed in Open Questions; whether unbounded retraction is permitted or a structural ratio must hold is new territory, not a gap in the present claims.

### Topic 2: Concurrency/atomicity of Emit vs Observe
**Why out of scope**: The substrate's SequentialAtomicTransitions axiom (ASN-0093) gives single-threaded transitions; a consistency model for concurrent observation is a future layer, correctly deferred to Open Questions.

VERDICT: REVISE
