# Review of ASN-0053

The mathematics here is genuinely strong — every multi-case proof (SC exhaustiveness, S3, S9's six sub-cases, S11 tightness) is spelled out rather than waved through, boundary cases are handled, and the foundation citations (D0/D1/D2/TA-LC/TA-assoc) are discharged precondition-by-precondition. I checked the proofs and could not find a load-bearing gap. The findings below are the anti-bloat patterns the `review-mode.anti-bloat` classifier asks me to surface at source.

## REVISE

### Issue 1: Post-QED commentary in S4a restates the proof
**ASN-0053, S4a**: "Level-uniformity is what makes the recovery exact: it guarantees #s = #reach(σ), so WR recovers the merged width exactly as ℓ, and the split-then-merge round-trip returns σ rather than an approximation."
**Problem**: The proof body already establishes exactly this ("The merged width is reach(σ) ⊖ s = reach(σ) ⊖ start(σ) = ℓ, by WR (σ is level-uniform). So γ = (s, ℓ) = σ"). The trailing sentence is the same claim in different words — the "two paragraphs say the same thing" pattern. A precise reader must verify it adds nothing, then discard it.
**Required**: Delete the restating sentence; the Gregory/Q15 citation can stand alone.

### Issue 2: Q15 cited twice for the same implementation fact
**ASN-0053, S6 and S4a**: S6 — "the split operation requires the cut and the width to share a tumbler length and aborts when this invariant is violated (Q14, Q15)"; S4a — "The split is exact precisely because the code aborts rather than proceeding when the arithmetic would be approximate (Q15)."
**Problem**: Both invoke the same "split aborts rather than approximating" evidence point. Repeated deference to the same source across sections is the accretion pattern that compounds across cycles.
**Required**: Keep the abort-on-approximation grounding at one site (S6, where level-uniformity is introduced) and drop the duplicate in S4a.

### Issue 3: Essay framing in the introduction
**ASN-0053, intro**: "We are looking for the laws this algebra satisfies. The question, as always, is: what must any implementation maintain?"
**Problem**: The four-question rhetorical buildup ("It must compare them… combine them… decompose them… reduce them…") plus "as always" is motivational essay content that does not advance any claim. Borderline, but it is prose the reader skips to reach the first definition.
**Required**: Compress to one sentence naming the operations the ASN formalizes (compare, merge, split, normalize, difference).

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
The final Open Question asks for the tight bound on |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|. S11d bounds single-span difference at 2; the span-set generalization is correctly deferred, not an omission in this ASN.

### Topic 2: Cross-level intersection and subspace-boundary guarantees
The level_compat precondition deliberately excludes deeper-level endpoints (illustrated by the [1,3,0,1] example). Intersection/difference across hierarchical levels is correctly left to a future ASN.

VERDICT: REVISE
