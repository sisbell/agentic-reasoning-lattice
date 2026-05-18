# Review of ASN-0047

## REVISE

### Issue 1: Forward-reference accretion — "defer to this canonical site" markers
**ASN-0047, multiple locations**: "All subsequent cross-references in this ASN to 'link withdrawal under D-CTG★/D-MIN★' or to 'Nelson's tombstoning design' defer back to this site." Also: "All other sites in this ASN that reference the deferred contract defer to this canonical site."
**Problem**: These are meta-prose statements about cross-reference bookkeeping rather than substantive content. Stating that future references will defer here is bloat — the references themselves should be terse, and the existence of a canonical site needs no announcement.
**Required**: Remove the explicit "defers back to this site" / "defer to this canonical site" sentences. Let downstream references be brief inline pointers; no preamble needed.

### Issue 2: Defensive justification of SubspaceConventionAxiom
**ASN-0047, *Link store and extended system state***: "Under these values the chain `d → inc(d, 2) = b_C(d) → ...` is a single-inc-per-step T10a-conforming sequence — the explicit witness for L1c's existential... The immediate consequence `s_C ≠ s_L`... is the structural precondition for every disjointness argument in this ASN: without it, L0 would not partition addresses (the L-clause and C-clause would coincide), L14 would be vacuous, and the link-subspace fixity argument under K.μ~ would collapse. SubspaceConventionAxiom stands alongside NoDeallocation (ASN-0034) and S0 (ASN-0036) as an axiom."
**Problem**: This is essay-style motivation explaining *why* the axiom is needed and *what would break without it* rather than stating what the axiom says. The "stands alongside NoDeallocation... as an axiom" sentence is a status announcement, not content.
**Required**: State the axiom (`s_C = 1 ∧ s_L = 2`) and the citation to Nelson/Gregory. Drop the "without it, L0 would not..." enumeration and the standing-alongside-other-axioms claim.

### Issue 3: Defensive justification of SubAllocatorAxiom
**ASN-0047, *Allocator hierarchy under documents***: "T10a's at-most-once spawning constraint prevents deriving the operational existence of two simultaneously-active sub-allocator frontiers from a single spawning event at `d`, so we admit it as an axiom."
**Problem**: This explains *why* SubAllocatorAxiom is axiomatic rather than what it says. The reasoning ("T10a prevents derivation, so we admit") is the anti-bloat pattern explicitly flagged.
**Required**: Either drop the sentence entirely or compress to a parenthetical: "(not derivable from T10a alone)."

### Issue 4: L3 local-extension consistency paragraph
**ASN-0047, L3 definition**: "*Consistency with the foundation.* ASN-0043's L3 carries `Σ.L(a).e₃ ≠ ∅` as a verified-stable invariant of the foundation. A downstream ASN cannot relax it without first revising ASN-0043 — this ASN preserves the constraint. Were a future revision to admit empty Θ (the 'untyped link' extension), the appropriate vehicle is an ASN-0043 amendment, with the downstream consequences for L8..."
**Problem**: This is a multi-paragraph explanation of what would happen if a future ASN did something different. It is hypothetical content about future ASNs, not content about the current one.
**Required**: Remove the "Consistency with the foundation" sub-paragraph. The local-extension status in the L3 header already conveys the relationship; the hypothetical-future analysis adds no constraint on the present specification.

### Issue 5: Redundant notation for the same projection
**ASN-0047, *Notation***: `fields(a) := E(a)` declared as "a local abbreviation used throughout this ASN for readability." Also `subspace_I(a) := fields(a).E₁` declared as "the bridge to foundation notation." Then: "Both notations are used interchangeably in this ASN."
**Problem**: Three names for the same projection (`E(a)` / `fields(a)`, `E(a).E₁` / `fields(a).E₁` / `subspace_I(a)`) used interchangeably increases cognitive load without adding precision. The justification ("readability when the I-address is the natural subject") is itself meta-prose.
**Required**: Pick one. Drop `fields(a)` (foundation already has `E(a)`) or drop `subspace_I(a)` (foundation form is `E(a)₁`). State that the chosen name is used uniformly. Remove the "interchangeable" prose.

### Issue 6: Imprecise analogy in K.μ~ classification
**ASN-0047, *Elementary transitions***: "K.μ~ — *arrangement reordering* — is a named composite of K.μ⁻ + K.μ⁺ (analogous to J0/J1★/J2/J3/J4), not a primitive transition."
**Problem**: J0 and J1★ are coupling constraints (predicates over transitions); J2 and J3 are isolation properties (predicates over individual transitions); only J4 is a composite definition. The analogy "to J0/J1★/J2/J3/J4" lumps four distinct categories under one label.
**Required**: Either drop the analogy entirely or restrict to "analogous to J4." The reader does not need the framing to grasp "named composite, not primitive."

