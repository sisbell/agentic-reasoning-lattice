# Review of ASN-0093

This note is technically sound — the simultaneous-induction discipline is stated carefully, the chain exhibitions for C1c/L1c are explicit, the Cross-document disjointness argument handles both the prefix-comparable and prefix-incomparable cases, and FirstEmissionFreshness consumes only pre-state facts so the induction is non-circular. The worked example is appropriately concrete. The remaining findings are accretion: meta-prose and redundant discharge that the precise reader must skip past, flagged under the note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Factoring-provenance prose in the introduction does not advance substrate reasoning

**ASN-0093, intro**: "The factoring is downward from a fuller transition model: the central rewrite is one notational substitution — `E_doc` ... is replaced by `dom(M)` ..." and "Higher-layer transition models fold both into a larger state model that also tracks entity allocation and arrangement provenance — `Σ = (C, L, E, M, R)` — and supply the operational primitives for the full state."

**Problem**: This explains *where the note came from* and *what a downstream layer looks like* (`E`, `R` components the substrate explicitly disclaims). It is provenance rationale, not content the substrate's claims depend on. The reader must skip past `Σ = (C,L,E,M,R)` and the `E_doc → dom(M)` history to reach the actual state model `Σ = (C,L,M)`.

**Required**: Reduce to the one load-bearing sentence — the substrate state is `(C,L,M)` and `dom(M)` is the document set — and delete the factoring-history and higher-layer-fold prose.

### Issue 2: Defensive justifications for restating/adding inherited invariants

**ASN-0093, C0**: "Restated here (rather than inherited silently) so the substrate is self-contained — symmetric to L12 on the link side."
**ASN-0093, C1b**: "ASN-0036 carries no content-side `#E(a) ≥ 2` invariant, so this is added here as a substrate-level commitment (parallel to the L0 C-clause)."

**Problem**: These explain *why* a claim is present rather than what it asserts. Whether a claim is inherited or fresh is bookkeeping; the invariant either holds in this note or it does not. The "symmetric to L12" / "parallel to the L0 C-clause" asides are cross-claim editorializing.

**Required**: State each invariant and its discharge. Drop the meta-commentary about inheritance provenance; the Properties table's Source column already records origin.

### Issue 3: Each invariant's discharge is stated in three or four places

**ASN-0093, C1c / L1c**: the discharge appears in (a) the invariant body, (b) the discharge matrix row, (c) the dedicated "C1c/L1c chain exhibition" subsection, and (d) the Properties Introduced "Source" cell — the latter reproducing the full chain ("first-emit chain has two steps `(d → b_C(d) → a)` with `k₁ = 2`, `k₂ = 1` and lengths `#d → #d + 2 → #d + 3`...").

**Problem**: The Source column of the Properties table restates the chain exhibitions in compressed form; the discharge matrix restates them again as "Discharged at new key via the T10a-conforming step sequence (see ... below)." Two paragraphs (matrix cell, table cell) plus the full exhibition say the same thing. This is exactly the "say the same thing in different words" pattern, multiplied across every invariant.

**Required**: Pick one authoritative location for each discharge (the chain exhibition for C1c/L1c, the matrix for the frame-only invariants) and make the other locations bare pointers ("C1c: see chain exhibition") rather than re-derivations.

### Issue 4: `K.σ` admissibility-scope paragraph is forward-reference rationale

**ASN-0093, K.σ**: "*K.σ admissibility scope.* ... In particular, K.σ admits configurations broader than Nelson's hierarchical baptism ... Downstream ASNs that lift entity-hierarchy discipline (entity stratification, lineage, version-allocator activation — see Scope, *Entity allocation*) tighten K.σ's precondition accordingly."

**Problem**: The operative content — K.σ's precondition is structural-only (`ValidAddress ∧ zeros = 2`) — is already in the precondition list. The paragraph then justifies that breadth by appeal to what downstream ASNs will do, deferring to the same "Entity allocation" Scope item already cited elsewhere. This is "explains why the axiom/precondition is the way it is rather than what it says," plus a redundant downstream deferral.

**Required**: Keep at most one sentence stating the precondition is structural-only; delete the Nelson-baptism contrast and the downstream-tightening forward reference (the Scope section already records the deferral).

### Issue 5: `ValidAddress` identification carries a use-site inventory

**ASN-0093, M0 Definitional identification**: "The substrate uses `ValidAddress(d)` in operation preconditions and invariants for readability; any foundation claim whose precondition names T4-validity discharges that precondition directly via this identification."

**Problem**: The identity `ValidAddress(d) ≡ d satisfies T4` plus T4's four conjuncts is the content. The trailing sentence is a use-site inventory ("in operation preconditions and invariants for readability ... discharges that precondition directly") — instructions about how the term will be consumed, not the definition itself.

**Required**: Keep the identity and the conjunct expansion; delete the readability/discharge-mechanics sentence.

### Issue 6: The same deferred machinery is deferred in multiple sections

**ASN-0093**: link withdrawal is deferred in Scope ("Link withdrawal ... deferred to a higher-layer ASN ... e.g., a future tombstoning ASN"), again in the state-model commentary, and again at length in Open Questions ("Link withdrawal — which invariant must a withdrawal mechanism revisit?"). Entity allocation and arrangement mutation are likewise deferred in Scope and re-deferred in the K.σ paragraph and the state-model prose.

**Problem**: "Multiple paragraphs in different sections defer to the same downstream location" — each deferral re-explains the same boundary. The Open Questions entry on withdrawal additionally enumerates three hypothetical formulations the substrate does not adopt, which is design-space essay content rather than a substrate claim.

**Required**: Consolidate each deferral to a single Scope bullet. Trim the Open Questions withdrawal entry to the one fact that matters here (L12's value-equality clause is the load-bearing constraint a withdrawal mechanism must revisit); move the three-formulation taxonomy to the withdrawal ASN where it belongs.

## OUT_OF_SCOPE

The deferrals to arrangement mutation, entity stratification, provenance, coupling, and tombstoning are correctly scoped out; the substrate's `(C,L,M)` factoring is a legitimate spec layer (it defines state, three operations on state, and the invariants they preserve). No content has drifted into implementation mechanics — the `inc`/`zeros`/anchor structure is all stated abstractly against the foundation. The issues above are presentation accretion, not scope or drift problems.

VERDICT: REVISE
