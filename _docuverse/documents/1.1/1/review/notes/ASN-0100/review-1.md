# Review of ASN-0100

## REVISE

### Issue 1: Composite vs. primitive ambiguity is unresolved

**ASN-0100, "The Operation: Formal Contract"**: "We now state INSERT as a transition `Σ → Σ'`."

**Problem**: ASN-0047's `ValidComposite★` restricts transitions to elementary kinds (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ). No single elementary transition can both allocate n content addresses AND extend AND shift existing mappings. K.α modifies only C; K.μ⁺ preserves existing mappings at their existing positions and cannot shift them. The only substrate path to the post-state appears to be: n K.α steps + K.μ⁻ (retaining the Left prefix) + K.μ⁺ (adding Insertion + Shifted-right) + n K.ρ steps. The ASN treats INSERT as a single transition without identifying it as either (a) a new elementary primitive (requiring substrate amendment) or (b) a composite governed by `ValidComposite★`. The atomicity discussion compounds this — the claim "no observable intermediate state exists" only holds if INSERT is a new primitive.

**Required**: Resolve INSERT's status. Either declare it a new elementary transition (amending the substrate vocabulary and re-verifying coupling constraints), or identify the substrate composite that realizes it and reframe atomicity in terms of composite-boundary properties under `ValidComposite★`.

### Issue 2: Provenance recording (R) not addressed

**ASN-0100, throughout**: The Effect section covers C and M. Provenance is mentioned only conditionally: "If the system maintains a provenance relation tracking which documents have ever contained which I-addresses, INSERT extends this relation by `{(a_k, d) : 0 ≤ k < n}`."

**Problem**: ASN-0047 makes R a mandatory component of state. J1★ (ExtensionRecordsProvenanceContentSubspace) requires every newly placed content-subspace I-address that wasn't previously in `ran(M(d))` to have its provenance pair `(a, d)` in R'. Each freshly allocated `a_k` is placed at Insertion position `shift(p, k)` with `a_k ∉ ran(M(d))` (freshness ⟹ not previously mapped). So J1★ forces `(a_k, d) ∈ R'` for every k. J0 (AllocationRequiresPlacement) and J1'★ have parallel implications. Provenance is not optional.

**Required**: Make R part of the operation effect: `R' = R ∪ {(a_k, d) : 0 ≤ k < n}`. Include K.ρ in the operation's substrate decomposition. Add this to the formal contract and the claims table.

### Issue 3: No concrete worked example

**ASN-0100, entire spec**: The ASN states the operation abstractly but never instantiates it.

**Problem**: Review standards require a concrete example. Without one, the ASN's most subtle claims (region disjointness for interior insertion, the `j = N` append case, the empty-document first insertion) cannot be verified by inspection.

**Required**: Add a worked example. E.g., starting with `V_{s_C}(d) = {[1,1]→a₁, [1,2]→a₂, [1,3]→a₃, [1,4]→a₄, [1,5]→a₅}`, perform INSERT(d, [1,3], ⟨v₀, v₁⟩). Show the Left/Insertion/Shifted-right partition explicitly: Left = `{[1,1]→a₁, [1,2]→a₂}`, Insertion = `{[1,3]→a_new0, [1,4]→a_new1}`, Shifted-right = `{[1,5]→a₃, [1,6]→a₄, [1,7]→a₅}`. Verify INS.M-left, INS.M-insert, INS.M-shift, INS.inv.seq against this. Include at least one empty-document case and one append (`j = N`) case.

### Issue 4: Foundation lemmas not cited in proofs

**ASN-0100, "Verifying the Invariants" and throughout**: Many proof steps rely on foundation results without explicit citation.

**Problem**: Proofs become hand-waves when the load-bearing foundation lemmas aren't named. Specifically:
- The shift behavior of right-region positions duplicates I3 from ASN-0082 (PostInsertionShift); the ASN should cite I3 rather than re-derive.
- "Coverage and link discoverability" derives the projection-shift behavior without citing LP3★ (CoverageInvariance) or LP9 (ExtensionMonotonicity) from ASN-0098.
- The tight-endset freshness argument should cite LP19a (TightFreshness) from ASN-0098.
- The fresh-address chain structure should cite ChainPrefixExtension and ChainEnumerationInjectivity from ASN-0093.
- The depth claim (m_C uniform) should cite S8-depth from ASN-0036.
- The precondition predicates `ValidInsertionPosition` and `ValidFirstInsertionPosition` are paraphrased rather than named.
- The shift injectivity used in region-disjointness should cite TS2 from ASN-0034.

