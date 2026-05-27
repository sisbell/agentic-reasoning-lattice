# Review of ASN-0099

## REVISE

### Issue 1: F9's multi-step extension conflates pure K.μ sequences with mixed sequences
**ASN-0099, F9 paragraph after the displayed claim**: "Across multi-step reachable sequences, link survivability is obtained by composing F9 over the K.μ-family steps and applying LP13 (UnconditionalLinkPersistence, ASN-0098) for the link-store-preserving guarantee across mixed step sequences."
**Problem**: F9 is single-step and asserts equality `findlinks(I, Σ) = findlinks(I, Σ')`. Two qualitatively different multi-step cases get folded into one sentence: (a) sequences containing only K.μ-family steps, where F9 composes inductively to give findlinks equality, and (b) mixed sequences containing K.λ steps, where findlinks may strictly grow (new matching links can join) and only persistence of *matching* links holds — that's F11's job, not F9's. The current wording suggests both cases are covered by composing F9 + LP13, which is incorrect for case (b).
**Required**: Split the multi-step claim. State that for K.μ-only sequences F9 composes inductively to give findlinks-equality. For mixed sequences, F11 gives persistence of matching links but not result-set equality.

### Issue 2: Determinism and survivability for filtered and scoped forms are never stated
**ASN-0099, F8, F9, and F14**: F8 and F9 are stated only for `findlinks(I, Σ)`. The filtered form `findlinks_filtered(C, Σ)` (introduced before F7) and the scoped form `findlinks_scoped(I, S, Σ)` (F14) admit analogous determinism and survivability properties by the same reasoning, but neither claim appears.
**Problem**: Implementations relying on filter or scope have no spec-level guarantee that their results are deterministic functions of `(Σ.L, C)` or `(Σ.L, I, S)`, nor that they survive K.μ-family edits unchanged. The omission is asymmetric across the operation's three forms.
**Required**: State determinism and survivability for `findlinks_filtered` and `findlinks_scoped` as corollaries of F8 and F9, or add a short paragraph noting the proofs transfer unchanged because the comprehension predicates depend only on `(Σ.L, ·)` and coverage is determined by `Σ.L`.

### Issue 3: F11's derivation double-counts LP13 + L6 and LP3★
**ASN-0099, F11 derivation paragraph**: "ASN-0098's LP13 ... gives the dom-and-value part directly ... From per-link value equality, per-slot endset equality follows by component-wise tuple equality on Link values (L6 ...). LP3★ (multi-step coverage invariance, ASN-0098) then lifts per-slot endset equality to per-slot coverage equality across the sequence ..."
**Problem**: Two paths to the same conclusion are stitched together. LP13 + L6 already gives per-slot endset equality across the sequence; coverage equality then follows from `coverage(·)` being a deterministic function of its endset argument. LP3★ alone independently gives both link persistence and per-slot coverage equality. The text casts LP3★ as "lifting endset equality to coverage equality" — but LP3★ doesn't lift anything; it's a stand-alone multi-step claim. The double-citation obscures which premise carries the work.
**Required**: Pick one path. Either (a) LP13 + L6 + coverage-as-function (path (a) is internally complete because LP13's full value equality gives slot-range alignment `|Σ.L(a)| = |Σ'.L(a)|` for the match existential), or (b) LP3★ alone with a brief note on slot-range. Remove the other citation.

### Issue 4: Worked example does not exercise F10 (ordering) or F14 (scope)
**ASN-0099, "A Worked Example"**: The example contains exactly one link `ℓ` and runs `findlinks_V` / `findlinks` without any filter or scope.
**Problem**: With one link, F10's canonical T1-sorted presentation is structurally trivial — the cross-document ordering machinery (CrossDocDisjointness, anchor-order lifting via T1 case (i)/(ii), PrefixOrderingExtension) is never exercised against a concrete instance. F14 and the filtered form's conjunctive semantics also stay untested. The standard's "concrete example verifies postconditions" requirement is met for F2, F3, F5, F6, F9, F11, F13 but skipped for F10 and F14.
**Required**: Add at least one additional link from a different home document (exercising cross-document T1 ordering of F10) and at least one filtered or scoped query (exercising F14's intersection and F7's filter conjunction).

### Issue 5: Empty-endset boundary case not discussed
**ASN-0099, F1 and surrounding text**: The match predicate is `(E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)`. L3 requires only the type-endset (slot 3) non-empty; other slots may be empty.
**Problem**: For a link with `Σ.L(a).e₁ = ∅`, slot 1 has coverage `∅` and never witnesses the existential. The match predicate handles this mechanically — other non-empty slots may still match — but the boundary is never named. A reader running a filtered query `{(1, I)}` will find no link with an empty from-endset, even when its to-endset overlaps `I`. That's a real distinction worth surfacing.
**Required**: Note in the match-predicate discussion that L3 permits empty endsets at non-type slots, that empty endsets cannot witness the slot existential, and that filtered queries naming such a slot exclude links whose slot is empty.

### Issue 6: Effect-clause exhaustivity is load-bearing but rests on an unwritten convention
**ASN-0099, F9 derivation**: "We surface effect-clause exhaustivity explicitly because it is load-bearing for F9 in the absence of explicit L' = L clauses in ASN-0047's K.μ⁺ and K.μ⁻ frames."
**Problem**: F9 for K.μ⁺ and K.μ⁻ rests on a convention — that operation effect clauses are exhaustive over modified state — that no foundation ASN formally establishes. The author is transparent about this and provides a closing enumeration argument, but the closure step still depends on the convention. The same convention is reinvoked in the worked example's Query 4. Future readers of F9 will have to re-derive their confidence in the convention each time.
**Required**: Either (a) get explicit `L' = L` clauses added to ASN-0047's K.μ⁺ and K.μ⁻ frames so F9 no longer depends on the convention, or (b) flag the dependency in F9's claim text so downstream consumers see the load-bearing premise, or (c) leave a tracking note pointing at the ASN-0047 gap.

## OUT_OF_SCOPE

### Topic 1: Multi-instance partition tolerance and consistency models
**Why out of scope**: The author explicitly notes the spec does not cover distributed link stores. Replication is also listed as out of scope at the review boundary.

### Topic 2: Access control formalization
**Why out of scope**: Access control composes with discovery as a scope filter without altering discovery semantics; correctly deferred.

### Topic 3: I→V resolution (FOLLOWLINK / RETRIEVEENDSETS)
**Why out of scope**: The inverse direction is a separate operation with its own subtleties (handling unmappped I-addresses, etc.) and belongs in its own ASN.

### Topic 4: Query semantics for addresses outside dom(Σ.C) ∪ dom(Σ.L)
**Why out of scope**: Author identifies as an open question. The match predicate is mechanically well-defined for any `I ⊆ T` but the operational meaning of phantom addresses is unresolved.

### Topic 5: Implementation-level index maintenance, durability, and atomicity protocols
**Why out of scope**: The abstract spec correctly stops at `result(I, Σ) = findlinks(I, Σ)` and leaves mechanism unconstrained.

### Topic 6: Concurrency model for K.λ during FINDLINKS evaluation
**Why out of scope**: ASN-0099 inherits ASN-0093's sequential-transition axiom; multi-reader / interleaved-write models are a separate concern.

### Topic 7: Time-bound guarantees on K.λ visibility
**Why out of scope**: "Without appreciable delay" is operational, not formal; "next query after K.λ" is the only abstract handle and the spec correctly stops there.

VERDICT: REVISE
