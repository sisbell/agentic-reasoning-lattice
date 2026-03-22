# ASN-0072: State Transitions 0

*2026-03-22*

ASN-0047 defines the system state as Σ = (C, E, M, R) with elementary transitions K.α (content), K.δ (entity), K.μ⁺/K.μ⁻/K.μ~ (arrangement), and K.ρ (provenance). The link store L adds a fifth state component but has no transitions defined for it. This ASN integrates the link store into the transition framework: it defines two new elementary transitions (link allocation and link-subspace arrangement extension), amends existing transitions for subspace-correct operation, generalizes the referential integrity and provenance invariants for the two-subspace state, and proves that every reachable state of the extended system satisfies the full invariant set.


## Link Store: Restated Definitions

This ASN uses properties of the link store. For self-containment, we restate the definitions and invariants needed.

**Definition — Endset.** An *endset* is a finite set of well-formed spans: `Endset = 𝒫_fin(Span)`, where `Span` is the set of well-formed span pairs `(s, ℓ)` satisfying T12 (ASN-0034). The empty set ∅ is a valid endset.

**Definition — Link.** A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively.

**Definition — Subspace identifiers.** We write `s_C` for the content subspace identifier and `s_L` for the link subspace identifier. These are the first components of the element field for content and link addresses respectively: `fields(a).E₁ = s_C` for content addresses, `fields(ℓ).E₁ = s_L` for link addresses. The same identifiers serve for V-positions: `subspace(v) = v₁`.

**SC-NEQ** — *SubspaceDistinctness* (AX, axiom). `s_C ≠ s_L`.

This is the structural precondition for every disjointness argument in this ASN. By T7 (SubspaceDisjointness, ASN-0034), `s_C ≠ s_L` implies that no tumbler can be both a content address and a link address. Without SC-NEQ, L0 and L14 would be vacuous. We note that `s_C ≥ 1` follows from S8a (all V-position components strictly positive) and `s_L ≥ 1` follows from T4 (element-field components strictly positive) combined with L1 below.

**L0** — *SubspacePartition* (INV, predicate).

  `(A a ∈ dom(Σ.L) :: fields(a).E₁ = s_L)`

  `(A a ∈ dom(Σ.C) :: fields(a).E₁ = s_C)`

**L1** — *LinkElementLevel* (INV, predicate).

  `(A a ∈ dom(Σ.L) :: zeros(a) = 3)`

Every link address is an element-level tumbler.

**L1a** — *LinkScopedAllocation* (INV, predicate).

  `(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)`

Every link address is allocated under the tumbler prefix of a document in E_doc.

**L3** — *TripleEndsetStructure* (INV, predicate).

  `(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset)`

Every link in the link store has exactly three endsets.

**L12** — *LinkImmutability* (INV, predicate).

  `(A Σ → Σ' : (A a : a ∈ dom(Σ.L) : a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)))`

Once created, a link's address persists in dom(L) and its value is permanently fixed.

**L14** — *StoreDisjointness* (INV, predicate).

  `dom(Σ.C) ∩ dom(Σ.L) = ∅`

Derived from L0 and SC-NEQ via T7: if `a ∈ dom(C)` then `fields(a).E₁ = s_C`, and if `a ∈ dom(L)` then `fields(a).E₁ = s_L`; since `s_C ≠ s_L`, no address inhabits both domains.


## Extended System State

The extended system state is **Σ = (C, L, E, M, R)**, where L : T ⇀ Link is the link store.

**Extended initial state.** Σ₀ = (C₀, L₀, E₀, M₀, R₀) with L₀ = ∅. The extended invariants hold vacuously at Σ₀: L0, L1, L1a, L3, L12, L14 are satisfied by empty L; S3★'s link-subspace clause is vacuous (no link-subspace V-positions exist in M₀); P4★ reduces to P4 (which holds at Σ₀ per ASN-0047); D-CTG and D-MIN hold vacuously since M₀(d) = ∅ for all d, so V_S(d) = ∅ for every subspace S. This closes the inductive base for the ExtendedReachableStateInvariants theorem.

All existing elementary transitions from ASN-0047 hold L in their frame: L' = L.


## Amendments to Existing Transitions

**K.α amendment** — *ContentSubspaceRestriction*. In the extended state, K.α is amended with a content-subspace restriction: the allocated address must satisfy `fields(a).E₁ = s_C`. This parallels K.λ's `fields(ℓ).E₁ = s_L` and is required by L0 clause 2 — without it, K.α could allocate an address with subspace s_L, placing it in dom(C') and violating the partition. The amendment also preserves L14: since `fields(a).E₁ = s_C` and `s_C ≠ s_L` (SC-NEQ), the address `a` cannot appear in dom(L) — L0 clause 1 at the pre-state ensures all dom(L) addresses have subspace s_L — so `dom(C') ∩ dom(L') = ∅`.

**K.μ⁺ amendment** — *ContentSubspaceRestriction*. K.μ⁺ is amended with a content-subspace restriction: new V-positions must satisfy `subspace(v) = s_C`. This complements K.μ⁺_L (defined below), which handles link-subspace extensions exclusively. The restriction is necessary — without it, K.μ⁺ could create a link-subspace V-position mapping to dom(C), violating S3★. With this amendment, the two transitions partition arrangement extensions by subspace. K.μ⁺ (amended) additionally requires that M'(d) satisfies D-CTG and D-MIN for each subspace — paralleling K.μ⁺_L's explicit contiguity and minimum-position preconditions.

**K.μ⁻ amendment** — *PerSubspaceContiguity*. K.μ⁻ (ASN-0047), when applied in the extended state, must produce M'(d) satisfying D-CTG and D-MIN for each subspace. By D-SEQ at the *input* state (ASN-0036), V_S(d) for each non-empty subspace S is a contiguous ordinal range {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}; the postcondition constrains contraction to removal from the maximum end of V_S(d) or removal of all positions in V_S(d).

