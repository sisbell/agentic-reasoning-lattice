# Review of ASN-0100

## REVISE

### Issue 1: Forward-reference deferral and document-ordering justification for INS.M-exhaustive
**ASN-0100, §The Operation: Formal Contract (Exhaustiveness clause)**: "*Exhaustiveness* (INS.M-exhaustive) — … (Justified in §Arrangement functionality, where it is first consumed.)"
**Problem**: The parenthetical justifies *where* the proof lives and *when* it is consumed rather than advancing the claim. This is the flagged forward-reference/ordering-justification pattern — the reader must hold the deferral and jump forward. The same deferral logic recurs at the end of §Effect Three ("The formal per-component frame clauses that pin these down appear under §The Operation: Formal Contract → Frame Conditions").
**Required**: State INS.M-exhaustive without the placement commentary; let the §Arrangement functionality proof stand on its own. Remove the "where it is first consumed" and "appear under §…" pointers.

### Issue 2: Identity-by-allocation restated three times
**ASN-0100, §Effect One / §INSERT vs. COPY / claim INS.identity**: "It *grows* `C` by appending fresh entries…" (Effect One) restated as "INSERT allocates *fresh* I-addresses for new content" and again "The defining structural difference is that INSERT allocates fresh I-addresses (INS.identity); COPY does not."
**Problem**: Two-plus paragraphs assert the same proposition in different words (flagged "two paragraphs saying the same thing"). The §INSERT-vs-COPY section in particular re-derives a point already fixed by INS.C and INS.alloc.
**Required**: Assert fresh allocation once (at INS.C/INS.alloc) and have the identity corollaries cite it rather than re-narrate it.

### Issue 3: Worked-example stipulation imagines out-of-scope pre-states
**ASN-0100, §A Worked Example**: "a pre-state reached through prior deletion or copy could map V-positions to non-contiguous I-addresses, and the projection instantiation would then read off `M(d)` directly rather than via the chain-shift identity."
**Problem**: DELETE and COPY mechanics are out of scope. The applicability condition for INS.chain-shift is "contiguous emissions of `A_C(d)`"; that condition stands on its own. Naming the excluded operations to motivate the stipulation is reviser drift (imagining a case the chain-shift carrier already excludes) and reaches into out-of-scope territory.
**Required**: State that INS.chain-shift requires a contiguous pre-state chain segment and that the worked example stipulates one; drop the deletion/copy speculation.

### Issue 4: Meta-prose explaining why a lemma does *not* apply
**ASN-0100, §Per-subspace span decomposition (S8★)**: "so existence is supplied not by M2 (DecompositionExistence; ASN-0058) — which is stated for whole arrangements — but by C1a (RestrictionDecomposition; ASN-0058)…"; and §Atomicity: "S4 ranges over `dom(C)`, not over E or `dom(M)`, so the 'no K.δ fires' frame reasoning above does not apply."
**Problem**: These explain why an *alternative* argument is inapplicable rather than making the argument. The reader does not need the rejected path narrated; citing C1a (or giving the S4 argument) suffices.
**Required**: Cite the operative lemma and discharge the obligation directly. Remove the "not by X which is stated for…" and "so the reasoning above does not apply" signposting.

### Issue 5: Worked example asserts "specialises INS.proj" without exhibiting π
**ASN-0100, §A Worked Example (Projection-shift correspondence)**: "We compute the post-state projection *directly* from the exhibited `M'(d)`… `project(ℓ, 1, d, Σ') = {[1,2], [1,5], [1,6]}`. … (This numeric instance specialises INS.proj.)"
**Problem**: The example computes both projections independently and narrates the tracking story, but never instantiates the INS.proj formula `π(project(…,Σ)) ∪ N_{ℓ,i}` numerically — i.e., it does not show `π(P_0^L) = {[1,2]}`, `shift(P_0^R, 2) = {[1,5],[1,6]}`, `N_{ℓ,1} = ∅` combining to the result. The depth standard asks the key postcondition (here INS.proj) be verified *against* the scenario, not merely reconciled.
**Required**: Exhibit the π-application and the `N_{ℓ,i} = ∅` step explicitly so the example verifies INS.proj's formula rather than asserting agreement.

## OUT_OF_SCOPE

### Topic 1: COPY contrast framing
**Why out of scope**: §"INSERT vs. COPY: Identity Through Allocation" frames a comparison with COPY, whose mechanics are out of scope. The *in-scope* content is the INSERT identity corollaries (INS.identity.crossdoc, .version, .tightsurv); the COPY contrast itself ("COPY does not", "two operations that may produce visually identical Vstream effects") is scaffolding that belongs in COPY's ASN. Retitle around INSERT's identity guarantees and let COPY be named only as the negative case in a single clause.

META: not needed — the ASN defines state effects, operations, and invariants of INSERT at the right level of abstraction; the findings are prose accretion and one example-depth gap, all fixable.

VERDICT: REVISE
