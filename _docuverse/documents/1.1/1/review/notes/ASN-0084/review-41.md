# Review of ASN-0084

## REVISE

### Issue 1: R-NS forward reference not acknowledged

**ASN-0084, "Non-S Subspace Invariance" section, R-NS proof of (NS-π)**: "The non-S branch of the R-PPERM piecewise definition (and of R-SPERM) sets π(v) = v whenever subspace(v) ≠ S."

**Problem**: R-NS is placed before R-PPERM and R-SPERM in the document, but its (NS-π) proof depends on the specific piecewise definition introduced only in those later sections. The forward reference is implicit. The ASN does acknowledge other forward references explicitly (R-WP's "Forward-reference note" to R-COMM and R-BLK), so the absence here creates a structural inconsistency. The reference is substantive, not merely cosmetic: under S5 (unrestricted sharing), other bijections satisfying M'(d)(π(v)) = M(d)(v) need not fix non-S positions; R-NS(NS-π) holds because R-PPERM/R-SPERM *choose* π(v) = v on non-S, a choice made only later.

**Required**: Either add an explicit forward-reference note to R-NS (mirroring R-WP's style), or reorder so R-NS appears after R-PPERM and R-SPERM.

### Issue 2: Operation REARRANGE_C partiality not explicit

**ASN-0084, "Operation — REARRANGE_C" paragraph**: "REARRANGE_C has precondition R-PRE(C) and runtime signature (Σ, d) ↦ Σ'."

**Problem**: The operation is specified by its postcondition under R-PRE. The R-PRE counterexample sketches show that the postcondition can be unsatisfiable when R-PRE fails (e.g., R-P1 references M(d) at positions outside dom(M(d))), so REARRANGE_C must be partial. But the ASN never explicitly states that the operation is undefined when R-PRE fails. The convention is standard for partial operations, but for a Dijkstra-style specification the partiality should be on-the-page.

**Required**: One sentence stating REARRANGE_C is partial — undefined when R-PRE(C) fails — or specifying the failure semantics.

### Issue 3: Canonical-decomposition step (b), n₁ = n₂ derivation has gap

**ASN-0084, canonical decomposition proof, step (b), "n₁ = n₂" paragraph**: "By symmetry, n₁ > n₂ is excluded."

**Problem**: The "by symmetry" appeals to swapping b₁ and b₂. But step (b)'s hypothesis was *"Let b₁ and b₂ be maximal runs"* — symmetric in the labels, so swapping preserves the hypothesis. However, the immediately preceding sub-arguments (v₁ = v₂, a₁ = a₂) established that v₁ = v₂ and a₁ = a₂ *as derived facts*; the "by symmetry" for n₁ > n₂ needs to re-run those sub-arguments under the swapped labelling, which works but is not literally "swap and apply the same paragraph." A brief note clarifying that the symmetry holds because the hypothesis "two maximal runs share a V-position" is label-symmetric would close the gap.

**Required**: One sentence clarifying that the n₁ > n₂ case follows by re-applying the entire (b) argument with b₁ and b₂ swapped, since the hypothesis is symmetric in the run labels.

## OUT_OF_SCOPE

### Topic 1: Generalization to deeper text subspace (m_1 > 2)

**Why out of scope**: The ASN deliberately fixes m_1 = 2; lifting this requires multi-component ordinal arithmetic on V-positions that the singleton-tumbler identification doesn't address.

### Topic 2: Cross-subspace and link-subspace rearrangement

**Why out of scope**: CS3 confines REARRANGE_C to the text subspace; link rearrangement and cross-subspace operations are explicitly named as future work.

### Topic 3: k-cut rearrangements for k > 4

**Why out of scope**: CS1 restricts to n ∈ {3, 4}. Open question 1 asks for the natural class for k > 4.

### Topic 4: Composition of REARRANGE operations

**Why out of scope**: Open question 2 — whether a composition of two rearrangements is itself a rearrangement — is acknowledged as future work.

### Topic 5: Full weakest-precondition (necessity for every R-PRE conjunct)

**Why out of scope**: R-WP claims sufficiency only. Necessity is sketched for R-PRE(iv) and CS3 with a note on R-PRE(v)'s logical dependence; full necessity for R-PRE(i), R-PRE(ii), CS1, CS2, CS4 is explicitly deferred.

### Topic 6: Characterizing post-rearrangement merge formation

**Why out of scope**: R-BLK closes with "this ASN does not characterize *which* pre-state run pairs produce post-state mergeability." Open question 3 asks for bounds on canonical-partition size change; this analysis belongs in a downstream ASN.

VERDICT: REVISE
