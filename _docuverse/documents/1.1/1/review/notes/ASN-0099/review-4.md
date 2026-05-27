# Review of ASN-0099

## REVISE

### Issue 1: F9 derivation relies on an unstated "standing convention"
**ASN-0099, Arrangement Independence section**: "By the standing convention that operations modify only what their effect clauses name, `L` is unchanged at K.μ⁺ and K.μ⁻ steps."

**Problem**: F9 (LinkSurvivabilityUnderEdits) requires `Σ.L = Σ'.L` at every K.μ-family transition. For K.μ~ and K.μ⁺_L this follows from their published frames (`L' = L` is listed). For K.μ⁺ and K.μ⁻, however, the frame clauses in ASN-0047 do NOT list `L' = L`:
- K.μ⁺ frame: `C' = C; E' = E; (A d' : d' ≠ d : M'(d') = M(d')); R' = R` — L absent
- K.μ⁻ frame: `C' = C; E' = E; R' = R; (A d' : d' ≠ d : M'(d') = M(d'))` — L absent

The derivation patches this via a "standing convention" that is not cited from any foundation. L12 (LinkImmutability) gives only `dom(Σ.L) ⊆ dom(Σ'.L)` with existing values preserved — it does NOT establish `dom(Σ'.L) ⊆ dom(Σ.L)`, so K.μ⁺/K.μ⁻ could (under a strict frame reading) add new links to `dom(L)`, which would falsify F9. The convention is then re-invoked in Query 4 of the worked example, making it load-bearing for the entire link survivability result.

**Required**: Either (a) state the "effect-clause closure" convention as an explicit axiom in this ASN, or (b) derive `Σ.L = Σ'.L` for K.μ⁺/K.μ⁻ by enumerating the link-modifying operations as exactly {K.λ} and arguing completeness of the enumeration, or (c) flag the gap as a dependency on a revision of ASN-0047 to publish `L' = L` in the K.μ⁺ and K.μ⁻ frames.

### Issue 2: Worked example mis-computes coverage of canonical spans
**ASN-0099, A Worked Example section**:
- "Slot 1 (from-endset): one canonical span `(α₂, δ(1, #α₂))`, so `coverage(Σ.L(ℓ).e₁) = {α₂}` by PrefixSpanCoverage (ASN-0043)."
- "Slot 2 (to-endset): one canonical span `(α₃, δ(1, #α₃))`, so `coverage(Σ.L(ℓ).e₂) = {α₃}`."

**Problem**: PrefixSpanCoverage (ASN-0043) says `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}` — the set of tumblers extending `x`, NOT the singleton `{x}`. The actual coverage of the slot-1 endset is `{t : α₂ ≼ t}`, which strictly contains `α₂` and all its prefix-extensions (`α₂.0`, `α₂.1`, `α₂.0.0`, …). No canonical (or any other) single span can have coverage equal to a singleton — every span is a half-open interval of width ≥ 1 under T1, and the smallest such interval contains the start tumbler together with its entire prefix-subtree.

The error propagates through Query 1 (`{α₂} ∩ {α₂} = {α₂}`), Query 3 (`{α₂} ∩ {α₂, α₃} = {α₂}`), Query 4, and the F5/F13 verifications. The final query results are correct (singleton intersections collapse the same way), but the intermediate derivations shown are mathematically incorrect, and a future reader could conclude that canonical spans have singleton coverage.

**Required**: Rewrite the worked example with correct coverage values. The correct chain for Query 1 reads `{t : α₂ ≼ t} ∩ {α₂} = {α₂}` (since `α₂ ≼ α₂` by reflexivity, and no other element of `{α₂}` extends `α₂`). For Query 3, slot-1 reads `{t : α₂ ≼ t} ∩ {α₂, α₃} = {α₂}` (since `α₂ ⋠ α₃` by last-component disagreement). The same correction is needed throughout.

