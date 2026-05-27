# ASN-0099: FINDLINKS Operation

*2026-05-26*

## The Reader's Question

A reader looks at a stretch of content and asks: *what connects here from elsewhere?* This is one half of the Xanadu reader-side promise — that the literature is bidirectionally navigable, and that backlink discovery from the rest of the docuverse must be answerable on demand (Nelson, *Literary Machines* 2/46: "without appreciable delay"). The reader knows only what they see: arranged content at V-positions in some document `d`. They do not see I-addresses directly, do not see the content store, do not see other documents' arrangements, and they certainly do not see the link store. The links the reader wants live in `dom(Σ.L)` at element-level tumbler addresses (L1, ASN-0043), with endsets referencing content I-addresses (L3) rather than V-positions. The arrangement `Σ.M(d)` bridges V-coordinates to I-coordinates.

## A Two-Phase Factoring

The question splits cleanly into two phases.

**Phase 1 (V→I).** Given a document `d ∈ dom(Σ.M)` and a query region `R ⊆ T`, produce the *I-image* of the region:

```
image(R, d, Σ)
  defined when  d ∈ dom(Σ.M)
  ≡             {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}
```

The single precondition `d ∈ dom(Σ.M)` is load-bearing so that `Σ.M(d)` is defined. V-positions in `R` that are absent from the arrangement contribute nothing to the image — silent projection is the only treatment that leaves the operation total over `R ⊆ T` for a fixed allocated document.

**Phase 2 (I→Link).** Given a set of I-addresses `I ⊆ T`, produce the set of links whose endsets intersect `I`:

```
findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}
```

The two phases compose into the reader-facing operation:

```
F12 (TwoPhaseFactoring) — DEFINITION of findlinks_V:
   findlinks_V(R, d, Σ)
     defined when  d ∈ dom(Σ.M)
     ≡             findlinks(image(R, d, Σ), Σ).
```

F12 is a definition; the "F12" label is a citation handle so downstream derivations can name the definitional unfolding. For `d ∉ dom(Σ.M)`, `findlinks_V(R, d, Σ)` is *undefined* — no silent fallback. For V-positions in `R` outside `dom(Σ.M(d))`, the silent projection in `image` absorbs them; the caller has no pre-validation obligation beyond establishing `d ∈ dom(Σ.M)`.

The factoring matters because the two phases have different stability properties. `Σ.M` is mutable (K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L all modify it); `Σ.L` is monotonic (K.λ adds, L12 forbids modification of existing entries). Phase 1 consults the mutable component; phase 2 consults the monotonic component.

## The Image Set

`R` is unconstrained beyond `R ⊆ T` — single position, contiguous V-span, or any subset. When `R` is a contiguous V-span in subspace `s_C`, ASN-0058's mapping-block decomposition gives the image as a union of disjoint I-runs, one per maximal correspondence run. When `v ∈ R` has `subspace(v) = s_L`, S3★ (ASN-0047) routes `Σ.M(d)(v) ∈ dom(Σ.L)` and the image picks up a link address. The match predicate accepts this without modification: endsets may reference any addresses in `T` (L4, ASN-0043), so the link subspace is admissible as a coverage target.

## The Match Predicate

```
F1 (MatchPredicate):
   matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅).
```

