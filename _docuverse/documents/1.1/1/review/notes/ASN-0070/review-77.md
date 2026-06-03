# Review of ASN-0070

This is a careful, complete note. The central object (the inverse image `R(d, e) = M(d)⁻¹(coverage(e))`) is correctly defined, the subspace partition is sound, and F-canonical's existence/uniqueness proof is genuinely rigorous — Step 1's case split on the action point, Step 2's consecutivity Characterisation (both directions, with the discreteness contradiction at position `m`), and Step 4's right/left-closure arguments are all worked in full, not waved through. The six worked configurations exercise distinct derived properties (full clip, no-reach, state-dependence, cross-subspace straddle, interior offset `j>0`/`c<n`, vacuous subspace) and each checks the named postconditions concretely. F-sound/F-complete correctly factor the postcondition equality. I found no mathematical gap.

The findings below are anti-bloat (the note carries that classifier): residual meta-prose that does not advance the argument.

## REVISE

### Issue 1: Citation-choice justification adds nothing
**ASN-0070, "Computation via Decomposition"**: "We cite M1 directly rather than re-deriving the monotonicity from the underlying shift lemmas."
**Problem**: The preceding sentence already cites M1 (OrderPreservation) as the source of strict monotonicity. This trailing sentence justifies the *choice* to cite rather than re-derive — pure defensive meta-prose. The reader does not need to be told the citation was preferred to a re-derivation; the citation stands on its own.
**Required**: Delete the sentence.

### Issue 2: Performance claim drifts toward implementation
**ASN-0070, "Computation via Decomposition"**: "The decomposition view confirms the computation is finite and well-structured: linear in the number of (block, endset-span) pairs whose I-extents intersect."
**Problem**: Finiteness is load-bearing (it justifies span-set representability of `R`). The "linear in the number of (block, endset-span) pairs" clause is a complexity/performance statement — implementation mechanics, not a system guarantee. It is not used by any claim.
**Required**: Keep the finiteness assertion; drop the complexity clause.

### Issue 3: Editorial restatement of preconditions
**ASN-0070, F1**: "The preconditions are weak: only that the link exists, the document is allocated, and the endset index is in range."
**Problem**: This restates the three preconditions listed immediately above and asserts their weakness — a claim the "Weakest Precondition Analysis" section then proves formally. The sentence neither states a new fact nor advances the definition; the minimality result belongs to (and is delivered by) the wp section.
**Required**: Remove the restatement; let the wp section carry the minimality claim.

## OUT_OF_SCOPE

### Topic 1: Multi-home / cross-server traversal consistency
The Open Questions correctly defer the multi-home `follow(ℓ, d, i)` vs `follow(ℓ, d', i)` relationship and the BEBE replication consistency question. These are appropriately framed as future-ASN territory, not gaps in this note. No action needed.

VERDICT: REVISE
