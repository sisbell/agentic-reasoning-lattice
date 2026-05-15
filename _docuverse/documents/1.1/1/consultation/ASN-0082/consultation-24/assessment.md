# Channel Assignment — ASN-0082 review-24

**Date:** 2026-05-15 07:46

## Issue 1: S8a restated incorrectly from foundation
Reason: The fix requires only faithful citation of ASN-0036's existing S8a — the foundation definition is already in scope, so the correction is internal.

## Issue 2: Redundant redefinition of ord, vpos, w_ord
Reason: The fix replaces local redefinitions with citations to ASN-0036's existing definitions and retains only the new order-equivalence postcondition. Derivable from foundation reuse, no channels needed.

## Issue 3: Redundant lemma OrdinalAdditiveCompatibility
Reason: The fix substitutes a citation of OrdAddHom from ASN-0036 for a reproved lemma. Internal — the foundation already supplies the needed three-part contract.

## Issue 4: Asymmetry in depth coverage between insertion and contraction
Reason: Deciding whether to generalize contraction to arbitrary m ≥ 2 or justify the depth-2 restriction depends on whether the restriction reflects design intent (deletion conceived only at the ordinal level) or implementation constraint (udanax-green only supports depth-2 contraction).
Nelson question: Was contraction/deletion designed in Literary Machines as an operation on arbitrary V-position depths, or specifically scoped to the single-ordinal (depth-2) level analogous to a within-subspace span?
Gregory question: Does the udanax-green implementation handle contraction at V-position depths greater than 2 (e.g., for nested subspace structures), or is it restricted to depth-2 ordinal-level spans?

## Issue 5: Postcondition vs lemma labeling inconsistency
Reason: The fix is a labeling change to match the contraction-section convention already established within the ASN. Purely internal.

## Issue 6: D-DOM closure direction not derived
Reason: The justification needed parallels I3-CS/I3-CX's existing rationale, already articulated earlier in the same ASN. Derivable from the ASN's own content.

## Issue 7: I3-VP appeals to "all components positive" without restating it
Reason: The fix depends on resolving Issue 1 (faithful S8a citation supplies componentwise positivity) or adding an inline derivation step. No external evidence required.
