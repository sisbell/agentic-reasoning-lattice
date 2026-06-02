# Review of ASN-0086

I checked the six relational properties (R0–R6c), the three operations, the wp analysis, and the worked sketch against the ASN-0034/0036/0040/0043/0093 foundations. The core is sound: R0a's antichain argument (both cross-home zero-counting and same-home uniform-length cases) is correct, R-Scope's single-tuple scope holds on both P-tgt branches, CoverageEqualityDecidable's cell argument is airtight (including the `c_k.0` immediate-successor gap test), and the worked-sketch arithmetic checks out digit-by-digit (`a₁=1.0.1.0.1.0.2.1` through `a₃=…2.5`). No correctness defect found. The findings below are the accreted meta-prose this note's anti-bloat classifier targets.

## REVISE

### Issue 1: L8-alignment restated three times
**ASN-0086, Definition — TypeEquivalence / Definition — TypedRelation / Notation — subscript read modulo ~**: "This is L8's (TypeByAddress, ASN-0043) notion of same_type, lifted…"; then after TypedRelation: "Coverage-equivalence at the type slot aligns `L_K` with L8's same-type relation, which also projects through coverage."
**Problem**: That `L_K`/`~` coincides with L8's `same_type` is asserted in TypeEquivalence, again in the subscript-notation note (coverage-class indexing), and again in the trailing sentence after TypedRelation. Two paragraphs saying the same thing in different words — the reader must confirm three times that no new content is being added.
**Required**: State the L8 alignment once (at TypeEquivalence, where `~` is defined) and drop the restatements.

### Issue 2: Definition — TupleAddress forward-asserts R1's result
**ASN-0086, Definition — TupleAddress**: "Define `addr : L^Σ → A_rel^Σ` by `addr(a, F, G) = a`. The map is an injection, with image the arity-3 slice…"
**Problem**: "The map is an injection" is exactly R1 (AddressInjectivity), proved two sections later. A definition slot asserts a lemma result that is then independently proved; the reader meets the same claim twice with no indication the first is unproved.
**Required**: Let the definition define the map (and, if needed, its image); move the injection claim to R1 alone, or have the definition point forward rather than assert.

### Issue 3: Corollary R5.1's type-slot exclusion is scope-defense, not derivation
**ASN-0086, Corollary R5.1**: "The type slot (slot 3) is excluded: R5 proves only the content slots, and placing `(a, δ(1, #a))` in slot 3 would alter the link's type endset — hence its coverage class — a materially different claim outside R5's scope."
**Problem**: This paragraph imagines and then rebuts a case the corollary already does not make. It explains why the corollary stops where it stops rather than advancing what it claims — the defensive-justification pattern. The corollary's content is "either content slot may carry the self-span"; the slot-3 disclaimer is meta-prose around that content.
**Required**: Drop the slot-3 exclusion paragraph. If a boundary marker is wanted, "(content slots only)" in the corollary statement suffices.

## OUT_OF_SCOPE

### Topic 1: Empty-to-set retraction (`G = ∅`, `K ~ R`)
The wp Case 2 escape branch states that a `K ~ R` call with `G = ∅` leaves `a ∉ nullified(Σ')`, but the worked sketch never exercises it. This is a legitimate illustrative gap, not an error — the wp derivation already covers it formally.

### Topic 2: Cross-`L_K`/`Σ.M` visibility invariants
The first Open Question (relating `L_K` membership to arrangement visibility) is genuinely new territory layered above this note's link-store scope, correctly deferred.

VERDICT: REVISE