**Consequence for J4 (Fork, ASN-0047).** Since J4's K.μ⁺ step is now restricted to content-subspace V-positions, forking a document populates only the content subspace of the new document. Link-subspace mappings from the source document are not copied — the forked document's link subspace starts empty. J4 remains a valid composite under the amended coupling constraints. J1★ is satisfied because J4's K.μ⁺ creates only content-subspace V-positions (by the amendment) and J4's K.ρ records provenance for each `a ∈ ran(M'(d_new))`, covering every content-subspace extension. J1'★ is satisfied because each new `(a, d_new) ∈ R' \ R` has `a ∈ ran(M'(d_new))` from content-subspace extensions — `ran(M'(d_new)) ⊆ ran(M(d_src)) ⊆ dom(C)` by J4's definition, so P7 compatibility is maintained. D-CTG and D-MIN are satisfied: J4's K.μ⁺ step operates on a freshly created document (M(d_new) = ∅ after K.δ), constructing the entire content-subspace arrangement; by choosing V-positions contiguously from the minimum [s_C, 1, ..., 1], D-CTG and D-MIN hold for the content subspace, and the link subspace of d_new is empty (J4's K.μ⁺ is content-subspace-only by the amendment), so D-CTG and D-MIN hold vacuously for it. This is consistent with Nelson's design: each document owns only its home links, and links from the source remain discoverable through the shared I-addresses via refractive following — "a link to one version of a Prismatic Document is a link to all versions" (Nelson). A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope.


## Link Allocation

**K.λ** — *LinkAllocation* (TRANS, definition). Creates a new entry in the link store.

*Precondition:*
- d ∈ E_doc  (home document exists)
- ℓ ∉ dom(L) ∪ dom(C)  (fresh address — L14)
- zeros(ℓ) = 3 ∧ fields(ℓ).E₁ = s_L  (element-level, link subspace — L0, L1)
- origin(ℓ) = d  (scoped to home document — L1a)
- `(A ℓ' : ℓ' ∈ dom(L) ∧ origin(ℓ') = d : ℓ' < ℓ)`  (forward allocation — T9)
- (F, G, Θ) ∈ Link  (well-formed link value — L3)

*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`

*Frame:* `C' = C; E' = E; (A d' :: M'(d') = M(d')); R' = R`

The address ℓ is produced by the same forward-allocation discipline as content addresses (T9, ASN-0034): within each document's link subspace, addresses are monotonically increasing. By T7 (SubspaceDisjointness, ASN-0034) and SC-NEQ, the link subspace s_L is disjoint from the content subspace s_C, so ℓ cannot collide with any content address. By T10 (PartitionIndependence, ASN-0034), link addresses in different documents cannot collide either.


## Generalized Referential Integrity

**S3★** — *GeneralizedReferentialIntegrity* (INV, predicate). The arrangement maps V-positions to addresses in the store appropriate to their subspace:

  `(A d, v : v ∈ dom(Σ.M(d)) : (subspace(v) = s_C ⟹ Σ.M(d)(v) ∈ dom(Σ.C)) ∧ (subspace(v) = s_L ⟹ Σ.M(d)(v) ∈ dom(Σ.L)))`

where `subspace(v)` denotes the first component of the V-position. S3★ supersedes S3 (ASN-0036) for the extended state Σ = (C, L, E, M, R): S3 requires every V-position to map into dom(C), which is violated by link-subspace mappings targeting dom(L). S3 remains valid when restricted to states with no link-subspace mappings — the pre-extension states of ASN-0047 have only content-subspace V-positions, for which S3★ reduces to S3.

Existing transitions preserve S3★: K.α, K.δ, K.ρ hold M in frame; K.μ⁺ creates only content-subspace V-positions (by its amended precondition `subspace(v) = s_C`), so new mappings target dom(C) and the link-subspace clause is unaffected; K.μ⁻ contracts dom(M(d)), preserving both clauses; K.μ~ is a distinguished composite K.μ⁻ + K.μ⁺ (ASN-0047) with a bijection `π : dom(M(d)) → dom(M'(d))` satisfying `M'(d)(π(v)) = M(d)(v)`. We establish S3★ preservation first by direct decomposition, then derive the stronger property that link-subspace mappings are fixed.

*S3★ by decomposition.* K.μ~ decomposes into K.μ⁻ followed by K.μ⁺. K.μ⁻ restricts dom(M(d)) with values unchanged — content-subspace mappings still target dom(C), link-subspace mappings still target dom(L) — so S3★ holds for the intermediate state. K.μ⁺ (amended) adds only content-subspace V-positions targeting dom(C) by precondition, preserving existing mappings by frame — S3★ holds for M'(d).

**S3★-aux** — *SubspaceExhaustiveness* (INV, predicate). In every reachable state, all V-positions have subspace s_C or s_L:

  `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)`

*Proof.* By induction on transition sequences from Σ₀. Base: M₀ = ∅, the property holds vacuously. Step: K.μ⁺ (amended) creates only s_C positions; K.μ⁺_L creates only s_L positions; K.μ⁻ removes positions without altering subspaces of survivors; K.μ~ decomposes into K.μ⁻ + K.μ⁺, each maintaining the property independently of fixity; K.α, K.δ, K.λ, K.ρ hold M in frame. ∎

**Link-subspace fixity under K.μ~.** Since K.μ⁺ (amended) requires `subspace(v) = s_C` for new V-positions, K.μ⁺ cannot create link-subspace V-positions. Let `dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_L}` denote the link-subspace V-positions. With S3★ now established for M'(d), π must map link-subspace positions to link-subspace positions: if `v ∈ dom_L(M(d))` then `M(d)(v) ∈ dom(L)`, and `M'(d)(π(v)) = M(d)(v) ∈ dom(L)`, so `subspace(π(v)) = s_L`: by S3★-aux, `subspace(π(v)) ∈ {s_C, s_L}`; the case `subspace(π(v)) = s_C` is eliminated because a content-subspace position mapping to dom(L) would violate S3★'s content clause, since `M'(d)(π(v)) ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14, which depends on SC-NEQ). Thus `π` restricted to `dom_L(M(d))` is an injection into `dom_L(M'(d))`. Since K.μ⁺ cannot create link-subspace V-positions, `|dom_L(M'(d))| ≤ |dom_L(M(d))|`. If K.μ⁻ removed `r ≥ 1` link-subspace positions, then `|dom_L(M'(d))| ≤ |dom_L(M(d))| − r`, and the injection from `dom_L(M(d))` (size N) into `dom_L(M'(d))` (size at most N − r) cannot exist. Therefore `r = 0` — no link-subspace positions are removed. It follows that `M'(d)` restricted to `dom_L(M(d))` equals `M(d)` restricted to `dom_L(M(d))`. Let `M_int(d)` denote the intermediate arrangement after K.μ⁻ but before K.μ⁺. K.μ⁻ removes none of the link-subspace positions (`r = 0`) and preserves the values of all surviving positions, so `M_int(d)|_{dom_L} = M(d)|_{dom_L}`. K.μ⁺ (amended) operates on `M_int(d)`: its frame preserves pre-existing mappings (`(A v : v ∈ dom(M_int(d)) : M'(d)(v) = M_int(d)(v))`), and its subspace restriction prevents creating new link-subspace positions. Chaining: `M'(d)|_{dom_L} = M_int(d)|_{dom_L} = M(d)|_{dom_L}`. Each surviving link-subspace mapping retains its value in dom(L).


## Link-Subspace Extension

**K.μ⁺_L** — *LinkSubspaceExtension* (TRANS, definition). Extends a document's arrangement in the link subspace.

*Precondition:*
- d ∈ E_doc
- ℓ ∈ dom(L)  (the target link must already exist in dom(L) — placed there by some prior K.λ)
- origin(ℓ) = d  (only home-document links may be arranged)
- V-position v_ℓ satisfies:
  - subspace(v_ℓ) = s_L
  - m_L ≥ 2, where: if V_{s_L}(d) ≠ ∅, m_L is the common depth of existing link-subspace V-positions (determined by S8-depth); if V_{s_L}(d) = ∅, m_L is a parameter of the transition, subject only to m_L ≥ 2. The lower bound is structural: ordinal shift at depth 1 alters the subspace identifier (`shift([s_L], 1) = [s_L + 1]`, violating subspace closure TA7a), so the link subspace requires depth at least 2
  - If V_{s_L}(d) = ∅: v_ℓ is the minimum position `[s_L, 1, ..., 1]` of depth m_L (D-MIN)
  - If V_{s_L}(d) ≠ ∅: v_ℓ = shift(max(V_{s_L}(d)), 1), extending the contiguous range (D-CTG)
  - #v_ℓ = m_L (S8-depth within the link subspace)

*Effect:* `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}`

*Frame:* `C' = C; L' = L; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R`

We verify `v_ℓ ∉ dom(M(d))`, as required for M'(d) to be a proper extension preserving S2 (ArrangementFunctionality). When `V_{s_L}(d) = ∅`: no link-subspace V-position exists in dom(M(d)), and `subspace(v_ℓ) = s_L`, so `v_ℓ ∉ dom(M(d))`. When `V_{s_L}(d) ≠ ∅`: `v_ℓ = shift(max(V_{s_L}(d)), 1) > max(V_{s_L}(d))` by TS4 (ShiftStrictIncrease, ASN-0034), placing v_ℓ beyond all existing link-subspace positions. In both cases, `subspace(v_ℓ) = s_L` and `s_L ≠ s_C` (SC-NEQ) ensures no collision with text-subspace positions (T7). Therefore `v_ℓ ∉ dom(M(d))`.

The preconditions ensure that after the extension, D-CTG (contiguity), D-MIN (minimum position), and S8-depth (uniform depth) hold for the link subspace of d. S3★ is satisfied: `subspace(v_ℓ) = s_L` and `M'(d)(v_ℓ) = ℓ ∈ dom(L')`.

The origin restriction `origin(ℓ) = d` distinguishes link-subspace extension from content-subspace extension, where K.μ⁺ intentionally permits `origin(a) ≠ d` — that is content transclusion, an established architectural feature. Link transclusion — arranging a foreign-origin link in a document's link subspace — is excluded by design. Nelson: "A document includes only the links of which it is the home document" (LM 4/31). The byte stream admits transclusion ("The virtual byte stream of a document may include bytes from any other document," LM 4/10); links do not. Links maintain "permanent order of arrival" in their home document, and home document determines ownership ("A link need not point anywhere in its home document. Its home document indicates who owns it," LM 4/12). Arranging a link with `origin(ℓ) ≠ d` would place an out-link in a document that does not own it — violating the ownership semantics that home-document identity is meant to carry. The architecture provides alternatives: bidirectional link search discovers all links attached to transcluded content regardless of which document houses them; creating a new link in one's own document is the natural analog of annotation. Gregory confirms that the implementation achieves origin matching by procedural atomicity — `docreatelink` both allocates the link ISA under the document's address and places it in the document's arrangement in a single operation — but no runtime guard exists; `acceptablevsa` unconditionally returns TRUE and `docopy` performs no origin check. The origin restriction in K.μ⁺_L formalizes the structural guarantee that the implementation achieves by construction.

**Per-subspace arrangement invariants under K.μ⁺_L.** S8a (VPositionWellFormedness): the quantifier `(A v ∈ dom(M(d)) : v₁ ≥ 1 : zeros(v) = 0 ∧ v > 0)` covers *all* V-positions with `v₁ ≥ 1`, including link-subspace positions. We must establish that `s_L ≥ 1`: by L1, every link address is element-level (`zeros(ℓ) = 3`), so by T4 (ASN-0034), every element-field component is strictly positive — in particular `fields(ℓ).E₁ = s_L > 0`. Since K.μ⁺_L uses the same identifier s_L for V-positions, link-subspace V-positions have `v₁ = s_L ≥ 1` and fall under S8a's quantifier. For text-subspace positions: unchanged. For the new link-subspace position v_ℓ: K.μ⁺_L places `v_ℓ = [s_L, 1, ..., 1]` (D-MIN) or `shift(max(V_{s_L}(d)), 1)` (D-CTG). In either case, every component of v_ℓ is strictly positive — s_L > 0 by the above, and the remaining components are 1 or incremented from positive values — so `zeros(v_ℓ) = 0 ∧ v_ℓ > 0`. S8-fin: adding one position to a finite set preserves finiteness. For the link subspace specifically: S8-depth is satisfied by K.μ⁺_L's precondition (`#v_ℓ = m_L`). D-CTG (VContiguity) and D-MIN (VMinimumPosition) are quantified over *all* subspaces S. For the text subspace (S = s_C): V_{s_C}(d) is unchanged. For the link subspace (S = s_L): K.μ⁺_L's precondition places v_ℓ at the minimum position if V_{s_L}(d) was empty, or at the next contiguous position if non-empty, satisfying both D-CTG and D-MIN. D-SEQ follows from D-CTG, D-MIN, S8-fin, and S8-depth (as derived in ASN-0036). S8 (SpanDecomposition): S8's quantifier `v₁ ≥ 1` captures all V-positions in the extended state — since both `s_C ≥ 1` and `s_L ≥ 1` (established above for S8a) — extending coverage to the link subspace. S8 is derived from S8-fin, S8a, S2, and S8-depth (ASN-0036), all verified above. The new link-subspace mapping `(v_ℓ, ℓ)` either forms a new width-1 correspondence run or extends the last existing link-subspace run by one position if I-adjacent. All existing runs — both text-subspace and link-subspace — are unchanged: K.μ⁺_L preserves existing mappings (frame), and the new position `v_ℓ ∉ dom(M(d))` falls in no existing run, so no existing run is split or modified.


