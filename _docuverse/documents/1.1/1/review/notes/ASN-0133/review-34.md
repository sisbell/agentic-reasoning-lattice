# Review of ASN-0133

I checked the load-bearing proofs (Q0's view-rewrite, Q5/Q5a's bounds, Q6's regime split, the worked trace) and they hold up — the hypothesis accounting is honest and the obstruction analysis in Q6 is genuinely complete. The findings below are the accreted meta-prose the `review-mode.anti-bloat` classifier asks for, plus one miscited premise.

## REVISE

### Issue 1: The H-RF/H-W relationship is argued in full, then restated three more times

**ASN-0133, H-RF / H-W / Q5a / Q6**: The H-RF definition already carries the complete separation argument — *"The H-RF/H-W separation. H-RF bounds only the fires; H-W bounds trigger-true step-instances ... the two come apart at starvation ... a registry can satisfy H-RF (indeed have zero real fires) yet violate H-W: H-W is generically false under starvation, no usable route to H-RF though it formally implies it ... The route that does supply H-RF is Q5a."* It is then re-stated in H-W's definition (*"It implies the weaker H-RF ... but is no usable route to it; the structural route (Q5a) supplies the attainable H-RF directly, never H-W"*), again in Q5a (*"This supplies H-RF (above) by a route disjoint from Q5 ... does not establish H-W. The W machinery, the re-arm analysis, and the stratification heuristic are all unnecessary in this case"*), and again in Q6 (*"The starvation mode is why the operative hypothesis is H-RF, not H-W"*).

**Problem**: One relationship, four statements. After the H-RF separation argument the reader already knows H-W ⟹ H-RF, that the converse route is Q5a, and that starvation defeats H-W; the three restatements advance no reasoning. This is exactly the forward-reference accretion the classifier names: the H-RF and H-W *definitions* are front-loaded with which downstream claim supplies or consumes them (*"the operative hypothesis of the termination theorem (Q6)"*, *"consumed in Q6"*, *"The route that does supply H-RF is Q5a (below)"*) rather than with the hypothesis's content.

**Required**: State the separation once. Reduce the H-W-definition, Q5a, and Q6 restatements to a bare back-reference or cut them, and strip the downstream-consumer enumerations from the two definitions.

### Issue 2: Q0 states the members/targets_of/M_K default-value treatment twice

**ASN-0133, Q0**: First as a preview — *"three of the four — the collection-valued members, targets_of, and the domain base M_K — are also UV-rewritten, so carrying their default value takes, in addition, the same UV filter the behavior collections take (below)"* — then in full — *"The two view-parameterized collections members/targets_of, and with them the domain base M_K, carry their default value the same way: the UV filter {· : ¬filtered(·)} ... wrapped around the active rebuild ⋃(A_K, addrs_F) — both view-parameterized and UV-rewritten, they take the PC3 ⋃/∃-over-fixed-base rebuild for the audit and active values and this UV filter for the default."*

**Problem**: The same classification (these three are both view-parameterized and UV-rewritten, so they take the PC3 rebuild for audit/active and the UV filter for default) is given twice, the first with a "(below)" pointer to the second. The preview adds nothing the full statement doesn't.

**Required**: State it once, where the rewrite is actually specified; drop the preview.

### Issue 3: PC4 miscited as the warrant for value-preservation across the rewrite

**ASN-0133, Q0 and the "Value-preservation, at one state" subsection**: *"a change of spelling, not of value (PC4)"*; and *"The two spellings agree — PC4 —"*.

**Problem**: PC4 (Purity) says a *single* PL term is a deterministic function of state — two evaluators of the same term agree. It does not establish that two *distinct* terms (the naive merge and the rewrite) denote the same value. What establishes equal value is PC3's view machinery (succs is fixed-view, so reads its active slice at any term view) composed with UV's default-view *definition* of the filtered result — and the worked computation demonstrates it (both spellings yield ∅ for succs(s₀)). Citing PC4 names the wrong premise for the agreement.

**Required**: Attribute value-preservation to PC3's fixed-view/cross-view rebuild equations and UV's default-view definition (the premises doing the work). Keep PC4 only if invoked for the separate principle that equal denotation implies interchangeability.

## OUT_OF_SCOPE

### Topic 1: Compositional quiescence across registries

**Why out of scope**: RG models one registry with all other registries folded into the environment (*"other agents, other registries ... all emit through the same surface"*). The natural global question — when is the *union* of all registries jointly quiescent, given each is the others' non-idling environment — is not a single-registry property and does not follow by composing Q6 (registry B's real fires are registry A's environment steps, which re-arm A). This is a distinct abstraction from OQ3's per-scope/global split *within* a registry, and belongs to a future compositional treatment rather than a revision here.

VERDICT: REVISE
