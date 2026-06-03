# Channel Assignment — ASN-0100 review-26

**Date:** 2026-06-03 09:27

## Issue 1: OrdAddHom misattributed to ASN-0036
Reason: Pure citation correction; the review supplies both valid targets (OrdAddHom clause (b), ASN-0082, or OrdShiftHom (a), ASN-0036, in shift form). Choosing and applying the swap is a within-corpus cross-reference fix requiring neither design intent nor implementation evidence.

## Issue 2: S7c cited as an ASN-0036 invariant — does not exist
Reason: The review identifies the correct invariant names (C1b for `#E(a)≥2`, C1c for allocator conformance) and their sources. The `#E(a_k) ≥ 2` fact and the A_C(d)-chain provenance of each `a_k` are already established in the ASN's own Effect One and S7 analysis, so the C1b/C1c discharge is derivable internally.

## Issue 3: M2's precondition list overstated
Reason: The review states M2's actual precondition list ("S8-fin, S2, S3, S8a, S8-depth") from ASN-0058; dropping the spurious S7b/S7c is a mechanical correction needing no external channel.

## Issue 4: ChainUniformLength and ChainUniformZeroCount cited as ASN-0093 lemmas — do not exist
Reason: The review names the correct foundation lemmas (TA5(c), ASN-0034, for length; C1, ASN-0093, for zero count), which the ASN already cites correctly elsewhere. A self-consistency citation fix, derivable from the document.

## Issue 5: "SubAllocatorAxiom.{Disjointness, Subspace, FirstEmission}" — reinvented naming for foundation lemmas
Reason: The review supplies the actual foundation lemma names (SubAllocatorBundle/DisjointSubAllocatorChains/CrossDocumentDisjointness, ASN-0047/0093; FirstEmission, ASN-0093) for each reinvented reference. Straightforward name substitution within the spec corpus.
