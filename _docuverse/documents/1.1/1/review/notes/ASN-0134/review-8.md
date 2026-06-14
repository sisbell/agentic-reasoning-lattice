# Review of ASN-0134

This is a strong, unusually self-aware note. It correctly separates step / batch / operation levels, handles the first-emission boundary in H2, makes the stack commitment explicit (load-bearing for A6), grounds the conflict theory in a concrete worked example (§7), and is candid about its own non-confluences. Two issues remain — one substantive.

## REVISE

### Issue 1: The §4 enumeration of operation-level non-confluences is incomplete

**ASN-0134, §4 (final paragraph), and the G1 row of the Claims table**: "the operation-level realization is order-stable only when neither source is present: no two concurrent operations are idem = ⊤ with coverage-equal (F, G), and no Nullify races the emission of its own cross-home target ... Concurrent idem-⊤ coverage-equal emissions into distinct homes, and a cross-home Nullify/emit race, are **the two** operation-level non-confluences we have found"

**Problem**: There is a third cross-home operation-level non-confluence, so "order-stable only when neither source is present" is false. Take a state Σ with an active incumbent `T = (a_T, F_T, G_T) ∈ A_K^Σ`, `idem(K) = ⊤`. Agent A issues `Emit_K(d_A, F, G)` with `(F, G)` coverage-equal to T; agent B issues `Nullify_Binary(d_B, a_T)` targeting the **incumbent** `a_T` (resident, so P-tgt holds via residence). Choose `d_A`, `d_B`, `home(T)` pairwise distinct, so A and B are ≺-incomparable (free-running).

- *Order A;B:* A's dedup reads the global `A_K^Σ`, sees T active → **hit**, zero steps, returns `a_T` (ASN-0128 I1). Then B nullifies `a_T`. Final: class K has no active tuple; `dom(L)` gains only B's emitter.
- *Order B;A:* B nullifies `a_T` first. A now reads `A_K^{Σ_B}`, in which T is gone (ASN-0128 I2) → **miss**, deposits a fresh `A' = (a_A, F, G)` active at `a_emit(Σ_B, d_A)`. Final: class K has active `A'`; `dom(L)` gains B's emitter **and** `a_A`.

The committed states differ (`Observe_K(F-pattern, oper)` returns `∅` vs `{A'}`; the realized step count is 1 vs 2), yet **neither listed source is present**: there is only one concurrent emit, so this is not source 1 (which requires *two* coverage-equal idem=⊤ emits); and B targets the pre-existing incumbent, not A's emission output, so it is not source 2. This is exactly the mechanism the note itself states in I2/I3 (a concurrent Nullify of the incumbent flips A's hit to a miss) — it is simply omitted from the §4 *concurrency* enumeration. Worse, this source is **not** removed by the disciplines the note relies on elsewhere: B's retraction of T satisfies emit-before-retract (T was emitted long before B) and the derivation is surface-disciplined, so order-instability persists even on the disciplined domain where source 2 is excluded. The general phenomenon is that an idem=⊤ Emit's hit/miss verdict reads the *global* `A_K`, so *any* concurrent cross-home operation that toggles the active-membership of a coverage-equal tuple — a competing emit (source 1) *or* a nullify of the incumbent (this case) — flips it.

**Required**: Either add this third source to the §4 enumeration and the G1 row — an idem=⊤ Emit whose hit/miss is flipped by a concurrent cross-home Nullify of a coverage-equal active incumbent — or weaken the exhaustiveness claims ("the two ... we have found", "order-stable only when neither source is present") so they no longer assert the two listed sources are the only ones. The cleanest repair unifies source 1 and this case under "an idem=⊤ Emit racing any cross-home operation that toggles a coverage-equal tuple's active-membership," and notes that — unlike source 2 — this survives both emit-before-retract and SD.

### Issue 2: H0's proof leaves the cross-document, cross-subspace case to lemmas that do not cover it

**ASN-0134, §4 (H0 proof)**: "an allocation into a different `(d', S') ≠ (d, S)` — to another home, or to the sibling subspace of the same home — which by DisjointSubAllocatorChains (S' ≠ S) and CrossDocumentDisjointness (d' ≠ d) deposits outside `P_S(d, ·)`."

**Problem**: `(d', S') ≠ (d, S)` splits three ways — `(d'≠d, S'=S)`, `(d'=d, S'≠S)`, and `(d'≠d, S'≠S)` — but the two-way phrasing ("another home, or the sibling subspace") and the two cited lemmas cover only the first two. CrossDocumentDisjointness covers only the same-subspace cross-document case — as the note *itself states three paragraphs later in H1* ("CrossDocumentDisjointness names only the S = S' instance") — and DisjointSubAllocatorChains covers only the same-document cross-subspace case (`A_C(d)` vs `A_L(d)`). The cross-document-cross-subspace case `(d'≠d, S'≠S)` is covered by neither cited lemma. This is the exact gap H1 repairs (anchors diverge at the document component); H0 leaves it open while invoking the lemma H1 disclaims.

**Required**: H0 needs no disjointness lemma here. `P_S(d, ·)` is filtered by `origin = d` *and* store `dom_S`, so any allocation into `(d', S') ≠ (d, S)` deposits an address with `origin = d' ≠ d` or in `dom_{S'} ≠ dom_S`, hence outside `P_S(d, ·)`. Replace the lemma citations with this direct origin/store-membership argument (or, less cleanly, add the cross-document-cross-subspace case explicitly as H1 does).

## OUT_OF_SCOPE

### Topic 1: Concurrency of the arrangement/provenance stack (ASN-0047's K.μ⁺/K.μ⁻/K.ρ/K.δ)

A6's claim that "every state is *fully* per-state-canonical; no boundary-only invariant class exists" holds only because the note commits 𝔼 to the ASN-0093 stack, where M is always empty (M2) and there is no provenance relation. ASN-0047's stack carries genuine composite-boundary properties (P4★, P4a, P7a) that a mid-batch snapshot *can* violate, so a concurrent-isolation model for arrangement edits and provenance recording is materially harder and needs its own treatment.

**Why out of scope**: The note's stack commitment is explicit and defensible, and it acknowledges the dependence ("no provenance relation to leave dangling and no arrangement to leave half-coupled"). Extending the model to the arrangement layer is a distinct note, not a revision to this one.

VERDICT: REVISE
