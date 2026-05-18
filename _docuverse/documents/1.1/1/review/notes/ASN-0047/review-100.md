# Review of ASN-0047

## REVISE

### Issue 1: K.α and K.μ⁺ split-definition pattern obscures the actual contracts

**ASN-0047, "Elementary transitions" vs. "Amendments to existing transitions"**: K.α is defined first with the precondition "IsElement(a) ∧ origin(a) ∈ E_doc ∧ a ∉ dom(C) ∧ ..." but no subspace restriction. Then much later: "K.α amendment (ContentSubspaceRestriction). In the extended state, K.α is amended with a content-subspace restriction: the allocated address must satisfy `subspace_I(a) = s_C`." K.μ⁺ is split the same way.

**Problem**: A reader following the section order encounters the "complete" K.α and K.μ⁺ definitions, builds a mental model around them, and only later learns those definitions were provisional. The K.μ⁻ definition uses D-CTG★/D-MIN★ (extended-state forms) without flagging this; its "amendment" is implicit via invariant supersession while K.α and K.μ⁺ get explicit amendment paragraphs. The asymmetric treatment makes it harder to identify which transitions have how many definitional layers.

**Required**: Either (a) define each transition once with its final precondition set, with a forward-pointer to "Link store extension introduces L and s_L" where the link-related conjuncts originate; or (b) consistently mark *every* amended transition (including K.μ⁻) with an explicit amendment paragraph so the reader knows the section structure is "initial → amendment". The current asymmetry is the worst case.

### Issue 2: L3 narrative claims an implicit Θ ≠ ∅ that conflicts with the foundation Link definition

**ASN-0047, "Link store and extended system state"**: "L3 (TripleEndsetStructure). [...] K.λ's precondition `(F, G, Θ) ∈ Link` carries the implicit `Θ ≠ ∅` requirement."

But K.λ's actual precondition reads: "(F, G, Θ) ∈ Link ∧ Θ ≠ ∅  (well-formed link value with mandatory non-empty type endset — L3)" — Θ ≠ ∅ is explicit. And foundation ASN-0043's Link definition is `Link = {(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}` — no Θ ≠ ∅ clause.

**Problem**: The text says "implicit", but the precondition states it explicitly, and the foundation definition does not include it. So either L3 redefines Link locally (in which case the conjunct is implicit but the redefinition should be flagged), or it doesn't (in which case the conjunct is explicit but the narrative is wrong). A careful reader cannot tell which.

**Required**: Pick one. Either (a) state explicitly that L3 narrows Link to `{(F, G, Θ) : F, G, Θ ∈ Endset ∧ Θ ≠ ∅}` and remove the redundant ∧ Θ ≠ ∅ from K.λ; or (b) keep K.λ's explicit ∧ Θ ≠ ∅ and remove the "implicit" claim from the L3 narrative.

### Issue 3: Atomic-vs-composite framework and notation collision underspecified

**ASN-0047, "The state model"** introduces SequentialTransitionAxiom: "each transition is an atomic, uninterruptible event ... transitions are totally ordered". Later, "Definition (Valid composite transition). A composite transition Σ → Σ' is valid iff it is a finite sequence of elementary transitions ...". Then P3 quantifies `(A Σ → Σ' :: ...)` and J0 quantifies `(A Σ → Σ', a : a ∈ dom(C') \ dom(C) : ...)`.

**Problem**: The notation `Σ → Σ'` is overloaded — sometimes atomic-elementary (SequentialTransitionAxiom), sometimes composite (ValidComposite★, J0). When interpreted atomically, J0 fails for K.α alone (which grows dom(C) without populating any arrangement) — but K.α *is* a permitted elementary atomic transition. When interpreted compositely, J0 holds at composite boundaries but says nothing about K.α-only intermediate states. The ASN never explicitly tells the reader: "elementary transitions can produce intermediate states violating J0/J1/J1'; only post-composite states are required to satisfy them, and the operations layer is responsible for ensuring composite completion." This is the load-bearing semantic invariant of the whole transition model.

