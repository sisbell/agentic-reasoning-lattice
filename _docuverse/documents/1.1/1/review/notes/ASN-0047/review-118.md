# Review of ASN-0047

## REVISE

### Issue 1: K.δ case (ii) k=2 sub-case A induction omits sub-case C as a base

**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation", sub-case A inductive structure**: "*Induction on K.δ case (ii) k = 2 events activating account sub-allocators.* Base case: the first K.δ case (ii) k = 2 event with operand `t = node` (sub-case B below)..." and "...or directly the sub-case B base case at the lineage's root (`parent(t) ∈ E_node`...)."

**Problem**: The ASN defines three sub-cases (A: t is account, B: t is non-bootstrap node, C: t = n₀ bootstrap). Sub-cases B AND C both activate account sub-allocators (A_account(node)) that can serve as the spawnPt source for subsequent sub-case A events. When the first account in the docuverse is created — K.δ case (ii) k=2 with t = n₀, which is sub-case C — the spawned A_account(n₀) becomes the state-tracked source for the next sub-case A event (creating the first document under this first account). The induction's stated base "sub-case B" excludes this concrete lineage. The parenthetical `parent(t) ∈ E_node` covers both bootstrap and non-bootstrap nodes, but the named base "sub-case B" is restricted to non-bootstrap nodes only.

**Required**: The base case description and inductive step prose must include both sub-case B (non-bootstrap node ancestor) and sub-case C (n₀ bootstrap ancestor) as valid bases. The cleanest phrasing: "directly a sub-case B or sub-case C base case at the lineage's root (`parent(t) ∈ E_node`, and the K.δ case (ii) k = 2 event that minted t fired with `A_account(parent(t))` as the spawn allocator — via NodeUniqueAllocation clause (c) when parent(t) is non-bootstrap, or via NodeRegistryBootstrap when parent(t) = n₀)."

### Issue 2: P7a proof uses dom(L) where dom(L') is required

**ASN-0047, "Extended reachable-state invariants", Class (b) P7a derivation**: "Suppose for contradiction `subspace(v) = s_L`. Then by S3★'s link clause, `M'(d)(v) ∈ dom(L)`, i.e., `a ∈ dom(L)`. But `a ∈ dom(C')` (J0's defining membership) and L14 gives `dom(C') ∩ dom(L') = ∅`; with `dom(L) ⊆ dom(L')` (P3), `a ∈ dom(L) ⊆ dom(L')` contradicts `a ∈ dom(C')`."

**Problem**: The argument invokes S3★ at v ∈ dom(M'(d)), which is in the post-state Σ'. S3★ applied at the post-state gives `M'(d)(v) ∈ dom(L')`, not `dom(L)`. The detour "with `dom(L) ⊆ dom(L')` (P3), `a ∈ dom(L) ⊆ dom(L')`" is unnecessary and conflates the pre-state and post-state link domains. The natural form applies S3★ at Σ' to get dom(L') directly, then closes via L14 at Σ': `a ∈ dom(C') ∩ dom(L') = ∅`. As written, the proof works only because dom(L) ⊆ dom(L'), but it gives the impression that S3★ is being read at the pre-state, which would be incorrect (v ∉ dom(M(d)) in general).

**Required**: Restate as "by S3★ at Σ', `M'(d)(v) ∈ dom(L')`, i.e., `a ∈ dom(L')`. But `a ∈ dom(C')` (J0's defining membership) and L14 at Σ' gives `dom(C') ∩ dom(L') = ∅`, contradiction."

### Issue 3: S7b matrix entry misattributes the zeros(a) = 3 source

**ASN-0047, "Class (a) Verification matrix", S7b row K.α column**: "K.α's `E(a)₁ = s_C` precondition (per ASN-0093) + content sub-allocator chain ⟹ zeros(a)=3"

**Problem**: ASN-0093's foundation K.α has `zeros(a) = 3 ∧ E(a)₁ = s_C` as part of its precondition list directly (the ASN-0047 body restates this verbatim under K.α's elementary specification: "zeros(a) = 3 ∧ E(a)₁ = s_C (element-level, content subspace)"). The matrix entry derives `zeros(a) = 3` from the conjunction of `E(a)₁ = s_C` and the content sub-allocator chain, but `zeros(a) = 3` is supplied independently as a precondition; no derivation is needed. The other precondition (`E(a)₁ = s_C`) is also independent.

