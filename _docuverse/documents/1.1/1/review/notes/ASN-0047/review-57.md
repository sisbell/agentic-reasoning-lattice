# Review of ASN-0047

The ASN is substantively sound: state model is well-defined, transitions have complete preconditions/effects/frames, invariants are precisely stated, the inductive proof structure works, and worked examples ground the abstract claims. My objections are presentation-level, but in Dijkstra's spirit they merit revision before this becomes load-bearing for downstream work.

## REVISE

### Issue 1: Forward reference to D-SEQ★ in K.μ⁻ amendment

**ASN-0047, K.μ⁻ precondition**: "under the D-SEQ★-shaped pre-state `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` (guaranteed by induction over the elementary set; established at D-SEQ★'s definition site below)"

**Problem**: K.μ⁻ is defined in the *Elementary transitions* section but its precondition cites D-SEQ★, which is defined later in *Amendments to existing transitions*. The induction resolves the logical dependency, but a first-pass reader hits an undefined symbol.

**Required**: Either (a) move the D-CTG★/D-MIN★/D-SEQ★ definitions earlier (before K.μ⁻'s precondition), or (b) state D-SEQ★ inline at the K.μ⁻ site with a forward note that it will be elevated to a system-wide invariant in a later section.

### Issue 2: Conflicting characterization of J0 as axiom vs. derived theorem

**ASN-0047, J0 (Allocation requires placement)**: "This is an axiom of the state transition model, not a theorem of ASN-0036."

**ASN-0047, Temporal decomposition**: "J0 is necessitated by P7a through a longer chain: P7a requires every I-address to have provenance; provenance is created by J1★ when content enters an arrangement; therefore freshly allocated content must enter some arrangement (J0) or P7a would fail for that address."

**Problem**: These two claims are not reconciled. If J0 is necessitated by P7a + J1★, then it's a derived theorem given those premises. If it's an independent axiom, then P7a is the derived theorem (from J0 + J1★ + P0 + P2). The ASN should pick one logical orientation.

**Required**: State the orientation clearly. Either: (a) J0 is the axiom and P7a follows from {J0, J1★, P0, P2} (which matches the actual proof structure of P7a in the Reachable-state invariants section), or (b) P7a is asserted as a design constraint and J0 is its operational consequence. The current treatment leaves the logical direction ambiguous.

### Issue 3: Layer-decomposition table conflates value immutability with set monotonicity

**ASN-0047, Temporal decomposition table**: "| Existential | C, L, E | Append-only, values immutable | K.α, K.δ, K.λ |"

**Problem**: E is a set of allocated entity *addresses* — it has no values to be immutable. The "values immutable" property applies to C (content values) and L (link values), not to E (membership only). The table groups three components under a single mutability characterization that doesn't actually apply uniformly.

**Required**: Either split E into its own row ("E — Set monotone, no value structure"), or describe the existential layer more precisely: "C and L: append-only with immutable values; E: append-only membership." The current characterization is technically incorrect for E.

### Issue 4: Structural sufficiency caveat stated four times

**ASN-0047**: The bounded-sufficiency caveat ("we do not claim completeness in the stronger sense...") appears at the end of the *Elementary transitions* section, again at the end of the *Scoped coupling constraints* section under "Extended structural sufficiency", a third time in the dedicated *Structural sufficiency and known gaps* section, and a fourth time implicitly in the "Known gap" prose throughout.

**Problem**: The repetition obscures rather than clarifies. A reader scanning for what the elementary set covers must read four similar disclaimers to extract the bounded scope.

**Required**: Consolidate into the dedicated *Structural sufficiency and known gaps* section, with terse forward/backward pointers from the earlier sites. The first occurrence can flag "see consolidated treatment below"; later occurrences can be elided.

### Issue 5: K.μ~ Case 1 subcase split adds verbosity without analytic content

**ASN-0047, Decomposition of K.μ~, Case 1**: "Case 1a: dom(M(d)) = ∅ (the empty-bijection subcase)... Case 1b: dom(M(d)) ≠ ∅ with π = id..."

**Problem**: Both subcases conclude with "K.μ~ expands into zero elementary steps, producing M'(d) = M(d)" and the same vacuous invariant preservation. The split adds prose without analytic distinction — the empty bijection on ∅ and the identity bijection on a non-empty domain are both instances of "π = id, zero steps, M unchanged."

**Required**: Treat Case 1 as a single case: "π = id (degenerate, expanding into zero elementary steps; the case `dom(M(d)) = ∅` is the empty bijection on ∅, the case `dom(M(d)) ≠ ∅` is the identity bijection on a non-empty domain; both yield M'(d) = M(d) and preserve all invariants vacuously)."

### Issue 6: K.μ~ "derived contract" relationship to its decomposition is circular in presentation

**ASN-0047, Decomposition of K.μ~**: "*Derived contract (theorem from the decomposition).* For some d ∈ E_doc, there exists a bijection π..."

**ASN-0047, Elementary transitions, K.μ~ subsection**: "The formal contract (the bijection equation and admissibility constraints), the link-subspace fixity argument, and the frame are all derived from the K.μ⁻ + K.μ⁺ decomposition..."

**ASN-0047, ValidComposite★ clause (1)**: "K.μ~ appearing in the sequence is shorthand for its decomposition (per its definition above)..."

**Problem**: K.μ~ is "shorthand for its decomposition," and its contract is "derived from the decomposition." But the decomposition is admissible *because* it satisfies K.μ~'s contract (the bijection equation). The relationship reads: K.μ~ ≡ {K.μ⁻ + K.μ⁺ satisfying K.μ~'s contract}, which is circular unless K.μ~'s contract is stated independently first.

