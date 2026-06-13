# Review of ASN-0124

## REVISE

### Issue 1: FD-FRESH composes a transition the note's own state model cannot express
**ASN-0124, Dynamics, FD-FRESH**: "Let the insertion composite on `d` be: the gap-shift transition of ASN-0082 at `(p, n)` (postconditions I3, I3-V, frames I3-L, I3-X, I3-D, I3-C), then K.α allocating fresh addresses `A_new`…, then the K.μ⁺ filling the vacated gap with images in `A_new` (restoring D-SEQ★ at the boundary)…"

**Problem**: The State section fixes the atomic vocabulary as `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.ρ}` with `K.μ~` the only named composite, and FD-FRAME + FD-STEP together claim to characterize *all* movers over that vocabulary ("The only movers are the content-subspace arrangement transitions…"). The ASN-0082 gap-shift is not in that vocabulary and is not realizable within it: its post-state content domain is `[1, p) ∪ [p+n, N+n]` (I3, I3-V, I3-CS), which violates the D-SEQ★ package (gapped domain for interior `p`; minimum off `[1,1]` for `p` at the front). K.μ⁺'s precondition requires D-CTG★/D-MIN★ on its result and K.μ⁻ retains only per-subspace initial segments, so the gapped state is unreachable in-vocabulary — and ASN-0047's ExtendedReachableStateInvariants asserts D-CTG★ ∧ D-MIN★ ∧ D-SEQ★ at *every elementary-reachable state*, not merely at composite boundaries. The parenthetical "(restoring D-SEQ★ at the boundary)" concedes the mid-composite violation. The note cannot simultaneously rely on that invariant package (FD-CWP's `Ret ⊆ dom(Σ.M(d))` "by D-SEQ★"; FD-CONVEX's gap-free form; the worked illustration's boundary states) and traverse states that falsify it. As written, FD-FRESH proves invariance of a composite that is not a valid composite of the declared model.

**Required**: Either (a) restate the insertion composite in-vocabulary — K.α* allocating `A_new`; K.μ⁻[d, n'_{s_C} = 0] (full content clear, link subspace retained; degenerate first-insertion case has no K.μ⁻ step); one K.μ⁺ rebuilding `[1, N+n]` with the old images at shifted positions and `A_new` at `[p, p+n)`; K.ρ for the `A_new` range-entries (J0/J1★ are initial-to-final, so the old images' mid-composite absence is harmless) — note that the net effect realizes I3/I3-L/I3-V/I3-CS as initial-to-final postconditions, and derive invariance stepwise from FD-STEP (clear drops `d` iff it was a member; rebuild restores membership iff `ran_C(d, Σ_pre) ∩ I ≠ ∅`, since `N ∩ I = ∅` by freshness); or (b) declare the ASN-0082 shift an explicit extension of the transition vocabulary and re-scope FD-FRAME/FD-STEP's exhaustiveness claim and every use of the per-elementary-state invariant package accordingly.

### Issue 2: FD-LOSSY's witness is a sketch, not a construction
**ASN-0124, What Scattered Regions Reveal, FD-LOSSY**: "Witness: let `d` arrange `a₁ ∈ I₁` and not `a₂ ∈ I₂` in `Σ¹`, and `a₂` but not `a₁` in `Σ²` (both arrangements reachable by the insertion/transclusion composites already used); both answers are `{d, …}` with identical membership…"

**Problem**: This is an existence claim over reachable states, and the exhibited witness leaves unverified exactly the parts that need verifying. "{d, …}" hides the obligation that every *other* document's membership coincide across `Σ¹` and `Σ²` — yet J0 forces every freshly allocated address into some arrangement at its allocating composite's boundary, so where `a₂` lives in `Σ¹` (or whether it is allocated there at all) materially affects the answer set. And "a₂ but not a₁" in `Σ²` is not one composite away: K.μ⁻ retention is per-subspace *initial segments*, so an earlier position cannot be dropped while a later one is kept in a single step, and if `a₂` is a later emission of the same content chain, its allocation presupposes `a₁`'s. The pattern is realizable (e.g., `Σ¹`: allocate-and-arrange `a₁` only, leaving `a₂` unallocated and inert by FD-GROUND; `Σ²`: allocate both with their J0 arrangements, K.μ⁻ full clear, K.μ⁺ re-arranging `[1,1] ↦ a₂`, with J1★ checked at each boundary), but none of this is in the note — in contrast to FD-NEUT(c), which pins its construction completely.

**Required**: Exhibit the two states concretely — documents, allocation events, composite sequence for each, and the verification that the two answers are equal as sets — at the level of detail FD-NEUT(c) already demonstrates.

### Issue 3: Two-phase dynamics for `finddocs_V` stop at a qualitative remark
**ASN-0124, Dynamics, FD-NONMONO**: "For the two-phase operation there is one further motion: the resolution itself is present-tense — editing a named document moves `resolve(Q, ·)` … The motion enters through the pointing, not through the containing — which is why this section fixed `I` first."

**Problem**: The operation FD-V specifies is `finddocs_V`, but the dynamics section proves results only for `finddocs` at fixed `I`; the behavior when a transition hits a *named* document — half the editing surface — is acknowledged and then dropped. The sibling this note claims kinship with carries exactly these composed results for its two-phase query (ASN-0127's D-NONMONO per-transition case analysis, D-ABSORB, D-CWP). Here the monotone cases are two-line consequences of lemmas already proved and are never stated: K.μ⁺/K.μ⁺_L on a named `d_q` gives `resolve(Q, Σ) ⊆ resolve(Q, Σ')` (F-IMG-MONO through FD-IMGC, `dom(C)` framed), whence `finddocs_V(Q, Σ) ⊆ finddocs_V(Q, Σ')` by FD-STEP growth then FD-IMONO; K.μ⁻ on a named `d_q` gives the reverse inclusion by F-IMG-CONTR, FD-IMONO, and FD-STEP shrinkage. The genuinely two-phase case — K.μ~ on a named `d_q`, where the resolved set can swing (F-IMG-SWING) while every fixed-`I` answer is invariant (FD-STEP) — gets neither a lemma nor a counterexample.

**Required**: State the composed per-transition results for `finddocs_V`: at minimum the two monotone inclusions with their derivations, plus either a D-CWP-style stability condition or a concrete example for the reorder-on-named-document case.

### Issue 4: The worked illustration fires a reorder whose precondition fails
**ASN-0124, Worked Illustration**: "d_C reorders — unchanged (FD-STEP, reorder clause)."

**Problem**: As constructed, `d_C` arranges exactly one content position (`[1,1] ↦ a₃`). K.μ~ requires `M(d)|_{dom_C}` to take at least two distinct values, and its admissibility clause (ii) requires a non-trivial net effect `M'(d) ≠ M(d)`; on a one-entry content arrangement no admissible π exists, so this step cannot fire. The illustration — whose purpose is concrete verification — checks a claim against an operation that is not enabled.

**Required**: Apply the reorder where it is enabled: `d_A` (three positions, pairwise distinct images) or `d_B` before its contraction (two positions, `a₂ ≠ a₃`), or first extend `d_C`'s arrangement.

### Issue 5: FD-COOC's full-containment identity breaks at `I = ∅`
**ASN-0124, What Scattered Regions Reveal, FD-COOC**: "full containment at address grain is the finest such composition, `{d : I ⊆ ran_C(d, Σ)} = ∩_{a ∈ I} finddocs({a}, Σ)`."

**Problem**: At `I = ∅` the left side is all of `dom(Σ.M)` — every document vacuously contains all of nothing — while the right side is an intersection over an empty index set, which is undefined (or "everything") absent a declared universe. Every other claim in the note handles its empty boundary explicitly (FD-FIND, FD-RES, FD-CWP at `Ret = ∅`); this one is silent.

**Required**: Guard the identity with `I ≠ ∅`, or declare the convention that the empty intersection is taken within the universe `dom(Σ.M)` (under which the identity holds).

## OUT_OF_SCOPE

### Topic 1: Link-arrangement containment
A "which documents arrange link `ℓ`" query — the link-subspace mirror of this note's content-restricted question — is deliberately excluded by FD-IMGC ("queries name material, not link machinery"). It is a separate, largely degenerate operation (CL-OWN pins each link's arranger to its origin) and belongs in its own note, not here.
**Why out of scope**: new territory created by the content restriction, not an error in this ASN.

### Topic 2: Temporal contract of the historical answer
FD-HIST returns membership without order, time, or version rank; *when* a ghost contained the material, attribution-bearing enrichments, asker authority, intra-composite coherence, and provenance compaction are all parked in the note's Open Questions, correctly.
**Why out of scope**: these require new state or new obligations (ordered provenance, authority model) beyond the containment relation specified here.

VERDICT: REVISE
