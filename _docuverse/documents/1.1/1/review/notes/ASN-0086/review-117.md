# Review of ASN-0086

The mathematical core is sound: R0–R6c, the wp analyses, and the worked example check out, and the four-conjunct wp in Case 2 is genuinely weakest. The issues are concentrated in the forward-reference meta-prose the anti-bloat classifier targets, plus one naming collision.

## REVISE

### Issue 1: Forward-reference non-circularity justification in R0a-Cor1
**ASN-0086, R0a-Cor1 proof**: "The contiguous-prefix form follows from conformance clause (b) alone, by induction on the conformance-witnessing transition sequence ...; the argument never invokes R0a, so the forward reference in R0a Case 2 is non-circular."
**Problem**: This is the explicitly-flagged "prose justifies document ordering / the forward pointer is non-circular by Y argument" pattern. The non-circularity is a fact about citation order, not about what R0a-Cor1 claims; a reader following the contiguity induction must skip past it.
**Required**: Delete the clause. If circularity is a genuine hazard, reorder the lemmas so R0a-Cor1 precedes R0a; the proof then stands without the disclaimer.

### Issue 2: Use-site inventory in "Definition — state-local-conforming state"
**ASN-0086, Definition — state-local-conforming state**: "This restriction is load-bearing: R0's freshness derivations invoke L1c (to obtain `T4-valid(ℓ_prev)`), and the function-ness of Emit_K invokes L-fin (so the homed-`max` exists), and the full `↝*` space need not preserve either."
**Problem**: A definition's introduction enumerating its downstream consumers (R0, Emit_K) — flagged pattern. The definition's *meaning* is the four-way containment already stated; the consumer list belongs at the consuming sites (R0 already cites L1c; Emit_K function-ness already cites L-fin), where it is in fact repeated.
**Required**: Cut the "load-bearing" sentence. The containment `{→*-reachable} ⊆ {substrate-conforming} ⊆ {state-local-conforming} ⊆ {↝*-reachable}` and the witness suffice to define the set.

### Issue 3: ASN-0040 seed contrast in EmptyInitialLinkStore
**ASN-0086, Assumption — EmptyInitialLinkStore**: "This differs deliberately from ASN-0040's seed `B₀`, which is permitted to be non-empty; we make no use of a non-empty seed."
**Problem**: Essay content justifying a design choice rather than advancing the assumption's content. The assumption is `dom(Σ_init.L) = ∅`; whether ASN-0040 permits otherwise does not change what this note assumes.
**Required**: Remove the parenthetical contrast. If the empty-root choice needs grounding, the `initmagicktricks` sentence already supplies it.

### Issue 4: `P2`/`P2c` subscript collision across Nullify and wp Case 1
**ASN-0086, Definition — Nullify vs. WP Case 1**: Nullify lists "(P2) `|Σ.L(a)| = 3`"; wp Case 1 introduces "P2c: `Σ substrate-conforming`" and then states "The scope condition P2 (`|Σ.L(a)| = 3`) is consequently absent from the wp."
**Problem**: Two distinct conditions share the `P2` stem within a few paragraphs (P0/P1 are shared and consistent; only the third differs). A reader tracking the precondition labels must disambiguate `P2` (arity) from `P2c` (conformance) by content, not label.
**Required**: Rename the conformance conjunct to a non-`P2` label (e.g., `PC`), so the wp's conjuncts do not collide with Nullify's scope conditions.

## OUT_OF_SCOPE

### Topic 1: Interaction of `L_K` with non-empty arrangements
**Why out of scope**: The note correctly inherits ASN-0093's M2 (EmptyArrangement) and scopes out arrangement modification; the `L_K`/`Σ.M` visibility question is already named in Open Question 1 and belongs to a successor ASN that admits arrangement-modifying transitions.

### Topic 2: Higher-arity typed relations (`|Σ.L(a)| > 3`)
**Why out of scope**: Restricting `L^Σ` to standard triples is a stated boundary, and Open Question 2 reserves the `L_K^{(n)}` generalization. Nullify's arity-3 scoping (P2) and the single-tuple-scope arity-independence remark together leave the higher-arity case cleanly deferred, not broken.

VERDICT: REVISE
