# Review of ASN-0047

## REVISE

### Issue 1: Broken reference to "rejection model fixed in the preamble above"
**ASN-0047, worked examples**: Multiple counterfactual steps reference "Per the rejection model fixed in the preamble above" (node baptism Steps 2 and 3; ghost-base versioning Step 3; link allocation Step 5 reasoning).
**Problem**: No preamble or section in the ASN establishes a "rejection model." The intended semantic — that a transition fails to fire when its preconditions are unsatisfied — is standard operational semantics but is not formalized anywhere in the body.
**Required**: Either add an explicit "Rejection model" subsection (e.g., in the elementary transitions preamble) stating that a transition with unsatisfied preconditions does not enter the transition set, or rephrase the references to cite the precondition mechanism directly.

### Issue 2: Broken reference to "Scope and base-liveness analysis above"
**ASN-0047, ghost-base versioning example**: "The case admits `t ∉ E_doc` per *Scope and base-liveness* at K.δ."
**Problem**: No section titled *Scope and base-liveness* exists in the ASN. The intended content (ghost-base versioning admissibility) is discussed inline in the K.δ table but not under that section heading.
**Required**: Either add a named subsection in K.δ titled "Scope and base-liveness," or rephrase the cross-reference to point to the actual location (e.g., "per the K.δ table's k=1 ghost-base row").

### Issue 3: Broken reference to "Reconciliation with ASN-0043's L1c"
**ASN-0047, K.λ first-link case**: "exactly as the *Reconciliation with ASN-0043's L1c* paragraph in the *Allocator hierarchy under documents* section above establishes."
**Problem**: No paragraph by that name exists in the Allocator hierarchy section. The reconciliation content (treating L1c as structural producibility, not state) is discussed but not under that section heading.
**Required**: Add the named paragraph or rephrase the reference.

### Issue 4: Broken reference to "Per-state arrangement shape (D-SEQ★)"
**ASN-0047, D-SEQ★ derivation**: "D-SEQ★ is the per-state invariant pointed to from *Per-state arrangement shape (D-SEQ★)* in the Elementary transitions section above."
**Problem**: No section by that name exists in Elementary transitions. The forward reference structure (K.μ⁻ depends on D-SEQ★, which is derived later) is real, but the named pointer doesn't resolve.
**Required**: Add the named subsection or remove the broken pointer.

### Issue 5: T_link undefined
**ASN-0047, Orphan links section**: References "R_L ⊆ T_link × E_doc" in a hypothetical aside about a counterfactual link-provenance relation.
**Problem**: T_link is never defined. T_elem is defined (`{a ∈ T : IsElement(a)}`) but no analogous T_link definition exists.
**Required**: Either define T_link (e.g., `{a ∈ T : IsElement(a) ∧ fields(a).E₁ = s_L}`) or rephrase to avoid the undefined symbol.

### Issue 6: K.μ~ Case 2 labeling misleads — it is a sub-argument, not a third case
**ASN-0047, Decomposition of K.μ~**: Cases 1, 2, 3 are presented as if they partition the decomposition space, but Case 2 actually proves "π ≠ id implies dom_C(M(d)) ≠ ∅," which is a precondition argument for Case 3, not a separate decomposition case. The substantive cases are: (a) π = id ⟹ zero steps; (b) π ≠ id ∧ dom_C(M(d)) ≠ ∅ ⟹ K.μ⁻ + K.μ⁺.
**Problem**: The Case 1/Case 2/Case 3 numbering suggests three exhaustive cases when there are really two cases plus a sub-argument; readers must work past the labeling to follow the actual decomposition logic.
**Required**: Either relabel (e.g., "Case 1: π = id (zero steps, applies whenever dom_C(M(d)) = ∅, per the argument below); Case 2: π ≠ id with dom_C(M(d)) ≠ ∅"), or fold the Case 2 argument into Case 1's justification.

### Issue 7: P3 retained as "orienting prose only" with no proof obligation
**ASN-0047, Permanence section**: P3 is explicitly described as "purely qualitative mode-enumeration" carrying "no formal proof obligation in this ASN," with P3★ doing all the load-bearing work.
**Problem**: A labeled invariant that carries no proof obligation is an accretion that the reader must mentally distinguish from the formal version. The text instructs readers to "treat P3 as a one-line mode-enumeration summary" — but then it should be one line, not a labeled invariant with a derivation framework.
**Required**: Either remove P3 entirely (P3★ is sufficient) or reduce it to one inline sentence describing the three modes, without a separate labeled invariant.

