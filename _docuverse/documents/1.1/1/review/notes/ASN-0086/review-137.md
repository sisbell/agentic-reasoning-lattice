# Review of ASN-0086

## REVISE

### Issue 1: Orphaned corollary numbering — R0a-Cor2 with no R0a-Cor1

**ASN-0086, "R0a-Cor2 — DepthTwoLinkAddresses"** and Properties Introduced table row "R0a-Cor2"

**Problem**: The document defines and references a corollary named `R0a-Cor2` but contains no `R0a-Cor1` anywhere in the body. A reader navigating the corollary numbering hits a dead reference — "Cor2" presupposes a "Cor1" that was apparently removed in a prior revision (the Previously-Declined-Findings boilerplate still references an `R0a-Cor1` that no longer exists in the text). Orphaned numbering is a navigational defect in a document whose entire value is precise cross-reference.

**Required**: Rename the corollary to `R0a-Cor1`, or restore/explain the missing Cor1. The numbering must be self-consistent within the ASN.

### Issue 2: Duplicated non-circularity justification (anti-bloat)

**ASN-0086, L-ContiguousPrefix proof opening**: "This proof rests only on conformance clause (b) and ASN-0093's chain machinery — it does not invoke R0a; hence R0a's same-home case may consume this lemma without circularity."

**ASN-0086, R0a Case 2**: "By L-ContiguousPrefix (ContiguousPrefix, established above — its proof does not invoke R0a, so this consumption is non-circular), ..."

**Problem**: The same non-circularity claim — "L-ContiguousPrefix's proof does not invoke R0a, so R0a may consume it" — is asserted in two places. This is exactly the flagged pattern: prose justifying document ordering / proving non-circularity, stated redundantly across sections. One statement carries the load; the second is meta-prose the reader must recognize as a restatement.

**Required**: State the non-circularity once (the L-ContiguousPrefix statement is the natural site). Drop the parenthetical restatement in R0a Case 2, leaving only the citation.

### Issue 3: R7a "Two instances of the general construction" is redundant use-site enumeration (anti-bloat)

**ASN-0086, R7a proof, final paragraph**: "When the ↝-step is itself a single-fresh-key primitive ... the replay collapses to the length-1 sequence ... When instead the ↝-step adds one fresh document together with one link homed at it ... the length-2 sequence."

**Problem**: This paragraph enumerates two special cases (n=1 with/without K.σ-prefix) that the general construction already covers without remainder. It advances no part of the proof — it is a use-site inventory in a structural (proof) slot, the flagged essay-content pattern. The general argument's correctness does not depend on, nor is it clarified by, naming these two collapses.

**Required**: Delete the paragraph. If the connection to Emit_K-reduction and Nullify is worth recording, it belongs (and already appears) in the Definition — relational layer corollary, not re-spelled inside R7a's proof.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity model for Emit vs Observe

**Why out of scope**: The Open Questions correctly defer Emit-Observe atomicity and the `A_K` consistency model. This note proves single-state and `→*`-sequential properties; a concurrent observation model is genuinely new territory, not a gap in the present claims.

VERDICT: REVISE