### Issue 7: Use-site inventory in V-ordering definition
**ASN-0047, *Amendments to existing transitions***: "**V-ordering on subspace S (definition).** *Anchoring the 'V-ordering' language used by D-CTG★, D-MIN★, and D-SEQ★ below; by the K.μ⁻ admissibility case analysis above (which speaks of 'lex order on terminal-varying tuples' — a special case under this definition); by the K.μ~-FIX domain-fixity argument; and by the link-subspace fixity proof.*"
**Problem**: This is a four-item use-site inventory in the definition's preamble. Every subsequent consumer will discharge through this definition by construction; the inventory is meta-bookkeeping.
**Required**: Drop the "Anchoring..." sentence. State the V-ordering definition and let consumers cite it naturally.

### Issue 8: Defensive justification of P3★ in Properties Introduced
**ASN-0047, P3★ row**: "Synthesises ASN-0036's P0/P1/P2 + ASN-0043's L12 with the qualitative mode-enumeration 'no contraction or reordering on C, L, E, R'"
**Problem**: Reasonable as a table entry. But the body text introducing P3★ states: "P3★ is a quantitative conjunction (a predicate over `Σ → Σ'` with explicit domain-inclusion and value-preservation conjuncts) covering C, L, E, R uniformly. It synthesises P0 ∧ L12 ∧ P1 ∧ P2 with the qualitative mode-enumeration 'no contraction, no reordering' of C, L, E, R into one named predicate. The mode-enumeration form (extension / contraction / reordering) appears in the Permanence section above as a one-sentence orienting observation; P3★ is the monotonicity premise invoked anywhere in this ASN's proofs."
The "mode-enumeration form... appears in the Permanence section above as a one-sentence orienting observation; P3★ is the monotonicity premise invoked anywhere..." is bookkeeping about where forms appear and which is invoked.
**Required**: State P3★'s predicate. Drop the explanation of where its prose ancestor appears and what role it plays in proofs.

### Issue 9: Defensive prose around the entity-allocator-tracked predicate
**ASN-0047, *Notation***: After defining `InEntityAllocatorDomain`: "This is the scope at which K.δ's `e ∉ E` precondition is discharged via T10a's GlobalUniqueness, which gives 'inc(t, k) is distinct from every previously allocated address *within that allocator's domain*'; 'within that allocator's domain' requires the operand to inhabit some entity allocator's tracked frontier in `Act(s)`, which a ghost operand by stipulation does not."
**Problem**: This is essay-style justification of why the predicate is needed and how it differs from naive readings of T10a. The predicate's definition stands on its own.
**Required**: Remove the "This is the scope at which..." paragraph. Move the Path 1 / Path 2 / Path 3 split content to where K.δ's freshness discharge is actually stated, and let the predicate definition be minimal.

### Issue 10: Ghost-base versioning canonical-site framing
**ASN-0047, K.δ definition**: "*Ghost-base versioning (k = 1) — canonical site of the version-management deferral.* K.δ's k = 1 sub-case admits an inc operand `t` that need not be in E_doc... The richer version contract — arrangement invariants between successive versions, content-allocator linkage, provenance flow, lineage acyclicity, S7d-foundation reconciliation (when a downstream operation may 'upgrade' a ghost-base emission to T10a-tracked status), and the semantic admissibility of version-of-version chains — is deferred to a subsequent version-management ASN. All other sites in this ASN that reference the deferred contract defer to this canonical site."
**Problem**: The "canonical site of the version-management deferral" labeling plus the closing "All other sites... defer to this canonical site" is the cross-reference bookkeeping pattern. The list of what is deferred is itself an inventory.
**Required**: State the K.δ k=1 precondition relaxation and that the broader version contract is deferred. Drop the "canonical site" label and the closing cross-reference notice. Keep the list of deferred topics terse or move to Open Questions.

### Issue 11: Repetition of "see the canonical X site"
**ASN-0047, multiple locations**: Phrases like "see the canonical *Link-withdrawal gap under D-CTG★ / D-MIN★* site above" and "see the canonical K.δ ghost-base site above" appear multiple times across the ASN.
**Problem**: The pattern of named canonical sites with explicit "see... site" pointers is the cross-reference accretion the anti-bloat note flags. Multiple paragraphs in different sections deferring to the same downstream location.
**Required**: Reduce to inline references without the "canonical site" framing. E.g., "(see *Link-withdrawal gap* above)" or just "(L3-section above)."

