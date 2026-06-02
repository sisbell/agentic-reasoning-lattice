# Review of ASN-0086

I checked the proofs (CoverageEqualityDecidable, R0, R0a, R-Scope, the two wp cases, and the five-step worked sketch) and the foundation usage. The mathematics is sound: the inlined T1-successor argument in CoverageEqualityDecidable is valid, R0a's two-case antichain proof holds, R-Scope's arity-independence is correctly grounded in the R0a antichain, and the boundary cases (empty link store, first/subsequent emission, self-targeting, retraction-of-retractor, self-nullification) are each exercised concretely. Cross-references are all to foundation ASNs (0034/0036/0040/0043/0093).

The note carries the anti-bloat classifier, and the residual findings are accreted foundation-inventory prose, not correctness defects.

## REVISE

### Issue 1: ASN-0093 K-operation / chain structure inventoried three times
**ASN-0086, "The Two Foundational Sets" → *Foundation.***: "ASN-0093 owns the K-operation contract — the three primitive emissions K.σ (DocumentRegistration), K.α (ContentAllocation), K.λ (LinkAllocation) — together with the sub-allocator chain lemmas making T10a's runtime activation chain explicit..."

**Problem**: This is a use-site inventory of the foundation's contents that duplicates the intro paragraph ("ASN-0093 wraps that primitive ... in three K-operations — K.σ, K.α, K.λ — that fix the sibling-frontier emission discipline and the sub-allocator chain structure") and overlaps again with the "Allocator Structure" opening ("ASN-0093 supplies the sub-allocator structure this note relies on..."). Three paragraphs assert that ASN-0093 provides the K-operations and chain lemmas. The "Allocator Structure" instance is load-bearing (it introduces the names `A_C(d)`, `A_L(d)`, `b_C(d)`, `b_L(d)` actually used); the *Foundation.* paragraph adds only the `SC-NEQ` naming on top of pure restatement.

**Required**: Collapse the *Foundation.* paragraph to the one fact it uniquely contributes (the named consequence `SC-NEQ`), and let the intro carry the motivation and "Allocator Structure" carry the name introductions. The K.σ/K.α/K.λ roster does not need a third statement.

### Issue 2: scope-justification parentheticals in the wp load-bearingness prose
**ASN-0086, Weakest-Precondition Analysis, *The unit-depth discipline is load-bearing***: "(Every Σ reached using only the relational layer's operations qualifies under both restrictions: those operations keep states →*-reachable and commit to the discipline.)"

**Problem**: This parenthetical re-states, in a justification slot, a fact already established by the "Definition — relational layer" commitment and the layer's stated discipline obligation. It explains *why the restriction is safe for the layer's own callers* rather than advancing the wp derivation, which is the meta-prose pattern the classifier targets. The same point recurs at the end of the *Result* disjunction paragraph ("The Nullify-as-sole-R-producer rule satisfies the first disjunct...").

**Required**: Drop the parenthetical; the layer-coverage claim belongs once, at the relational-layer definition, not duplicated inside the load-bearingness argument.

## OUT_OF_SCOPE

### Topic 1: elevating the unit-depth retraction discipline to a substrate guarantee
The wp Case 2 result holds only over the unit-depth-disciplined sub-domain, with the discipline kept as a layer convention rather than a substrate-enforced shape constraint on `L_R` to-spans. This is a genuine design tension (a direct K.λ caller can craft a non-unit-depth retraction span), but the note already records it as an explicit Open Question. It is future-ASN territory (a possible designated retraction K-operation), not an error here.

VERDICT: REVISE