F1 generalizes ASN-0098's `discoverable_from(a, d, Σ) = matches(a, ran(Σ.M(d)), Σ)`. The existential ranges uniformly over all slots, including the type-endset and any further slots: L7 (ASN-0043) leaves directional significance to the link type, and the reader's question — *what connects here?* — does not privilege from over to. Intersection (rather than containment) is forced by symmetry: a link is about every byte its endsets cover (L13), one shared byte suffices, and to require containment in either direction would impose a circular precondition (the reader would need to know each link's extent to know whether to include it in the query).

```
F4 (MatchFormulaMinimality):
   F1's slot-existential / singleton-overlap form is the unique match
   predicate that, when wired into F2 ∧ F3, produces conformance with
   the reader's promise. F2 forbids strengthenings (which would miss
   F1-admitted matches); F3 forbids weakenings (which would return
   non-F1 links). The uniqueness is operational: any predicate
   disagreeing with F1 on a realizable (a, I) pair defines a different
   operation.
```

*Realizability discharge.* Any predicate `P` disagreeing with F1 on some pair `(a, I)` defines a different operation, provided that disagreement is realizable in a conforming state. We close the realizability gap universally. From any base state `Σ` with `dom(Σ.M) ≠ ∅` — itself reachable from `Σ₀` by two K.δ steps (account, document) — K.λ admits, at any such state, allocation of a link with arity `N ≥ 3` whose endset tuple `(e₁, …, e_N)` is freely chosen subject only to K.λ's well-formedness preconditions (`eᵢ ∈ Endset`, `e₃ ≠ ∅`). L4 (ASN-0043) places no constraint on which addresses the spans reference. The query I-set `I ⊆ T` is a query parameter, not state, so any `I` is admissible. Therefore every F1-admitted `(endset configuration, I)` pair is realizable by a K.λ allocation under any document. Witness chain index `k ≥ 2` requires `k − 1` prior K.λ steps under the same document (each step advances the chain by one); the prior endsets are immaterial to the witness's match status. The three illustrative refutations below — containment, reverse containment, cardinality threshold — are concrete instances of this universal realization at canonical-span coverage shapes.

*Containment from coverage to query (`coverage ⊆ I`).* Witness: slot `i` with one canonical span `(α, δ(1, #α))`, so `coverage = {t : α ≼ t}` (by PrefixSpanCoverage, ASN-0043), and `I = {α}`. Then `coverage ∩ I = {α} ≠ ∅` (F1 admits), but `coverage ⊄ I` since `α.0 ∈ coverage` (any tumbler extending `α` belongs by T0's allowance of trailing zeros) while `α.0 ∉ I`. Strengthening excludes `a`.

*Containment from query to coverage (`I ⊆ coverage`).* Same canonical span; `I = {α, γ}` for any `γ ∈ T` with `α ⋠ γ` (e.g., a same-length sibling differing at position `#α`). Then `coverage ∩ I = {α} ≠ ∅` (F1 admits), but `I ⊄ coverage` since `γ ∉ coverage`. Strengthening excludes `a`.

*Cardinality threshold (`|coverage ∩ I| ≥ k` for `k > 1`).* Same canonical span; `I = {α}`. Then `|coverage ∩ I| = 1 < k` for every `k > 1`. F1 admits via singleton overlap; threshold strengthening excludes `a`.

The reader's promise rests on the singleton-overlap reading: one shared byte is one shared byte. Alternative match formulas are alternative operations, not alternative implementations of FINDLINKS.

**Empty endsets at non-type slots.** L3 requires only slot 3 to be non-empty; other slots may carry `∅`. Then `coverage(∅) = ∅` and the slot is never a witness — but other non-empty slots may witness the existential. The filtered form (below) behaves differently: a filter constraint `(i, J)` is unsatisfiable at a link with `Σ.L(a).eᵢ = ∅`. Two distinct short-circuits for an unsatisfied per-constraint conjunct: when `i > |Σ.L(a)|` the slot is structurally absent; when `i ≤ |Σ.L(a)| ∧ Σ.L(a).eᵢ = ∅` the slot exists but its endset carries no spans. Both routes exclude the link; abstract conformance is indifferent to which fires.

## Endset Filtering

A *slot constraint* is a pair `(i, J)` with `i ∈ ℕ⁺`, `J ⊆ T`. A link satisfies the constraint iff its slot `i` exists and the coverage at that slot meets `J`. The positional accessor is undefined for `i > |Σ.L(a)|` (L6), so we fold the out-of-range case into an explicit guard:

```
findlinks_filtered(C, Σ)
  = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

The from-to query is `{(1, I_from), (2, I_to)}`; the three-endset query adds `(3, I_type)`; a type-only restriction is `{(3, I_type)}`. The filtered form is *not* a strict generalization: the unfiltered match is an existential over slots, the filtered match a universal over constraints. The unfiltered form is recovered as a finite union over single-slot filters:

```
findlinks(I, Σ) = ⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)
   where N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}  when dom(Σ.L) ≠ ∅
         N = 0                              when dom(Σ.L) = ∅  (empty union = ∅)
```

`L-fin` gives `|dom(Σ.L)| < ∞` so the max is well-defined when the link store is non-empty.

```
F7 (EndsetSymmetry):
   (a) Slot symmetry: matches(a, I, Σ) consults all slots uniformly.
   (b) Filter conjunction: findlinks_filtered(C, Σ) intersects per-slot
       constraints — a link must satisfy every constraint to appear.
```

Both halves follow from the quantifier structure of the definitions: existential ⇒ slot-symmetric; universal ⇒ conjunctive.

## Completeness

The defining obligation is *completeness*: every link in `dom(Σ.L)` satisfying the match predicate must appear in an implementation's output. Let `result : 𝒫(T) × 𝒮 → 𝒫(T)` denote a conforming implementation's output function, where `𝒮` is the Xanadu system state space (states of the form `Σ = (C, L, M, E, R, …)` from ASN-0036, ASN-0043, ASN-0047, ASN-0093). The signature commits the implementation to functionality (equal arguments yield equal outputs).

```
F2 (Completeness):  findlinks(I, Σ) ⊆ result(I, Σ).
F3 (Soundness):     result(I, Σ) ⊆ findlinks(I, Σ).
```

Together F2 ∧ F3 force `result(I, Σ) = findlinks(I, Σ)`. The same conformance contract transfers to the filtered, scoped, and V-side forms, each with its own `result_*` function functional in its arguments and pinned to the corresponding abstract specification:

```
F2-filt ∧ F3-filt:  result_filtered(C, Σ)    = findlinks_filtered(C, Σ).
F2-sco  ∧ F3-sco:   result_scoped(I, S, Σ)   = findlinks_scoped(I, S, Σ).
F2-V    ∧ F3-V:     result_V(R, d, Σ)        = findlinks_V(R, d, Σ),
                    for every (R, d, Σ) with d ∈ dom(Σ.M).
