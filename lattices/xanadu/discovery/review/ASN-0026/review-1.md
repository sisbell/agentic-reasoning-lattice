# Review of ASN-0026

## REVISE

### Issue 1: P6 is formally identical to P0; P8 is formally identical to P1
**ASN-0026, P6 / P8**: P6 states `(A a : a in dom(Sigma.I) : Sigma'.I(a) = Sigma.I(a))` for V-space operations. P8 states `[a in dom(Sigma.I) ==> a in dom(Sigma'.I)]` regardless of `|refs(a)|`.
**Problem**: P0 already quantifies over *all* state transitions — not just V-operations. So P6's core claim is a specialization of P0 to a subset of transitions, adding nothing. P8 is literally P1 with an emphasis clause. The properties table lists all four as independently "introduced," obscuring the logical structure: there are two axioms (P0, P1) and two corollaries (P6, P8).
**Required**: Organize as axioms + corollaries. P0 and P1 are the axioms. P6's genuinely new content — the classification of which operations extend dom(Sigma.I) and the extension formula `Sigma'.I = Sigma.I +_ext fresh` — should be presented as a derived classification, not an independent property. P8 should be presented as a corollary of P1 with the design-contrast commentary preserved but the duplicate formal statement removed.

### Issue 2: P3 introduces an undefined term
**ASN-0026, P3**: `[Sigma.V(d)(p) = a ==> content delivered at position p is Sigma.I(a)]`
**Problem**: "Content delivered at position p" has no definition in the state model. The state model gives Sigma.V(d)(p) = a and Sigma.I(a) = byte. If "content delivered" means Sigma.I(Sigma.V(d)(p)), then P3 says Sigma.I(a) = Sigma.I(a) — tautological. If "content delivered" is a separate retrieval function, it must be defined. The explanatory text makes clear that P3 is ruling out transformed views, which is a meaningful constraint, but the formal statement doesn't capture it.
**Required**: Either define a retrieval function RETRIEVE(d, p) independently and assert RETRIEVE(d, p) = Sigma.I(Sigma.V(d)(p)), or state P3 as a constraint on the operation set: no operation in the system computes a function of Sigma.I(a) before delivering it. The current formulation falls between tautology and informal principle.

### Issue 3: P4 is not a well-formed state invariant
**ASN-0026, P4**: `[a ≠ b ==> the content at a and the content at b are distinct identities]`
**Problem**: "Distinct identities" is undefined. If it means "a ≠ b" — that is the hypothesis, not the conclusion. If it means "not interchangeable despite possibly equal byte values" — that is a semantic statement about what the system treats as identity, not a predicate on state. The table (Same I-addresses? / Shared origin visible?) communicates the intent better than the formal statement. P4 is really a constraint on the allocator: independent INSERT operations never produce the same I-address, regardless of content equality. This is formalizable but the current statement does not formalize it.
**Required**: Restate P4 as: for any two INSERT operations producing addresses a and b, if the operations are independent (not derived from the same creation act), then a ≠ b — even when the inserted byte sequences are identical. This captures "creation-based identity" as a property of allocation, not as a vague predicate on state.

### Issue 4: P9 and P10 describe implementation representation, not abstract state
**ASN-0026, P9 / P10**: P9 discusses "mapping entries" being split with exact I-span partition. P10 discusses "coalescing" two entries requiring exact I-address adjacency.
**Problem**: The abstract state model defines Sigma.V(d) as a function from positions to addresses. Functions do not have "entries." Entries are a representational choice (how the function is stored — e.g., as a span table in a POOM). Splitting an entry into two entries that represent the same function does not change the abstract state. P10 is entirely about representation: coalescing two entries into one that represents the same function is an optimization invisible at the abstract level. The ASN acknowledges this tension ("P10 is an abstract property, not an implementation detail") but the claim is false — coalescing IS an implementation detail because it has no effect on Sigma.V(d).
**Required**: P9 should be reformulated as a property of INSERT: inserting at position p preserves the I-mapping at all positions that survive (with appropriate index shifting). This is the abstract content underlying the span-splitting discussion. P10 should be removed from this ASN or moved to a note — it constrains representation, not state. If the ASN wants to discuss span-level representation, it should first introduce spans as part of the abstract model (as ASN-0001 does with T12).

### Issue 5: Mutable vs. immutable document-version ambiguity
**ASN-0026, State section**: "For each document-version d, Sigma.V(d) : [1..n_d] → Addr"
**Problem**: The vocabulary defines a version as "an immutable snapshot of a document's V-space arrangement." If d is a version (immutable), then Sigma.V(d) is fixed — operations create new versions, they don't modify existing ones. But the operation descriptions say DELETE "removes mappings, shifts positions" and INSERT "inserts new mappings" — language implying mutation of d's mapping. P7 ("editing d does not affect Sigma.V(d') for d' ≠ d") is either trivially true (if versions are immutable, no operation affects any existing version's mapping) or meaningful (if the model permits mutation). The ASN must choose: does an operation on document d mutate Sigma.V(d), or does it create a fresh d' with the modified mapping? The answer affects the interpretation of every property.
**Required**: Either (a) model Sigma.V(d) as mutable, drop the word "version," and call d a document with mutable state, or (b) model operations as producing new version identifiers d' ∈ Sigma.D with the modified mapping, and state properties in terms of version creation rather than state mutation. Option (b) aligns with the vocabulary and makes the version DAG explicit. Either way, the choice must be stated.

### Issue 6: No base case for the invariant framework
**ASN-0026, Preservation Obligation**: "Each operation ASN must verify that its defined operation preserves P0 through P11."
**Problem**: This is the inductive step of an invariant proof. Where is the base case? The ASN must define the initial state Sigma_0 and verify that P0–P11 hold in it. Without this, the invariant framework is incomplete — you cannot conclude that the properties hold in any reachable state.
**Required**: Define Sigma_0 (e.g., Sigma_0.I = ∅, Sigma_0.D = ∅) and verify that all properties hold vacuously or substantively in the initial state.

### Issue 7: No concrete example
**ASN-0026**: The ASN proves REF-STABILITY and derives several consequences but never instantiates the model against a specific scenario.
**Problem**: A concrete example (e.g., "Document d has V-mapping {1↦a, 2↦b, 3↦c}; INSERT 'XY' at position 2 allocates fresh addresses f₁, f₂; the new mapping is {1↦a, 2↦f₁, 3↦f₂, 4↦b, 5↦c}; verify P0, P1, P2, P6 against this state") would ground the abstract definitions and expose any mismatch between the formal model and the intended semantics.
**Required**: At least one worked example showing a state, an operation, and verification of key properties against the resulting state.

### Issue 8: Cross-ASN forward references
**ASN-0026, Operations Classification / Preservation Obligation**: "INSERT ... Defined in ASN-0004", "Each operation ASN (ASN-0004, ASN-0005, ASN-0006, ASN-0011, ASN-0017) must verify..."
**Problem**: Self-containment requires that the ASN not reference other ASNs by number (exception: ASN-0001). These are forward references — they don't use other ASNs' results — but they create an explicit numbering dependency. If ASN-0004 is renumbered, merged, or split, ASN-0026 becomes stale.
**Required**: Replace ASN numbers with descriptions: "the ASN defining INSERT must verify..." The operations table's "Defined in" column should be removed or replaced with a note that operation definitions are deferred.

### Issue 9: Preservation obligation is over-broad
**ASN-0026, Preservation Obligation**: "Each operation ASN must verify that its defined operation preserves P0 through P11."
**Problem**: Not all properties are meaningful to verify per-operation. P11 (viewer independence) is a protocol-level architectural constraint — no single operation can violate it unless the operation introduces a viewer parameter. P4 (creation-based identity) constrains the allocator, not operations like DELETE or REARRANGE that never allocate. P3 (mapping exactness) constrains the retrieval path, not individual state transitions. Requiring all operation ASNs to verify all eleven properties creates busywork for properties that are structurally impossible to violate.
**Required**: Classify which properties are operation-relevant invariants (P0, P1, P2, P5, P6, P7 — these can be violated by a badly defined operation) and which are architectural constraints (P3, P4, P11 — these are verified once, not per-operation). State the preservation obligation only for the former.

## OUT_OF_SCOPE

### Topic 1: Full operation definitions and per-operation invariant proofs
**Why out of scope**: The ASN explicitly defers operation definitions and states a preservation obligation. The proofs belong in the operation ASNs.

### Topic 2: Link model formalization
**Why out of scope**: The ASN correctly marks Link Survivability as a "claim" and notes the link model is not formalized here. Link endsets, discovery, and the link index are separate concerns.

### Topic 3: Atomicity of compound operations
**Why out of scope**: The ASN raises this as an open question. Atomicity semantics require defining a failure model, which is a distinct specification concern.

### Topic 4: Version DAG structure and CREATENEWVERSION semantics
**Why out of scope**: How versions relate (DAG structure, forking, sharing) is a distinct specification concern, though Issue 5 above requires the ASN to at least clarify whether d is mutable or immutable.

VERDICT: REVISE
