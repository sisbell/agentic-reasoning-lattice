# Review of ASN-0051

## REVISE

### Issue 1: SV0 inconsistently labeled as both an SV claim and not a theorem

**ASN-0051, "Endset Projection" section, SV0**: The author writes "SV0 (NoStaleResolutionState). *Schema observation, not derivation.* SV0 records a property of the state-space Σ and the transition system K that is read off directly from the foundation definitions... we do not equip it with a proof because none is required."

**Problem**: SV0 receives an SV label placing it on the same footing as SV2–SV13 (which are proved properties about state transitions), yet the author explicitly disclaims that it is a theorem. The substantive content splits into (a) a trivial definitional fact (locate depends only on its arguments) and (b) an architectural inspection of ASN-0047's schema (no V-position field exists). Mixing these under one SV label blurs the line between proved survivability and architectural assumption.

**Required**: Either prove SV0 as a derivation with explicit premises drawn from ASN-0047's transition definitions, or move it out of the SV numbering into a clearly-labeled "Schema Observations" or "Architectural Invariants" category. The current treatment is honest but inconsistent.

### Issue 2: Same-origin coverage growth has no formal claim or explicit exclusion

**ASN-0051, "Content Allocation and Coverage Stability" section**: The author identifies two mechanisms (sequential overshoot, child-depth entry) by which same-origin allocations can enter existing endset coverage, then writes: "*Scope.* We make no formal SV claim about same-origin coverage growth in this ASN. The analysis below is descriptive..."

**Problem**: SV6 excludes cross-origin growth, but same-origin growth is left in limbo — neither claimed nor excluded. The counterexample with child-depth entry shows that even within Nelson's "strap between bytes" at the byte level, child-depth allocation can enter an existing span. This directly affects SV13's synthesis (item f) which cites only SV6. A link holder reading SV13 cannot answer "can my endset's coverage grow under same-origin allocation?" — the answer is "yes, by mechanisms not captured in any SV claim."

**Required**: Either state an SV claim characterizing same-origin coverage growth conditions (possibly bounded under the allocator regime), or include same-origin growth explicitly in the open questions and add a scope sentence to SV13 acknowledging this gap in the "complete guarantee."

### Issue 3: SV7 transclusion corollary conflates fixed-A with document-derived A

**ASN-0051, "Link Discovery" section, after SV7**: The corollary states "When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no coupling step beyond K.μ⁺ itself: by SV7 instantiated to K.μ⁺, discover_s(A) is unchanged across the transition for every A..."