**Required**: Add one paragraph after ValidComposite★ that disambiguates: (a) `Σ → Σ'` in elementary contexts (frame, effect) is atomic; (b) `Σ → Σ'` in coupling/invariant statements (J0/J1/J1'/ExtendedReachableStateInvariants) is composite-boundary; (c) intermediate states within a composite may transiently violate composite invariants; (d) the operations layer (out of scope) is responsible for ensuring composites complete. Distinguish the two uses notationally if possible (e.g., `Σ → Σ'` for atomic, `Σ ⇒ Σ'` for composite).

### Issue 4: K.μ~ "canonical expansion" status unclear — is it the only valid decomposition?

**ASN-0047, "Decomposition of K.μ~"**: "The canonical expansion is *full content-subspace clearance and rebuild*: K.μ⁻ removes V_{s_C}(d) entirely [...] K.μ⁻ must retain link-subspace mappings".

**Problem**: A non-identity content-subspace permutation that affects only positions k₀..n_{s_C} can also be realized by a partial-suffix K.μ⁻ removing only positions k₀..n_{s_C}, followed by K.μ⁺ rebuilding the same suffix with the permutation applied. Both the canonical and partial decompositions satisfy K.μ⁻'s admissibility and K.μ⁺'s preconditions and produce the same net bijection. The text says "the canonical expansion" (definite article) but does not state whether: (a) K.μ~ canonically denotes *only* the full-clearance expansion (in which case the partial decomposition is a non-K.μ~ composite); or (b) K.μ~ denotes *any* valid K.μ⁻ + K.μ⁺ pair realizing the bijection (in which case "canonical" is illustrative).

**Required**: Pick one and say so. If (a), explain why full clearance is privileged. If (b), reword "the canonical expansion" to "one valid expansion" and note that partial-suffix decompositions are equally valid.

### Issue 5: K.μ⁻ "Admissible removal pattern" precondition is verbose and entangles three separate concerns

**ASN-0047, K.μ⁻ definition**: The "Admissible removal pattern" paragraph runs to over 150 words covering (i) per-subspace suffix pattern, (ii) at-least-one strict contraction, (iii) D-SEQ★ shape sourcing, (iv) effect-clause restoration of `dom(M'(d)) ⊂ dom(M(d))`, and (v) parenthetical justification of why per-subspace independence does not undermine the effect clause.

**Problem**: This is hard to parse on first reading and harder to refer to. The reader cannot extract a clean "K.μ⁻ admissibility precondition" statement; everything is interleaved with justification.

**Required**: Split into three numbered clauses: (1) per-subspace suffix pattern with n'_S range, (2) strict-contraction conjunct, (3) effect-clause derivation noting per-subspace independence. Move the D-SEQ★ sourcing remark to a parenthetical at the end. The exhaustiveness lemma below already does the partition cleanly — the precondition statement should match it.

### Issue 6: L1c "T10a-conforming chain" terminology overstates the property

**ASN-0047, L1c (LinkAllocatorConformance)**: "Link allocation operates within a system conforming to T10a (AllocatorDiscipline, ASN-0034). [...] There exists a T4-valid document-level seed `s` and a T10a-conforming step sequence terminating at `a`".

And in the discharge proof: "Under SubspaceConventionAxiom (`s_C = 1`, `s_L = 2`), the chain `t₀ = d, t₁ = inc(d, 2) = b_C(d) = [d.0.1], t₂ = inc(t₁, 0) = [d.0.2] = b_L(d), t₃ = inc(t₂, 1) = ℓ = [d.0.2.1]` is T10a-conforming".

**Problem**: The chain visits b_C(d) and b_L(d), which the ASN says are *not* in dom(C) ∪ dom(L) — they are virtual anchors that no allocator's tracked domain contains. T10a in the foundation operates on activated allocators with realized domains. The chain `d → b_C(d) → b_L(d) → ℓ` is a sequence of structural inc operations satisfying the per-step `k ∈ {0, 1, 2}` and zeros bounds, but it is *not* an allocator-tracked T10a chain in the strict sense — the step `t₂ = inc(t₁, 0)` would, under T10a's T1 rule, advance A_C(d)'s frontier (yielding an output in A_C(d)'s domain) rather than crossing into A_L(d)'s anchor. The ASN handles this elsewhere by axiomatic activation (SubAllocatorAxiom) but the L1c chain term "T10a-conforming" elides this gap.

