# Review of ASN-0055

## REVISE

### Issue 1: TA-MTO converse claimed but not formally proven
**ASN-0055, ManyToOne section**: "The converse also holds: if a ⊕ w = b ⊕ w, then a and b must agree on components 1..k (from the 'copy from start' region of TumblerAdd)"
**Problem**: The statement registry declares TA-MTO as a biconditional (⟺), and the prose claims the converse holds. But only the forward direction (agreement ⟹ equal results) receives a structured proof. The reverse direction is dismissed in one sentence citing "the 'copy from start' region." That sentence covers positions i < k but silently relies on cancellation of w_k at position i = k without showing it. Two distinct steps are needed: (a) for i < k, results copy from starts, so a_i = b_i; (b) at i = k, a_k + w_k = b_k + w_k gives a_k = b_k by cancellation in ℕ. Both are straightforward, but a biconditional in the registry needs both directions proven with equal explicitness.
**Required**: Either give the converse its own proof block with the two cases shown, or demote the registry entry to ⟹ and state the converse separately as a corollary with its argument.

### Issue 2: No worked example for TA-LC
**ASN-0055, Left cancellation section**
**Problem**: TA-LC is the primary result of the ASN. TA-RC has a concrete example verifying the counterexample; TA-LC has none. A concrete scenario — e.g., a = [2, 5], x = [0, 3], y = [0, 3], verifying that the result [2, 8] uniquely determines the displacement — would ground the general proof and demonstrate the component-by-component recovery.
**Required**: Add a worked example that exercises TA-LC on specific tumblers, showing how equality of results forces equality of displacements through the action-point argument.

### Issue 3: TA-RC proof contains unrevised draft prose
**ASN-0055, Right cancellation fails section**: "Wait — b₂ = 3 as well, so b ⊕ w = [1, 5, 4] also."
**Problem**: The computation immediately above already shows b ⊕ w = [1, 3 + 2, 4] = [1, 5, 4]. The "Wait —" sentence re-derives a conclusion already established, adding nothing except the impression that the proof was not reviewed after drafting. In a specification note, stream-of-consciousness text undermines confidence in the rigor of surrounding material.
**Required**: Remove the "Wait —" sentence. The computation and the final sentence ("So a ⊕ w = b ⊕ w = [1, 5, 4] despite a ≠ b") are sufficient.

## OUT_OF_SCOPE

### Topic 1: Order cancellation (a ⊕ x ≤ a ⊕ y ⟹ x ≤ y)
**Why out of scope**: The ASN correctly flags this as an open question. It would strengthen TA1-strict but is a distinct property requiring its own analysis — particularly around whether the weak order case (with possible length mismatches) preserves the implication.

VERDICT: REVISE