## Link-Subspace Ownership

**CL-OWN** — *LinkSubspaceOwnership* (INV, predicate). In every reachable state:

  `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)`

Every document's link-subspace arrangement contains only its own links. This is maintained by two mechanisms: K.μ⁺_L's precondition `origin(ℓ) = d` ensures ownership at creation, and link-subspace fixity under K.μ~ ensures preservation through reordering — no transition can place a foreign-origin link in a document's link subspace.

*Proof.* By induction on transition sequences from Σ₀. Base: M₀(d) = ∅ for all d, so the property holds vacuously. Step: K.μ⁺_L adds `(v_ℓ, ℓ)` with `origin(ℓ) = d` (precondition) and preserves existing mappings (frame); K.μ⁺ (amended) adds only content-subspace positions (`subspace(v) = s_C`), so no link-subspace change; K.μ⁻ removes positions without altering values of survivors; K.μ~ preserves link-subspace mappings identically (link-subspace fixity); K.α, K.δ, K.λ, K.ρ hold M in frame. ∎


## Content-Scoped Containment and Provenance

The containment relation `Contains(Σ)` (ASN-0047) is defined as `{(a, d) : d ∈ E_doc ∧ a ∈ ran(M(d))}` — unscoped across all subspaces. With link-subspace mappings, `Contains(Σ')` includes `(ℓ, d)` for every link ℓ mapped in d's arrangement. P4 requires `Contains(Σ) ⊆ R`, but provenance entries satisfy P7: `(A (a, d) ∈ R :: a ∈ dom(C))`. Since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14), `(ℓ, d) ∉ R` — P4 is unsatisfiable for the unscoped relation once link-subspace mappings exist.

