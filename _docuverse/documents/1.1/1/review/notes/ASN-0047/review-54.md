# Review of ASN-0047

## REVISE

### Issue 1: K.δ case (ii) k=2 sub-case description contains a confused sentence

**ASN-0047, K.δ definition, case (ii) "True hierarchical descent (k = 2)"**: "Hierarchically e drops one level... t is at parent(e)'s level — most directly t = parent(e) itself when extending from parent(e) for the first child of e's level." Then later, in the summary paragraph: "or in t being a sibling of parent(e) under parent(e)'s parent (when k = 2 enters parent(e)'s child-level from a sibling of parent(e))."

**Problem**: For k=2, `e = inc(t, 2)` appends `.0.1` to t, so `parent(e) = t` always. The "sibling of parent(e)" wording describes a case that cannot arise — if t were a sibling of parent(e), then `parent(e) = parent(t)`, but `parent(e) = t` directly contradicts this unless `t = parent(t)` (which is only possible at the root). The K.δ contract should be exhibited cleanly: for k=2, `parent(e) = t`.

**Required**: Remove the "sibling of parent(e)" sentence, or clarify that it describes the k=0 sub-case where t is at e's level (and parent(t) = parent(e)). The current text conflates the two sub-cases.

### Issue 2: SubAllocatorAxiom's relationship to T10a's allocator discipline is unclear

**ASN-0047, Allocator hierarchy section**: "These are *virtual allocator predecessors*: they are not themselves in `dom(C) ∪ dom(L)`... and they are not in any T10a allocator's domain — they have no inc-history."

**Problem**: Under T10a's normal interpretation, `[d.0.1]` and `[d.0.2]` would be siblings via `inc([d.0.1], 0) = [d.0.2]` within d's child sub-allocator — i.e., they would be in the *same* T10a allocator's domain. The axiom asserts they are bases of *distinct* sub-allocators with disjoint domains, which is a stronger structural claim than T10a admits. The ASN says T10a "forbids a single allocator from emitting two distinct sub-allocators via one inc operation," but does not clarify whether SubAllocatorAxiom (a) admits a richer allocator structure beyond T10a, (b) reinterprets `[d.0.s_C]` and `[d.0.s_L]` as non-T10a entities, or (c) something else. Downstream proofs (especially the cross-document T10a.6 → T10 chain) cite T10a.6 on document-level allocators, but the same chain at the sub-allocator level would need separate justification.

**Required**: Make explicit whether b_C(d) and b_L(d) are inside or outside T10a's allocator tree, and how T10a.6 (DomainDisjointness) applies to them. If they are outside T10a's tree, the axiom should state this explicitly and justify why downstream uses of T10a's machinery (e.g., GlobalUniqueness for subsequent inc(·, 0) steps within each sub-allocator's frontier) remain valid.

### Issue 3: K.μ~ has dual definitional structure (contract + decomposition) without clear primacy

**ASN-0047, K.μ~ definition and "Decomposition of K.μ~" subsection**: K.μ~ is given an inline contract (precondition, effect, frame), then described as "a distinguished composite, not a primitive transition" whose K.μ⁻ + K.μ⁺ decomposition serves as "a *consistency check*."

**Problem**: This dual treatment is structurally ambiguous. If K.μ~ is composite, its contract should be *derived* from the decomposition, and the inline statement is a theorem, not a definition. If K.μ~ is primitive, the decomposition is an admissibility witness, not the operator's semantics. The choice matters because: (a) the K.μ~-FIX domain-fixity argument relies on K.μ~'s inline contract; (b) the link-subspace identity precondition is stated definitionally AND derived as "overdetermined" via CL-UNIQ — this dual presentation is symptomatic of the underlying ambiguity. The "Frame consistency check" paragraph reads as if either characterization could be primary.

**Required**: Commit to one characterization. If composite, derive the contract from the decomposition and prove K.μ~-FIX from the elementary frames. If primitive, treat the decomposition as a sufficiency lemma showing K.μ~ does not extend the elementary set.

### Issue 4: K.μ~ link-subspace identity precondition is "overdetermined" but still stated

**ASN-0047, K.μ~ precondition**: Includes both subspace-preservation `subspace(π(v)) = subspace(v)` and link-subspace identity `π(v) = v` for `subspace(v) = s_L`.