**Required**: Cite specific foundation lemmas at each proof step. The current prose-only derivations are insufficient for the substrate ASN-0082 already proved.

### Issue 5: shift(p, 0) = p convention not cited

**ASN-0100, arrangement effect, Insertion region**: "`(A k : 0 ≤ k < n :: shift(p, k) ∈ dom(M'(d)) ∧ M'(d)(shift(p, k)) = a_k)`"

**Problem**: ASN-0034's OrdinalShift is defined for `n ≥ 1`. The k=0 case requires the OrdinalShiftBase convention from ASN-0058 (`t + 0 = t`). The ASN uses shift(p, 0) without citing this convention, leaving the k=0 case formally undefined.

**Required**: Cite OrdinalShiftBase from ASN-0058, or split the Insertion clause into "`M'(d)(p) = a_0`" and "`M'(d)(shift(p, k)) = a_k` for `1 ≤ k < n`".

### Issue 6: Frame condition for E (entities) missing

**ASN-0100, Frame Conditions**: Frame addresses L, dom(M), other documents, other subspaces — but not E (the entity set from ASN-0047) or R (provenance).

**Problem**: ASN-0047's state is `(C, L, E, M, R)`. INSERT does not create entities, but the frame should state this: `E' = E`. Similarly for R (see Issue 2).

**Required**: Add `E' = E` to the frame. Add R to the effect (per Issue 2).

### Issue 7: "Edge cases require no special handling" claim contradicts the spec

**ASN-0100, "Position Constraints"**: "The edge cases require no special handling in the specification. The universal forms of the three regions handle them uniformly..."

**Problem**: The empty-document case DOES require special handling. The caller chooses depth `m`; the precondition predicate is different (`ValidFirstInsertionPosition(d, p, m)` vs. `ValidInsertionPosition(d, p)`); the post-state's m_C is fixed by the operation. The Precondition section acknowledges this with the conditional "either non-empty case... or empty case..." but the Position Constraints prose contradicts it.

**Required**: Either rewrite to acknowledge that the empty case has a different precondition predicate and parameter, or restrict the claim to the non-empty case.

### Issue 8: Discoverability preservation is argued informally, not stated as a postcondition

**ASN-0100, "Coverage and link discoverability"**: "Pre-state discoverability is preserved: `discoverable_from(ℓ, d', Σ) ⟹ discoverable_from(ℓ, d', Σ')`"

**Problem**: This is a key consequence of INSERT but is stated mid-prose rather than as a labelled postcondition with derivation. The argument relies on the projection identity "every pre-state mapping `v → M(d)(v)` re-appears in the post-state either as `v → M(d)(v)` (Left) or `shift(v, n) → M(d)(v)` (Shifted right)" — this should be derived explicitly from INS.M-left and INS.M-shift, then connected to `coverage(L(ℓ).eᵢ)` to establish projection preservation. INS.inv.discov in the claims table is too thin.

**Required**: State the projection-shift correspondence as a derived postcondition: for every `ℓ ∈ dom(L)`, slot `i`, and `d' ∈ dom(M)`, `project(ℓ, i, d', Σ') = π_L(project(ℓ, i, d', Σ)) ∪ π_R(project(ℓ, i, d', Σ)) ∪ N_ℓ` where `π_L` is identity on the Left region, `π_R` is shift-by-n on the right region, and `N_ℓ ⊆ {shift(p, k) : 0 ≤ k < n}` captures new V-positions whose fresh I-address happens to lie in coverage (empty for tight endsets by LP19a).

### Issue 9: Atomicity decomposition argument doesn't use the substrate decomposition

**ASN-0100, "Atomicity and Canonical Order"**: Three candidate decompositions are presented ("allocation alone", "allocation plus placement, no shift", "shift without placement"), each shown to violate an invariant.

**Problem**: None of these candidates corresponds to a sequence of substrate-level elementary transitions. K.α never "shifts"; K.μ⁺ doesn't shift existing mappings; the natural substrate composite is K.α steps + K.μ⁻ + K.μ⁺ + K.ρ. The intermediate after K.μ⁻ has the right region absent from `dom(M(d))` but D-SEQ is still satisfied on the retained prefix; that intermediate violates no per-state invariant. The argument as written conflates implementation concerns with substrate semantics.

