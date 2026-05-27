# Review of ASN-0099

## REVISE

### Issue 1: Implementation Notes section is borderline scope
**ASN-0099, "Implementation Notes (Non-Normative)"**: The section discusses index maintenance and crash-durability obligations.
**Problem**: Per the review standard, "if the ASN specifies implementation mechanics rather than system guarantees, it has drifted." Even labelled non-normative, including index-maintenance guidance in an abstract spec blurs the boundary. A reader scanning the ASN for the system's guarantees encounters implementation suggestions intermixed with normative content.
**Required**: Trim to one sentence noting that conformance = F2 ∧ F3 and that the spec is index-agnostic; move the index/durability discussion to a separate implementation guide or strike it.

### Issue 2: The unfiltered=union identity uses misleading infinite indexing
**ASN-0099, "Endset Filtering"**: "`findlinks(I, Σ) = ⋃_{i ∈ ℕ⁺} findlinks_filtered({(i, I)}, Σ)`"
**Problem**: The union is indexed over ℕ⁺ but only finitely many terms are non-empty (bounded by max link arity). The accompanying two paragraphs work to defend the notation, but the underlying object is a finite union with a clean finite bound. The current presentation invites a reader to think infinite iteration is intrinsic.
**Required**: State as `⋃_{i = 1}^{N} findlinks_filtered({(i, I)}, Σ)` where `N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}` when `dom(Σ.L) ≠ ∅` (and `N = 0` otherwise, with the empty union being `∅`). The well-definedness then needs no defense — finite by construction.

### Issue 3: Worked example doesn't exercise filtered/scoped variants or monotonicity claims
**ASN-0099, "A Worked Example"**: Queries 1–7 exercise F2, F3, F5, F6, F7(b), F8, F9, F10, F11, F13, F14.
**Problem**: F4 (PartialOverlapSuffices), F7(a) (slot symmetry), F12 (TwoPhaseFactoring), F15 (filtered determinism), F16 (scoped determinism), F17 (filtered survivability), F18 (scoped survivability), F19 (result-set monotonicity), F20 (image set-additive) are not directly exercised. The example is the only concrete verification surface; an implementer should see each named claim instantiated at least once.
**Required**: Add brief verifications: F15 against Query 5's filtered query at Σ vs. Query 7's Σ''; F17 against Query 5's filtered query across Query 4's K.μ⁻; F19 against a Σ → Σ' sequence with a K.λ that introduces a new matching link (showing the result strictly grows); F20 by splitting one of the existing V-region queries into two disjoint sub-regions. F4 and F7(a) can be flagged as implicit in Queries 1–3.

### Issue 4: A1 axiom is a meta-axiom workaround for ASN-0047
**ASN-0099, "Arrangement Independence"**: A1 (EffectClauseExhaustivity) reads ASN-0047's silence on `L` in K.μ⁺ and K.μ⁻ frames as `L' = L`.
**Problem**: A1 is a meta-axiom about *how to read* published specifications, not a substantive axiom about the system. It is fragile under the closure assumption — any future operation added to the substrate must explicitly state its L-behavior, or A1 silently weakens. The ASN itself flags this as an open question. Worse, A1 is also load-bearing for K.ρ (which has no `L' = L` in its ASN-0047 frame), but the ASN never names K.ρ in this connection — see Issue 6 below.
**Required**: Either (a) propose a concrete amendment to ASN-0047 adding `L' = L` to K.μ⁺, K.μ⁻, and K.ρ frames, and rewrite F9's K.μ⁺/K.μ⁻ cases to cite the amended frame directly; or (b) restate A1 as a property of the *currently published* vocabulary with an explicit closure premise, and name every operation that depends on A1 (currently K.μ⁺, K.μ⁻, K.ρ) so the dependency is visible. The current treatment buries the dependency in F9 alone.

### Issue 5: F10's cross-document ordering claim is potentially misleading
**ASN-0099, "Result Ordering"**: "sorting link addresses within a single home document by T1 yields exactly the order in which they were allocated" — followed by cross-document derivation.
**Problem**: The within-document chronological property is true and well-derived. But the cross-document ordering material that follows establishes T1-order = lexicographic order of home tumblers, which is NOT chronological allocation order across the system. Two documents on different accounts could allocate links in any temporal interleaving; the result presentation sorts by document-tumbler, not by K.λ event time. A reader who carries the "creation order" intuition from the within-document case to the cross-document case will form a wrong mental model.
**Required**: After the cross-document derivation, add one sentence: "Across documents, T1 ordering reflects the lexicographic order of home tumblers, NOT the chronological order of K.λ events. Within a home document, T1 = K.λ order; across home documents, T1 is canonical and deterministic but not chronological."

### Issue 6: F9 doesn't cover K.ρ (and other non-K.μ, non-K.λ operations)
**ASN-0099, "Arrangement Independence"**: F9 names only K.μ-family as preserving findlinks.
**Problem**: K.σ, K.α, K.δ explicitly state `L' = L` in their frames; K.ρ does not (its ASN-0047 frame omits L, requiring A1). All of these preserve findlinks by F8 + frame analysis (or F8 + A1 for K.ρ), but no named claim states it. K.ρ is particularly load-bearing: a reader applying the ASN should be able to look up "does K.ρ affect link discovery?" and find an explicit answer. Currently the answer is "by F8 + A1, no" but the reader has to derive this.
**Required**: Add a unified corollary to F9: "By F8 + frame analysis, every operation in the substrate other than K.λ preserves `findlinks(I, ·)` for any fixed `I`. K.σ, K.α, K.δ, K.μ~, K.μ⁺_L have `L' = L` in their published frames; K.μ⁺, K.μ⁻, K.ρ preserve `L` via A1. Only K.λ may add to the result set; F19 ensures the addition is monotone." This surfaces every dependency on A1 in one place.

## OUT_OF_SCOPE

### Topic 1: Distributed / multi-instance semantics
**Why out of scope**: Explicitly flagged in "What We Have Not Specified" and Open Questions. The single-state setting is the right level of abstraction.

### Topic 2: Access control composition
**Why out of scope**: Noted as orthogonal to discovery. The scope filter (F14) accommodates composition without formal treatment.

### Topic 3: Inverse direction (FOLLOWLINK / RETRIEVEENDSETS)
**Why out of scope**: Explicitly belongs to a future ASN.

### Topic 4: Phantom I-addresses (query I-sets containing addresses outside `dom(C) ∪ dom(L)`)
**Why out of scope**: The mechanical behavior is well-defined; the operational meaning is explicitly deferred. Match predicate is address-set agnostic.

### Topic 5: Index implementations and durability guarantees
**Why out of scope**: Implementation territory. The "Implementation Notes" section is itself borderline (see Issue 1).

### Topic 6: Time bounds on K.λ → result visibility
**Why out of scope**: Beyond the abstract sequential-transition model. "Next query after K.λ" is the only abstract handle.

### Topic 7: Concurrent K.λ + FINDLINKS semantics
**Why out of scope**: Requires a concurrency model not present in the foundation ASNs.

VERDICT: REVISE