**Contains_C(Σ)** — *ContentContainment* (DEF, function).

  `Contains_C(Σ) = {(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}`

**P4★** — *ProvenanceBounds (content-subspace)* (INV, predicate).

  `Contains_C(Σ) ⊆ R`

P4★ supersedes P4 for the extended state. In pre-extension states (no link-subspace mappings), `Contains_C(Σ) = Contains(Σ)`, so P4★ reduces to P4. Existing transitions preserve P4★: K.α, K.δ, K.ρ hold M in frame; K.μ⁻ contracts dom(M(d)), which can only shrink Contains_C; K.μ~ preserves P4★ by the link-subspace fixity established in the S3★ analysis above. Since π bijects dom(M(d)) onto dom(M'(d)) and maps dom_L bijectively onto dom_L (by fixity), it maps the complement dom_C(M(d)) = dom(M(d)) \ dom_L(M(d)) bijectively onto dom_C(M'(d)) = dom(M'(d)) \ dom_L(M'(d)). These complements are exactly the content-subspace positions by S3★-aux: every V-position has subspace s_C or s_L, so `dom(M(d)) \ dom_L(M(d)) = {v ∈ dom(M(d)) : subspace(v) = s_C}`. With `M'(d)(π(v)) = M(d)(v)` for each such v, the set `{a : (E v ∈ dom_C(M(d)) : M(d)(v) = a)} = {a : (E u ∈ dom_C(M'(d)) : M'(d)(u) = a)}`, so `Contains_C(Σ') = Contains_C(Σ) ⊆ R = R'`.

**Note on K.μ⁺ and P4★.** K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated at the intermediate state. P4★ is restored at composite boundaries by the coupling constraint J1★, which requires K.ρ to record provenance for every content-subspace arrangement extension. See the two-layer proof structure in ExtendedReachableStateInvariants.


## Scoped Coupling Constraints

