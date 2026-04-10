# Review of ASN-0084

## REVISE

### Issue 1: Corollary "ran(M'(d)) = ran(M(d))" stated without derivation; S3 preservation unstated

**ASN-0084, State and Vocabulary**: "The corollary is ran(M'(d)) = ran(M(d)) — the multiset of I-addresses is invariant."

**Problem**: This corollary is asserted without derivation. More significantly, the ASN verifies S0 preservation (C' = C, via R-FRAME) and S2 preservation (M' is a function, via R-PIV/R-SWP) but never states S3 (referential integrity) preservation — that ran(M'(d)) ⊆ dom(C'). The verification is selective: if you check S0 and S2, leaving S3 unstated is an incomplete invariant audit. Downstream ASNs that build on these postconditions need to know S3 holds without re-deriving it.

**Required**: (a) Derive the corollary explicitly: ran(M'(d)) = {M'(d)(u) : u ∈ dom(M'(d))} = {M'(d)(π(v)) : v ∈ dom(M(d))} (by surjectivity of π onto dom(M'(d)) = dom(M(d))) = {M(d)(v) : v ∈ dom(M(d))} = ran(M(d)). (b) State S3 preservation as a consequence: ran(M'(d)) = ran(M(d)) ⊆ dom(C) = dom(C'), by S3 for M(d) and C' = C.

## OUT_OF_SCOPE

### Topic 1: General-depth extension
**Why out of scope**: The ASN restricts to depth-2 V-positions and correctly notes generalization is "structurally identical by D-CTG-depth." Proving this for arbitrary m ≥ 3 — where displacements become multi-component and commutativity arguments require TS3 rather than plain natural-number commutativity — is new work, not a defect in the depth-2 analysis.

### Topic 2: Rearrangement composition and expressibility
**Why out of scope**: Already identified in the ASN's Open Questions. Whether compositions of cut-point transpositions are closed (always expressible as a single rearrangement) or generate a strictly larger permutation class is a separate algebraic question requiring new definitions.

VERDICT: REVISE