**Problem**: SV7's statement is `discover_s(A) in Σ' = discover_s(A) in Σ` for **fixed A**. The substantive transclusion claim concerns a **document-derived** query set: in Σ, A_Σ = {M(d₂)(v') : v' ∈ V ∩ dom(M(d₂))}; in Σ', A_{Σ'} additionally contains the new mapping's I-address a. So discover_s(A_Σ') ⊇ discover_s(A_Σ) strictly when V includes the new v. The corollary collapses these two distinct sets and asserts an invariance that holds only for fixed A.

**Required**: Either restate the corollary in terms of fixed A (sacrificing the transclusion narrative), or explicitly distinguish discover_s(A_Σ) from discover_s(A_{Σ'}) and show how A grows by exactly the new I-address. The current wording suggests the discoverable set is preserved, when in fact the corollary's punch is that the discoverable set grows by exactly what the new arrangement adds.

### Issue 4: SV13(e) "dual character" framing for K.λ is unclear

**ASN-0051, SV13(e)**: "K.λ (LinkAllocation) has a dual character. It preserves M in its frame... so locate(e, d) is unchanged for every endset e that existed prior to the transition. But K.λ also adds a new entry to dom(L) — extending the link store by exactly one new link with endsets (F_new, G_new, Θ_new) — and the locate sets of those *new* endsets come into existence for the first time..."

**Problem**: The "dual character" framing obscures a simple structural fact. K.λ has frame condition `(A d :: M'(d) = M(d))`, so M is entirely unchanged. For any pre-existing endset, locate is trivially unchanged. The new link introduces *new endsets* — their locate sets are computed fresh against the unchanged M. There is no "duality" here; the new endsets simply did not exist before, so saying their locate is "unchanged" or "computed for the first time" is a vacuous distinction.

**Required**: Replace the "dual character" framing with a direct statement: K.λ holds M in frame, so locate is unchanged for every pre-existing endset; new endsets introduced by the new link inherit locate values computed against the prevailing M.

### Issue 5: Bilateral vitality vacuous-case discussion is excessive

**ASN-0051, "Endset Projection" section, after "Definition — Endset Vitality"**: The author spends three lengthy paragraphs on degenerate satisfaction of the disjunction (F = ∅ ∨ π(F, d) ≠ ∅), covering the both-empty case, asymmetric-empty cases, and empty-coverage cases.

**Problem**: The disjunction structure makes the degenerate cases self-evident — when F = ∅, coverage(F) = ∅, hence π(F, d) = ∅ ∩ ran(M(d)) = ∅, and the disjunction is satisfied trivially by the left branch. Three paragraphs of prose unpack what one sentence makes obvious. The discussion partially obscures the substantive case (both endsets non-empty).

**Required**: Compress to a single short paragraph noting that empty endsets satisfy the disjunction degenerately and the substantive content of bilateral vitality emerges only when both content endsets are non-empty.

### Issue 6: Broader-level spans (k ≤ p₃) survivability not addressed

**ASN-0051, "Note on scope" within SV6**: The author observes that when k ≤ p₃, "the span machinery, applied with an action-point inside the document-prefix region rather than within the element field, yields the cross-document, cross-account, or cross-node reach that the design contemplates."

**Problem**: Spans with k ≤ p₃ are explicitly admitted by the design and used for hierarchical references (links to documents, accounts, nodes). SV6 excludes them. But none of the other SV claims (SV2–SV5, SV11) specifically address how survivability works for such spans. A broader-level span's coverage *grows* over time as new documents/accounts are allocated within its reach — and the survivability story for such spans is genuinely different from element-level spans. The ASN treats broader spans as an existence note but doesn't trace survivability properties for them.

**Required**: Either add an SV claim or scope note characterizing broader-level span survivability separately, or add this to the open questions explicitly.

### Issue 7: Decomposition term vs maximal fragment count statements

**ASN-0051, after SV11**: The author writes "The number of decomposition terms is exactly m · p (possibly with empty terms)" and "Across p blocks, the number of maximal fragments is bounded by m · p — the same upper bound as for decomposition terms..."

**Problem**: The two upper bounds m·p have different meanings. Decomposition terms: exactly m·p, by construction (one per span-block pair). Maximal fragments: at most m·p, after coalescence. The worked example shows 4 decomposition terms collapsing to 2 maximal fragments — so the bounds are not tight in the same way. The phrase "the same upper bound" understates the relationship: decomposition terms have a definite count, maximal fragments have a count bounded above by it.

**Required**: Clarify that decomposition terms are exactly m·p (with possible empty terms), while maximal fragments may number fewer than the non-empty term count after coalescence within blocks. Distinguish "exactly m·p decomposition terms" from "at most m·p maximal fragments."

### Issue 8: Worked example - K.μ~ + K.μ⁻ composite description awkward

**ASN-0051, "After removing a₃" subsection**: "The author notes K.μ⁻ alone cannot remove an interior position - needs composite K.μ~ + K.μ⁻. After this: M'(d) = {v₁ ↦ a₁, v₂ ↦ a₂, v₃ ↦ a₄, v₄ ↦ a₅}."

**Problem**: The intermediate step (M after K.μ~ but before K.μ⁻) is described in passing but the resulting M' jumps directly to the final state. A reader has to mentally reconstruct that K.μ~ first moves a₃ to v₅ (yielding {v₁↦a₁, v₂↦a₂, v₃↦a₄, v₄↦a₅, v₅↦a₃}) and K.μ⁻ then removes v₅. The example would benefit from showing the intermediate state explicitly to demonstrate D-SEQ compliance.

**Required**: Either show the intermediate state explicitly, or simplify the example by removing the maximum end (e.g., remove a₅ instead of a₃) so K.μ⁻ alone suffices.

## OUT_OF_SCOPE

### Topic 1: Detailed allocator discipline for same-origin coverage growth
**Why out of scope**: The fine-grained conditions under which same-origin allocations enter specific endset spans depend on the allocator-discipline machinery in ASN-0034 (T10a and friends). The descriptive treatment here is appropriate; formal claims belong in the allocator-discipline ASN.

### Topic 2: Bilateral vitality preservation across fork (version creation)
**Why out of scope**: Fork is J4 in ASN-0047 (ForkComposite). How vitality propagates from source to forked version is a distinct question. Listed correctly in open questions.

### Topic 3: Multiple links with overlapping endset coverage
**Why out of scope**: Listed in open questions. The interaction of independent links is a future analysis target.

### Topic 4: Discovery latency
**Why out of scope**: Replication/protocol concern (BEBE), explicitly out of scope per the review prompt.

### Topic 5: Link-subspace projection contribution
**Why out of scope**: Author explicitly defers to the Link Subspace ASN. The ASN's restriction to text-subspace projection (π_text) in SV11 is appropriate.

### Topic 6: Higher-arity links (N > 3)
**Why out of scope**: Author explicitly restricts to the standard triple (arity 3) per L3 in ASN-0043. Generalization to N > 3 is correctly deferred.

### Topic 7: Dormant link revival mechanism
**Why out of scope**: Listed in open questions. Operations for transitioning a non-vital link back to vital status are operational specification, not survivability.

VERDICT: REVISE
