# Channel Assignment — ASN-0047 review-52

**Date:** 2026-05-16 17:04

## Issue 1: NodeLineage axiom not formalized as invariant or precondition
Reason: The fix is internal — NodeLineage is already established as an axiom with both Nelson (LM 4/28) and Gregory (granfilade structure) citations in the ASN body. The revision is a formal/structural choice between adding it as a K.δ precondition or as an invariant conjunct, derivable from existing material.

## Issue 2: L14a from ASN-0043 contradicted without amendment
Reason: The fix is internal — the ASN body already establishes design intent for home-origin link mappings (Nelson LM 4/31, cited in K.μ⁺_L's origin restriction), and CL-OWN formalizes it. The required amendment paragraph can be written using existing citations to justify L14a's supersession by CL-OWN and S3★'s link clause.

## Issue 3: K.δ case (i) precondition does not establish lineage
Reason: Internal — once Issue 1 is resolved (NodeLineage incorporated formally), this is the corresponding precondition adjustment; the design intent (n₀-rooted node tree) is already documented from both consultations.

## Issue 4: K.μ⁻ undefined when M(d) is empty
Reason: Internal formal fix — add explicit precondition `dom(M(d)) ≠ ∅` or restate the strict-subset clause. Pure definitional adjustment derivable from the K.μ⁻ definition itself.

## Issue 5: "Completeness" claim is informal
Reason: Internal — defining the class of transitions covered (invariant-preserving state changes) or weakening the claim is a formal/mathematical choice about theorem scope, derivable from the elementary transition definitions already present.

## Issue 6: Property table omits several introduced axioms and invariants
Reason: Internal housekeeping — add table entries for NodeLineage, SubAllocatorAxiom, D-CTG★, D-MIN★, D-SEQ★, ExtendedTransitionInvariants, and L1b, all of which are already introduced in the body.

## Issue 7: Convoluted K.μ~ redundancy argument
Reason: Internal — both alternatives (restructure to separate stipulation from inductive consequence, or drop and stipulate via Nelson's "permanent order of arrival") rely only on existing citations and formal reasoning already in the ASN.

## Issue 8: Worked example does not verify J1'★ for the link-allocation steps
Reason: Internal — explicit verification (vacuous because R is unchanged across the link-allocation steps) is purely a writing-completeness fix derivable from J1'★'s definition and the worked example's frame conditions.

## Issue 9: Decomposition of K.μ~ Case 1 conflates two distinct subcases
Reason: Internal definitional clarification — whether "π = id with non-empty M(d)" is a valid no-op instance is a definitional choice; rationale (zero elementary steps as the unique admissible expansion) is derivable from K.μ⁻'s strict-contraction precondition already stated.

## Issue 10: Decomposition of K.μ~ forward references CL-UNIQ before establishing it inductively
Reason: Internal organizational fix — reorder sections so CL-UNIQ precedes the K.μ~ decomposition, or add a forward-reference note parallel to existing forward-reference notes (e.g., the D-CTG★/D-MIN★ acknowledgments in K.μ⁻'s admissibility derivation).
