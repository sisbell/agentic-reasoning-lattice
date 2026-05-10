# Review of ASN-0026

## REVISE

### Issue 1: P4 relies on undefined predicate `independent_creation`
**ASN-0026, P4 — Creation-Based Identity**: "`independent_creation(a, b)` holds when `a` and `b` were allocated by distinct creation acts"
**Problem**: The predicate `independent_creation` appears in the formal statement but is never formally defined. The prose says it means "allocated by distinct creation acts," but "creation act" is not formalized either. The ASN then claims P4 follows from T9 (forward allocation) and T10 (partition independence), but if it does, P4 is a derived property and the derivation should be shown — not a new axiom with an undefined predicate.
**Required**: Either (a) define `independent_creation(a, b)` formally in terms of the allocation model (e.g., "allocated by distinct invocations of `inc`" or "having distinct allocator prefixes"), or (b) state P4 as a corollary of T9+T10 with an explicit derivation. The current formulation sits between axiom and corollary and commits to neither.

### Issue 2: Σ.D has no structural properties
**ASN-0026, The State**: "Σ.D is the set of all documents that currently exist."
**Problem**: Two structural properties are missing. First: the ASN never states that Σ.V(d) is defined iff d ∈ Σ.D. Properties P2, P5, P7 quantify over Σ.D and presuppose that Σ.V(d) exists for each member, but this connection is implicit. Second: no axiom governs Σ.D's lifecycle — can documents be destroyed? If Σ.D can shrink, P7's postcondition needs a quantifier restriction (only over documents that survive the operation). If Σ.D is monotonic (like Σ.I), that should be stated as an axiom parallel to P1.
**Required**: (a) State the structural connection: `Σ.V(d) is defined ⟺ d ∈ Σ.D`. (b) Either state a monotonicity axiom for Σ.D or explicitly defer document lifecycle to a future ASN with a note that P7's universally quantified postcondition assumes all documents in the pre-state survive.

### Issue 3: P9 formalization is incomplete
**ASN-0026, P9 — Mapping Preservation Under INSERT**: "When INSERT introduces k new positions at position p in document d..."
**Problem**: Three gaps. (a) No precondition on p. The valid range is presumably `1 ≤ p ≤ n_d + 1` (allowing insertion before all content and after all content), but this is unstated. (b) The formal clauses cover surviving positions only. The new positions `p, p+1, ..., p+k-1` are described in prose ("map to the freshly allocated I-addresses") but not in the formal statement. A third clause is needed: `(∀ j : p ≤ j < p+k : Σ'.V(d)(j) ∈ fresh ∧ fresh ∩ dom(Σ.I) = ∅)`. (c) The post-state document length `n_d + k` is never formally asserted — the reader must infer it from the two clauses.
**Required**: Add the precondition `1 ≤ p ≤ n_d + 1` (or whatever the intended range is), add a formal clause for the new positions, and state the post-state length `|Σ'.V(d)| = n_d + k`.

### Issue 4: I-Space Extension freshness is assumed, not derived
**ASN-0026, I-Space Extension Classification**: "Σ'.I = Σ.I +_ext fresh where ... fresh ∩ dom(Σ.I) = ∅"
**Problem**: The freshness condition `fresh ∩ dom(Σ.I) = ∅` is stated as part of the definition of `+_ext`, but it is a substantive claim that requires derivation. The derivation exists: T9 (forward allocation) gives strictly increasing addresses within an allocator, and T10 (partition independence) prevents collisions between allocators, so no new address can coincide with an existing one. But the ASN presents freshness as a definitional given rather than a consequence of the allocation discipline.
**Required**: Derive the freshness condition explicitly from T9 and T10 (or from P4, if P4 is tightened per Issue 1). This is a two-line argument but it must be shown.

### Issue 5: Preservation Obligation misclassifies several properties
**ASN-0026, Preservation Obligation**: "Operation-relevant invariants — properties that a badly defined operation could violate, requiring per-operation verification: P0, P1, P2, P5, P7, P9."
**Problem**: This list conflates three different kinds of properties. (a) P5 is a *permission* (non-injectivity is allowed), not a constraint. No operation can violate a permission — there is nothing to preserve. (b) P9 is a *postcondition* of INSERT, not a state invariant. It constrains one operation's behavior, not all reachable states. Listing it alongside P0 and P1 (which every operation must preserve) creates a false equivalence. (c) P8 (no reference counting, corollary of P1) is omitted from both categories without explanation.
**Required**: Distinguish three categories: state invariants (P0, P1, P2, P7 — must hold in every reachable state), operation postconditions (P9 — must hold after INSERT), and structural permissions (P5 — permitted by the model, not an obligation). Note that P8 and NO-REUSE are corollaries that inherit preservation from their parent axioms.

### Issue 6: P11 is vacuous within the state model
**ASN-0026, P11 — Viewer Independence**: "(∀ viewers u₁, u₂ : Σ.V(d) as seen by u₁ = Σ.V(d) as seen by u₂)"
**Problem**: The state model defines `Σ.V(d) : [1..n_d] → Addr` with no viewer parameter. P11 quantifies over "viewers," but viewers are not a concept in the model. Since Σ.V(d) is a plain function with no viewer argument, the property is trivially true by construction — there is nothing to vary. The accompanying prose explains the *intent* clearly (back-end delivery is viewer-invariant; front-end rendering may differ), but the formal statement has no teeth.
**Required**: Either (a) introduce a minimal viewer concept into the model (even just to rule it out — e.g., "the signature of Σ.V deliberately excludes a viewer parameter; this is a design constraint, not an accident"), or (b) reformulate P11 as a constraint on the RETRIEVE protocol ("RETRIEVE takes (document, position) and returns a deterministic result — no viewer, session, or context parameter exists in the protocol signature"). The current formalization quantifies over a phantom type.

### Issue 7: Property numbering gaps
**ASN-0026, Properties Introduced**: Labels jump P5→P7 and P9→P11.
**Problem**: P6 and P10 are absent with no explanation. The commit history suggests these labels existed in a prior draft and were removed during revision. Unexplained gaps in a numbered property list create ambiguity — a reader cannot tell whether the gaps are reserved for future properties, accidentally deleted, or intentionally removed.
**Required**: Either renumber the properties to close the gaps, or add a note: "P6 and P10 are reserved / were removed during revision."

## OUT_OF_SCOPE

### Topic 1: Mapping preservation for DELETE, REARRANGE, COPY
**Why out of scope**: P9 establishes mapping preservation for INSERT. Analogous properties for the other operations (surviving positions retain I-addresses after DELETE; REARRANGE permutes but does not change I-addresses; COPY preserves target's existing mappings) belong in the respective operation ASNs, not here. The ASN correctly defers: "Full definitions are deferred to their respective operation ASNs."

### Topic 2: Connection layer referential rules
**Why out of scope**: The ASN notes that link endsets can reference addresses where nothing is stored ("ghost elements") and that "the content layer and the connection layer have different referential requirements." The content layer's rules (P2: no dangling V-references) are established here. The connection layer's more permissive referential rules belong in the link model ASN.

### Topic 3: Atomicity of compound operations
**Why out of scope**: The ASN raises this in Open Questions ("if INSERT requires both I-allocation and V-mapping, must both succeed or neither?"). This is a genuine design question but belongs in an operation semantics ASN, not in the dual-space architecture.

VERDICT: REVISE