### Issue 8: K.μ⁻ amendment paragraph is redundant with K.μ⁻'s own postcondition
**ASN-0047, Amendments to existing transitions, K.μ⁻ amendment (PerSubspaceContiguity)**: The amendment paragraph mostly restates that K.μ⁻'s D-CTG/D-MIN postconditions apply per-subspace — content that is already explicit in the K.μ⁻ definition's effect clause and case analysis.
**Problem**: The amendment paragraph adds no new constraint; it merely lifts the K.μ⁻ definition's per-subspace structure into a labeled "amendment." This is the kind of meta-prose around an axiom that explains rather than advances.
**Required**: Remove the redundant amendment paragraph, or strengthen it with content not already in K.μ⁻'s definition (e.g., explicit cross-subspace independence statements not derivable from the per-subspace postconditions).

### Issue 9: SubAllocatorAxiom's "namespace property" obscures the freshness chain
**ASN-0047, SubAllocatorAxiom**: The axiom packages multiple operational claims: (a) two distinct sub-allocators exist under each d, (b) they are disjoint, (c) each first emission satisfies a namespace property closing freshness without T10a's GlobalUniqueness.
**Problem**: The axiom is justified by Nelson and Gregory evidence (per Design provenance), but its formal structure conflates three distinct claims into one named axiom. The K.α and K.λ proofs alternate between "by SubAllocatorAxiom" and "by GlobalUniqueness" without a clean structural argument for *which* claim discharges which obligation in each case (first-emission vs. subsequent emission).
**Required**: Either split SubAllocatorAxiom into three labeled sub-axioms (Existence, Disjointness, NamespaceProperty), or add an explicit dispatch table showing exactly which claim discharges each freshness obligation across K.α, K.λ first-link, and K.λ subsequent-link cases.

### Issue 10: The "Two scopes of T10a's domain" predicate definitions are load-bearing but tucked inside K.δ
**ASN-0047, K.δ section**: `InTumblerUniverse(t, s)` and `InEntityAllocatorDomain(t, s)` are defined as predicates inside K.δ's precondition discussion, but they are used elsewhere (ghost-base discharge across the chain, freshness path discrimination).
**Problem**: Load-bearing predicate definitions belong at structural top-level or in a notation preamble, not embedded inside a transition's precondition table. As written, readers consulting later sections must trace back to the K.δ section to find these definitions.
**Required**: Promote these predicate definitions to a top-level "Predicates and notation" section, or at least to an explicit "Definitions used in K.δ" subsection with a clear cross-reference from downstream uses.

### Issue 11: Cross-document disjointness lemma Case B sub-case enumeration is informal
**ASN-0047, Cross-document disjointness chain proof**: The proof's Case B has three sub-cases (i) same-allocator siblings, (ii) cross-lineage allocators, (iii) mixed version/sibling configurations. The text states "(i)–(iii) are not formally disjoint sub-cases of a partition — they enumerate dispatch strategies under T10a."
**Problem**: A proof by case analysis whose cases are "not formally disjoint" but "enumerate dispatch strategies" is hand-wavy. Either the cases partition the space (formally disjoint and exhaustive) and dispatch to T10a is per-case, or they do not partition and the argument has a gap.
**Required**: Either rework Case B into formally disjoint sub-cases with explicit partition verification, or prove that any pair `(d₁, d₂)` of prefix-incomparable documents falls into *at least one* of (i)–(iii) by S7d's allocator structure — a coverage lemma, even if cases overlap.

### Issue 12: Notational inconsistency — dom_C(M(d)) vs V_{s_C}(d)
**ASN-0047, throughout**: Both `dom_C(M(d))` and `V_{s_C}(d)` are used to refer to the content-subspace V-positions of d. The ASN treats them as interchangeable but never explicitly equates them.
**Problem**: Two distinct notations for the same set, used in different sections, force the reader to mentally bridge.
**Required**: Either choose one notation and use it consistently, or add an explicit notational note: `dom_C(M(d)) := V_{s_C}(d) := {v ∈ dom(M(d)) : subspace(v) = s_C}`.

