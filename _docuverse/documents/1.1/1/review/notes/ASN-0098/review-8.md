# Review of ASN-0098

## REVISE

### Issue 1: LP13 is a restatement of LP12
**ASN-0098, LP13 — PartialSurvival**: "discoverability from `d` requires that, for at least one slot `i`, `coverage(Σ.L(a).eᵢ) ∩ ran(Σ.M(d)) ≠ ∅`."
**Problem**: This is the right-hand side of LP12 verbatim. LP13 introduces no new claim or proof — it is LP12 reformulated in prose. The "link cannot have its endsets rewritten" observation cites L12, not LP13 content.
**Required**: Either give LP13 distinct content (e.g., a quantitative survival claim about minimum surviving cardinality, or the unconditional persistence of `a ∈ dom(Σ'.L)` independent of any discoverability) or fold its discussion into LP12 and remove the label.

### Issue 2: Worked trace branches without demarcation
**ASN-0098, A Worked Trace**: After Σ_1, the trace introduces Σ_2 ("Now suppose another document `d₂` is registered…") then Σ_3 ("Now apply K.μ~ to `d₁`…").
**Problem**: Σ_3 derives from Σ_1, not Σ_2 — the reference `dom(Σ_1.M(d₁))` in the K.μ~ setup gives this away, but the prose reads as if Σ_3 follows Σ_2. The two are alternate continuations from Σ_1, not a linear sequence. A reader tracking the trace will derive contradictions (e.g., wondering whether Σ_3 still has d_2 registered).
**Required**: Explicit branching language: "We now consider an alternative continuation from Σ_1, this time omitting the d_2 registration." Or rename so that branching is visible from the state labels.

### Issue 3: Achievability discussion silent on nesting documents
**ASN-0098, after the tightness definition**: "Cross-chain interference is automatically excluded: by T10 (PartitionIndependence, ASN-0034), chain elements of `A_sub'(d')` for `d'` non-nesting with `d_0` differ from `s` at the document-prefix position..."
**Problem**: T10 only handles documents that are non-nesting under prefix. But documents can stand in prefix relation (e.g., version sub-allocator produces `[d_0.1]` from `d_0`, both T4-valid documents with zeros=2 and `d_0 ≼ [d_0.1]`). The argument does not say how chain elements of nesting descendants like `A_C([d_0.1])` are excluded from `[s, s ⊕ ℓ)`. The construction does work — descendants have a `1` (or `2`) at position `#d_0 + 1` whereas `s ⊕ ℓ ≤ inc(t_m, 0)` keeps position `#d_0 + 1` at `0` — but this is the load-bearing case and is omitted.
**Required**: Add a sentence handling nesting documents: spell out why version-document chains and their descendants lie above `inc(t_m^C(d_0), 0)` at the divergence position. Without this, the achievability proof is incomplete for the case that matters most under T10a.

### Issue 4: LP8's postcondition for newly registered d_new is informal
**ASN-0098, LP8 — Entity-Registration Invariance**: "The newly created `d_new` has `project(e, d_new, Σ') = ∅` since `dom(Σ'.M(d_new)) = ∅`."
**Problem**: The lemma statement (and "introduces" line in the claims table) names only invariance over existing documents. The d_new claim appears as a closing remark in the proof, not as a formal postcondition. Downstream LP18 (resurrection) depends on the post-state projection through a newly-registered document being well-defined and empty until K.μ⁺ fires, which is exactly this claim.
**Required**: Elevate to a second postcondition: (a) `(A d ∈ dom(Σ.M) :: project(e, d, Σ') = project(e, d, Σ))`; (b) `project(e, d_new, Σ') = ∅`. Both are needed by downstream argument; both should be stated as commitments.

### Issue 5: F infiniteness not acknowledged
**ASN-0098, tightness definition**: "The set of *substrate-emittable addresses* is the union of all such chain elements across all T4-valid document tumblers and both subspaces; we denote it `F`."
**Problem**: F is infinite — there are countably infinitely many T4-valid document tumblers (by T0(a), T0(b) of ASN-0034), each with an infinite chain. Tightness's universal quantifier `(A t ∈ F : s ≤ t < s ⊕ ℓ : ...)` ranges over an infinite set. The proofs work because membership `t ∈ F ∩ [s, s ⊕ ℓ)` is checked by structural form analysis, not enumeration, but a reader expecting a finite check will be confused.
**Required**: One sentence acknowledging that F is infinite and that the quantifier is decidable via structural analysis (`t` must have form `[d.0.s.k]` with T4-valid `d`, `s ∈ {s_C, s_L}`, `k ≥ 1`, and `t ∈ [s, s ⊕ ℓ)` — finitely many such forms intersect any given span by the bounded reach).

### Issue 6: No concrete numerical example for tightness or LP19
**ASN-0098, Boundary and Width Behaviour**: The tightness definition, LP19a, and LP19 are stated and proved abstractly without a worked numerical example.
**Problem**: Per the rubric ("the ASN should verify its key postconditions against at least one specific scenario"), tightness is the most subtle definition in this ASN and the one most likely to be misunderstood. The worked trace at the end covers LP9, LP10, LP11 but not LP19.
**Required**: Add a small example to the boundary section: a specific document `d`, content allocated up to a specific chain index `m`, a tight span with explicit endpoints (e.g., `s = [d.0.s_C.1]`, `ℓ = δ(m, 4)` so `s ⊕ ℓ = [d.0.s_C.m+1]`), then trace a K.α producing `[d.0.s_C.m+1]` and show by the tightness condition that `a_new ∉ coverage(e)`. A second example showing a *non*-tight span (where `s ⊕ ℓ = [d.0.s_C.m+2]` and the next K.α produces an in-coverage address) would sharpen the contrast.

## OUT_OF_SCOPE

### Topic 1: Reverse projection (V-position to links)
**Why out of scope**: Listed as an open question. Defining the inverse direction (given `v`, which links project through `v`) would require its own ASN with separate invariants about index data structures and discovery completeness.

### Topic 2: Cross-document projection comparisons
**Why out of scope**: Listed as open question. Comparing projections across two documents that have undergone "the same" sequence of operations requires defining operation equivalence across documents, which is new territory.

### Topic 3: Link-to-link discoverability transitivity
**Why out of scope**: Listed as open question. Whether discovering link `a` whose endset references link `b` implies `b`'s discoverability requires extending the projection framework with traversal semantics.

### Topic 4: Relationship to ASN-0058 mapping blocks
**Why out of scope**: The projection could be expressed in terms of mapping-block decompositions, but this connection is a future refinement, not a gap in the current claims.

VERDICT: REVISE
