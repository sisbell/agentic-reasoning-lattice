# Review of ASN-0099

## REVISE

### Issue 1: F4's "Any other refinement" hedging contradicts itself
**ASN-0099, F4 (MatchFormulaUniqueness)**: "a hypothetical strengthening like 'P fires only for endsets with finite coverage' would reject every canonical-span instance whether F1 fires or not (canonical-span coverages are always infinite prefix subtrees), so the abstract minimality still holds — such a P excludes F1-admitted pairs at every canonical-span shape — but the witness exhibiting the exclusion would need to be of a non-canonical form, outside the construction used above."

**Problem**: This is internally contradictory. If P "excludes F1-admitted pairs at every canonical-span shape," then any canonical-span pair on which F1 fires *is itself* a witness to the exclusion — F1 admits the pair, P rejects it, done. Take the first witness construction (`coverage = {t : α ≼ t}`, `I = {α}`): F1 fires (intersection `{α}` non-empty), the coverage is infinite, so "P fires only on finite coverage" rejects. That pair witnesses F1-admits / P-rejects without leaving the canonical-span construction. The ASN's claim that a "non-canonical form" would be required is wrong. Either remove the hedging or replace the "finite coverage" example with one where canonical witnesses genuinely fail — e.g., a strengthening that agrees with F1 on every canonical-span pair but diverges on a non-canonical pair (the prose seems to be reaching for this shape but doesn't land it).

**Required**: Correct or delete the hedging paragraph. The abstract minimality argument that follows ("any predicate `P` that fails on some `(a, I)` pair admitted by F1 ... defines a different match predicate") is sound on its own; the muddled example weakens rather than strengthens the case.

### Issue 2: F4 witness realizability under-cited
**ASN-0099, F4**: "Each witness is realizable through canonical spans of the form `(α, δ(1, #α))`. By L4 (ASN-0043), endset spans may reference any addresses in T..."

**Problem**: The witnesses describe *link configurations* — a link `a` with a specified slot `i` holding a specified endset. For F4 to demonstrate uniqueness via concrete witnesses, the witness states must be realizable. L4 only establishes that endset spans can reference any address; it does not establish that links with arbitrary endset configurations can be instantiated in a conforming state. The actual realizability premises live in L9 (TypeGhostPermission — existence of conforming extensions with arbitrary arity ≥ 3) and L11b (NonInjectivity — multiple addresses may store the same link value), both in ASN-0043. The ASN cites neither.

**Required**: Cite L9 and L11b alongside L4 in the realizability sentence, or briefly note that the canonical-span configurations used by the witnesses are realizable as link values in conforming states extending any base `Σ` (which is exactly what L9 supplies).

### Issue 3: F12 labeled as a theorem but stated as a definition
**ASN-0099, F12 (TwoPhaseFactoring)**: "`findlinks_V(R, d, Σ) ≡ findlinks(image(R, d, Σ), Σ)`"

**Problem**: `findlinks_V` is not defined anywhere else in the ASN. F12 is the sole definition. Yet F12 is presented in the same labeled-claim format as F1–F11, suggesting a theorem to be derived. The Claims table line "F12 | Two-phase factoring: `findlinks_V` composes `image` (V→I) and `findlinks` (I→Link)" reinforces the theorem reading. The pedagogical text supports a definitional reading ("The factoring matters because the two phases have entirely different stability properties"). The downstream derivations of F6 and the V-side additivity for `findlinks_V` consume F12 as a definitional unfolding, not as a substantive identity.

**Required**: Either explicitly label F12 as a definition (and adjust the surrounding prose), or precede F12 with a direct definition of `findlinks_V` and reframe F12 as a structural observation about that definition. The current presentation conflates the two roles.

## OUT_OF_SCOPE

### Topic 1: Multi-step preservation across `V ∖ {K.λ}` sequences
**Why out of scope**: F9★ covers the K.μ-only multi-step case; F19 covers monotone subset across any reachable sequence. The equality version across full `V ∖ {K.λ}` sequences (lifting F9-cor by transitivity) would be a natural next claim — *but* F11 + F19 together give the operationally-required content, and the K.μ-only restriction in F9★ reads as a deliberate scoping choice ("the editing surface against which links must remain findable"). Not a defect in this ASN.

### Topic 2: V-side determinism statement
**Why out of scope**: F8 supplies I-side determinism abstractly; V-side determinism for `findlinks_V` follows from F12 plus determinism of `image` (function of `Σ.M(d)` alone), but is not stated as a labeled claim. The omission is reasonable because the V-side variant adds nothing new beyond F12 + F8 + the elementary observation that `image` is `Σ.M`-deterministic. Could be added but not required for completeness of the I-side specification.

VERDICT: REVISE
