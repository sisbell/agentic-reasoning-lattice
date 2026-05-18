# Review of ASN-0047

## REVISE

### Issue 1: P4★/P4a/P7a misclassified in per-state invariant list

**ASN-0047, Extended reachable-state invariants**: "Every state reachable from Σ₀ by a finite sequence of valid composite transitions satisfies: S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ S7c ∧ S7d ∧ S8a ∧ S8-fin ∧ S8-depth ∧ S8★ ∧ D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ ∧ P4★ ∧ P4a ∧ P6 ∧ P7 ∧ P7a ∧ P8 ∧ NodeLineage ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ L-fin ∧ CL-OWN ∧ CL-UNIQ"

**Problem**: The proof's Class (a)/Class (b) partition correctly identifies P4★, P4a, and P7a as *composite-boundary* invariants — they may transiently fail at intermediate states (e.g., after K.α before its companion K.ρ in the same composite). But the theorem statement lists them alongside truly per-state invariants without distinction. A reader must consult the proof structure to learn that "reachable state" here means "composite-boundary state, not arbitrary intermediate state."

**Required**: Partition the invariant list explicitly. For example, separate clauses for "per-state invariants" (holding at every intermediate state) and "per-composite invariants" (holding at composite boundaries). Or annotate P4★, P4a, P7a with a marker (e.g., "(composite-boundary)") to make the temporal scope visible at the statement level.

### Issue 2: Interior replacement example overstates intermediate-state requirements

**ASN-0047, Worked example: interior content replacement**: "*Intermediate-state verification at M_int.* The decomposition routes the composite through M_int, which must itself satisfy the per-state invariant set including P4★."

**Problem**: This contradicts notation point (c) immediately above the worked example: "intermediate states may transiently violate composite invariants." P4★ is a composite invariant per the proof's Class (b). M_int *happens* to satisfy P4★ (because K.μ⁻ shrinks Contains_C), but this is incidental to K.μ⁻'s contraction behavior, not a requirement. The framing "must itself satisfy the per-state invariant set including P4★" misleads on what intermediate states are obligated to satisfy.

**Required**: Distinguish in the verification text between elementary per-state invariants (D-CTG★, D-MIN★, S2, S3★, etc., which *do* hold at M_int by elementary preservation) and composite invariants (P4★, P4a, P7a, which need not hold at intermediates but happen to here). State why P4★ holds at M_int as a consequence of K.μ⁻'s monotonicity, not as a precondition.

### Issue 3: Replacement composite description glosses K.α and K.ρ

**ASN-0047, Elementary transitions**: "**Replacement at the maximum position of a subspace.** When the replaced V-position is `max(V_S(d))` for its subspace S, K.μ⁻ removes that single position (a 1-element suffix of V_S(d)) and K.μ⁺ then re-adds it with the new value. Replacement is a single-position K.μ⁻ + K.μ⁺ pair."

**Problem**: When the "new value" is freshly allocated content (the typical case for an editing operation), the full composite is K.α + K.μ⁻ + K.μ⁺ + K.ρ — four elementary steps, not two. The K.α allocates the new I-address, the K.μ⁻ removes the old mapping, the K.μ⁺ places the new mapping, and the K.ρ records provenance (required by J1★). The interior worked example correctly shows K.μ⁻ + K.α + K.μ⁺ + K.ρ, but the elementary-transitions text describes only the M-touching pair. The same gloss appears for "Replacement at an interior position of a subspace."

**Required**: State that replacement decomposes as K.μ⁻ + K.μ⁺ on M, with co-occurring K.α and K.ρ when the replacement value is fresh content. The transclusion sub-case (replacing with an existing I-address) is the only case where K.μ⁻ + K.μ⁺ alone suffices.

### Issue 4: K.μ~ link-subspace fixity depends on pre-state CL-UNIQ — dependency chain implicit

**ASN-0047, Decomposition of K.μ~**: "(4) *Identity via CL-UNIQ at the pre-state.* From (3), `M'(d)|_{dom_L} = M(d)|_{dom_L}`, so for the V-position `v ∈ dom_L(M(d))` under consideration, `M(d)(v) = ℓ`. ... CL-UNIQ at Σ — the inductive hypothesis, link-subspace injectivity of `M(d)|_{dom_L}` — forces `π(v) = v`."

