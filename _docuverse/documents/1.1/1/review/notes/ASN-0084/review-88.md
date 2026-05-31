# Review of ASN-0084

This note is mathematically careful and the well-definedness, permutation, and run-decomposition lemmas check out against the five worked examples. My findings target the meta-prose / forward-reference accretion that the `review-mode.anti-bloat` classifier flags, plus one structural ordering issue. I found no soundness errors in the proofs.

## REVISE

### Issue 1: R-COMM non-S case re-derives what its own precondition supplies
**ASN-0084, R-COMM proof, "Non-S subspace (both forms)"**: "the same-region hypothesis places v + k in the non-S subspace as well — by OrdShiftHom (a) of ASN-0036, subspace(v + k) = subspace(v) ≠ S, so v + k automatically inherits the non-S region."

**Problem**: R-COMM's precondition already requires "v, v + k lie in the same region," and for the non-S case that region is `{v ∈ dom(M(d)) : subspace(v) ≠ S}`. The conclusion `π(v + k) = v + k` follows immediately from R-NS(NS-π), which fixes *every* non-S position regardless of subspace. The OrdShiftHom (a) step adds nothing: π = identity does not require v and v+k to share a subspace, only that both are non-S, which the hypothesis gives directly. This is a defensive re-derivation of a case the precondition already provides.

**Required**: Reduce the non-S case to: "By the hypothesis, v and v+k are both non-S; R-NS(NS-π) gives π(v) = v and π(v + k) = v + k, hence π(v + k) = v + k = π(v) + k." Drop the OrdShiftHom invocation.

### Issue 2: Width-positivity alignment argument duplicates the singleton↔ordinal coincidence already established
**ASN-0084, "Consequences of R-PRE" / Width positivity**: "The alignment between T1-membership in the interval [c_i, c_{i+1}) and ordinal-membership in [ord(c_i), ord(c_{i+1})) is what CS3 and CS4 carry: because each cut c_i is itself subspace-S (CS3) at depth 2 (CS4), it has the form [S, ord(c_i)], so for any subspace-S depth-2 position v = [S, ord(v)] the T1 comparison of v against c_i reduces to the ordinal comparison..."

**Problem**: The "Identification of singleton tumblers with natural numbers" paragraph (State and Vocabulary) already establishes that "T1's strict ordering on tumblers restricted to singletons coincides with the standard `<` on ℕ⁺ (lexicographic order on a single component reduces to comparison of that component)." Width positivity re-derives the identical fact at length for the depth-2 cut positions, dressing the same reduction (shared leading component S cancels, single remaining component decides T1) as if it were new. Two paragraphs saying the same thing in different words.

**Required**: Collapse the alignment sub-argument to one sentence citing the established singleton-ordinal coincidence applied to depth-2 subspace-S positions, then proceed to `count = ord(c_{i+1}) − ord(c_i) ≥ 1`.

### Issue 3: R-NS forward-references R-PPERM/R-SPERM definitions that appear after it
**ASN-0084, R-NS statement and proof**: "Let π be the cut-point-induced bijection on dom(M(d)) (R-PPERM for n = 3, R-SPERM for n = 4)" and "The non-S clause of the bijection definition (the first clause of R-PPERM's piecewise definition, mirrored as the first clause of R-SPERM's) stipulates π(v) = v on this domain."

**Problem**: R-NS is stated and proved before R-PPERM and R-SPERM are defined, yet its proof depends on those definitions for the value of π on non-S positions. R-PPERM/R-SPERM in turn cite R-NS(NS-π) to discharge their non-S verification. The result is a forward-reference loop that forces the reader to jump ahead to two later lemmas to follow a proof presented earlier — exactly the forward-reference accretion the anti-bloat pass targets. R-NS's actual content (π = identity and M' = M on non-S) is immediate from R-FRAME-P(a)/R-FRAME-S(a) alone, without invoking the not-yet-stated piecewise π.

**Required**: Either (a) prove R-NS from the frame conditions alone (`M'(d)(v) = M(d)(v)` directly; the π = identity claim then follows once π is defined), removing the forward citation to R-PPERM/R-SPERM; or (b) relocate R-NS after the permutation definitions so it cites established material.

### Issue 4: Intro dependency inventory is meta-prose
**ASN-0084, opening paragraph**: "The proofs draw directly on ASN-0036 (Strand Model — correspondence runs S8, contiguity D-CTG, sequential positions D-SEQ) and ASN-0034 (Tumbler Algebra — ordinal shift OrdinalShift, shift composition TS3, lexicographic order T1)."

**Problem**: This is a use-site inventory that advances no reasoning — each cited foundation result is invoked, with its citation, at the point it is used. The opening sentence pre-announcing the dependency list is the kind of structural-slot meta-prose that compounds across cycles.

**Required**: Delete the sentence; the in-proof citations already carry the dependencies.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and the full permutation class
Already captured in Open Questions. The restriction to n ∈ {3, 4} (CS1) is a legitimate scope boundary, not a gap in this ASN.

### Topic 2: Composition of rearrangements and canonical-partition recovery from B'
The Open Questions correctly defer (a) whether composing two rearrangements is itself a single rearrangement, and (b) the operational merge process that recovers the maximal partition from R-BLK's non-maximal B'. R-BLK only needs to produce *a* valid partition; maximality recovery is future territory.

### Topic 3: Weakest precondition for REARRANGE_K
The wp question (what R-PRE(iv) guarantees beyond D-SEQ) is appropriately listed as open. The depth analysis in this ASN does not require it.

VERDICT: REVISE