### Issue 3: Slot-out-of-range convention is not folded into the definition
**ASN-0099, Endset Filtering section**: The definition `findlinks_filtered(C, Σ) = {a ∈ dom(Σ.L) : (A (i, J) ∈ C : coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}` references `Σ.L(a).eᵢ` for arbitrary `i ∈ ℕ⁺`. By L6 (ASN-0043), `Σ.L(a).eᵢ` is defined only for `i ∈ {1, …, |Σ.L(a)|}`. The text discusses a convention ("`coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅` is *false* whenever `i > |Σ.L(a)|`") but the formal definition does not incorporate this. As written, the definition is not well-formed when `C` contains a constraint `(i, J)` with `i > |Σ.L(a)|` for some `a ∈ dom(Σ.L)`.

**Required**: Fold the convention into the definition explicitly:
```
findlinks_filtered(C, Σ) = {a ∈ dom(Σ.L) : (A (i, J) ∈ C :
  i ≤ |Σ.L(a)| ∧ coverage(Σ.L(a).eᵢ) ∩ J ≠ ∅)}
```

### Issue 4: F12 preconditions should be stated explicitly
**ASN-0099, F12 (TwoPhaseFactoring)**: "findlinks_V(R, d, Σ) = findlinks(image(R, d, Σ), Σ)."

**Problem**: `findlinks_V` is defined by composition with `image`, which is partial (defined only when `d ∈ dom(Σ.M)` and `R ⊆ dom(Σ.M(d))`). The preconditions are inherited but not restated. A reader could miss that `findlinks_V(R, d, Σ)` is undefined when these preconditions fail.

**Required**: Add a `defined when` clause to F12 making the preconditions explicit, mirroring `image`'s presentation:
```
findlinks_V(R, d, Σ)
  defined when  d ∈ dom(Σ.M) ∧ R ⊆ dom(Σ.M(d))
  ≡             findlinks(image(R, d, Σ), Σ)
```

### Issue 5: Finite-non-empty terms in the filter recovery should be noted
**ASN-0099, Endset Filtering section**: "The right-hand side is therefore well-defined as a union over ℕ⁺: each link enters finitely many terms (bounded by its own arity)..."

**Problem**: The argument correctly notes that each link enters finitely many terms, but doesn't observe that only finitely many indices `i` make `findlinks_filtered({(i, I)}, Σ)` non-empty in total — specifically, `i ∈ {1, …, max{|Σ.L(a)| : a ∈ dom(Σ.L)}}` when `dom(Σ.L) ≠ ∅`. Without this observation, the infinite union notation could mislead a reader into thinking the computation is unbounded.

**Required**: Add one sentence noting that only finitely many terms in the union are non-empty (since `dom(Σ.L)` is finite by L-fin and each link has finite arity), so the infinite union has a finite effective range.

## OUT_OF_SCOPE

### Topic 1: Phantom address queries
**Why out of scope**: The ASN flags in "What We Have Not Specified" that the operational meaning of querying with addresses outside `dom(Σ.C) ∪ dom(Σ.L)` is unsettled. The match predicate works mechanically on any `I ⊆ T`, but the semantics for phantom queries belongs to a future ASN.

### Topic 2: Multi-instance / distributed link store
**Why out of scope**: Partition tolerance and consistency models across multiple physical instances are explicitly flagged as future work.

### Topic 3: Caching mechanisms
**Why out of scope**: The ASN deliberately specifies the result, not the procedure. Index design and cache coherence are outside the abstract specification.

### Topic 4: Access control composition
**Why out of scope**: Detailed access control formalization is noted as orthogonal to discovery semantics and belongs to a future ASN.

### Topic 5: I→V resolution (FOLLOWLINK)
**Why out of scope**: The inverse direction — resolving the result's endsets back to V-positions — is explicitly delegated to FOLLOWLINK/RETRIEVEENDSETS.

### Topic 6: Concurrent / interleaved query semantics
**Why out of scope**: Consistency with concurrent K.λ operations is flagged as an open question; the single-state setting under SequentialTransitionAxiom is what this ASN covers.

### Topic 7: Performance / appreciable-delay bounds
**Why out of scope**: The ASN explicitly leaves performance bounds unspecified.

### Topic 8: Cross-document V-region queries
**Why out of scope**: `findlinks_V(R, d, Σ)` is single-document by design. The set-additive property F13 lets callers compose per-document images for cross-document queries; a unified multi-document signature is a natural future extension.

VERDICT: REVISE