**Problem**: The fixity proof discharges CL-UNIQ preservation under K.μ~ by appealing to CL-UNIQ at the pre-state — which is the inductive hypothesis of ExtendedReachableStateInvariants. But the ExtendedReachableStateInvariants proof of K.μ~ preserving CL-UNIQ says only "link invariants preserved" without spelling out that CL-UNIQ preservation reduces to (a) fixity (M'(d)|_dom_L = M(d)|_dom_L as functions, from Steps 1–3 alone) and (b) pre-state injectivity carrying through. The dependency chain "pre-state CL-UNIQ → fixity Step 4 → post-state CL-UNIQ" is correct but invisible to a reader checking the inductive step.

**Required**: In the ExtendedReachableStateInvariants proof's K.μ~ paragraph, make CL-UNIQ preservation explicit: "CL-UNIQ preserved because M'(d)|_{dom_L} = M(d)|_{dom_L} as functions (link-subspace fixity Steps 1–3), so post-state injectivity equals pre-state injectivity, which is CL-UNIQ(Σ) by the inductive hypothesis."

### Issue 5: K.δ case (ii) k=2 activation discharge is dense

**ASN-0047, Freshness-discharge summary**: "*k = 2 (descent producing the first child under a node or account):* this is the activation case. The K.δ event itself is interpreted as a T10a T2 spawn step on the parent allocator (the parent node's account sub-allocator, or the parent account's document sub-allocator), with the operand `t` as spawnPt."

**Problem**: For the first account allocation under a freshly baptized node n, the "parent allocator" is the node's account sub-allocator, which is being activated by this K.δ event. T10a T2 requires the new allocator's *parent* allocator to be in Act(s) at the spawn — but the node's account sub-allocator's parent is... what? The reader has to construct the answer. The text says "operand `t` as spawnPt" but doesn't clarify which allocator in the tree is doing the spawning at the first activation. This contrasts with the SubAllocatorAxiom case for A_C(d)/A_L(d) (content/link sub-allocators), where the axiomatic activation is made explicit.

**Required**: Either (a) clarify whether K.δ case (ii) k=2 first activations are also covered by an axiomatic activation clause (analogous to SubAllocatorAxiom), or (b) walk through the T10a T2 chain for the first activation case, naming the parent allocator and showing how its tracked domain is established. If the answer is that node baptism implicitly activates node-rooted allocator chains, state this.

### Issue 6: L3 narrowing from foundation arity ≥3 to exactly 3 — local-extension inconsistency

**ASN-0047, Link store and extended system state**: "**Definition (Link).** A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset`..."

**Problem**: ASN-0043's Link definition admits `N ≥ 3` arity; this ASN narrows it to exactly 3. The narrative claim "This narrows ASN-0043's `N ≥ 3` arity to fixed three" is fine, but the implication is that ASN-0043's foundation Link values with N > 3 are now *prohibited* — yet ASN-0043's L3 invariant remains a foundation property. If a system in foundation-conforming state has a link with N = 4, can such a state transition into this ASN's extended-state regime? The ASN doesn't address this. In practice K.λ only creates triples, so dom(L) in any state reachable from Σ₀ contains only triples — but the foundation L3 as stated (N ≥ 3) is strictly weaker than this ASN's L3 (N = 3).

**Required**: Clarify whether (a) this ASN's L3 is a local strengthening that holds on states reachable from Σ₀ via this ASN's transitions, with no claim about foundation-conforming states reached otherwise; or (b) foundation L3 should be re-stated as N = 3 with this ASN as the strengthening site. Currently the Properties Introduced table says "Strengthens ASN-0043's ... to exactly three" which suggests (a), but the relationship to ASN-0043's L3 axiom needs explicit framing.

## OUT_OF_SCOPE

No items — the ASN appropriately scopes itself and uses the Open Questions section to defer downstream concerns (named user operations, authority model, concurrency, etc.). The worked examples illustrate the elementary transitions concretely without venturing into implementation specifics.

VERDICT: REVISE
