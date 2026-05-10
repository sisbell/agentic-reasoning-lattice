# Review of ASN-0002

## REVISE

### Issue 1: Worked example omits REARRANGE and CREATENEWVERSION
**ASN-0002, Worked example**: The four-step scenario exercises INSERT, DELETE, COPY, and CREATELINK but never REARRANGE or CREATENEWVERSION.
**Problem**: AP8 (I-address set invariance under rearrangement) and AP10 (version identity sharing) are key postconditions with non-trivial V-space content. Neither is verified against concrete values. The example should be a complete sanity check of the operation suite.
**Required**: Add a REARRANGE step (e.g., swap the two characters after step 1, verify the I-address set is unchanged and V-positions are permuted) and a CREATENEWVERSION step (e.g., fork document `d` after step 3, verify the new version references exactly `{α₂}` in its text subspace and `∅` in its link subspace per AP10/AP10a).

### Issue 2: Permanence hierarchy omits AP4b
**ASN-0002, The permanence hierarchy**: "I-space (fully immutable): governed by AP0, AP1, AP2, AP3, AP4, AP4c."
**Problem**: AP4b (subspace disjointness) is omitted from the list. AP4b is an I-space structural property essential to the AP4→AP2 derivation — without it, per-document-per-subspace monotonicity does not yield global freshness.
**Required**: Add AP4b to the I-space property list.

## OUT_OF_SCOPE

### Topic 1: Formal modeling of AP4a (range commitment permanence)
**Why out of scope**: The ASN correctly identifies that AP4a requires extending Σ with an `alloc : Range → Entity` mapping and deferring the formalization. This is a new modeling commitment, not an error in the current ASN.

### Topic 2: Spanindex maintenance obligation
**Why out of scope**: The forward correspondence `(A d, a : (E p : vspace(d).p = a) ⟹ (a, d) ∈ spanindex)` requires specifying per-operation spanindex writes. The ASN explicitly defers this and establishes only the monotonicity property (AP11). A future ASN should define which operations must write spanindex entries and verify the forward direction.

### Topic 3: Link discovery mechanism
**Why out of scope**: AP13 correctly notes that discoverability (given an I-address, find all links whose endsets reference it) requires a mechanism not defined here. This is a new capability, not a gap in the permanence analysis.

### Topic 4: V-subspace to I-subspace correspondence
**Why out of scope**: The ASN implies but does not state an invariant that text V-positions map to text I-addresses and link V-positions map to link I-addresses. This correspondence holds by construction (each operation maintains it), but formalizing it as an invariant is additional scope.

VERDICT: CONVERGED
