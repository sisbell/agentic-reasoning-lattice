# Review of ASN-0086

The mathematical content holds up under scrutiny. I verified R0a (both home-cases), R-Scope (both P-tgt branches), the two wp derivations, and the worked-sketch arithmetic (Steps 0–4, including the self-nullification in Step 4 and the non-fixpoint in Step 3) — all sound. Edge cases (first emission from empty store, full-slice nullification, self-targeting, self-emit) are covered, and CoverageEqualityDecidable's cell argument is correct including the empty-gap skip. The findings below are the meta-prose the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Emit_K definition repeats two facts three times
**ASN-0086, Definition — Emit_K**: Para 1 — "Emit_K is a function: the address is a = a_emit(Σ, d), the value Σ'.L(a) = (F, G, K) is fixed ... and K.λ's Frame fixes the rest"; Para 2 — "Emit_K is operationally K.λ of ASN-0093, specialized to the standard-triple link value (F, G, K)"; Effect — "invokes K.λ at home d with value (F, G, K). The fresh address is a = a_emit(Σ, d) ...".

**Problem**: "address = a_emit(Σ, d)" appears in Para 1 and Effect; "Emit_K is K.λ specialized to (F, G, K)" appears in Para 2 and Effect. Para 1 and Para 2 are largely subsumed by the Precondition/Effect/Frame block. A reader following the definition re-reads the same two claims in different words — exactly the "two paragraphs say the same thing" pattern.

**Required**: Collapse to the standard Precondition/Effect/Frame block plus a single one-line note ("Emit_K is K.λ specialized to value (F, G, K); the address a_emit and the function/totality properties follow from R0").

### Issue 2: Worked Sketch front-matter is a use-site inventory of what the labeled steps already state
**ASN-0086, Worked Sketch (opening)**: "the cycle proceeds in five steps: first, a first-emission step ... then a retraction (Step 1), a restoration (Step 2) ..." followed by "Step 0 exercises K.λ's first-emission branch (predicate ...); Steps 1, 2, 3, and 4 each exercise the subsequent-emission branch (predicate negated)."

**Problem**: Each step already carries a heading naming what it exercises (e.g., "Step 1: Nullify a₁", "Step 3 — Retracting the retractor exhibits R6b's non-fixpoint semantics", and each step states its own branch predicate explicitly). The two front-matter sentences are a use-site inventory duplicating those labels — the precise reader skips them.

**Required**: Drop the second sentence (the branch inventory) entirely; trim the roadmap sentence to at most a one-clause orientation, since the step headers carry the structure.

### Issue 3: "RT-closure" names a trivial closure property and the reachability framing overlaps
**ASN-0086, Working domain — →*-reachable states**: "This class is closed under → by construction — the reflexive-transitive closure absorbs each further →-step — so every emission from a →*-reachable state lands again in the class. We name this fact RT-closure."

**Problem**: "the reflexive-transitive closure absorbs each further →-step" is the definition of a reflexive-transitive closure restated as an explanation; closure of an RTC under one more step is not a fact needing naming. The surrounding clause overlaps the preceding "Definition — Reachability." The name RT-closure is cited later, so a label is fine, but the explanatory gloss is filler.

**Required**: Keep the RT-closure label as a one-liner ("RT-closure: the class is closed under →") and delete the "absorbs each further →-step" gloss.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs Observe and the cardinality bound on nullified(Σ)
**Why out of scope**: These are correctly posed in Open Questions; the substrate here is single-serialized (SequentialAtomicTransitions, ASN-0093), so a consistency model for concurrent Observe and a structural ratio bound on `|nullified(Σ)|/|dom(Σ.L)|` belong in a later ASN, not as defects in this one.

VERDICT: REVISE