**Required**: Change the matrix entry to "K.α's `zeros(a) = 3` precondition (per ASN-0093)". Or for consistency with downstream attribution, state both preconditions side by side without an implication arrow.

### Issue 4: P4a Class (b) matrix entry has muddled temporal language

**ASN-0047, "Composite-boundary verification matrix" for P4a row**: "After K.ρ before its companion K.μ⁺: vacuous (J1'★ rules out spurious K.ρ); within a composite that completes both, never violated"

**Problem**: The phrasing "After K.ρ before its companion K.μ⁺" presupposes a specific elementary ordering (K.ρ first, K.μ⁺ second), but the ASN's body explicitly notes that K.ρ must follow K.α (since K.ρ requires `a ∈ dom(C)`), and within a content-replacement composite K.ρ is the trailing step (see the worked example: K.μ⁻ → K.α → K.μ⁺ → K.ρ). The intermediate state at concern is "after K.μ⁺ before K.ρ" (where M' has the new content-subspace mapping but R does not yet have the provenance entry) — the *opposite* temporal order from what the matrix states. The "vacuous (J1'★ rules out spurious K.ρ)" phrasing is also imprecise: J1'★ at composite boundaries forbids stand-alone K.ρ events with no matching content-subspace range extension; "vacuous" doesn't describe this correctly. The composite-boundary framework already handles this — Class (b) properties are verified only at boundaries, not at intermediate states — so the temporal-direction muddle is purely a presentation issue but should be cleaned up.

**Required**: Either (a) remove the "After K.ρ before K.μ⁺" remark entirely (the boundary-only framework makes it superfluous), or (b) rephrase to match the actual elementary ordering: "After K.μ⁺ before K.ρ: composite-boundary discharge by J1'★ — P4a is asserted only at Σ' where K.ρ has fired; intermediate states may transiently lack the provenance entry."

### Issue 5: K.μ⁻ admissibility derivation circulates through D-SEQ★ at the post-state

**ASN-0047, "K.μ⁻ admissible contraction shape" derivation**: "If `V_S(d') = ∅`, the conclusion holds with `n'_S = 0`. Otherwise D-SEQ★ applied at the post-state gives `V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}` for some `n'_S ≥ 1` directly (D-SEQ★ holds at Σ' as a per-state invariant of ExtendedReachableStateInvariants); `V_S(d') ⊆ V_S(d)` (from K.μ⁻'s contraction effect) forces `n'_S ≤ n_S`."

**Problem**: This step invokes D-SEQ★ at the post-state Σ' as already-established, but K.μ⁻ is exactly the transition whose preservation of D-SEQ★ we are checking in the verification matrix row "D-SEQ★ | K.μ⁻ | derived". The chain is: D-SEQ★ at Σ' is "derived from D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a at Σ'" — those four are K.μ⁻ preconditions/restriction-preserved, so the derivation chain is sound, but the prose presentation gives the impression of circular dependence. A reviewer cannot easily verify that the chain is non-circular without explicitly tracing: K.μ⁻'s preconditions establish D-CTG★ and D-MIN★ at Σ'; restriction preserves S8-depth, S8-fin, S8a at Σ'; the D-SEQ★ definitional derivation then fires at Σ' using only those Class-(a)-elementary-preserved invariants; the suffix-shape consequence follows.

**Required**: Either (a) restate the derivation to explicitly invoke D-CTG★, D-MIN★, S8-depth, S8-fin, S8a at Σ' directly (rather than D-SEQ★ at Σ'), making the dependence chain visible; or (b) add a one-sentence note clarifying that "D-SEQ★ at Σ' here is the local D-SEQ★ derivation at the K.μ⁻ post-state, fired from K.μ⁻'s precondition-discharged D-CTG★ and D-MIN★, not from a prior inductive D-SEQ★ assumption" — making the non-circularity explicit.

## OUT_OF_SCOPE

None — the ASN's scope statement excludes named operations, authorization, atomicity, POOM, enfilades, span indexing, error model, sessions, and replication, all of which the ASN correctly does not address. The Open Questions at the end already explicitly enumerate appropriate forward topics (forking arrangement invariants, transitive transclusion provenance, version lineage vs. arrangement transitions, link permanence under content-link interaction, link subspace specifics, concurrent home-document operations, account-level depth-1 extension, link withdrawal mechanism, node-allocation registry abstraction).

VERDICT: REVISE
