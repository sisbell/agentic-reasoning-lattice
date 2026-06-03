# Review of ASN-0102

This is a thorough, well-structured note. The core transition is correctly stated over all five state components, the wp computation for S3★ is genuine, the displacement/no-overwrite argument (X7) carefully separates "freed slots" from "occupied copy region," the post-state density tiling (X16) is exact, and the coupling discharge (X14) handles the New/Old split correctly. The worked example exercises a non-trivial cross-origin, fragmented, mid-document case and checks the load-bearing claims against it. Two issues remain.

## REVISE

### Issue 1: The "uniqueness" characterization of COPY is false

**ASN-0102, "A remark on what COPY is"**: "It is the unique act that grows `ran(Σ.M(d))` while leaving `dom(Σ.C)` fixed (X1 ∧ X3)." and the supporting taxonomy: "Content creation grows both; deletion shrinks reach without touching the store; rearrangement permutes within fixed reach. COPY alone imports existing identity."

**Problem**: K.μ⁺ (ArrangementExtension, ASN-0047) also grows `ran(Σ.M(d))` while leaving `dom(Σ.C)` fixed. Its precondition requires every new mapping `M'(d)(v) = a` to satisfy `a ∈ dom(C)`, and its frame is `C' = C`. Adding a V-position that maps to an existing-but-not-yet-referenced content address enlarges `d`'s reach without enlarging the store — exactly the property claimed to be unique to COPY. The note even relies on this elsewhere: in the "Definition of COPY" it distinguishes COPY from K.μ⁺ *only* by the relabeling/displacement (`M'(d)(v) = M(d)(v)` failing), conceding that K.μ⁺ otherwise extends reach over existing content. The taxonomy that justifies "COPY alone" omits K.μ⁺ entirely, and the formal claim cited to (X1 ∧ X3) is therefore not established by X1 ∧ X3 — those establish that COPY does this, not that it is the only operation that does.

**Required**: Either drop the uniqueness claim, or restate the essence in terms of what genuinely distinguishes COPY (e.g., it is the operation that imports existing content *with displacement* — extension by reference into a position that relabels the incumbent content subspace forward — rather than the unique reach-without-store grower). Include K.μ⁺ in the contrasting taxonomy.

### Issue 2: "k = number of maximal contiguous I-runs the source occupies" is imprecise for multi-reference sequences

**ASN-0102, "The source designation and its resolution"**: "the run count `k` is the number of maximal contiguous I-runs the source occupies (C1a, M12) — it is a property of how fragmented the source content is in I-space, not of its width `W`."

**Problem**: `resolve_Σ(R) = resolve(r₁) ⌢ … ⌢ resolve(r_p)` concatenates per-reference maximally-merged decompositions; `k` is the *sum* of the per-reference run counts. When two consecutive references draw I-adjacent content of shared origin, the concatenation carries two runs across the inter-reference boundary that the source actually occupies as a *single* maximal I-run. So `k` over-counts the "maximal contiguous I-runs the source occupies," and the attribution "(C1a, M12)" — which is per-reference (single-restriction) machinery — does not justify the count for the whole sequence. X8 later states the precise picture (canonical count `≤ k`, equality iff no inter-reference boundary is I-adjacent), which contradicts the unqualified earlier sentence.

**Required**: Qualify the early statement: `k` is the total run count of the concatenated resolution (sum over references), which equals the source's maximal-I-run count only within a single reference; across references it may strictly exceed it. Reconcile with X8 rather than asserting equality up front.

## OUT_OF_SCOPE

The Open Questions (continued discoverability of displaced copied content, chained-reference containment recording, time-varying resolution, identity when the allocating document is unreachable) are correctly deferred — they concern link projection/discoverability (ASN-0098 territory) and future operation interactions, not defects in this note.

META: not applicable — the ASN stays in specification territory (state, transition, invariants stated abstractly, with implementation evidence kept subordinate via X8's explicit "abstract state commits only to the arrangement").

VERDICT: REVISE