### Issue 13: "Three discharge paths" is referenced as a named catalogue but not headlined
**ASN-0047, K.δ section**: The Two-scopes discussion mentions "the three discharge paths named in the table — Path 1 ..., Path 2 ..., Path 3 ..." Several worked examples cite "path 2 of the *Three discharge paths for `e ∉ E` — named rules* catalogued at K.δ."
**Problem**: The K.δ table lists Path 1/2/3 in a column, but there is no subsection or named catalogue headlined "Three discharge paths for `e ∉ E` — named rules." The reference is to a structure that exists implicitly in the table but isn't formally named at a section level.
**Required**: Add a brief headlined paragraph (e.g., "**Three discharge paths for `e ∉ E`** — named rules. Path 1: ..., Path 2: ..., Path 3: ...") so that downstream citations resolve to a concrete location.

### Issue 14: K.μ~ contract's bijection equation under-determines π without explicit acknowledgement of consequence
**ASN-0047, K.μ~ contract**: "π is existentially quantified: any bijection satisfying the equation is a witness. Under ASN-0036's S5 (UnrestrictedSharing), multiple witnesses may satisfy the equation when V-positions share an I-address, but the multiset of I-addresses placed at each subspace's V-positions is identical across witnesses, so under-determination is benign."
**Problem**: Under-determination is asserted to be benign, but no proof or example demonstrates that all valid witnesses produce semantically equivalent post-states. If multiple π satisfy the equation, an implementation might choose different ones; whether implementations differ in observable post-state is not analyzed.
**Required**: Either prove that all valid π satisfying the bijection equation yield identical M'(d) (which would make the under-determination irrelevant), or prove that the differences between valid π are unobservable through subsequent operations (which would justify "benign").

### Issue 15: P7a derivation's "fresh-content branch" leans on J0 but J0's introduction lacks proof of P7a sufficiency
**ASN-0047, P7a derivation**: For freshly allocated `a`, "J0 gives `a ∈ ran(M'(d))` for some d; ... J1 gives `(a, d) ∈ R'`."
**Problem**: J0 is axiomatic (places fresh `a` in some arrangement). J1 then forces `(a, d) ∈ R'`. But the chain is "J0 + J1 + frame ⟹ P7a." The ASN states this orientation but does not explicitly verify that the J0+J1 composite always covers *which* d receives the address — multiple valid composites might choose different d, and P7a needs only existence, which is supplied. The derivation is essentially correct, but the "J0 alone underdetermines d" observation deserves explicit acknowledgement to forestall confusion about whether P7a requires a unique d.
**Required**: Add one sentence clarifying that P7a's existential is closed regardless of *which* d J0 places the fresh address in.

## OUT_OF_SCOPE

### Topic 1: Tombstone-style link withdrawal mechanism
**Why out of scope**: The ASN explicitly identifies this as a known gap (Structural sufficiency and known gaps, plus Open Questions). The K.μ⁻ amendment forbids interior link-subspace contraction, ruling out Nelson's tombstoning design as expressible. A separate mechanism (status flag, retraction link, per-link liveness) belongs to a future withdrawal-specific ASN.

### Topic 2: Version-management semantics beyond K.δ k=1
**Why out of scope**: The richer version contract (arrangement invariants between successive versions, content-allocator linkage, provenance flow, lineage acyclicity) is deferred to a subsequent version-management ASN. K.δ k=1 admits the elementary step; the surrounding semantics is future work.

### Topic 3: Non-T10a allocator admissibility
**Why out of scope**: The elementary set assumes T10a-conforming allocation for content (K.α), links (K.λ), and non-node entities. Externally injected addresses, reused decommissioned addresses, or alternative uniqueness disciplines fall outside the elementary set's contract and are correctly identified as a deferred topic.

### Topic 4: Account-level k=1 entity extension
**Why out of scope**: Currently excluded by K.δ's precondition. The ASN's Open Questions identifies this as a future-extension question; admitting it would require an account-version semantics not currently in the design.

### Topic 5: Self-transclusion (K.μ⁺ from a document to itself)
**Why out of scope**: K.μ⁺'s preconditions admit `M(d)` extending with new V-positions referencing existing I-addresses, including I-addresses originally allocated under d itself. The framework neither forbids nor specially accommodates this. Whether self-transclusion has special semantics belongs to operation-level design, which is correctly out of scope.

VERDICT: REVISE