**Required**: State K.μ~'s contract independently at the definition site (the bijection equation, admissibility constraints, and frame, with the link-subspace identity property identified as derived). Then say "every admissible K.μ⁻ + K.μ⁺ decomposition realising this contract is called a K.μ~ instance," and prove existence (Case 3 full-clearance witness). The contract is the primary; the decomposition realizes it.

### Issue 7: The ExtendedReachableStateInvariants inductive step for K.μ⁺_L misses an explicit CL-UNIQ case

**ASN-0047, Inductive proof of ExtendedReachableStateInvariants, K.μ⁺_L case**: Lists "S8a, S8-fin, S8-depth, D-CTG, D-MIN, D-SEQ, S8 all hold; S3★ satisfied by precondition (`ℓ ∈ dom(L)`); CL-OWN preserved (new mapping satisfies `origin(ℓ) = d` by precondition; existing link-subspace mappings unchanged by frame); L3 preserved (L unchanged); L-fin preserved (L unchanged)."

**Problem**: CL-UNIQ is in the per-state invariant conjunction but is not explicitly verified in the K.μ⁺_L case here. The CL-UNIQ proof for K.μ⁺_L is given in the *Link-subspace ownership* section, but the inductive-step prose elsewhere should at least name it as preserved (it's the load-bearing reason K.μ⁺_L's first-arrangement precondition `ℓ ∉ ran(M(d))` exists).

**Required**: Add CL-UNIQ to the K.μ⁺_L preservation list with a one-line citation to the CL-UNIQ proof: "CL-UNIQ preserved by the first-arrangement precondition `ℓ ∉ ran(M(d))` — see the CL-UNIQ inductive proof above."

### Issue 8: Two paragraphs of P3 vs P3★ commentary belie a definitional ambiguity

**ASN-0047, Permanence section**: "**P3 (Arrangement as sole locus of destructive change).** Arrangements admit three modes of change: (a) extension... (b) contraction... (c) reordering. No other component — specifically C, E, and R — admits contraction or reordering."

**ASN-0047, Extended monotonicity invariants section**: "**P3★ (ArrangementMutabilityOnly, extended).** ...P3★ supersedes the earlier P3 by including L in the enumeration *and by adding the value-preservation clauses for C and L*. The two added conjuncts state that existing entries in C and L are immutable, not merely that their domains grow..."

