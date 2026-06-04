# Review of ASN-0076

## REVISE

### Issue 1: Precondition justification is a use-site inventory with forward references
**ASN-0076, The Composite (precondition)**: "The reachability conjunct ... is the outer hypothesis E5 carries explicitly. It is required twice over: the K.λ precondition discharges below lean on per-state facts at `Σ` (SubAllocatorBundle presumes... L0, used to derive `ℓ_new ∉ dom(Σ.C)`, is a per-state invariant), and the invariant-inheritance conclusion below requires `Σ` reachable..."
**Problem**: This paragraph does not advance the precondition's meaning. It explains *why* the conjunct is needed and *where* it is consumed ("discharges below," "conclusion below") — exactly the "Why the axiom is needed" + downstream-consumer-inventory + forward-reference patterns the anti-bloat pass targets. The reachability conjunct is a precondition; its consumption is self-evident at the use sites that invoke SubAllocatorBundle, L0, and ExtendedReachableStateInvariants.
**Required**: State `Σ` reachable as a precondition line and delete the justifying paragraph. Let the use sites cite reachability where they need it.

### Issue 2: E0 adjacency observation carries a retrospective use-site inventory
**ASN-0076, E0**: "The discharges above — the identification `ℓ_sup = inc(ℓ_new, 0)` from `Σ_1` and the fact that `ℓ_new` is the maximum of `{ℓ' ∈ dom(Σ_1.L) : origin(ℓ') = d_new}` — depend on this adjacency."
**Problem**: The adjacency fact (no atomic transition intervenes) is legitimate content; the trailing clause enumerating which earlier discharges rely on it is meta-prose pointing backward at the proof's own steps. A reader following the supersession step already used `Σ_1` and the maximum directly.
**Required**: Keep the adjacency assertion; drop the "The discharges above ... depend on this adjacency" sentence.

### Issue 3: L12/LP13 single-step/multi-step gloss restated three times
**ASN-0076, Foundation Recap, E9 proof, Claims table**: e.g. E9 — "permanent under L12 (single-step, ASN-0043) — equivalently LP13 (multi-step, ASN-0098)"; Foundation Recap states the same L12/LP13 pairing; the claims table repeats it.
**Problem**: Two (here three) passages say the same thing in different words. The single-step/multi-step relationship is foundation-level and need not be re-narrated at each citation.
**Required**: State the L12⇔LP13 relationship once (Foundation Recap), then cite the relevant lemma by name without re-explaining the equivalence.

### Issue 4: Authorization concern deferred twice to the same downstream
**ASN-0076, The Composite** ("any further constraint on who may select `d_new` belongs to an authorization layer not formalized in this ASN (see E6)") and **E6, Application-layer note** ("deferred to a future ASN on authorization and capabilities").
**Problem**: Two sections defer the same authorization question — one via an intra-document forward pointer "(see E6)", the other to a future ASN. This matches the "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Defer authorization once (in E6) and remove the "(see E6)" forward pointer from The Composite, or state the `d_new ∈ E_doc`-only constraint there without the cross-pointer.

## OUT_OF_SCOPE

### Topic 1: Supersession chain invariants, cycle-freedom, "current successor" computation
**Why out of scope**: These are correctly relegated to Open Questions; they require a link-search / lineage-resolution specification, not a revision to EDITLINK's composite definition.

The substantive proofs (E0 precondition discharges at both K.λ steps, E1 via LP13, E2 via L11a, the `#E ≥ 2` length-preservation induction, E4–E10) are sound, complete on their boundary cases, and supported by the concrete worked example. The remaining issues are forward-reference/meta-prose accretion, consistent with the note's anti-bloat classifier.

VERDICT: REVISE