```

Each pair carries the same structure as F2 ∧ F3, with the predicate adjusted to the operation: the universal `(A (i, J) ∈ C : …)` for the filtered form, the intersection `dom(Σ.L) ∩ S` for the scoped form, and the I-image `image(R, d, Σ)` for the V-side form. F2-V ∧ F3-V is the **primary obligation on `result_V`**: any implementation exposing the V-side surface must satisfy it. When the implementation also exposes the I-side surface satisfying F2 ∧ F3, the factoring equation `result_V(R, d, Σ) = result(image(R, d, Σ), Σ)` follows by F2 ∧ F3 + F2-V ∧ F3-V + F12, since both sides equal `findlinks_V(R, d, Σ)` exactly; the two surfaces are then coherently linked through F12's definitional unfolding. An implementation may compute the V-side result by routing through `result` internally or by a direct procedure — but the conformance contract is fixed at F2-V ∧ F3-V.

*Predicate domain.* `matches(a, I, Σ)` is defined only for `a ∈ dom(Σ.L)`. The scoped form's `a ∈ dom(Σ.L) ∩ S` clauses (in F2-sco's universal and F3-sco's conclusion) keep every invocation inside the domain; F2-V and F3-V respect the convention by quantifying over `a ∈ dom(Σ.L)`. The boundary case `a ∈ S ∖ dom(Σ.L)` is operationally excluded by F3-sco.

Completeness must hold *unconditionally* with respect to `dom(Σ.L)`. No early termination, sampling, or remote-latency exclusion. Soundness's dual force: no false positives from stale indexes. A conforming implementation's index, if any, remains in lockstep with the link store.

## Determinism and Comprehension Invariance

The result depends only on the link store and the query specification:

```
F8 (Determinism):
   findlinks(I, Σ) = findlinks(I, Σ')  whenever Σ.L = Σ'.L.
```

F8 is a property of the abstract operation; the implementation-side consequence `result(I, Σ) = result(I, Σ')` follows from F8 by F2 ∧ F3.

F8 is one instance of a structural pattern that recurs throughout this ASN: every claim of the form "the comprehension is unchanged when `Σ.L = Σ'.L`" rests on the same derivation chain. We name it once so downstream claims (F11, F15, F17, F19, F19-filt, and related variants) can cite it as a discrete step.

```
ComprehensionInvariantUnderΣL — meta-lemma:
   If Σ.L = Σ'.L as partial functions, then for every comprehension
   over dom(Σ.L) whose membership predicate consults only Σ.L and
   query-data (never Σ.M, Σ.C, Σ.E, Σ.R):
       {a ∈ dom(Σ.L) : P(a, Σ)} = {a ∈ dom(Σ'.L) : P(a, Σ')}.

   The chain: Σ.L = Σ'.L gives dom(Σ.L) = dom(Σ'.L) and per-link
   value equality Σ.L(a) = Σ'.L(a). Component-wise tuple equality on
   Link values (L6) gives |Σ.L(a)| = |Σ'.L(a)| and per-slot endset
   equality Σ.L(a).eᵢ = Σ'.L(a).eᵢ. Coverage is a deterministic
   function of its endset argument, so per-slot coverage agrees.
   Predicates built from these — F1's existential, the filtered
   form's universal, scoped intersection — evaluate identically at
   the two states. Set extensionality closes the equality.
```

F8 is the instance for F1's existential; F15 is the instance for the filtered universal; F11, F17, F19, F19-filt each invoke the same chain against the substitution `Σ' = post-state of a transition preserving Σ.L`.

## Arrangement Independence

The I→Link phase consults `Σ.L` and `I` alone. F8 already encodes this. The operationally salient frame condition exercised by editing operations rests on a structural lemma of the substrate: that operations other than K.λ preserve `Σ.L`. Five of the eight non-allocating operations list `L' = L` in their published frames; three (K.μ⁺, K.μ⁻, K.ρ) omit `L` from the published frame. We package the preservation lemma:

```
A1 (LinkStoreInertOfNonAllocatingOperations):
   For every transition Σ → Σ' produced by an operation in V ∖ {K.λ}:
       dom(Σ'.L) = dom(Σ.L) ∧ (A a ∈ dom(Σ.L) :: Σ'.L(a) = Σ.L(a)).
   Equivalently, K.λ is the unique operation of V that modifies the
   link store.

   A1 is the union of:
   - A1a (published-frame preservation, covering {K.σ, K.α, K.δ, K.μ~,
     K.μ⁺_L}): conclusion immediate from the substrate's published
     `L' = L` frame clause. No interpretive commitment.
   - A1b (closed-world preservation, covering {K.μ⁺, K.μ⁻, K.ρ}):
     conclusion derived from the substrate's effect-clause convention
     under the closed-world reading — components absent from both
     effect and frame are unchanged. The reading is adopted
     methodologically by this ASN; the substrate spec does not
     formally axiomatise it. Downstream citations at K.μ⁺, K.μ⁻, or
     K.ρ inherit this convention-grounded commitment.

   Vocabulary scope: V = {K.σ, K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L,
   K.ρ} as published in ASN-0047 and ASN-0093. Downstream ASNs
   consuming A1 against an evolved vocabulary must restate the claim.
```

For grounding of the closed-world reading and its alternatives, see the [design note appendix](#appendix-grounding-of-the-closed-world-reading) below.

```
F9 (LinkSurvivabilityUnderEdits):
   For any single-step transition Σ → Σ' produced by a K.μ-family
   operation (K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L) and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   F9 follows from F8 via ComprehensionInvariantUnderΣL once
   Σ.L = Σ'.L is discharged: by A1a at K.μ~ and K.μ⁺_L, by A1b at
   K.μ⁺ and K.μ⁻. F9 inherits A1b's commitment at the latter two
   sub-cases.
```

```
F9-cor (NonAllocatingPreservation):
   For every single-step transition Σ → Σ' produced by an operation
   in V ∖ {K.λ} and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   F9-cor inherits A1b's commitment at the K.μ⁺, K.μ⁻, K.ρ sub-cases;
   the other five operations discharge from A1a. K.δ has three
   sub-cases; the IsDocument sub-case modifies M(d_new) but K.δ's
   published frame includes L' = L uniformly, so F9-cor's I-side
   conclusion holds for all three.
```

```
F9★ (NonAllocatingMultiStepPreservation):
   For any reachable transition sequence Σ →* Σ' in which every step
   is in V ∖ {K.λ} and any I ⊆ T:
       findlinks(I, Σ) = findlinks(I, Σ').

   The per-step F9-cor chained by transitivity of equality.
```

(The K.μ-only specialization of F9★ is the one-line corollary: every K.μ-family step is in V ∖ {K.λ}, so any K.μ-only sequence is one for which F9★ applies; we do not name it separately.)

K.λ is the only operation of V that can change `findlinks(I, ·)` across a single step, and F19 below confirms the change is monotone.

## Transclusion Transparency

```
F6 (TransclusionTransparency):
   For documents d₁, d₂ ∈ dom(Σ.M) and V-positions v₁ ∈ dom(Σ.M(d₁)),
   v₂ ∈ dom(Σ.M(d₂)) with Σ.M(d₁)(v₁) = Σ.M(d₂)(v₂) = α:
       findlinks_V({v₁}, d₁, Σ) = findlinks_V({v₂}, d₂, Σ).
```

`image({v₁}, d₁, Σ) = {α} = image({v₂}, d₂, Σ)` (the silent projection survives the singleton on both sides since both V-positions are in their respective arrangement domains). By F12, both V-side queries unfold to `findlinks({α}, Σ)`, which by functional determinism is one set. The match consulted only the I-image and the link store; the document of origin vanished from the computation.

A link created against `α`'s native location is found via any document that transcludes `α`. The link belongs to its home document by L1a, but its *findability* is at the I-address.

## Identity, Not Value

```
F5 (IdentityNotValue):
   matches(a, I, Σ) consults dom(Σ.L), Σ.L, and coverage(·), never
   Σ.C(·). For distinct α ≠ β, matches(a, {α}, Σ) and
   matches(a, {β}, Σ) are computed independently — each decided by
   address-level membership in coverage(Σ.L(a).eᵢ), with no reference
   to content values.
```

If two users write the same string at different I-addresses, links to one are not links to the other. Identity comes from origin (GlobalUniqueness, ASN-0034) and is preserved through every operation touching the content store (P0, ASN-0047); discovery builds on this foundation, not on content equivalence.

## Composite Queries

```
F13 (SetAdditive):
   findlinks(I₁ ∪ I₂, Σ) = findlinks(I₁, Σ) ∪ findlinks(I₂, Σ).
```

By distributivity of intersection over union, `coverage(e) ∩ (I₁ ∪ I₂) = (coverage(e) ∩ I₁) ∪ (coverage(e) ∩ I₂)`, non-empty iff at least one disjunct is non-empty.

```
F20 (ImageSetAdditive):
   For d ∈ dom(Σ.M) and R₁, R₂ ⊆ T:
       image(R₁ ∪ R₂, d, Σ) = image(R₁, d, Σ) ∪ image(R₂, d, Σ).
```

The standard image-of-union identity for the partial function `Σ.M(d)`. V-side additivity for `findlinks_V` then follows from F12 + F20 + F13 directly.

## The Empty Query

For `I = ∅`: every `coverage(e) ∩ ∅ = ∅`, so the slot-existential never witnesses; `findlinks(∅, Σ) = ∅`. Symmetrically `image(∅, d, Σ) = ∅`, and a V-region `R` entirely disjoint from `dom(Σ.M(d))` gives `findlinks_V(R, d, Σ) = ∅`.

When `dom(Σ.L) = ∅` (the initial state, before the first K.λ), every query produces `∅`. F2, F3, F10, F11, F19 all hold vacuously.

For `findlinks_filtered`: the empty constraint set `C = ∅` makes the universal vacuously true at every link, so `findlinks_filtered(∅, Σ) = dom(Σ.L)`. The empty constraint target — any `(i, J) ∈ C` with `J = ∅` — makes that per-constraint conjunct false everywhere, so the filtered result is `∅`.

For `findlinks_scoped(I, ∅, Σ) = findlinks(I, Σ) ∩ ∅ = ∅` by F14.

## Scope

```
F14 (ScopeFilter):
   findlinks_scoped(I, S, Σ) = findlinks(I, Σ) ∩ S
                             = {a ∈ dom(Σ.L) ∩ S : matches(a, I, Σ)}
```

Natural choices for `S`: "all links in document `d`" (`{a : home(a) = d}`), "all links by user `u`", or any access-control narrowing.

The determinism and survivability properties extend uniformly to the filtered and scoped forms:

```
F15 (FilteredDeterminism):  findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ') when Σ.L = Σ'.L.
F16 (ScopedDeterminism):    findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ') when Σ.L = Σ'.L.
F17 (FilteredSurvivability): findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ') across a K.μ-family step.
F18 (ScopedSurvivability):   findlinks_scoped(I, S, Σ) = findlinks_scoped(I, S, Σ') across a K.μ-family step.
```

F15 follows from ComprehensionInvariantUnderΣL applied to the filtered universal. F16 follows from F8 + intersection-preservation with the query-supplied `S`. F17 follows from F9 (K.μ-family preserves Σ.L) + F15. F18 follows from F9 + intersection-preservation. F17 and F18 inherit A1b's commitment at the K.μ⁺ and K.μ⁻ sub-cases.

## Result Ordering

The result is a set, but the reader is shown an ordered list. We adopt T1's lexicographic order on tumbler addresses:

```
F10 (OrderedResult):
   The result set admits a unique presentation as a sequence
   ⟨a₁, a₂, ..., aₙ⟩ with aⱼ ∈ dom(Σ.L) satisfying matches(aⱼ, I, Σ),
   and a₁ < a₂ < ... < aₙ under T1.
```

Finiteness: F3 gives `result(I, Σ) ⊆ dom(Σ.L)`; L-fin gives `|dom(Σ.L)| < ∞`. T1 is a strict total order on `T` and so restricts to one on any subset. Any non-empty finite totally-ordered set admits a unique enumeration by finite induction. The canonical filtered and scoped presentations follow by the same finiteness + total-order argument:

```
F10-filt:  findlinks_filtered(C, Σ) admits a unique strictly T1-increasing sequence.
F10-sco:   findlinks_scoped(I, S, Σ) admits a unique strictly T1-increasing sequence.
```

The presentation order recovers a creation-order property within each home document. We surface the equivalence as a sub-lemma so F10's derivation can cite it cleanly:

```
ChainIndexEqualsAllocationOrder — sub-lemma:
   For any document d ∈ dom(Σ.M) and any link addresses
   ℓ₁, ℓ₂ ∈ dom(Σ.L) with home(ℓ₁) = home(ℓ₂) = d:
       ℓ₁ < ℓ₂ under T1  ⟺  ℓ₁ was allocated before ℓ₂ under d.

   Proof: ChainMembershipForOrigin (ASN-0093) places
   dom(L) ∩ {ℓ : home(ℓ) = d} as a contiguous prefix {t₁, ..., t_{m_d}}
   of A_L(d)'s enumeration, where t_i = inc^{i-1}(t_1, 0).
   ChainEnumerationInjectivity (ASN-0093) gives strict T1-ordering
   t₁ < t₂ < ... < t_{m_d} (via TA5(a) per-step and T1 transitivity).
   K.λ's subsequent-emission precondition pins each new allocation
   under d to ℓ = inc(max{prior emissions}, 0) = t_{m_d + 1}, so the
   chain index equals the K.λ event count under d at allocation time.
   The three identifications — chain index, K.λ event count, T1 rank
   within A_L(d) — agree.
```

For the cross-document part of F10's ordering:

```
F10a (AnchorLiftingOfDocumentOrdering):
   For documents d₁, d₂ ∈ dom(Σ.M) with zeros(d₁) = zeros(d₂) = 2
   (M0, ASN-0093) and d₁ < d₂ under T1, the link sub-allocator
   anchors satisfy b_L(d₁) < b_L(d₂) under T1 and are non-nesting
   under ≼. By PrefixOrderingExtension (ASN-0034), every ℓ₁
   extending b_L(d₁) is strictly less than every ℓ₂ extending b_L(d₂).

   *Case (i) (component divergence on documents).* The divergence
   position k ≤ min(#d₁, #d₂) with d₁_k < d₂_k carries over to
   b_L(d₁) vs b_L(d₂) at the same position. T1 case (i) at position k
   yields b_L(d₁) < b_L(d₂). Anchors are non-nesting by strict
   component disagreement at k.

   *Case (ii) (proper prefix on documents).* d₁ ≺ d₂ with
   #d₁ < #d₂ forces d₂_{#d₁+1} ≥ 1 (M0's zeros(·) = 2 excludes a zero
   at the extension), while b_L(d₁) has the appended 0 separator from
   b_L(·) = [·.0.s_L] at position #d₁ + 1. T1 case (i) at position
   #d₁ + 1 yields b_L(d₁) < b_L(d₂). Anchors non-nest at #d₁ + 1.
```

ChainMembershipForOrigin places every `ℓ` with `home(ℓ) = d` in `A_L(d)`, and ChainPrefixExtension (ASN-0093) gives `b_L(d) ≼ ℓ`. For `d₁ < d₂`, F10a lifts to `b_L(d₁) < b_L(d₂)` non-nesting, and PrefixOrderingExtension lifts to every extension. Under T1, link addresses with the same `home(·)` group together as a contiguous T1-block; blocks for distinct documents sort by their documents' tumblers. T1's strict total order on the finite set `dom(Σ.L)` chains the pairwise inequalities into the unique total order without inductive case analysis: T1 itself is the chaining mechanism.

Chronological reading: within a home document T1 = K.λ order (by ChainIndexEqualsAllocationOrder); across home documents T1 reflects the lexicographic order of home tumblers, not the operation-history order of K.λ events.

## Persistent Discoverability

```
F11 (PersistentDiscoverability):
   For any reachable state sequence Σ →* Σ' and any a ∈ dom(Σ.L) with
   matches(a, I, Σ):  a ∈ dom(Σ'.L) ∧ matches(a, I, Σ').
```

LP13 (UnconditionalLinkPersistence, ASN-0098) supplies the multi-step per-link guarantee `a ∈ dom(Σ'.L) ∧ Σ'.L(a) = Σ.L(a)`. ComprehensionInvariantUnderΣL's chain then gives per-slot coverage equality at `Σ` and `Σ'`, so the F1 existential evaluates identically — the witness slot found at Σ remains a witness at Σ'.

A link is permanently discoverable for any query I-set overlapping any of its endset coverages. Editing the documents around it, contracting the V-positions arranging its referenced content, transcluding the content into new documents — none alter the link's match status against a fixed I-set.

```
F19 (ResultSetMonotonicity):
   findlinks(I, Σ) ⊆ findlinks(I, Σ') for every reachable Σ →* Σ'.
```

Direct from F11 + the definition of `findlinks`. Monotonicity propagates to the filtered and scoped forms:

```
F19-filt: findlinks_filtered(C, Σ) ⊆ findlinks_filtered(C, Σ').
F19-sco:  findlinks_scoped(I, S, Σ) ⊆ findlinks_scoped(I, S, Σ').
```

F19-filt follows from LP13 + ComprehensionInvariantUnderΣL applied to the filtered universal: each per-constraint conjunct continues to hold at `Σ'` since `Σ'.L(a) = Σ.L(a)` for every `a` already in `dom(Σ.L)`. F19-sco follows from F19 + intersection-preservation with the query-supplied `S`.

F19 (and its filtered/scoped variants) is the load-bearing consequence behind any indexed implementation's promise: an index that mirrors `findlinks` is never required to remove entries as the state evolves, only to add them.

## A Worked Example

We fix a small instance. State `Σ` has two documents in `dom(Σ.M)`:

- `d_a`: content-bearing. `A_C(d_a)` has produced `α₁ = [d_a.0.s_C.1]`, `α₂ = [d_a.0.s_C.2]`, `α₃ = [d_a.0.s_C.3]`, each with content values `v₁, v₂, v₃ ∈ Val`. Arrangement: `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}` with `v_a^k = [s_C, k]` of depth 2.
- `d_b`: transcludes `α₂, α₃` from `d_a`. Arrangement: `Σ.M(d_b) = {v_b^1 ↦ α₂, v_b^2 ↦ α₃}` with `v_b^k = [s_C, k]`. We assume `d_b = inc(d_a, 0)`, the next sibling document under the same account, so `d_a < d_b`.
- Type-tumbler addresses `τ_comment, τ_reply, τ_meta` allocated under a separate registry document `d_τ` non-nesting with `d_a` and `d_b`.
- Three links: `ℓ ∈ A_L(d_a)` with slot 1 `(α₂, δ(1, #α₂))`, slot 2 `(α₃, δ(1, #α₃))`, slot 3 `(τ_comment, δ(1, #τ_comment))`; `ℓ' ∈ A_L(d_b)` with slot 1 `(α₃, ·)`, slot 2 `(α₁, ·)`, slot 3 `(τ_reply, ·)`; `ℓ_meta = inc(ℓ', 0) ∈ A_L(d_b)` with slot 1 `(ℓ, δ(1, #ℓ))` (annotation on `ℓ`), slot 2 `∅`, slot 3 `(τ_meta, ·)`.

By PrefixSpanCoverage, each canonical span's coverage is a prefix subtree. The three subtrees over `α₁, α₂, α₃` are pairwise disjoint (siblings with disagreeing final components); the subtrees over `τ_·` are pairwise disjoint and disjoint from content addresses (cross-document non-nesting); `{t : ℓ ≼ t}` is disjoint from any `{t : αᵢ ≼ t}` by subspace separation (`ℓ` has `s_L` at position `#d_a + 2`; each `αᵢ` has `s_C` there). Under T1, `ℓ < ℓ' < ℓ_meta` (cross-document by F10a; within `d_b` by ChainIndexEqualsAllocationOrder).

**Query 1 (basic match): `findlinks_V({v_a^2}, d_a, Σ)`.** Phase 1: `image({v_a^2}, d_a, Σ) = {α₂}`. Phase 2: at `ℓ`, slot 1's coverage `{t : α₂ ≼ t}` meets `{α₂}` in `{α₂}` (reflexivity of `≼`), so `matches(ℓ, {α₂}, Σ) = true`. At `ℓ'`, no slot's coverage meets `{α₂}` (sibling content-address mismatches; type τ-disjoint). At `ℓ_meta`, slot 1 covers `{t : ℓ ≼ t}` (subspace-disjoint from `{α₂}`), slot 2 is empty, slot 3 is τ-disjoint. Result: `{ℓ}`. This exercises F1's singleton-overlap reading (slot 1 alone witnesses; no strengthening of the intersection condition would let `ℓ` qualify against a singleton `I`) and F7(a)'s slot symmetry.

**Query 2 (F6, transclusion transparency): `findlinks_V({v_b^1}, d_b, Σ)`.** `image({v_b^1}, d_b, Σ) = {α₂}` — the same image as Query 1, because `d_b`'s transclusion of `α₂` produces the same I-address. Phase 2 is identical. Result: `{ℓ}`. The reader querying `d_b`'s view of `α₂` discovers the same link as via `d_a`'s native arrangement: identity travels with the I-address.

**Query 3 (F7, filtered conjunction): `findlinks_filtered({(1, {α₂}), (2, {α₃})}, Σ)`.** "Links from `α₂` to `α₃`". At `ℓ`: slot 1 meets `{α₂}`, slot 2 meets `{α₃}`; both constraints hold. At `ℓ'`: slot 1 covers `{t : α₃ ≼ t}`, intersected with `{α₂}` is `∅` (since `α₃ ⋠ α₂`); the slot-1 constraint fails, the universal fails, `ℓ'` excluded — even though `ℓ'`'s slot 1 *does* meet `{α₃}` (which would have satisfied a slot-1 constraint had we named the to-set under slot 1). At `ℓ_meta`: slot 1 is subspace-disjoint from `{α₂}`; the slot-1 constraint fails. Result: `{ℓ}`. Contrast with the union-form unfiltered query `findlinks({α₂} ∪ {α₃}, Σ) = {ℓ, ℓ'}` — the filtered form is strictly stricter, exercising F7(b)'s filter conjunction.

**Query 4 (cross-subspace, F12 with link-image): `findlinks_V({v_a^L}, d_a, Σ_L)`.** First, perform a K.μ⁺_L transition on `d_a` extending its arrangement with `v_a^L := [s_L, 1]` mapping to `ℓ` (the K.μ⁺_L preconditions are satisfied: `ℓ ∈ dom(Σ.L)`, `origin(ℓ) = d_a`, `ℓ ∉ ran(Σ.M(d_a))`, `v_a^L` is the canonical depth-2 minimum). Call the post-state `Σ_L`; `Σ_L.L = Σ.L` by A1a. Phase 1 at `v_a^L`: `image({v_a^L}, d_a, Σ_L) = {ℓ}` — the image is the *link address* `ℓ`, a member of `dom(Σ_L.L)`. Phase 2: at `ℓ_meta`, slot 1's coverage `{t : ℓ ≼ t}` meets `{ℓ}` in `{ℓ}` (reflexivity), so `matches(ℓ_meta, {ℓ}, Σ_L) = true`. At `ℓ` and `ℓ'`, no slot's coverage extends `ℓ` (subspace/τ-disjointness). Result: `{ℓ_meta}`. The reader selecting a V-position in the link subspace discovers the meta-link annotating `ℓ`. The match predicate is address-agnostic: it consults coverage and overlap, indifferent to whether the image's elements inhabit `dom(C)` or `dom(L)`. S3★'s cross-subspace routing of V-positions to `dom(L)` (ASN-0047) feeds naturally into F1.

**Query 5 (F9★, multi-step preservation across V ∖ {K.λ}).** From `Σ`, apply a five-step sequence touching `M`, `C`, `R`, and arrangement contraction — every state component the substrate non-allocating fragment can modify:

  (i) K.δ case (ii) at `k = 0` from `d_b` creates `d_c = inc(d_b, 0)` (K.δ-ID.zeros-0/1: `zeros(d_c) = 2`, so `IsDocument(d_c)`; K.δ effect places `d_c ∈ Σ_1.E_doc` and `Σ_1.M(d_c) = ∅`). K.δ's published frame names `L' = L` (A1a): `Σ_1.L = Σ.L`.

  (ii) K.α allocates `α_c = [d_c.0.s_C.1]` with value `v_c`. K.α's published frame (A1a): `Σ_2.L = Σ_1.L`.

  (iii) K.μ⁺ extends `Σ_2.M(d_c)` with `v_c^1 ↦ α_c`. K.μ⁺'s frame omits `L`; by A1b, `Σ_3.L = Σ_2.L`.

  (iv) K.ρ records `(α_c, d_c) ∈ R`. K.ρ's frame omits `L`; by A1b, `Σ_4.L = Σ_3.L`.

  (v) K.μ⁻ contracts `Σ_4.M(d_a)` to `{v_a^1 ↦ α₁}`. K.μ⁻'s frame omits `L`; by A1b, `Σ_5.L = Σ_4.L`.

Transitivity yields `Σ.L = Σ_5.L`. F8 forces `findlinks(I, Σ) = findlinks(I, Σ_5)` for every `I ⊆ T`. At `I = {α₂}`: `findlinks({α₂}, Σ) = {ℓ}` (Query 1) and `findlinks({α₂}, Σ_5) = {ℓ}` by direct evaluation (link values preserved by L12; the slot-1 test at `ℓ` still meets `{α₂}`). The V-side answer at `v_a^2` in `d_a` does change across the chain (the K.μ⁻ step contracts `v_a^2` out of `dom(M(d_a))`, so `findlinks_V({v_a^2}, d_a, Σ_5) = findlinks(∅, Σ_5) = ∅`); the I-side answer at the fixed I-set `{α₂}` does not. F9★ holds across the chain.

## What Completeness Demands of Implementations

The spec's demand is exactly F2 ∧ F3: `result(I, Σ) = findlinks(I, Σ)`. The mechanism is unspecified. Any implementation whose `result(I, Σ)` differs from the set comprehension is non-conforming, regardless of cause.

## Local Atomicity and the Single-State Setting

By SequentialTransitionAxiom (ASN-0093), every state transition is atomic and uninterruptible; `Σ` is well-defined at every query point. A K.λ commits `a` to `dom(Σ.L)` atomically: by the time the K.λ committing `a` returns, `a` is in `dom(Σ.L)` and the next query at any state succeeding the K.λ must include `a` if `a` matches. There is no intermediate state in which `a` exists in `dom(Σ.L)` but is undiscoverable.

Implementations that defer index maintenance to a background process create a window in which the index lags the link store; during that window, results from the index would violate F2. The abstract specification permits no such window. Nelson's design intent at LM 2/46 — backlinks returnable "without appreciable delay" — is the reader-experience commitment behind this; no foundation invariant of this ASN formalises a timing bound beyond "next query after K.λ commitment reflects the link".

## What We Have Not Specified

- The procedure by which the operation is computed.
- Behavior across multiple physical instances of the link store; partition tolerance; consistency models.
- Caching.
- Access control beyond noting it as an orthogonal scope filter.
- The inverse direction (resolving result endsets back to V-positions) — that is FOLLOWLINK/RETRIEVEENDSETS.
- The semantics of querying with I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)`.
- A combined filtered-and-scoped operation `findlinks_filtered_scoped(C, S, Σ)`. The intended composition is naive intersection `findlinks_filtered(C, Σ) ∩ S`; determinism, survivability, and monotonicity propagate pointwise from the per-component claims.

## Reflection

The discovery operation reduces to a single set comprehension: take the I-set the user named, test each link's endset coverage for overlap, return the matches. Complexity in real systems lies in implementation — index maintenance, server propagation, access control, large-endset storage. The abstract specification is just the comprehension.

The specification is spare because of design choices established for other reasons. Because links attach to bytes (L13), discovery is by address overlap. Because bytes carry permanent identity (S0, C0), the overlap is well-defined and stable. Because arrangement is separated from identity (S9), discovery is arrangement-independent. Because the address space is globally unique (T10), identity-based queries cannot collide across owners. Because the link store is monotonic (L12), discovery is monotone. None of these were established for discovery; discovery falls out of them.

## Appendix: Grounding of the Closed-World Reading

This appendix records design-rationale for A1b — methodological, not normative.

A1b adopts the closed-world reading of the substrate's effect-clause convention: components absent from both effect and frame are preserved across the transition. ASN-0047 does not formally axiomatise this convention; A1b adopts it as the methodological default for this ASN's evaluation of silent frames.

*Convergent grounding (non-constitutive).* Two outside-the-foundation sources converge with — but do not constitute — the closed-world reading.

(i) Nelson's design intent in *Literary Machines* requires operations to preserve state they do not explicitly modify: the Istream is append-only ("user makes changes, the changes difflessly into the storage system, filed, as it were, chronologically" at 2/14), edits are non-destructive ("users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals" at 2/45), and modification is restricted to the owner ("Only the owner has a right to withdraw a document or change it" at 2/29).

(ii) Gregory's udanax-green implementation leaves the link store unmodified across operations corresponding to K.μ⁺ (INSERT), K.μ⁻ (DELETE / `dodeletevspan`), and K.ρ (DOCISPAN insertion via `docopy`).

Both are *convergent* with A1b's conclusion but not constitutive; the methodological commitment remains primary because the substrate spec does not formally axiomatise the convention.

*Why not a substrate revision.* Publishing `L' = L` explicitly in the three silent frames of ASN-0047, or axiomatising the closed-world convention as a substrate-level meta-axiom, would discharge A1b directly. We prefer the local methodological commitment in ASN-0099 for two reasons: (1) *scope* — revising ASN-0047 is a substrate-level amendment whose impact extends to every consumer of the operation vocabulary, and ASN-0099 should not unilaterally commit the substrate to a convention other downstream ASNs may not need; (2) *separability* — tagging A1b with convention status keeps the interpretive commitment surfaced at the citation site of every claim depending on it, so a future substrate revision can replace A1b's convention-grounded reading with an axiomatised one cleanly. Readers who reject the closed-world reading must restate A1b against an alternative interpretation or weaken its conclusion at K.μ⁺, K.μ⁻, K.ρ.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| `image(R, d, Σ)` | I-image of a V-region with silent projection | definition |
| `findlinks(I, Σ)` | Discovery operation comprehension | definition |
| `findlinks_V(R, d, Σ)` | Two-phase composite (see F12) | definition |
| `findlinks_filtered(C, Σ)` | Filtered form with slot constraints | definition |
| `findlinks_scoped(I, S, Σ)` | Scoped form: `findlinks(I, Σ) ∩ S` | definition |
| ComprehensionInvariantUnderΣL | Meta-lemma: comprehensions over `dom(Σ.L)` with `Σ.L`-only predicates are invariant under `Σ.L = Σ'.L` | introduced (meta-lemma) |
| ChainIndexEqualsAllocationOrder | Within a home document, T1 rank = chain index = K.λ event count | introduced (sub-lemma) |
| A1a | PublishedFramePreservation: {K.σ, K.α, K.δ, K.μ~, K.μ⁺_L} preserve `Σ.L` from published frames | introduced (structural lemma) |
| A1b | ClosedWorldPreservation: {K.μ⁺, K.μ⁻, K.ρ} preserve `Σ.L` under closed-world reading of substrate effect-clause convention; convention-grounded | introduced (convention-grounded lemma) |
| A1 | LinkStoreInertOfNonAllocatingOperations: composite of A1a and A1b; K.λ unique L-modifying operation in V | introduced (composite lemma) |
| F1 | MatchPredicate definition | definition |
| F2 | Completeness: `findlinks(I, Σ) ⊆ result(I, Σ)` | introduced |
| F3 | Soundness: `result(I, Σ) ⊆ findlinks(I, Σ)` | introduced |
| F2-filt, F3-filt | Filtered conformance pair | introduced |
| F2-sco, F3-sco | Scoped conformance pair | introduced |
| F2-V, F3-V | V-side conformance pair (primary obligation on `result_V`) | introduced |
| F4 | MatchFormulaMinimality: F1 unique up to operational distinguishability | introduced |
| F5 | Identity, not value: match consults coverage, not content | introduced |
| F6 | Transclusion transparency | introduced |
| F7 | Endset symmetry (slot equality + filter conjunction) | introduced |
| F8 | Determinism: `findlinks(I, ·)` is a function of `(Σ.L, I)` | introduced |
| F9 | Link survivability under K.μ-family edits | introduced |
| F9-cor | Non-allocating preservation across single-step V ∖ {K.λ} | introduced |
| F9★ | Multi-step closure of F9-cor across V ∖ {K.λ} sequences | introduced |
| F10 | Ordered result: canonical T1-sorted presentation | introduced |
| F10-filt, F10-sco | Filtered and scoped ordered presentations | introduced |
| F10a | AnchorLiftingOfDocumentOrdering | introduced |
| F11 | Persistent discoverability across reachable sequences | introduced |
| F12 | TwoPhaseFactoring: `findlinks_V` definitional unfolding | definition |
| F13 | Set-additive in the I-input | introduced |
| F14 | Scope filter is intersection | introduced |
| F15, F16 | Filtered and scoped determinism | introduced |
| F17, F18 | Filtered and scoped survivability under K.μ-family | introduced |
| F19 | Result-set monotonicity across reachable sequences | introduced |
| F19-filt, F19-sco | Filtered and scoped monotonicity | introduced |
| F20 | Image set-additive | introduced |

## Open Questions

What semantics should the operation have when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`?

What completeness guarantees must hold when the link store is logically partitioned across multiple physical instances that may be temporarily disconnected?

What consistency model must FINDLINKS observe with respect to K.λ operations that may be concurrent with or interleaved with the query at a higher protocol layer?

How does access-control filtering compose with the completeness obligation — is completeness restated relative to the authorized scope, and what invariants must the access-control layer preserve to make the composition coherent?

What must an implementation maintain to make the completeness obligation auditable — is there a recoverable witness for every reachable state demonstrating that the index agrees with the link store?

Should the abstract specification require any bound on the time between K.λ commitment and the link's appearance in subsequent FINDLINKS results, or is "next query after K.λ" the only abstract handle available?

What is the relationship between FINDLINKS and the inverse direction (resolving the result's endsets back to V-positions in some target document), and what additional guarantees does the inverse direction require that FINDLINKS does not?

What is the minimum structural commitment any conforming substrate must make to the non-allocating fragment of its operation vocabulary in order to support link-discovery invariance under those operations?
