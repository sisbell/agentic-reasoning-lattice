# Review of ASN-0084

## REVISE

### Issue 1: CS3 redundancy-rebuttal is "why the clause is needed" meta-prose
**ASN-0084, Definition — CutSequence**: "CS3 is not implied by CS2 + R-PRE(iv): an all-higher-subspace cut sequence passes R-PRE(iv) vacuously (its quantification range is empty) while collapsing the regions, so CS3 is the clause that rejects it."
**Problem**: This paragraph explains *why* CS3 is necessary (a non-redundancy defense against a hypothetical all-higher-subspace cut sequence) rather than stating what CS3 says. It is the flagged "new prose around a clause explains why it is needed" pattern — a precise reader does not need a redundancy proof inlined into a definition. CS1–CS4 already stand on their own; the constraint subspace(cᵢ)=S is self-evidently doing work.
**Required**: Delete the rebuttal paragraph. If a non-redundancy note is genuinely wanted, it belongs (at most) as a one-clause parenthetical, not a worked vacuous-quantification argument.

### Issue 2: Region non-degeneracy stated twice
**ASN-0084, R-PRE clause (iv) commentary**: "Region non-degeneracy (w_α ≥ 1, w_β ≥ 1 in both forms, and w_μ ≥ 1 when n = 4) follows from (iii) and (iv)."
**ASN-0084, Consequences of R-PRE / Width positivity**: "each region width equals a cut-ordinal difference and is a positive natural number: w_α ≥ 1 and w_β ≥ 1 in both forms, and additionally w_μ ≥ 1 when n = 4."
**Problem**: The same conclusion is asserted in the R-PRE note and then proved in the Width positivity consequence — two paragraphs saying the same thing, with the first a bare forward-pointer to the second. This is the duplicate-statement pattern.
**Required**: Drop the non-degeneracy sentence from the R-PRE(iv) commentary and let Width positivity carry it; the clause (iv) note should confine itself to what (iv) asserts (range coverage / no gaps).

### Issue 3: Defensive tail in EXT-VAC
**ASN-0084, Consequences of R-PRE / Empty-exterior boundary cases**: "R-PRE(iv) is unaffected because it constrains only [c₀, c_{n−1}), which excludes c_{n−1} itself."
**Problem**: The EXT-VAC derivation itself (forcing ord(c_{n−1}) ≤ N+1, characterizing the empty-right-exterior configuration) is substantive and used by R-BLK. But this trailing sentence is a defensive reassurance that nothing was broken, not a step that advances the argument. It is meta-prose appended to an otherwise load-bearing paragraph.
**Required**: Remove the trailing reassurance sentence; the exclusive-bound semantics of [c₀, c_{n−1}) is already fixed by the interval notation.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: Generalizing beyond pivot/swap, and the algebra of composing rearrangements, is genuinely new territory — correctly deferred to the Open Questions, not a defect in this ASN's pivot/swap treatment.

### Topic 2: Cross-subspace and m₁ > 2 rearrangements
**Why out of scope**: The depth-2, single-subspace restriction is stated explicitly as a scope boundary. Lifting it (link-subspace transposition, deeper text subspaces) is future work, not an error here. The non-S worked example correctly demonstrates only *pass-through*, which is the right obligation at this scope.

VERDICT: REVISE