### Issue 12: Document-ordering justification in proof structure
**ASN-0047, proof of ExtendedReachableStateInvariants**: The proof is partitioned into "Class (a): Elementary per-state invariants" and "Class (b): Composite invariants" with extensive prose explaining the rationale for the partition.
**Problem**: The partition itself is fine, but the prose includes statements like "P4★ (...): An elementary K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated at the intermediate state." These narrative justifications explain why the partition exists rather than discharging the proof.
**Required**: Tighten the partition prose: state which invariant goes into which class and why (one line each). The detailed "violated at intermediate, restored at boundary" elaboration is what J1★/J1'★ are *for* and need not be re-narrated.

### Issue 13: Multi-paragraph axiom prose without separation between content and rationale
**ASN-0047, SubAllocatorAxiom**: The axiom has three labeled clauses (Exists, Disjoint, Namespace) — good structure. But it's followed by: "**Dispatch of freshness obligations across K.α and K.λ.** SubAllocatorAxiom.Exists underwrites the 'produced by d's sub-allocator' clause whenever `d ∈ E_doc`. The freshness premise on each per-allocation event is *SubAllocatorAxiom.Namespace* for the first emission of either sub-allocator under d, and *T10a's GlobalUniqueness* on the `inc(·, 0)` chain for every subsequent emission..."
**Problem**: The "Dispatch of freshness obligations" sub-paragraph is a use-site inventory explaining which clauses are invoked where downstream. This belongs at K.α and K.λ's freshness-discharge sites, not at SubAllocatorAxiom.
**Required**: Move the dispatch content to where it is consumed (K.α and K.λ preconditions). Keep the axiom statement self-contained.

### Issue 14: Missing intermediate-state P4★ check in interior-replacement example
**ASN-0047, *Worked example: interior content replacement***: The example traces K.μ⁻ → K.α → K.μ⁺ → K.ρ with explicit intermediate-state verification at M_int (after K.μ⁻) including P4★, but does *not* explicitly verify P4★ at the post-K.μ⁺ pre-K.ρ intermediate state, where P4★ is genuinely violated (a₂' is in `Contains_C` but not yet in R).
**Problem**: The example introduces "composite invariant" / "violated at intermediate" terminology in its discussion of P4★ but doesn't show the violation in a worked-example trace. Since this is exactly the intermediate state where the composite-boundary discharge is non-trivial, the example would gain rigor by tracing it explicitly.
**Required**: Add one verification line showing P4★ violated at the post-K.μ⁺ intermediate state and restored at the K.ρ boundary. This makes the "composite invariant" notion concrete.

### Issue 15: Bootstrap node single-tree decision under-examined
**ASN-0047, *The state model***: "The choice of `1` as the singular root value is a definitional convention of this ASN..." with NodeLineage forcing "n₀ ≼ e for every node e ∈ E" and explicitly "This rules out disconnected-forest node addresses (`[2]`, `[2, 1]`, etc.); the present specification admits no such allocation."
**Problem**: Nelson's design admits multiple servers, each with its own root address. The decision to admit only a single bootstrap tree is substantive but presented as a "definitional convention." The cross-server/multi-server federation case is not addressed in the Open Questions list either.
**Required**: Either justify the single-tree choice with citation to a Nelson-design commitment (LM evidence that the docuverse is structurally a single tree, not a forest), or add to Open Questions: "What invariants must hold if the entity hierarchy admits multiple roots (federation across servers)?"

## OUT_OF_SCOPE

### Topic 1: Withdrawal/tombstoning mechanism specification
**Why out of scope**: The ASN explicitly identifies and defers this (the *Link-withdrawal gap under D-CTG★ / D-MIN★* canonical site). The reconciliation mechanism — status flag, tombstone marker, or retraction link — belongs to a separate ASN. Listed in Open Questions correctly.

### Topic 2: Version management contract
**Why out of scope**: The ghost-base versioning relaxation is admitted at K.δ k=1, with the richer contract (arrangement invariants between versions, lineage acyclicity, version-of-version semantics) deferred to a version-management ASN. Correctly bounded.

### Topic 3: Account-level k=1 versioning
**Why out of scope**: Listed in Open Questions; the structural admissibility is acknowledged but no implementation evidence supports admitting it.

### Topic 4: Concurrency and Path 2 freshness soundness
**Why out of scope**: Single-event sequential semantics is this ASN's frame; concurrency requirements (per-allocator serialization, transactional commit) belong to a separate concurrency-discipline ASN.

### Topic 5: Multi-server federation
**Why out of scope**: The single bootstrap node `n₀ = [1]` constrains to a single rooted tree. Federation would require admitting multiple roots and is not implementation territory for this ASN — though see Issue 15 above on whether the constraint should be more visibly justified or open-questioned.

### Topic 6: Operation-level specifications (INSERT, DELETE, COPY, MAKELINK, etc.)
**Why out of scope**: This ASN's elementary transitions are the building blocks; named protocol operations are downstream composites and explicitly listed in Scope as out of scope.

VERDICT: REVISE