The coupling constraints J1, J1' (ASN-0047) were formulated before link-subspace mappings existed. They must be scoped to content-subspace arrangement extensions; otherwise J1 and P7 are mutually unsatisfiable — J1 would require provenance recording for the link address ℓ entering ran(M'(d)), but P7 requires every provenance entry to reference dom(C), and ℓ ∈ dom(L) with dom(L) ∩ dom(C) = ∅ (L14).

**J1★** — *ExtensionRecordsProvenance (content-subspace)* (AX, predicate).

  `(A Σ → Σ', d, v, a : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C ∧ M'(d)(v) = a : (a, d) ∈ R')`

**J1'★** — *ProvenanceRequiresExtension (content-subspace)* (AX, predicate).

  `(A Σ → Σ', a, d : (a, d) ∈ R' \ R : (E v : v ∈ dom(M'(d)) \ dom(M(d)) ∧ subspace(v) = s_C : M'(d)(v) = a))`

Link-subspace extensions (K.μ⁺_L) do not trigger provenance recording: the link address ℓ enters ran(M'(d)) but `subspace(v_ℓ) = s_L ≠ s_C` (SC-NEQ), so J1★ does not apply. P7 (ProvenanceGrounding) — `(A (a, d) ∈ R :: a ∈ dom(C))` — is preserved because R is unchanged (K.μ⁺_L holds R in frame).

The coupling constraints for valid composites in the extended state Σ = (C, L, E, M, R) are J0, J1★, J1'★. J1★ and J1'★ replace J1 and J1' (ASN-0047) by scoping provenance coupling to content-subspace arrangement changes. J0 (AllocationRequiresPlacement) is unchanged — it constrains content allocation (K.α), which remains content-subspace only.


## Extended Monotonicity Invariants

**P3★** — *ArrangementMutabilityOnly (extended)* (INV, predicate). Arrangements admit three modes of change: (a) extension, (b) contraction, (c) reordering. No other component — specifically C, L, E, R — admits contraction or reordering:

  `(A Σ → Σ' :: dom(C) ⊆ dom(C') ∧ dom(L) ⊆ dom(L') ∧ E ⊆ E' ∧ R ⊆ R')`

P3★ supersedes P3 (ASN-0047) by including L in the enumeration. L admits only extension, by L12: `dom(L) ⊆ dom(L') ∧ (A ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`.

**P5★** — *DestructionConfinement (extended)* (INV, predicate). For every state transition Σ → Σ':

  (a) `dom(C') ⊇ dom(C) ∧ (A a : a ∈ dom(C) : C'(a) = C(a))`

  (b) `dom(L') ⊇ dom(L) ∧ (A ℓ : ℓ ∈ dom(L) : L'(ℓ) = L(ℓ))`

  (c) `E' ⊇ E`

  (d) `R' ⊇ R`

The only component that can lose information is M. P5★ supersedes P5 (ASN-0047) by adding clause (b), immediate from L12.


## Orphan Links and Coupling Flexibility

The coupling constraints do not require K.λ to be paired with K.μ⁺_L. A composite consisting of K.λ alone is valid: J0 is vacuous (no content allocated), J1★ is vacuous (no content-subspace extension), and J1'★ is vacuous (no provenance change). The result is a link in dom(L) with no placement in any document's arrangement — an *orphan link*. This is a valid system state, not an error condition. State invariants are preserved: M, C, E, R are all in K.λ's frame (unchanged), so all arrangement, content, entity, and provenance invariants hold identically. L grows by one entry: dom(L') = dom(L) ∪ {ℓ}. K.λ's preconditions guarantee L0 (ℓ has subspace s_L, and ℓ ∉ dom(C) ensures dom(L') ∩ dom(C) = ∅), L1 (zeros(ℓ) = 3), L1a (origin(ℓ) ∈ E_doc), L3 (K.λ requires (F, G, Θ) ∈ Link, so L3 is established for the new entry; L12 preserves all existing entries), L12 (existing entries unchanged: L'(ℓ') = L(ℓ') for all ℓ' ∈ dom(L)), and L14 (disjointness: ℓ ∉ dom(C), so dom(L') ∩ dom(C') = ∅). Nelson explicitly diagrams "deleted links" as a category of document content (LM 4/9): links that exist in permanent storage but are "not currently addressable, awaiting historical backtrack functions."

Link withdrawal via K.μ⁻ applied to the link subspace would in principle produce the same state — a link present in L but absent from all current arrangements — but is constrained by D-CTG: removing an interior link-subspace V-position creates a gap in the contiguous range, and K.μ~ cannot close it (link-subspace mappings are fixed, as shown above). Valid link-subspace contractions are suffix truncations: for `V_{s_L}(d) = {[s_L, 1, …, 1, k] : 1 ≤ k ≤ n}` (by D-SEQ), the result must be `{[s_L, 1, …, 1, k] : 1 ≤ k ≤ n'}` for some `0 ≤ n' < n`. Removing an interior position breaks contiguity (violating D-CTG), and removing the minimum while positions above it remain violates D-MIN. Any suffix `{[s_L, 1, …, 1, k] : n' < k ≤ n}` can be removed at once — including all positions when `n' = 0`, since D-CTG and D-MIN hold vacuously for the empty set. Nelson's design suggests a different mechanism: link addresses are permanent and "not currently addressable" when withdrawn (LM 4/9), paralleling deleted bytes — the link transitions to inactive status while preserving its arrangement position, rather than being removed from M(d). The precise withdrawal mechanism is deferred to the open question on withdrawal invariants.

We do not add a J0 analog for links — the orphan state is architecturally intentional, satisfying both the permanence guarantee (L12: links are immutable once created) and the owner's right to withdraw (Nelson, LM 2/29).


## Worked Example

We verify the central postconditions on concrete tumbler values. Let `s_C = 1` and `s_L = 2` (satisfying SC-NEQ: `1 ≠ 2`). Consider document `d` at address `1.0.1.0.1` with two text content addresses allocated and arranged.

