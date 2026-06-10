# Review of ASN-0126

The framework is sound and unusually well-argued: the projection bridge cleanly isolates this note's additions from ASN-0086's machinery, P3/P6 establish gate safety, P5 establishes gate liveness, the wp analysis correctly identifies C3 as the conjunct newly made live by non-unit retraction spans, and the three-move R-Scope transfer for the Binary wrapper is airtight. The findings below are narrow.

## REVISE

### Issue 1: "permanently inert substrate" overstates the empty-registry consequence
**ASN-0126, Worked illustration ("Two Multi types coexist (C0)")**: "At the opposite extreme C0 permits the empty registry `Σ_init.registry = ∅` ..., which yields a *permanently* inert substrate"

**Problem**: An empty registry disables only `K.λ_sh` — precondition (i) (*K* registered) fails for every emit. `K.σ` and `K.α` are *not* gated by the registry; by the frame conditions in Registry permanence they merely *frame* it. So under `→_sh` the empty-registry substrate still grows `dom(Σ.M)` (via `K.σ`) and `dom(Σ.C)` (via `K.α`). The substrate is not "inert"; only its link store `dom(Σ.L)` is permanently frozen. The clause after the colon — "`→_sh` can never extend `dom(Σ.L)`" — states the precise fact, which the headline phrase contradicts.

**Required**: Scope the claim to the link store ("a substrate whose link store can never grow" / "permanently link-inert"), aligning the prose with the `dom(Σ.L)` statement that already follows it.

### Issue 2: the retraction section's central guarantee is grounded only by its failure mode
**ASN-0126, Retraction as an attributed Binary / Worked illustration**: single-tuple-scope for the Binary wrapper, `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`.

**Problem**: This is the retraction section's one new operational guarantee, and the section is careful that it is *not* automatic — it requires the unit-depth form **and** a P-tgt-valid target, and is declared an "app obligation." The worked illustration instantiates only the **failure** path: the ghost link-subspace root `a = d_retr.0.s_L` (= `1.1.0.1.0.1.0.2`) where P-tgt fails on both disjuncts and scope blows out to the whole subspace. There is no concrete instance confirming the **success** path. The reader gets the abstract three-move transfer plus a counterexample, but never sees a P-tgt-valid target concretely yield `{a}`.

**Required**: Add a short positive instance beside the ghost-root failure — e.g. `Nullify_Binary` aimed at the existing *leaf* `ℓ₁ = 1.1.0.1.0.1.0.2.1`, showing `{t : ℓ₁ ≼ t} ∩ A_rel^{Σ'} = {ℓ₁}` via R0a's antichain. The leaf-succeeds / interior-prefix-fails contrast is exactly what the "app obligation" claim turns on, so grounding both halves completes the section.

### Issue 3: the empty-from/Nullify exclusion is established, then re-established, deferring twice to the same downstream section
**ASN-0126, The shape-gated emit**: The empty-from-exclusion paragraph establishes "ASN-0086's `Nullify` ... is one such empty-from emit, so it too has no `→_sh` image. Retraction must therefore be re-expressed ... (Retraction as an attributed Binary)." The later operation-set paragraph then re-states "the empty-from `Nullify`, having no `→_sh` image (above), is *superseded* by the attributed-Binary wrapper `Nullify_Binary` (Retraction as an attributed Binary)."

**Problem**: The second paragraph re-derives the exclusion the first already proved and forward-points to the same section a second time; its only genuinely new content is the operation-set conclusion `{Emit_K, Observe_K, Nullify_Binary}`. This is the forward-reference-accretion pattern (two paragraphs deferring to one downstream location), flaggable at source per this note's anti-bloat classifier.

**Required**: Have the operation-set paragraph state its conclusion while leaning on the prior paragraph for the "`Nullify` is excluded / re-expressed" fact — drop the re-derivation and the repeated forward pointer.

## OUT_OF_SCOPE

### Topic 1: dynamic / runtime type registration
**Why out of scope**: The framework deliberately fixes the registry at `Σ_init` and proves it never drifts (P1); "no runtime registration to add one" is a stated non-goal. An app needing to register types after dynamics begin would require a *mutable-registry* variant — a separate framework carrying its own soundness obligations (drift, re-checking already-stored tuples) — not a revision of this immutable one.

### Topic 2: extension beyond F=1 / N=3, and the per-type predicate/behavior layer
**Why out of scope**: Open Questions 1–6 already route these (richer arity, idempotence, behavior catalog, default predicates, composition) to the successor note that layers operational semantics on this shape framework. They are correctly deferred, not gaps in this note.

Anti-bloat scan note (informational, not a required fix beyond Issue 3): the note is otherwise tight — the recent restructure shows; `effect-identity` is a genuinely reused named lemma, the "divergence cuts both ways" passage and the worked illustration are concrete examples (not meta-prose), and the B2-limitation, though restated once in Gate realizability, is load-bearing scaffolding that justifies proving P5 directly.

VERDICT: REVISE
