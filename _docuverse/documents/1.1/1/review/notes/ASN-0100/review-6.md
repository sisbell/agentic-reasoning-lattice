# Review of ASN-0100

## REVISE

### Issue 1: K.ρ ordering claim misrepresents substrate semantics
**ASN-0100, Atomicity and Canonical Order section**: "K.ρ(a_k, d) recording provenance for an arranged `a_k` must follow K.μ⁺ if J1★ is to be discharged at the boundary by historical state."
**Problem**: J1★ is not discharged "by historical state" — that mechanism belongs to P4a. J1★ simply requires (a_k, d) ∈ R' at the boundary, which is satisfied regardless of when K.ρ fires within the composite (as long as it fires after the corresponding K.α). K.ρ can fire before K.μ⁺ without violating any per-state invariant (P4a is composite-boundary, not per-state) or compromising J1★ discharge. The ASN's "K.α and K.ρ do not commute with K.μ⁺ and K.μ⁻" sentence is also imprecise: K.μ⁻ has no dependency on dom(C), so K.μ⁻ commutes with K.α firings entirely.
**Required**: Correct the claim. The only forced orderings are: (i) K.α(a_k) precedes K.α(a_{k+1}) (by chain emission discipline); (ii) K.α(a_k) precedes K.μ⁺ placing a_k (by K.μ⁺'s `a ∈ dom(C)` precondition); (iii) K.α(a_k) precedes K.ρ(a_k, d). K.μ⁻ has no ordering constraint relative to K.α firings. K.ρ has no ordering constraint relative to K.μ⁺.

### Issue 2: Per-state invariant verification at intermediates is not exhaustive
**ASN-0100, Atomicity and Canonical Order section**: The verification traces through intermediate states but only explicitly verifies a subset of per-state invariants.
**Problem**: ASN-0047's ExtendedReachableStateInvariants lists ~28 per-state invariants. The ASN explicitly verifies the "hard" ones (S2, S3★, S7a-d, S8a, S8-depth, S8-fin, S8★, D-CTG★, D-MIN★, D-SEQ★, P6, P7, L0, L12, L14) but never names P8, NodeLineage, S4, S3★-aux, CL-OWN, CL-UNIQ, L1, L1a, L1b, L1c, L3, L-fin, M0, C-fin. These are trivially preserved (their state components are unchanged by INSERT) but the ASN doesn't say so. A reviewer cannot tell whether they were checked, deferred, or overlooked.
**Required**: Add a brief paragraph enumerating the trivially-preserved per-state invariants and noting they hold by frame (E unchanged ⟹ P8, NodeLineage, M0; L unchanged ⟹ L1, L1a-c, L3, L-fin, CL-OWN, CL-UNIQ; etc.). One sentence per group suffices, but the list must be complete.

### Issue 3: Projection-shift correspondence derivation under-detailed
**ASN-0100, Coverage and link discoverability subsection**: "LP9 (ExtensionMonotonicity; ASN-0098) gives the per-step characterisation of K.μ⁺'s contribution to projection growth; the composite's projection-shift correspondence is the combined Left-fixed + Right-shifted form, accounting also for K.μ⁻'s temporary retraction of the Right region within the composite's interior (which LP10, ContractionMonotonicity; ASN-0098, governs per-step but cancels against K.μ⁺'s re-introduction at the composite boundary)."
**Problem**: This is one sentence summarizing a multi-step composition. The intermediate-state projections under K.μ⁻ (where the Right region disappears from `project`) and K.μ⁺ (where Insertion and Shifted-right positions reappear) are not shown. The claim that K.μ⁻'s retraction "cancels against K.μ⁺'s re-introduction" is a load-bearing step but receives no derivation. The asserted equality `project(ℓ, i, d', Σ') = π(project(ℓ, i, d', Σ)) ∪ N_{ℓ,i}` is non-trivial; LP9 alone does not establish it.
**Required**: Show the projection composition step-by-step: (i) state `project_pre`, (ii) compute `project_intermediate` after each K.α (unchanged by LP6), (iii) compute `project_intermediate` after K.μ⁻ (LP10 gives the contracted form), (iv) compute `project_intermediate` after K.μ⁺ (LP9 gives the extended form, with explicit characterization of which new V-positions enter `project`), (v) show this equals `π(project_pre) ∪ N_{ℓ,i}`.

### Issue 4: "Strengthened by P0" wording suggests P0 ⊋ S0
**ASN-0100, Permanence of existing content subsection**: "This is S0 (ContentImmutability; ASN-0036), strengthened by P0 (ContentPermanence; ASN-0047), verbatim."
**Problem**: P0 is not strictly stronger than S0; they are equivalent statements of the same property (dom(C) monotone, values preserved). P0 also subsumes S1 (StoreMonotonicity), which is derived from S0. The "strengthened" framing is misleading.
**Required**: Replace with "This is S0 (ContentImmutability; ASN-0036), equivalently P0 (ContentPermanence; ASN-0047), which subsumes S0 ∧ S1."

### Issue 5: Composite atomicity assumption listed as state precondition
**ASN-0100, The Operation: Formal Contract — Preconditions**: The "Composite atomicity assumption" is bulleted under Preconditions alongside state conditions like `d ∈ dom(M)` and `n ≥ 1`.
**Problem**: Composite-level atomicity is not a property of the pre-state Σ; it is a property of the substrate execution model. Mixing it with state preconditions obscures the distinction between "what Σ must satisfy" and "what the execution environment must provide". The ASN's prose later acknowledges this ("INSERT requires it as a precondition" but "is *not* entailed by SequentialTransitionAxiom"), but the layout still conflates the two.
**Required**: Separate the formal contract into "State preconditions" and "Environmental assumptions" (or similar). Move composite atomicity into the latter. This makes wp-style reasoning about INSERT cleaner — wp applies to state preconditions, not to execution-model assumptions.

### Issue 6: "K.α and K.ρ do not commute with K.μ⁺ and K.μ⁻" — overbroad claim
**ASN-0100, Atomicity and Canonical Order section**: "K.α and K.ρ do not commute with K.μ⁺ and K.μ⁻."
**Problem**: This is too broad. K.α and K.μ⁻ DO commute (K.μ⁻'s effect on M does not affect K.α's freshness or chain-emission discipline, which depends on dom(C) only; K.α's effect on C does not affect K.μ⁻'s precondition `dom(M(d)) ≠ ∅` or its M-shrinkage logic). Only the K.μ⁺-after-K.α dependency (via K.μ⁺'s `a ∈ dom(C)` precondition) and K.ρ-after-K.α dependency (via K.ρ's `a ∈ dom(C)` precondition) are forced.
**Required**: Replace with a precise enumeration: K.μ⁺(adding `v ↦ a_k`) follows K.α(a_k); K.ρ(a_k, d) follows K.α(a_k). All other orderings among K.α, K.μ⁻, K.μ⁺, K.ρ are admissible at the per-state level.

## OUT_OF_SCOPE

None to flag. The ASN explicitly bounds its scope (content subspace only) and the user's scope statement confirms link-subspace insertion, COPY, DELETE, REARRANGE, version creation, and replication are excluded.

VERDICT: REVISE