*Initial state.* `dom(C) = {1.0.1.0.1.0.1.1, 1.0.1.0.1.0.1.2}`, `dom(L) = ∅`, `E_doc = {1.0.1.0.1}`.

Arrangement: `M(d) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2}`.

Text-subspace V-positions: `V_1(d) = {[1,1], [1,2]}` — contiguous (D-CTG), minimum at `[1,1]` (D-MIN), depth 2 (S8-depth). Link subspace: `V_2(d) = ∅`.

**Step 1: K.λ — allocate link.** Create link `ℓ = 1.0.1.0.1.0.2.1` with value `(F, G, Θ)`.

Precondition verification:
- `d = 1.0.1.0.1 ∈ E_doc`
- `ℓ ∉ dom(L) ∪ dom(C)`: `dom(L) = ∅`; content addresses have element field `1.1` and `1.2` (subspace 1), while ℓ has element field `2.1` (subspace 2) — by T7 and SC-NEQ, disjoint
- `zeros(ℓ) = 3`: zeros at positions 2, 4, 6 in the tumbler `1.0.1.0.1.0.2.1`
- `fields(ℓ).E₁ = 2 = s_L`
- `origin(ℓ) = 1.0.1.0.1 = d`
- Forward allocation: no prior links in dom(L) with origin d, so vacuously satisfied
- `(F, G, Θ) ∈ Link` by assumption (L3)

Effect: `L' = {1.0.1.0.1.0.2.1 ↦ (F, G, Θ)}`. Frame: C, E, M, R unchanged.

