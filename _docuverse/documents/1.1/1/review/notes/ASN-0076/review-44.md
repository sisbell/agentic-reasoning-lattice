# Review of ASN-0076

## REVISE

### Issue 1: E2's distinctness proof is over-engineered — freshness already established in E0 gives the result directly

**ASN-0076, E2 (SuccessorDistinctness) proof**: "By SequentialTransitionAxiom (ASN-0047), each K.λ firing is an atomic, totally-ordered transition... With all three producing events now established as T10a-conforming, L11a (LinkUniqueness, ASN-0043) ... applies to each pair, giving ℓ_new ≠ ℓ_old, ℓ_sup ≠ ℓ_old, and ℓ_sup ≠ ℓ_new."

**Problem**: All three inequalities follow immediately from the freshness/membership facts E0 already discharges, with no appeal to SequentialTransitionAxiom, L1c-conformance of `ℓ_old`, or L11a. E0 establishes `ℓ_new ∉ dom(Σ.L) ∪ dom(Σ.C)` and `ℓ_sup ∉ dom(Σ_1.L)`, while `ℓ_old ∈ dom(Σ.L) ⊆ dom(Σ_1.L)` and `ℓ_new ∈ dom(Σ_1.L)`:
- `ℓ_new ∉ dom(Σ.L)`, `ℓ_old ∈ dom(Σ.L)` ⟹ `ℓ_new ≠ ℓ_old`;
- `ℓ_sup ∉ dom(Σ_1.L)`, `ℓ_old, ℓ_new ∈ dom(Σ_1.L)` ⟹ `ℓ_sup ≠ ℓ_old ∧ ℓ_sup ≠ ℓ_new`.

The proof instead constructs a three-event ordering apparatus and certifies `ℓ_old`'s conformance via L1c purely to invoke L11a — machinery the conclusion does not need. This is exactly the accreted-justification pattern the anti-bloat pass targets: a heavier downstream lemma stands in for a one-line membership argument the preceding claim already supplies.

**Required**: Replace the L11a/SequentialTransitionAxiom/L1c route with the direct membership argument from E0's freshness facts, or state explicitly why L11a is preferred over freshness (it is not — freshness is strictly weaker and already on hand).

### Issue 2: No weakest-precondition analysis, though the operation's central reader-facing question is a non-trivial wp

**ASN-0076, E7 (LineageWitness) proof**: "absent independent arrangement of ℓ_old or ℓ_new in some document, ℓ_sup is orphaned (LP17, ASN-0098) and becomes discoverable once a later transition arranges an I-address in its coverage (LP18, ASN-0098)."

**Problem**: The ASN derives many consequences (E1–E10) and includes a concrete worked example, but supplies no weakest-precondition analysis. The standards call for a non-trivial wp and name "wp for 'link discoverability is preserved'" as the example — which maps directly onto this ASN. E7 gestures at the discoverability condition informally (orphaned unless arranged) but never formalizes it as a wp. Because EDITLINK touches no arrangement (E10), `wp(EDITLINK, discoverable_from(ℓ_sup, d, ·))` is precisely the interesting case: the post-state never makes `ℓ_sup` discoverable on its own, so the wp collapses to a condition on prior arrangement of `ℓ_old`/`ℓ_new` — a genuinely non-trivial result the ASN states in prose but does not derive.

**Required**: Add a wp computation for a non-trivial postcondition — discoverability of `ℓ_sup` (or of `ℓ_old` via the supersession) is the natural target — naming the premises and showing the pullback through E10's frame, rather than leaving it as the informal LP17/LP18 remark in E7.

## OUT_OF_SCOPE

### Topic 1: Supersession-chain invariants, cycles, retraction semantics, "current successor" computation
**Why out of scope**: These are correctly deferred in the Open Questions section. They require new state or new conventions over the supersession relation that EDITLINK does not itself establish — future-ASN territory, not defects here.

### Topic 2: Authorization of who may publish a supersession against another owner's link
**Why out of scope**: E6's application-layer note correctly defers this to a future capabilities/authorization ASN; the link model has no executor field to constrain it.

VERDICT: REVISE
