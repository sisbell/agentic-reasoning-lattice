# Review of ASN-0086

## REVISE

### Issue 1: "the converse fails" is mis-cited and possibly false
**ASN-0086, Lemma — K-Step Conformance Preservation**: "since `Σ_init` is substrate-conforming, every `→*`-reachable state is substrate-conforming, and the converse fails (Remark — NestedLinkWitness)."

**Problem**: The stated implication is `→*-reachable ⟹ substrate-conforming`. Its converse is `substrate-conforming ⟹ →*-reachable`; "the converse fails" therefore asserts the existence of a *substrate-conforming* state that is *not* `→*`-reachable. The cited witness — NestedLinkWitness — is explicitly **not** substrate-conforming (it violates frontier-landing clause (c)); it witnesses the strictness of a different inclusion, `substrate-conforming ⊊ state-local-conforming`. The Remark's own containment chain marks only the *rightmost* inclusion strict and is silent on `→*-reachable ⊊ substrate-conforming`. So the citation does not support the claim.

Worse, the claim may be false: R7a (NoExtraClassAffectsL) shows every conforming `↝`-step's `Σ.L`-effect decomposes into K.σ/K.λ `→`-steps, and `→ ≡ K.σ ∪ K.α ∪ K.λ` is asserted to be the complete primitive vocabulary — which suggests every conformance-reachable state may in fact be `→*`-reachable, i.e. the converse *holds*.

**Required**: Either (a) exhibit a genuine substrate-conforming state reached only by a conforming non-K-op `↝`-step and not `→*`-reachable, and reconcile it with R7a; or (b) drop the "converse fails" clause entirely. As written it is an unsupported/mis-cited claim in a load-bearing lemma.

### Issue 2: a_emit "formula, not a commitment" — defensive meta-prose with forward deferral
**ASN-0086, Definition — `a_emit`**: "It is a formula, not a commitment: `a_emit` carries no claim that K.λ deposits its value. K.λ commits `a_emit(Σ, d)` only when the chain frontier at `d` is well-formed (Definition — Emit_K); at a non-frontier state (Remark — NestedLinkWitness) the formula still yields a value but no legitimate K.λ-edge exists there, so the two are co-extensive precisely on the frontier-well-formed states."

**Problem**: `a_emit` is a total function of `(Σ, d)` by its preceding definition; the paragraph then defends against a non-frontier case the definition does not exclude, deferring forward to two downstream locations. This is the flagged "imagines a case / forward-deferral" pattern — the reader must hold Emit_K and NestedLinkWitness in mind to parse a definition that is already complete.

**Required**: Delete. `a_emit`'s totality is stated; the frontier/commitment relationship belongs (once) at Emit_K, where partiality is actually defined.

### Issue 3: the non-frontier / NestedLinkWitness case is re-explained in four separate sections
**ASN-0086** — the same non-frontier nested-pair scenario is restated at: Definition — `a_emit` ("at a non-frontier state…"), Definition — Emit_K ("At a state carrying a non-frontier nested link pair `a ≼ a''`…"), wp Case 1 PC load-bearingness ("Dropping PC admits the non-conforming nested link pair…"), and wp "The discipline alone is insufficient" ("Witness a state-local-conforming but non-substrate-conforming Σ of the kind Remark — NestedLinkWitness constructs…").

**Problem**: This is the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." The wp uses (Case 1 PC, discipline-insufficiency) are legitimate object-level invocations; the a_emit and Emit_K restatements are redundant scaffolding around the same Remark.

**Required**: Keep the single canonical statement at Remark — NestedLinkWitness and the two genuine wp invocations; remove the duplicative explanatory restatements at a_emit and trim Emit_K to a one-line pointer.

### Issue 4: Emit_K introduction explains notation rather than advancing meaning
**ASN-0086, Definition — Emit_K**: "K is a type-index (subscript), not a value argument; each fixed K gives a distinct operation with the same shape."

**Problem**: This is notation commentary in a structural slot — it tells the reader how to read the subscript rather than stating what Emit_K does. The signature line already shows K as a family index.

**Required**: Remove; the indexed signature carries this without prose.

## OUT_OF_SCOPE

### Topic 1: cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: Raised in Open Questions; a structural ratio guarantee on retraction is new territory, not a defect in the present invariants.

### Topic 2: relationship between `L_K` and arrangements `Σ.M` for visibility-dependent predicates
**Why out of scope**: Listed as an Open Question; requires coupling the relational layer to arrangement state, which this note deliberately holds out of scope.

VERDICT: REVISE
