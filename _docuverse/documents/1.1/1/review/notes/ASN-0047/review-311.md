# Review of ASN-0047

## REVISE

### Issue 1: Forward-pointer announcement and repeated "imposed (not derived)" status of J0/J1★/J1'★

**ASN-0047, "Coupling and isolation" intro**: "The couplings named in this and the following statements — J0, J1★, J1'★ — and the composite-validity predicate ValidComposite★ that aggregates them are all defined in *Scoped coupling constraints* below; we name them here at first use and do not repeat the forward pointer."

**Problem**: This sentence's entire content is meta-prose about the document's own forward references ("we name them here at first use and do not repeat the forward pointer") — it advances no reasoning about coupling. It is exactly the "prose justifies document ordering / forward-pointer scaffolding" pattern. Compounding it, the "imposed (not derived)" status of the couplings is asserted in four places: this intro, the J0 box ("J0 is an imposed coupling constraint (not derived)... stated once at ValidComposite★ clause (2) below"), the "Scoped coupling constraints" intro ("J1★ and J1'★ are imposed (not derived)"), and ValidComposite★ clause (2) ("The couplings J0, J1★, and J1'★ are *imposed* validity conditions, not axioms..."). The J0 box even claims the status is "stated once" downstream, yet the Scoped intro restates it. A reader tracking where the couplings are actually defined must skip three deferral notes to reach the one definition.

**Required**: Delete the forward-pointer announcement sentence. State the "imposed, not derived" status exactly once (at ValidComposite★ clause (2), where the K.α-alone counterexample lives), and replace the J0-box and Scoped-intro restatements with nothing — first use needs no announcement that a definition follows.

### Issue 2: TrackedEmission preservation argument duplicated across three locations

**ASN-0047, ExtendedReachableStateInvariants preamble and Class (a) *TrackedEmission* paragraph**: The preamble says "All per-state invariants except TrackedEmission are discharged cell-by-cell in the Class (a) verification matrix below; TrackedEmission is the one per-state invariant discharged separately, by the self-contained induction in its definition box (restated in the *TrackedEmission* paragraph below)." The Class (a) paragraph then *restates* the induction: "vacuous at Σ₀, preserved by K.δ case (ii)..., and held in frame by every non-K.δ transition."

**Problem**: The same preservation induction appears in (a) the TrackedEmission definition box's *Preservation* paragraph, (b) the navigation note in the ExtendedReachableStateInvariants preamble, and (c) the Class (a) *TrackedEmission* paragraph — the latter two restating what the definition box already proves. The navigation note ("the one per-state invariant discharged separately... restated in the paragraph below") is pure routing meta-prose, and the Class (a) paragraph adds no content beyond the definition box.

**Required**: Keep the preservation argument in the definition box only. In Class (a), replace the restatement with a one-line pointer ("TrackedEmission: see its definition-box induction"), and drop the preamble's "restated in the paragraph below" clause.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link/content withdrawal (DELETEVSPAN)
**Why out of scope**: The ASN's own open questions flag that K.μ⁻ models only suffix removal, not the implementation's compact-and-renumber interior deletion. This is correctly deferred — modeling interior compaction is new territory, not an error in the present suffix-removal contract.

### Topic 2: Transitive transclusion-chain provenance and concurrency of link allocation
**Why out of scope**: Provenance under chained transclusion and serialization of concurrent same-document allocation are listed as open questions; they require state/operations this ASN does not introduce.

VERDICT: REVISE