**Required**: If INSERT is a composite, identify the actual substrate decomposition and verify that each intermediate satisfies per-state invariants while composite-boundary coupling (J0, J1★, J1'★) is only required at the boundary. If INSERT is a new primitive, drop the three-candidate argument and state the atomicity directly.

### Issue 10: The "n successive emissions" of A_C(d) requires justification

**ASN-0100, INS.alloc**: "Let `a_0, a_1, …, a_{n−1}` denote `n` successive emissions of `A_C(d)` produced at this transition... each `a_k` satisfies `a_k ∉ dom(C) ∪ dom(L)` at the operation's pre-state."

**Problem**: K.α's freshness precondition is against the pre-state of the K.α firing, not against the operation's pre-state. For the composite (Issue 1), `a_1`'s freshness must hold at the state after `a_0` has been added. The pairwise distinctness `a_k ≠ a_j` for `j < k` is guaranteed by ChainEnumerationInjectivity from ASN-0093, but the ASN doesn't make this explicit.

**Required**: Either (a) re-derive the freshness of each `a_k` against the appropriate intermediate state and cite ChainEnumerationInjectivity, or (b) declare INSERT a primitive that emits n addresses simultaneously and prove (or axiomatize) joint freshness.

### Issue 11: Out-of-scope topics correctly flagged as Open Questions, but one belongs in this ASN

**ASN-0100, Open Questions**: "What must INSERT preserve about its post-state's relationship to the pre-state's link projections — must every pre-state projection's image be a contiguous sub-set of the post-state projection's image, or only a subset?"

**Problem**: This is the projection-shift correspondence from Issue 8. It's not an open question — it's a derivable property of INSERT that should be a postcondition of this ASN.

**Required**: Move this from Open Questions to a derived postcondition.

### Issue 12: INS.identity claim lacks derived consequences

**ASN-0100, INS.identity**: "INSERT creates fresh content identity: each `a_k` is a new allocation with `origin(a_k) = d`; INSERT cannot identify new content with any pre-existing I-address regardless of value coincidence"

**Problem**: This claim has consequences (cross-document independence, version chain independence, link survivability through value coincidence) that the prose mentions but doesn't derive formally. Per review standards, "postconditions established but consequences not explored" is a REVISE item.

**Required**: Add explicit derived corollaries: (a) if two documents `d₁, d₂` each INSERT the same value `v`, they produce I-addresses with `origin(a_{d₁}) = d₁ ≠ d₂ = origin(a_{d₂})`; (b) coverage of any pre-state tight endset cannot accidentally capture freshly allocated `a_k` (cite LP19a from ASN-0098).

### Issue 13: Empty-case post-state's depth fixation not formally derived

**ASN-0100, Discovering the Three Effects**: "This first insertion fixes `m_C = m` for all subsequent text-subspace operations on `d`."

**Problem**: The "fixation" is presented as a property of INSERT, but it's actually a consequence of S8-depth (FixedDepthVPositions) from ASN-0036 — uniform depth within a subspace is a per-state invariant, so once `V_{s_C}(d)` becomes non-empty with depth m, S8-depth forces all subsequent text positions in `d` to have depth m.

**Required**: Cite S8-depth and state explicitly that the post-state with `V_{s_C}(d') ≠ ∅` satisfies S8-depth at depth m_C.

## OUT_OF_SCOPE

### Topic 1: Concurrent INSERTs and serialization

The Open Questions section asks "what does the abstract specification say about concurrent INSERTs targeting the same V-position from independent agents". Concurrency is governed by SequentialTransitionAxiom (ASN-0093) at the substrate level — transitions are atomic and totally ordered. The choice of which INSERT fires first is a scheduling concern outside this ASN.

**Why out of scope**: Concurrency is a substrate-level concern handled by SequentialTransitionAxiom.

### Topic 2: Whether INSERT is closed under composition with itself

Whether `Σ → INSERT₁ → Σ_1 → INSERT₂ → Σ_2` can be re-expressed as a single INSERT from Σ to Σ_2.

**Why out of scope**: This is a question about composite algebra, not the operation's specification. The composite framework lives in ASN-0047's ValidComposite★, not in operation-specification ASNs.

### Topic 3: Chunked INSERT and implementation freedom

Whether an implementation may decompose a long INSERT into smaller sub-INSERTs with equivalent abstract effect.

**Why out of scope**: Implementation realization of the abstract operation is below the spec's level of abstraction.

### Topic 4: Derived document metadata (size, last-modified, footprint)

What derived properties INSERT updates.

**Why out of scope**: Derived metadata is application-layer concern, not core spec.

### Topic 5: Link subspace insertion analogue

The Open Questions ask about the analogous insertion operation for the link subspace.

**Why out of scope**: Link subspace operations are not covered by the review's scope (link semantics out of scope).

VERDICT: REVISE