Post-state verification:
- L14: `dom(C) ∩ dom(L') = ∅` — content addresses have `fields(a).E₁ = 1`, link has `fields(ℓ).E₁ = 2`, and `1 ≠ 2`
- L0: all dom(L') addresses have subspace s_L = 2; all dom(C) addresses have subspace s_C = 1
- L3: `L'(ℓ) = (F, G, Θ)` with `F, G, Θ ∈ Endset`
- S3★, CL-OWN: M unchanged, hold from pre-state

**Step 2: K.μ⁺_L — arrange link.** Place ℓ at V-position `v_ℓ = [2, 1]`.

Precondition verification:
- `d ∈ E_doc`
- `ℓ = 1.0.1.0.1.0.2.1 ∈ dom(L')`
- `origin(ℓ) = 1.0.1.0.1 = d`
- `subspace(v_ℓ) = 2 = s_L`
- `V_{s_L}(d) = ∅`, so `v_ℓ = [s_L, 1] = [2, 1]` with `m_L = 2 ≥ 2` (D-MIN for empty link subspace)
- `#v_ℓ = 2 = m_L` (S8-depth)

Effect: `M'(d) = {[1,1] ↦ 1.0.1.0.1.0.1.1, [1,2] ↦ 1.0.1.0.1.0.1.2, [2,1] ↦ 1.0.1.0.1.0.2.1}`.

Post-state verification:
- S3★: `subspace([1,1]) = 1 = s_C` and `M'(d)([1,1]) = 1.0.1.0.1.0.1.1 ∈ dom(C)`; `subspace([1,2]) = 1 = s_C` and `M'(d)([1,2]) = 1.0.1.0.1.0.1.2 ∈ dom(C)`; `subspace([2,1]) = 2 = s_L` and `M'(d)([2,1]) = 1.0.1.0.1.0.2.1 ∈ dom(L')`
- CL-OWN: the only link-subspace position is `[2,1]` with `origin(M'(d)([2,1])) = origin(1.0.1.0.1.0.2.1) = 1.0.1.0.1 = d`
- D-CTG: `V_1(d) = {[1,1], [1,2]}` contiguous; `V_2(d) = {[2,1]}` singleton, trivially contiguous
- D-MIN: `min(V_1(d)) = [1,1] = [s_C, 1]`; `min(V_2(d)) = [2,1] = [s_L, 1]`
- L14: subspace identifiers 1 and 2 are distinct (SC-NEQ), so dom(C) ∩ dom(L') = ∅

**Step 3: K.μ~ — reorder text, verify link fixity.** Swap the two text positions: `π([1,1]) = [1,2]`, `π([1,2]) = [1,1]`, `π([2,1]) = [2,1]`.

Let `a₁ = 1.0.1.0.1.0.1.1` and `a₂ = 1.0.1.0.1.0.1.2`. Pre-state arrangement: `M'(d) = {[1,1] ↦ a₁, [1,2] ↦ a₂, [2,1] ↦ ℓ}`.

Post-state: `M''(d) = {[1,1] ↦ a₂, [1,2] ↦ a₁, [2,1] ↦ ℓ}`.

Link-subspace fixity: `M''(d)|_{dom_L} = {[2,1] ↦ ℓ} = M'(d)|_{dom_L}` — the link-subspace mapping is unchanged. The fixity argument: π maps `[2,1]` to some position `u`; `M''(d)(u) = M'(d)([2,1]) = ℓ ∈ dom(L')`. By S3★-aux, `subspace(u) ∈ {s_C, s_L}`. If `subspace(u) = s_C = 1`, then S3★ requires `M''(d)(u) ∈ dom(C)`, but `ℓ ∈ dom(L')` and `dom(L') ∩ dom(C) = ∅` (L14) — contradiction. So `subspace(u) = s_L = 2`. Since K.μ⁺ cannot create link-subspace positions, `u` must have existed in the pre-state's link subspace: `u = [2,1]`. Therefore `π([2,1]) = [2,1]` — the link-subspace mapping is fixed by logical necessity, not by fiat.


## Extended Reachable-State Invariants

**ExtendedReachableStateInvariants** — (THEOREM, theorem). Every state reachable from Σ₀ = (C₀, L₀, E₀, M₀, R₀) by a finite sequence of valid composite transitions — composed from the elementary transitions K.α, K.δ, K.λ, K.μ⁺ (amended), K.μ⁺_L, K.μ⁻, K.μ~, and K.ρ — satisfies:

  S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN

This supersedes the ReachableStateInvariants theorem (ASN-0047) by replacing S3 with S3★, P4 with P4★, P3 with P3★, P5 with P5★, adding S3★-aux (subspace exhaustiveness), CL-OWN (link-subspace ownership), L3 (triple endset structure), and the remaining link invariants L0, L1, L1a, L12, L14, and covering the extended transition set including K.λ and K.μ⁺_L.

*Proof.* The proof proceeds by induction on the number of valid composite transitions from Σ₀. The invariant set partitions into two classes: *elementary invariants* preserved by each elementary transition individually, and *composite invariants* that may be violated at intermediate states within a composite but hold at every composite boundary.

**Base.** The extended initial state Σ₀ satisfies all invariants (verified in the Extended System State section — L₀ = ∅ satisfies link invariants vacuously, including L3; S3★ and P4★ reduce to S3 and P4; S3★-aux holds vacuously since M₀(d) = ∅ for all d; D-CTG and D-MIN hold vacuously since V_S(d) = ∅ for every subspace S).

**Class (a): Elementary invariants** — preserved by each elementary transition individually. These are all invariants except P4★ and P7a: S0, S1, S2, S3★, S3★-aux, S8a, S8-fin, S8-depth, S8, D-CTG, D-MIN, P0, P1, P2, P3★, P5★, P6, P8, L0, L1, L1a, L3, L12, L14, CL-OWN.

For K.α (amended): holds M and L in frame; S3★, S3★-aux preserved (M unchanged); content, entity, and provenance invariants preserved. L0 clause 2: `fields(a).E₁ = s_C` by the K.α amendment, so the new content address satisfies `(A a ∈ dom(C') :: fields(a).E₁ = s_C)`. L14: `fields(a).E₁ = s_C` and `s_C ≠ s_L` (SC-NEQ), and L0 clause 1 at the pre-state gives `(A ℓ ∈ dom(L) :: fields(ℓ).E₁ = s_L)`, so `a ∉ dom(L)` and `dom(C') ∩ dom(L') = (dom(C) ∪ {a}) ∩ dom(L) = ∅`. L1, L1a, L3, L12 preserved (L unchanged). For K.δ, K.ρ: hold both M and L in frame; C, L unchanged; S3★, S3★-aux preserved (M unchanged); link invariants preserved since neither L nor dom(C) is modified. For K.μ⁺ (amended): holds L in frame; S3★ preserved (analyses above); S3★-aux preserved (new positions have subspace s_C by amendment); D-CTG, D-MIN preserved by the K.μ⁺ postcondition requirement; S8 follows from S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a via the derivation chain in ASN-0036; link invariants preserved since L is unchanged. For K.μ⁻: holds L in frame; S3★ preserved (restriction of M(d) preserves both clauses); S3★-aux preserved (removal does not alter subspaces of surviving positions); D-CTG, D-MIN preserved by the K.μ⁻ amendment postcondition — by D-SEQ at the input state, V_S(d) is {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}, so valid contractions remove from the maximum end or remove all positions; S8 follows from S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a via the derivation chain in ASN-0036; link invariants preserved since L is unchanged. For K.μ~: holds L in frame; K.μ~ decomposes into K.μ⁻ + K.μ⁺ (ASN-0047). S3★ preserved (decomposition analysis above); S3★-aux preserved (K.μ⁻ removes positions without altering subspaces, K.μ⁺ adds only s_C positions); link-subspace positions are fixed (link-subspace fixity, which requires S3★ and S3★-aux at the output — both now established). D-CTG and D-MIN hold at every intermediate state of the K.μ⁻ + K.μ⁺ decomposition and at the output: link-subspace fixity (r = 0) implies K.μ⁻ removes only content-subspace positions; by D-SEQ at the input, content-subspace positions form {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n}, so K.μ⁻ can remove a suffix leaving {[s_C, 1, ..., 1, k] : 1 ≤ k ≤ n'} for some 0 ≤ n' ≤ n, which satisfies D-CTG and D-MIN; the link subspace at the intermediate state equals the input (r = 0), preserving D-CTG/D-MIN. K.μ⁺ (amended) then rebuilds the content subspace satisfying D-CTG and D-MIN as a postcondition. For any bijection π, a valid decomposition always exists — in particular, n' = 0 (remove all content-subspace positions, then re-add with new mappings) satisfies D-CTG/D-MIN at the intermediate state vacuously for the content subspace. D-SEQ then applies at the output state. π bijects dom(M(d)) onto dom(M'(d)) preserving S8a, S8-depth, S8-fin (K.μ~ preconditions, ASN-0047), and link-subspace fixity forces π to biject dom_C(M(d)) onto dom_C(M'(d)); equal cardinality combined with D-SEQ at both input and output yields V_S(d') = V_S(d) for each content subspace S. S8 follows from S8-fin, S8a, S2, S8-depth, T5, TA5(c), TA7a via the derivation chain in ASN-0036; CL-OWN preserved by link-subspace fixity; link invariants preserved since L is unchanged. For K.λ: holds M, C, E, R in frame; S3★, S3★-aux preserved (M unchanged); link invariants verified (orphan link analysis in the Orphan Links and Coupling Flexibility section); L3 is established for the new entry (K.λ requires `(F, G, Θ) ∈ Link`) and preserved for all existing entries (L12). For K.μ⁺_L: holds C, L, E, R in frame; S3★-aux preserved (new position has subspace s_L); per-subspace arrangement invariants verified in the Link-Subspace Extension section — S8a, S8-fin, S8-depth, D-CTG, D-MIN, D-SEQ, S8 all hold; S3★ satisfied by precondition (`ℓ ∈ dom(L)`); CL-OWN preserved (new mapping satisfies `origin(ℓ) = d` by precondition; existing link-subspace mappings unchanged by frame); L3 preserved (L unchanged).

**Class (b): Composite invariants** — may be violated at intermediate states within a composite, but hold at every valid composite boundary. These are: P4★ and P7a.

P4★ (`Contains_C(Σ) ⊆ R`): An elementary K.μ⁺ alone adds a content-subspace V-position mapping to address `a`, placing `(a, d) ∈ Contains_C(Σ')`. Its frame has `R' = R`, so if `(a, d) ∉ R`, P4★ is violated at the intermediate state. The coupling constraint J1★, evaluated at composite boundaries, guarantees that every content-subspace arrangement extension is paired with provenance recording: for each `(a, d) ∈ Contains_C(Σ') \ Contains_C(Σ)`, the new V-position has `subspace(v) = s_C` (by K.μ⁺ amendment), so J1★ requires `(a, d) ∈ R'`. Therefore `Contains_C(Σ') ⊆ R'` at the composite boundary. K.μ⁺_L does not affect P4★: it adds only link-subspace V-positions, which are excluded from Contains_C by definition. K.μ⁻ can only shrink Contains_C. K.μ~ preserves Contains_C exactly (analysis in the Content-Scoped Containment section). All other transitions hold M in frame.

P7a (`(A a ∈ dom(C) :: (E d :: (a, d) ∈ R))`): An elementary K.α alone adds `a` to `dom(C')` with `R' = R`, so `(a, d) ∉ R` for the newly allocated address — P7a is violated at the intermediate state. At composite boundaries, J0 guarantees every newly allocated content address is placed in some document's arrangement: `(E d, v :: M'(d)(v) = a)`. By the K.μ⁺ amendment, this V-position has `subspace(v) = s_C`. J1★ then requires `(a, d) ∈ R'`. Therefore P7a holds at the composite boundary. No other elementary transition removes addresses from dom(C) (by P0) or entries from R (by P2), so P7a, once established, is not broken by subsequent composites.

Coupling constraints J0, J1★, J1'★ hold for all valid composites by the analysis in the Scoped Coupling Constraints section. ∎


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| SC-NEQ | AX | `s_C ≠ s_L` — subspace identifiers are distinct | introduced |
| K.α amendment | TRANS | Content-subspace restriction (`fields(a).E₁ = s_C`); preserves L0 clause 2 and L14 in the extended state | amended |
| K.μ⁺ amendment | TRANS | Content-subspace restriction (`subspace(v) = s_C`) and D-CTG/D-MIN postcondition; partitions arrangement extension by subspace with K.μ⁺_L | amended |
| K.μ⁻ amendment | TRANS | D-CTG/D-MIN postcondition: M'(d) must satisfy D-CTG and D-MIN for each subspace; constrains contraction to removal from the maximum end or removal of all positions | amended |
| K.λ | TRANS | Elementary transition: L' = L ∪ {ℓ ↦ (F, G, Θ)}, frame C' = C, E' = E, M' = M, R' = R | introduced |
| K.μ⁺_L | TRANS | Elementary transition: link-subspace arrangement extension, M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}, origin(ℓ) = d | introduced |
| S3★ | INV | Subspace-conditional referential integrity: text → dom(C), link → dom(L); supersedes S3 | introduced |
| S3★-aux | INV | Subspace exhaustiveness: `(A d, v : v ∈ dom(M(d)) : subspace(v) = s_C ∨ subspace(v) = s_L)` in every reachable state | introduced |
| Contains_C(Σ) | DEF | `{(a, d) : d ∈ E_doc ∧ (E v : v ∈ dom(M(d)) ∧ subspace(v) = s_C : M(d)(v) = a)}` — content-scoped containment | introduced |
| P4★ | INV | `Contains_C(Σ) ⊆ R` — provenance bounds scoped to content subspace; supersedes P4 | introduced |
| J1★ | AX | Content-subspace scoping of J1: provenance recording only for subspace(v) = s_C | introduced |
| J1'★ | AX | Content-subspace scoping of J1': provenance entries only from subspace(v) = s_C | introduced |
| P3★ | INV | No component other than M — specifically C, L, E, R — admits contraction or reordering; supersedes P3 | introduced |
| P5★ | INV | dom(C), dom(L), E, R can only grow; only M can lose information; supersedes P5 | introduced |
| CL-OWN | INV | LinkSubspaceOwnership: `(A d, v : v ∈ dom(M(d)) ∧ subspace(v) = s_L : origin(M(d)(v)) = d)` — every document's link subspace contains only its own links | introduced |
| ExtendedReachableStateInvariants | THEOREM | Every reachable state satisfies S0 ∧ S1 ∧ S2 ∧ S3★ ∧ S3★-aux ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG ∧ D-MIN ∧ P0–P2 ∧ P3★ ∧ P4★ ∧ P5★ ∧ P6–P8 ∧ L0 ∧ L1 ∧ L1a ∧ L3 ∧ L12 ∧ L14 ∧ CL-OWN; supersedes ASN-0047 ReachableStateInvariants | introduced |


## Open Questions

What invariants must the link subspace satisfy beyond those inherited from D-CTG, D-MIN, and S8-depth — are there link-specific ordering constraints, capacity bounds, or structural properties that D-SEQ does not capture?

Must the system guarantee that a fresh link address is always available within a document's link subspace, or can link allocation fail due to address space exhaustion?

What must the system guarantee when concurrent operations target the same home document — must link address allocation be serialized, or can concurrent allocations produce distinct addresses without coordination?

What invariants must link withdrawal maintain — must withdrawn links remain arranged, or does withdrawal remove them from M(d)? The transition framework constrains link-subspace contractions to suffix truncations (by D-CTG and link-subspace fixity under K.μ~); Nelson's design suggests an inactive-status mechanism rather than arrangement removal. The precise withdrawal mechanism is an open question.
