# Review of ASN-0086

## REVISE

### Issue 1: ASN-0036 invariant naming inconsistencies

**ASN-0086, multiple sites**: The ASN attaches parenthetical names to ASN-0036 invariants that do not match ASN-0036's actual labels:

- "S3 (ArrangementReferentialIntegrity, ASN-0036)" — actual name is **ReferentialIntegrity** (R0 Step 4 L14a bullet; R0a Setup; Worked Sketch).
- "S7d (LevelTwoZeroCount, ASN-0036)" — actual name is **DocumentAllocationDiscipline** (SharedDepthOneAllocator proof Step (a); Setup; Worked Sketch).
- "S9 (ContentStoreInvarianceUnderArrangementModification, ASN-0036)" — actual name is **TwoStreamSeparation** (Scoping note on arrangement modifications).

**Problem**: A reader who looks up the cited names against ASN-0036 will not find them. This erodes verifiability of cross-references to foundation ASNs, which are the only cross-references permitted.

**Required**: Replace each parenthetical with the actual invariant name from ASN-0036. The semantic content of the citations is correct; only the labels are wrong.

### Issue 2: Misuse of "subspaces" for ghost type-endset addresses in Worked Sketch

**ASN-0086, Worked Sketch (Setup)**: "By construction `coverage(K) ∩ coverage(R) = ∅` (different first components in subspaces 3 and 4)".

**Problem**: The ghost addresses `k = 3.0.0.0.1` and `r = 4.0.0.0.1` have adjacent zeros (positions 2 and 3), so they are not T4-valid and have no well-defined subspace identifier in the T4b/ASN-0036 sense. The term "subspace" in the rest of this note and in the foundation ASNs refers to `E(t)₁` (the first element-field component of a T4-valid address), not to `t₁` (the first tumbler component, which is the node-identifier position). Calling positions `t₁ = 3` and `t₁ = 4` "subspaces 3 and 4" conflates two distinct levels of the tumbler hierarchy.

**Required**: Rephrase as "different first tumbler components (3 and 4 respectively), so no tumbler can extend both prefixes" — which is the substantive disjointness argument and does not invoke the (inapplicable) subspace concept.

## OUT_OF_SCOPE

Nothing further. The Open Questions section already covers the major outstanding work — discipline elevation, depth-N relaxation, slice-wise statements under native L14, higher-arity links, observe ordering, atomicity, T_cat dynamics, and L_K / Σ.M visibility interactions.

VERDICT: REVISE
