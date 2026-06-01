# Review of ASN-0047

## REVISE

### Issue 1: Worked example mis-attributes the source of the `k₀` / `n'_{s_C}` cut-point notation
**ASN-0047, *Worked example: interior content replacement* (opening sentence)**: "We trace the interior-position case of the content-replacement decomposition (K.μ⁻ + K.μ⁺ with `n'_{s_C} = k₀ − 1` rather than the single-position pair at `k₀ = n_{s_C}`) introduced in the *Elementary transitions* section."

**Problem**: The *Elementary transitions* section introduces no such notation. Its only statement about replacement is one sentence — "Replacement … is a *separate, range-changing* K.μ⁻ + K.μ⁺ composite, excluded from K.μ~ by its range-preservation clause." There is no `k₀`, no `n'_{s_C}`, and no "single-position pair" form there. The `k₀` cut-point notation (`n'_{s_C} = k₀ − 1 with 1 ≤ k₀ ≤ n_{s_C}`) is actually defined only in the *Decomposition of K.μ~* section, and there it parameterises K.μ~ *permutations*, not content replacement. The worked example borrows K.μ~'s cut-point notation, applies it to a non-K.μ~ composite, and falsely credits its introduction to a section that doesn't contain it. A reader following the back-reference to ground the notation finds nothing.

**Required**: Either introduce the `n'_{s_C} = k₀ − 1` content-replacement decomposition explicitly where the example claims it lives (the *Elementary transitions* replacement sentence), or correct the citation to point at the K.μ~ *Decomposition* section and state plainly that the example reuses that cut-point notation for the (distinct) range-changing replacement composite.

### Issue 2: Repeated exposition of the per-state / composite-boundary distinction
**ASN-0047, *Extended reachable-state invariants* and *Temporal decomposition***: The same per-state-invariant-vs-composite-boundary-property distinction is restated at least five times in different words: (a) the bulleted preamble ("Per-state invariants hold at every reachable state … Composite-boundary properties hold only at composite boundaries … may transiently fail"); (b) the `ExtendedReachableStateInvariants` statement itself; (c) the "Class (b) properties may transiently fail … recorded once in the … matrix" note; (d) the proof's opening ("The reachable-state property set partitions into two classes by temporal scope …"); and (e) the Class (b) header ("discharged at composite boundaries … not preserved by each elementary transition").

**Problem**: This is the "two paragraphs … say the same thing in different words" pattern compounded across one section. The distinction is load-bearing and deserves one precise statement, but the reader must skip past four re-statements to reach the actual matrix and per-property arguments. Each restatement adds wording, not reasoning.

**Required**: State the temporal-scope distinction once (the bulleted preamble is the natural home), and have the proof body and matrix preamble reference it rather than re-explain it.

### Issue 3: `P4` is referenced as a superseded property but never given a definition
**ASN-0047, *Definition (Current containment)* and the supersession table**: The text repeatedly treats `P4` as an existing property — "P4 would require `Contains(Σ) ⊆ R`", "P4★ supersedes P4 for the extended state", "In pre-extension states … P4★ reduces to P4" — and the *Local extensions* table lists `P4★` as superseding "This ASN's own P4 with subspace scoping."

**Problem**: `P4` has no formal statement box anywhere in this ASN. It exists only as a phrase ("`Contains(Σ) ⊆ R`") buried in a motivational paragraph, yet it is named, superseded, and reduced-to as if it were an established labelled property. A reader cannot locate the definition of a property the document explicitly says it is replacing.

**Required**: Either give `P4` a one-line formal statement (and label it as introduced-and-immediately-superseded), or drop the `P4` label entirely and speak directly of the unscoped bound `Contains(Σ) ⊆ R` that `P4★` refines. Do not carry a named-but-undefined property through the supersession table.

## OUT_OF_SCOPE

### Topic 1: Address-space exhaustion and fresh-address availability
**Why out of scope**: Whether `K.α`/`K.λ` can fail because no fresh address is available is a genuine question, but the ASN correctly defers it to the Open Questions (relying on T0(a)/T0(b) unboundedness in the abstract). This belongs to a future allocation-liveness ASN, not a revision here.

### Topic 2: Concurrency / serialization of same-document allocation
**Why out of scope**: `SequentialTransitionAxiom` makes transitions atomic and totally ordered, deferring concurrent-allocation guarantees to the Open Questions. This is future territory, not an error in the present model.

META: not applicable — the ASN defines abstract state, primitive transitions, and their invariants without drifting into implementation mechanics.

VERDICT: REVISE