**Problem**: P3 as originally stated is a *qualitative* observation about mutability modes (it doesn't formalize value preservation). P3★ is a *quantitative* monotonicity conjunction (it does). The label P3★ as "extension of P3 to include L" hides that P3★ also strengthens the value-preservation content — which P3 didn't have at all. P3★ is essentially a synthesis label for P0 ∧ L12 ∧ P1 ∧ P2, with the original P3 being a separate qualitative claim.

**Required**: Either keep P3 as the qualitative claim and rename P3★ to something like "MonotonicityConjunction" or "Mon★" (making clear it's a different kind of statement), or fold P3 into P3★ and acknowledge that the "extension" includes a formal strengthening, not just adding L to the enumeration.

### Issue 9: Worked example "fork with subsequent insertion" verifies J1', not J1'★

**ASN-0047, Worked example: fork with subsequent insertion, fork verification**: "*J1':* `R₂ \ R₁ = {(a₁, d₂), (a₂, d₂)}` — both are new provenance entries from the K.ρ step. For each, the address must be new to d₂'s content-subspace range..."

**Problem**: The bullet is labeled J1'★ (the content-scoped form) but the text says "J1'". Since this worked example is in the four-component state (no link subspace, J1' and J1'★ coincide), the verification is correct, but the label is inconsistent. The other worked examples (ghost-base, link allocation) consistently label J1'★. Pick one convention.

**Required**: Either label the bullet J1'★ uniformly throughout (and note in the prose that J1'★ reduces to J1' in the four-component subspace), or use J1' in the fork example explicitly and note that the extension to J1'★ is verified in later examples. The current mix is jarring.

### Issue 10: The cross-document T10a chain is correct but stated three times verbatim

**ASN-0047**: The "T10a.{2,5} → T10 chain" is stated in full in:
- *Allocator hierarchy under documents* (paragraphs on the chain)
- *Link allocation* (K.λ section's cross-document disjointness derivation)
- *SubAllocatorAxiom* discussion

Each occurrence repeats the chain: T10a.2 for sibling case, T10a.5 for non-sibling case, T10a.6 as packaging, suffix-extension preservation, T10 application.

**Problem**: The chain is sound but its three full restatements add length without adding content. A single canonical statement with backward citations would suffice.

**Required**: State the chain once (in *Allocator hierarchy under documents*, as a labeled "Cross-document disjointness chain" lemma), and cite it by name at the K.λ and SubAllocatorAxiom sites.

## OUT_OF_SCOPE

### Topic 1: Tombstoning mechanism and per-link liveness predicates

The ASN explicitly identifies this as a named structural gap (interior link-subspace withdrawal is not expressible) and defers it to the open question on withdrawal invariants. The deferred mechanism would require a state-model extension (per-link status flag or tombstone marker on M(d)).

**Why out of scope**: New state-model territory, deferred to a withdrawal-mechanism ASN. Not an error in this ASN.

### Topic 2: Concurrent allocation under multiple simultaneous K.λ events

The ASN states K.λ's preconditions sequentially and doesn't address what happens if two K.λ events target the same home document simultaneously. The open question "Must the system guarantee that a fresh link address is always available within a document's link subspace, or can link allocation fail due to address space exhaustion?" hints at this.

**Why out of scope**: Concurrency model belongs to a future operational ASN. The abstract transition model treats each elementary transition atomically.

### Topic 3: Cross-version arrangement contracts

The K.δ ghost-base versioning analysis correctly defers "the richer version contract" to a future version-management ASN. Specifically: what relationship must hold between successive versions' arrangements, whether content allocators of base and version are linked, how provenance flows.

**Why out of scope**: Version semantics deferred to a dedicated version-management ASN; the elementary K.δ here is structurally complete for what it covers.

VERDICT: REVISE