**Problem**: The ASN argues at length that the identity clause is derivable from subspace-preservation + S3★ + CL-UNIQ + K.μ⁺ amendment. If so, the precondition should not include it — preconditions should be minimal. Including a derivable clause as a precondition obscures which conditions are constraints versus consequences, and complicates the inductive proof of CL-UNIQ for K.μ~ (where the cleaner argument uses only subspace-preservation + bijectivity of π + CL-UNIQ at pre-state, not the identity clause).

**Required**: Either drop the identity clause from the precondition (citing the derivation), or drop the derivation argument and accept the identity clause as part of the contract. The current "stated and then proved redundant" structure is unusual.

### Issue 5: K.δ k=1 ghost-base prohibition lacks invariant-level justification

**ASN-0047, K.δ definition and "Scope and base-liveness" paragraph**: The strengthened precondition `k = 1 ⟹ t ∈ E_doc` forbids creating a version of a non-existent document. The ASN then verifies, layer by layer, that the *weaker* form (without entity-membership) would have been "harmless across the entity-hierarchy, arrangement, link, provenance, and coupling layers" and concludes the strengthening is "a precondition tightening for clarity and entity-allocation discipline, not a fix for any invariant-level defect."

**Problem**: If the strengthening fixes no invariant defect, the justification "lifting the implementation's contract to the specification" is asymmetric — the abstract specification is meant to constrain implementations, not inherit implementation choices that have no abstract grounding. The verification paragraph supports admitting the *weaker* precondition (consistent with Nelson's ghost-element doctrine), not strengthening to require `t ∈ E_doc`. The current text adopts the stronger form without invariant-level necessity.

**Required**: Either (a) identify an invariant that requires the strengthening (and adjust the verification paragraph), or (b) relax to the weaker precondition (admitting ghost-base versioning) and explain how the implementation's contract is enforced at a different layer, or (c) explicitly mark this as a substantive scope choice that future ASNs may revisit.

### Issue 6: K.μ⁻ admissibility precondition duplicates D-CTG★/D-MIN★ postcondition information

**ASN-0047, K.μ⁻ amendment, "Admissible removal" paragraph**: K.μ⁻'s precondition restricts contractions to per-subspace suffix removal or full clearance. The detailed case analysis (a)/(b)/(c) shows that this admissibility is *equivalent* to "the post-state satisfies D-CTG★ and D-MIN★" given D-SEQ★-shaped pre-state.

**Problem**: Stating the constraint twice — once as a precondition (suffix discipline) and once as a postcondition (D-CTG★/D-MIN★) — is redundant and risks divergence if either is amended in the future. The ASN argues for the dual statement ("mirrors K.μ⁺_L's explicit positional precondition and makes the operator's input space explicit") but K.μ⁺_L's precondition is genuinely informational (it specifies which V-position is added, not constrained by postconditions alone), while K.μ⁻'s admissibility precondition adds no information beyond D-CTG★/D-MIN★ given the structural shape of the input.

**Required**: Drop the admissibility precondition, relying on D-CTG★/D-MIN★ postconditions to implicitly constrain valid K.μ⁻ contractions. The detailed case analysis can remain as a worked verification that the postconditions force the suffix discipline, rather than as a precondition derivation.

### Issue 7: K.μ⁻ amendment forbids interior link withdrawal — structural defect deferred to open question

**ASN-0047, D-CTG★/D-MIN★ amendment, "Consequence for link withdrawal" paragraph**: "Under D-CTG★, a user cannot withdraw a single link at a non-maximum link-subspace position while leaving subsequent links in place... withdrawing one interior link requires withdrawing every link allocated after it as well." The ASN identifies that "the consultation responses confirm tombstoning as essentially the only model Nelson contemplates for link withdrawal" and defers the mechanism to an open question.

**Problem**: This is a substantive gap in the elementary transition set, not a minor open question. The ASN's claim of "structural sufficiency" is undermined by the documented inability to express Nelson's tombstoning mechanism — a core link-management operation. The "structural sufficiency" paragraph qualifies its claim ("we do not claim completeness in the stronger sense"), but the link-withdrawal gap is specific and known, not hypothetical.

**Required**: Make explicit in the "Structural sufficiency" subsection that link withdrawal in Nelson's tombstoning sense is *not* expressible in the present transition set, separating this known gap from the general open-completeness caveat. The Open Questions list mentions this, but the structural sufficiency claim should acknowledge it at the point of claim.

### Issue 8: Forward references to CL-UNIQ and S3★-aux from K.μ~ section

**ASN-0047, "Decomposition of K.μ~" and "Link-subspace fixity under K.μ~"**: Both subsections appeal to CL-UNIQ and S3★-aux, defined in later sections. The ASN includes a "*Forward references in this section*" disclaimer claiming the dependencies are non-circular.

**Problem**: While the inductive proofs may be non-circular, the presentation order forces readers to accept forward references without local verification. The disclaimer notes that reordering "could be avoided by reordering the sections (placing Link-subspace ownership before Decomposition of K.μ~)" — and indeed it should be.

**Required**: Reorder the presentation: define S3★-aux and CL-UNIQ before invoking them in the K.μ~ decomposition argument. The current ordering trades minor exposition flow for forward-reference confusion.

### Issue 9: The verification of K.δ k=1 base-liveness is presented as exhaustive but conclusory

**ASN-0047, K.δ "Scope and base-liveness (per-invariant verification)"**: The verification works through every invariant (P0-P8, S0-S9, L0-L14, J0-J4, plus starred forms) to show the weaker form would be harmless.

**Problem**: The exhaustive layer-by-layer verification reads as defensive over-explanation rather than focused proof. Each layer's argument is a one-paragraph dismissal ("trivially," "by frame," "vacuously"). The structure suggests the author anticipated objections rather than working through genuine invariant interactions. Either the verification reveals a substantive interaction (and should be more detailed), or it is a routine application of frame discipline (and could be a single paragraph).

**Required**: Compress the verification to its essential structure: K.δ frames all state components except E and (for documents) M(e); preserves entity-hierarchy spine via parent(·); subsequent K.α + K.μ⁺ + K.ρ under the new document anchor through `e` itself, not the (possibly absent) base. The case-by-case enumeration adds bulk without proportional clarification.

### Issue 10: Properties Introduced table contains duplicate or near-duplicate entries

**ASN-0047, Properties Introduced section**: The table lists both unamended forms (P3, P4, P5) and starred forms (P3★, P4★, P5★) as separate "introduced" entries. Many entries are local extensions of foundation invariants (e.g., L0, L1, L3, L1b, L-fin) without clear indication that they are restatements of foundation properties.

**Problem**: The table conflates three categories: (a) genuinely new properties introduced in this ASN, (b) local extensions of foundation properties applied to the extended state, (c) restatements of foundation properties for self-contained reference. Listing all as "introduced" is misleading — the foundation invariants are not being introduced here.

**Required**: Partition the table into three sections (or mark with status flags): genuinely new, local extension/strengthening, and foundation restatement. The L0 entry is a particularly clear case where the C-clause is new but the L-clause is from ASN-0043.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal mechanism (tombstoning)

**Why out of scope**: The ASN explicitly defers this to an open question. The tombstoning mechanism Nelson describes requires either a status flag on dom(L) or a retraction-link convention, both of which are extensions to the state model not present here. A separate ASN on link lifecycle would be the appropriate vehicle.

### Topic 2: Version semantics beyond bare entity creation

**ASN-0047, K.δ k=1 case "Deferred semantics" paragraph**: The richer version contract — arrangement-transition invariants between successive versions, content allocator linkage, provenance flows, version lineage acyclicity — is deferred.

**Why out of scope**: This belongs in a subsequent version-management ASN. The present ASN treats versions structurally as `[N, 0, U, 0, D, k]` with the appropriate K.δ precondition; the semantic apparatus is genuinely separate work.

### Topic 3: Concurrency and serialization of allocations

The open question on concurrent operations targeting the same home document.

**Why out of scope**: The ASN's transition model is sequential (single-state-to-state transitions). Concurrent execution semantics require a separate concurrency model — possibly interleaving or partial-order semantics over the present transitions. Not a defect in this ASN.

### Topic 4: P7a-analog invariants for links (orphan link bounds)

**ASN-0047, "Orphan links and coupling flexibility" section**: The wp analysis shows no link-coverage invariant analog of P7a exists, admitting orphan links.

**Why out of scope**: The decision to not have such an invariant is intentional (matching Nelson's "deleted links" status). Adding one would be a substantive design change, not a defect in the present specification.

### Topic 5: K.δ k=1 admissibility for accounts

The open question on whether account-level depth-1 tumbler extension should be admitted.

**Why out of scope**: This is correctly flagged as an open question. The present scope choice (documents only) matches consultation evidence; a future extension can relax without structural reorganization.

VERDICT: REVISE
