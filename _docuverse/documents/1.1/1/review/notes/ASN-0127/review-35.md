# Review of ASN-0127

## REVISE

No REVISE items. The findings below document what was checked and why each delicate point holds.

**Phase-1 image algebra.** F-IMG-MONO and F-IMG-CONTR are correct two-line forward-image arguments from the extension/contraction frames. F-IMG-SWING's reindexing was recomputed: with `dom(Σ'.M(d)) = dom(Σ.M(d))` (K.μ~-FIX) the substitution `v = π(u)` is exhaustive, and the index-set cardinality identity `|π⁻¹(W) ∩ dom| = |W ∩ dom|` follows from π restricting to a bijection `π⁻¹(W) ∩ dom → W ∩ dom`. The injectivity-pins-image-cardinality step is sound, and F-IMG-TAX correctly supplies the finiteness premise (S8-fin) that "distinct equal-size sets cannot nest" actually requires — this would fail for infinite sets, and the ASN cites it rather than leaving it implicit.

**Reorder witnesses.** All four witnesses were recomputed against the bijection equation `Σ'.M(d)(π(u)) = Σ.M(d)(u)`. Gain: `π⁻¹({v₁,v₂}) = {v₁,v₃}`, image `{a} ↦ {a,b}` ✓. Loss: `π⁻¹({v₁,v₂}) = {v₂,v₃}`, image `{a,b} ↦ {b}` ✓. Four-position: `{a,b} ↦ {a,c}`, incomparable ✓. The witness-admissibility paragraph discharges all five K.μ~ admissibility clauses, including the two easy to skip: (ii) non-triviality (each π moves some position's image — verified per witness) and the precondition that `M(d)|_{dom_C}` takes at least two distinct values (holds in all four). The S3★-persistence argument via range preservation is valid here because every pinned position is content-subspace.

**Phase-2 algebra and composite.** F-UDIST's derivation is complete (intersection-over-union, existential-over-disjunction, set-builder split), and the note correctly identifies why the law must be unrestricted: F-VDIST's middle step feeds it images that can overlap even for disjoint V-regions under content sharing. F-FULL's reduction to ASN-0098's `discoverable_from` is an exact match against LP12's right-hand side at `I = ran(Σ.M(d))`.

**Store-fixed lane.** F-PRES was checked against ASN-0047's frames: all seven atomic operations other than K.λ publish `L' = L` (the amended K.μ⁺/K.μ⁻ frames include it), and K.μ~ inherits it by composition. F-INERT's path lift does the induction explicitly rather than waving at closure. F-LAMBDA's decomposition is complete: prior keys via F-CIL-perlink, the fresh key via the freshness precondition pulled back through monotonicity, disjointness of the two parts established.

**E-CONS.** This is the hardest proof in the note and it holds. The anchor's two readings of "created on the path" are proven equivalent in both directions — the difference-to-event direction correctly extracts the least index, identifies the dom(L)-changing step as a K.λ via F-PRES, and forces `a = ℓ_new` from the singleton effect. The match warrant (E-INV on the suffix) legitimately converts the state-indexed `matches` into a per-link constant. The exclusion direction's case split on `a ∈ dom(Σ.L)` uses E-INV exactly where needed.

**D-CWP.** The bridge `image(W, d_q, Σ') = I_R` is correct (D-SEQ★ gives `R ⊆ dom(Σ.M(d_q))`, so the restriction's domain is exactly `R`), the biconditional reduces cleanly to `A = A ∪ B ⟺ B ⊆ A`, and the claim that both `I_R` and `Δ` are pre-state quantities — making the wp evaluable before the step — is true and load-bearing. The `R = ∅` boundary is handled.

**Worked illustration.** All slot intersections were recomputed across every bullet; they are right, and they rest on the structural premise (pairwise prefix-incomparability via T10a.2 for the content siblings, and T7-distinctness plus Prefix's length gap for `a_θ`), which is itself proven rather than assumed. The composite-validity obligations are handled where a lone atomic step would not be a valid composite: the K.α bullet wraps in a J0-discharging composite, and the Rise bullet discharges J1★ via the standing provenance record carried by P2 — a detail easy to get wrong and gotten right. The stable-contraction bullet does real work, separating the wp from the cruder "no in-region drop" condition with both a link-free drop and a re-witnessed link-bearing drop.

**Anti-bloat scan.** No compounding forward-reference patterns found. The single forward pointer from F-IMG-SWING to F-IMG-TAX is one sentence to the adjacent lemma; the cross-state definedness paragraph after F-IMG is load-bearing (it discharges F-IMG's definedness condition once for every post-state claim); E-CONS's "we fix them first" preamble structures a genuine proof obligation rather than deferring it. No paragraph imagines a precondition-excluded case, no axiom-rationale sub-paragraphs, no consumer inventories, no duplicated content across sections.

## OUT_OF_SCOPE

### Topic 1: Uniform stability wp across the whole K-vocabulary
**Why out of scope**: D-CWP covers the contraction instance; the uniform characterisation over extension, reorder, and off-document steps is correctly deferred as Q3 — new territory, not a gap in the contraction result.

### Topic 2: Slot-indexed conjunctive query algebra
**Why out of scope**: The conjunctive per-slot filter semantics (Q2) is a different query primitive; which of F-UDIST/F-IMONO survive there is a fresh question, not an error in the disjunctive `matches` treated here.

### Topic 3: Content-keyed queries and composition with ASN-0098 projection
**Why out of scope**: Q1 and Q4 name genuinely separate combinators (`Σ.C`-mediated naming; project-then-intersect). This note's scope statement ("that — and only that") correctly excludes them.

VERDICT: CONVERGED