**Required**: Either rename L1c's chain property "structural inc-chain from a T4-valid document seed" (which is what the formal statement actually constrains), or explicitly state that L1c's chain captures only the per-step inc-rule conformance (k bounds, zeros bounds, length monotonicity) and that allocator-activation discharge for the anchor traversal goes through SubAllocatorAxiom. The current wording reads as if T10a's full discipline is invoked.

### Issue 7: K.μ⁻ amendment is supplied implicitly via D-CTG★/D-MIN★ supersession

**ASN-0047, "Amendments to existing transitions"** has explicit "K.α amendment" and "K.μ⁺ amendment" subsections. K.μ⁻ has no parallel "K.μ⁻ amendment" subsection — its extension to per-subspace operation is delivered through the D-CTG★/D-MIN★ replacements alone, with the table at the bottom adding "K.μ⁻ (per-subspace scope)" as an after-the-fact note.

**Problem**: The reader who reads the K.μ⁻ definition in "Elementary transitions" sees its postconditions written in terms of D-CTG/D-MIN. Then the amendment section silently replaces D-CTG/D-MIN with D-CTG★/D-MIN★ globally. The reader has to back-substitute to realize K.μ⁻'s contract changed. This is the same issue as Issue 1 but applied to K.μ⁻, missed by the explicit-amendment list.

**Required**: Add an explicit "K.μ⁻ amendment (PerSubspaceScope)" subsection to the Amendments section, stating that K.μ⁻'s D-CTG/D-MIN postconditions now read as D-CTG★/D-MIN★ and apply per-subspace, with the suffix-removal admissibility pattern made explicit. This matches K.α's and K.μ⁺'s amendment treatment and removes the asymmetry.

### Issue 8: Worked example "interior content replacement" leaves J1★ vacuity for re-added addresses implicit at the suffix length

**ASN-0047, "Worked example: interior content replacement"**: The example replaces position [1,2] in a 4-position document, decomposing as K.μ⁻ removing the suffix from [1,2] onward (positions [1,2], [1,3], [1,4]), then K.α + K.μ⁺ + K.ρ. Verification states "the re-added addresses a₃ and a₄ are *not* new to d's content-subspace range".

**Problem**: The example asserts J1★ vacuity for a₃ and a₄ but does not explicitly compute `ran(M(d)|_{s_C})` and `ran(M'(d)|_{s_C})` to confirm. A reader who is not already convinced of the range-based interpretation might wonder whether the K.μ⁻ + K.μ⁺ "round trip" for a₃ and a₄ resets their membership for J1★ purposes (i.e., is the pre/post comparison taken at composite boundaries or at intermediate K.μ⁻/K.μ⁺ boundaries?). The example states the conclusion but does not derive it from the J1★ predicate evaluated at the actual composite endpoints.

**Required**: In the J1★ verification line, write out both sets explicitly: `ran(M(d)|_{s_C}) = {a₁, a₂, a₃, a₄}` (pre-composite) and `ran(M'(d)|_{s_C}) = {a₁, a₂', a₃, a₄}` (post-composite), with the difference being `{a₂'}` only. This makes the range-based-at-composite-boundary semantics concrete in the example, not just stated.

### Issue 9: K.δ "freshness via T10a GlobalUniqueness" discharge implicitly relies on parent-allocator activation discipline not laid out

**ASN-0047, Freshness-discharge summary table**: "K.δ | ¬IsNode(e) | `e ∉ E` | T10a GlobalUniqueness on parent allocator's tracked domain".

