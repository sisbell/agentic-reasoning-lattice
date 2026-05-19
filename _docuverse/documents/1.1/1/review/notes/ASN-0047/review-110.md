# Review of ASN-0047

## REVISE

### Issue 1: K.α reinvents ASN-0093's allocation primitive
**ASN-0047, Elementary transitions, K.α definition**: "**K.α (Content allocation).** A fresh I-address is bound to a value in the content store: `C' = C ∪ {a ↦ v}` where `a ∉ dom(C)`"
**Problem**: ASN-0093 (foundation) defines K.α (ContentAllocation) with substantively equivalent precondition (d ∈ dom(M), a ∉ dom(C) ∪ dom(L), zeros(a) = 3, E(a)₁ = s_C, #E(a) ≥ 2, origin(a) = d, first-/subsequent-emission split) and effect. ASN-0047 restates it locally rather than referencing the foundation.
**Required**: Reference ASN-0093's K.α; retain only the K.α amendment if it adds genuinely new content (the content-subspace restriction is already in ASN-0093).

### Issue 2: K.λ reinvents ASN-0093's allocation primitive
**ASN-0047, Link allocation, K.λ definition**: "**K.λ (LinkAllocation).** Creates a new entry in the link store. ... ℓ is produced by d's link sub-allocator. The first-emission and subsequent-emission cases have structurally distinct discharge routes..."
**Problem**: ASN-0093 (foundation) defines K.λ with the same precondition structure (first/subsequent emission split, SubAllocatorAxiom.FirstEmission discharge, T10a GlobalUniqueness for subsequent emissions). ASN-0047 reintroduces K.λ without citing ASN-0093.
**Required**: Reference ASN-0093's K.λ.

### Issue 3: SubAllocatorAxiom reinvents ASN-0093's axiom verbatim
**ASN-0047, Allocator hierarchy under documents**: "**SubAllocatorAxiom (Axiom, ContentLinkSubAllocatorExistence).** ... The axiom comprises five sub-clauses: SubAllocatorAxiom.Subspace, SubAllocatorAxiom.FirstEmission, SubAllocatorAxiom.Namespace, SubAllocatorAxiom.T10aConformance, SubAllocatorAxiom.Disjointness."
**Problem**: ASN-0093 (foundation) states the same axiom with the same five named sub-clauses. ASN-0047's version is a near-verbatim restatement.
**Required**: Adopt ASN-0093's SubAllocatorAxiom directly; remove the local restatement.

### Issue 4: Anchor and sub-allocator notation reinvents ASN-0093
**ASN-0047, Allocator hierarchy under documents**: "Two element-field bases sit immediately under d: `b_C(d) := [d.0.s_C]` ... `b_L(d) := [d.0.s_L]`. ... Three T10a sub-allocators are associated with d: `A_C(d)` ... `A_L(d)` ... `A_v(d)`."
**Problem**: ASN-0093 (foundation) defines b_C(d), b_L(d), A_C(d), A_L(d) with the same meanings. ASN-0047 redefines them.
**Required**: Reference ASN-0093's definitions of these symbols.

### Issue 5: L0's C-clause is not new in current foundation
**ASN-0047, Link store and extended system state**: "The L-clause is from ASN-0043; the C-clause is introduced here, supplied by the K.α amendment below."
**Problem**: ASN-0093 (foundation) states L0 with both clauses. ASN-0047 describes the C-clause as introduced locally, but it exists in foundation.
**Required**: Reference ASN-0093's L0 in its full form; remove the "introduced here" framing.

### Issue 6: K.α and K.ρ frames in extended state omit explicit `L' = L`
**ASN-0047, Elementary transitions**: K.α frame: "E' = E; (A d :: M'(d) = M(d)); R' = R." K.ρ frame: "C' = C; E' = E; (A d :: M'(d) = M(d))."
**Problem**: Both transitions predate the link store. The K.μ⁺ and K.μ⁻ amendments add "*Frame (extended state)*" paragraphs that explicitly restate the full frame including `L' = L`. The K.α amendment paragraph adds a content-subspace restriction but does not restate the frame; K.ρ has no amendment paragraph at all. The verification matrix discharges L invariants under K.α and K.ρ as "frame", but the operation definitions never make `L' = L` explicit for these two transitions. This is inconsistent with how K.μ⁺/K.μ⁻ are handled.
**Required**: Add a *Frame (extended state)* paragraph to the K.α amendment and add a K.ρ amendment paragraph, each restating the full extended-state frame including `L' = L`. Match the explicit treatment of K.μ⁺/K.μ⁻ amendments.

### Issue 7: J0 quantifies over E'_doc with no explicit guarantee that K.α's content-subspace amendment forces s_C placement
**ASN-0047, Coupling and isolation, P7a discharge**: The proof of P7a (composite-boundary) says "For `a ∈ dom(C') \ dom(C)`, J0 supplies `d` with `a ∈ ran(M'(d))` at a content-subspace V-position (forced by the K.μ⁺ amendment, with K.μ⁺ following K.α in the elementary sequence by referential integrity); J1★ then supplies `(a, d) ∈ R'`."
**Problem**: J0's statement is "(A Σ →* Σ', a : a ∈ dom(C') \ dom(C) : (E d, v : d ∈ E'_doc ∧ v ∈ dom(M'(d)) : M'(d)(v) = a))" — no clause forces `subspace(v) = s_C`. The argument that "J0 supplies content-subspace placement" goes via S3★ + L14: if `subspace(v) = s_L` then `M'(d)(v) ∈ dom(L)`, but `a ∈ dom(C) \ dom(L)` by L14, so `subspace(v) = s_C`. This derivation is correct but is left implicit in the P7a proof.
**Required**: State explicitly in J0's analysis (or in the P7a discharge) that J0 + S3★ + L14 together force the V-position to be content-subspace; do not present it as "forced by the K.μ⁺ amendment" alone.

### Issue 8: The Cross-document disjointness lemma's Case A length verification has an unverified depth assumption
**ASN-0047, Allocator hierarchy under documents, Cross-document disjointness chain lemma, Case A**: "We verify the divergence index `#e₁ + 1` sits inside both prefixes: each `pᵢ = [eᵢ.0.s]` extends `eᵢ` by exactly two components (one zero separator at position `#eᵢ + 1`, one component `s` at position `#eᵢ + 2`), so `#p₁ = #e₁ + 2` and `#p₂ = #e₂ + 2`. From `#e₁ < #e₂` we obtain `#e₁ + 2 ≤ #e₂ + 2`, i.e., `#p₁ ≤ #p₂`; hence `min(#p₁, #p₂) = #p₁ = #e₁ + 2`, and `#e₁ + 1 < #e₁ + 2 = #p₁ ≤ #p₂` places `#e₁ + 1` strictly inside `#p₁` and a fortiori inside `#p₂`."
**Problem**: The lemma is stated for "any two distinct entities `e₁, e₂` ... of the same allocator-hierarchy level". The argument that `e₂[#e₁+1] ≠ 0` relies on zeros(e₂) = zeros(e₁) = z and on e₂'s first #e₁ positions reproducing e₁'s zeros exactly. This is sound, but the prose elides why "Since e₂'s first #e₁ positions reproduce e₁ exactly" — that step depends on `e₁ ≺ e₂` (proper-prefix), which holds in Case A by hypothesis. Fine. However, `#e₁ < #e₂` in Case A is unstated; the WLOG `e₁ ≺ e₂` gives `#e₁ ≤ #e₂` by Prefix, and `e₁ ≠ e₂` (distinct entities) combined with prefix-equal-length-implies-equal (T3) forces `#e₁ < #e₂`. This chain is not made explicit.
**Required**: Add the one-line derivation `e₁ ≺ e₂ ⟹ #e₁ < #e₂` (via Prefix and T3) at the start of Case A so the length comparison is grounded.

### Issue 9: K.μ~ admissibility clause (iii) creates a derivation-vs-precondition ambiguity for the empty/singleton case
**ASN-0047, Decomposition of K.μ~**: "Admissibility clause (iii) requires `π ≠ id`. Combined with link-subspace fixity (which forces `π|_{dom_L} = id`) and subspace preservation (which forces `π` to map `dom_C(M(d))` bijectively onto itself, with cardinality `|dom_C(M(d))|`), `π ≠ id` requires a non-trivial permutation of `dom_C(M(d))` to exist."
**Problem**: Link-subspace fixity (Step 4 of the fixity proof) uses CL-UNIQ at the pre-state — but its Steps 1–3 invoke subspace preservation. The K.μ~ definition presents subspace preservation as a *derived* consequence of S3★ at both endpoints. So the chain is: K.μ~ admissibility includes (ii) "the induced post-state M'(d) would satisfy ... S3★" → subspace preservation is derived → fixity Steps 1–3 derive functional identity on dom_L → Step 4 derives pointwise identity using CL-UNIQ. The text does walk through this, but the matrix entry for CL-UNIQ under K.μ~ ("functional identity on dom_L (Steps 1–3 of K.μ~ link-fixity proof)") and the Decomposition's "necessary-and-sufficient existence condition is `|dom_C(M(d))| ≥ 2`" both reference fixity outputs without naming the chain. A reader following the matrix straight to the Decomposition has to reconstruct the dependency order.
**Required**: At the head of the K.μ~ Decomposition section, state the dependency chain explicitly: "S3★(Σ') from K.μ~ admissibility (ii) → subspace preservation derived → link-subspace fixity Steps 1–3 (functional identity) → admissibility (iii) excludes identity → existence condition |dom_C(M(d))| ≥ 2."

## OUT_OF_SCOPE

### Topic 1: Operational layer (INSERT, DELETE, COPY, REARRANGE, MAKELINK, CREATENEWVERSION)
**Why out of scope**: ASN-0047 specifies elementary transitions and named composites; the operational vocabulary that composes them is correctly deferred per the explicit Scope block.

### Topic 2: Concurrency and multi-user semantics
**Why out of scope**: SequentialTransitionAxiom commits to sequential atomic transitions. Concurrent execution discipline is a future topic.

### Topic 3: Tombstoning mechanism for link withdrawal
**Why out of scope**: Open Question identifies this. The K.μ⁻ amendment forces suffix-removal under D-CTG★, so interior link withdrawal would require a separate mechanism — appropriately deferred.

### Topic 4: Link inheritance under forking
**Why out of scope**: J4's Fork composite copies only content-subspace mappings; link-subspace inheritance is identified as a future-ASN topic.

### Topic 5: Account-level depth-1 extension
**Why out of scope**: Open Question explicitly identifies this. The current K.δ k = 1 case restricts to documents; extending to accounts is a future design choice.

### Topic 6: External node-allocation protocol details
**Why out of scope**: NodeUniqueAllocation and NodeRegistryBootstrap abstract over the protocol; the registry mechanism is correctly treated as external.

VERDICT: REVISE