**Problem**: For K.δ case (ii) k=2 producing the *first* account under a node n (i.e., e = inc(n, 2) when no account under n exists yet), the "parent allocator" — the node-scoped account sub-allocator — has not yet emitted anything. T10a's GlobalUniqueness applies to allocation events on tracked allocator frontiers, but the first emission's allocator must first be activated. The ASN axiomatizes activation for content/link sub-allocators via SubAllocatorAxiom but does not parallel-axiomatize it for entity-level sub-allocators (account-under-node, document-under-account). The discharge "T10a GlobalUniqueness" works by interpreting the first K.δ k=2 event itself as a T10a T2 spawn step (where the parent allocator is the node's root-attached allocator, and spawnPt is the node itself), but this is not spelled out — the reader has to reconstruct the activation argument.

**Required**: Either (a) add a sentence stating that K.δ case (ii)'s allocation events constitute T10a T2 spawn steps with the operand `t` as spawnPt, making the parent-allocator domain-tracking explicit; or (b) extend SubAllocatorAxiom-style activation to entity-level sub-allocators with an analogous "EntityAllocatorAxiom" that fixes activation at the first K.δ case (ii) event under each parent.

### Issue 10: "Cross-document disjointness chain" named as a lemma but no separate statement block

**ASN-0047, "Allocator hierarchy under documents"**: A paragraph begins "**Cross-document disjointness chain (Lemma; T10a.{2,5} → T10).** For any two distinct documents `d₁, d₂ ∈ E_doc` ..." and proceeds with proof inline.

**Problem**: The lemma is named in bold and given a derivation-chain tag, but it sits as an unnumbered paragraph rather than a standalone lemma block. Downstream sections cite it ("the *Cross-document disjointness chain* lemma") but the citation target is harder to locate than for similarly-cited lemmas with explicit block formatting.

**Required**: Either promote the lemma to a standalone block with its own statement and proof, parallel to other named lemmas in the ASN (e.g., the K.μ⁻ exhaustiveness lemma), or remove the lemma name and inline-cite the property at each use site.

## OUT_OF_SCOPE

### Topic 1: Operations layer (INSERT, DELETE, COPY, REARRANGE, MAKELINK)

**Why out of scope**: The ASN's Scope explicitly excludes named operations, their preconditions/postconditions, authority and authorization, atomicity at the operation level. The transition vocabulary K.α/K.δ/K.λ/K.μ⁺/K.μ⁺_L/K.μ⁻/K.ρ is at the elementary level beneath the operations, and the ASN is correct to defer operation specifications to a downstream ASN.

### Topic 2: Node-allocation registry mechanism

**Why out of scope**: NodeUniqueAllocation is axiomatized to deliver freshness and bootstrap-lineage conditions without committing to the registry's protocol, persistence model, or concurrency discipline. The Open Questions list captures this. Specifying the registry is genuinely a future-ASN concern.

### Topic 3: Account-level versioning (K.δ k=1 with IsAccount(t))

**Why out of scope**: The Open Questions list captures this as a deferred design choice. K.δ k=1's `t ∈ E_doc` precondition excludes it currently; relaxing the precondition would not violate per-state invariants but is not motivated by current use cases.

### Topic 4: Link-subspace tombstoning reconciliation with D-CTG★/D-MIN★

**Why out of scope**: The ASN explicitly identifies the link-withdrawal gap under D-CTG★/D-MIN★ and notes that a separate withdrawal mechanism (status flag, tombstone marker, retraction link) would be required to reconcile with Nelson's design. The Open Questions list captures this; designing the mechanism is a downstream ASN's task.

### Topic 5: Concurrent operations and serialization discipline

**Why out of scope**: SequentialTransitionAxiom posits totally-ordered atomic transitions. The Open Questions list captures concurrency reconciliation as a future-ASN concern. The present ASN's abstract sequential model is the appropriate scope for transition-level invariants.

VERDICT: REVISE
