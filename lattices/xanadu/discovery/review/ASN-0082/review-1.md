# Review of ASN-0082

## REVISE

### Issue 1: Cross-ASN reference to ASN-0047
**ASN-0082, Post-Insertion Shift**: "We work with the system state Σ = (C, E, M, R) of ASN-0047."
**Problem**: ASN-0047 is not a foundation ASN. The ASN must be self-contained per rule 7.
**Required**: Define M(d) : T ⇀ T locally as the document arrangement function (a partial map from V-positions to I-addresses). Drop the reference to ASN-0047.

### Issue 2: Implicit references to non-foundation ASN-0036
**ASN-0082, The Ordinal Shift**: "By S8-depth, all V-positions in the subspace share p's depth" and "the positivity required by S8a"
**Problem**: S8-depth and S8a are from ASN-0036, which is not a foundation. These labels appear without definition anywhere in this ASN. Both are load-bearing — the subspace-preservation argument and the positivity of shifted ordinals depend on them.
**Required**: State the needed properties as local axioms: (1) all V-positions within a subspace share the same tumbler depth; (2) the subspace identifier of every V-position is positive (≥ 1).

### Issue 3: I3 has no formal precondition block
**ASN-0082, Post-Insertion Shift**: I3 quantifies over free variables n, p, d, S, M, M' whose constraints are scattered across surrounding prose.
**Problem**: The constraints include n ≥ 1, p ∈ T with #p ≥ 2, S = subspace(p) ≥ 1, v ∈ dom(M(d)), and the existence of M'(d). None appear in a *Preconditions* block. A downstream ASN citing I3 cannot extract its interface without reading the prose.
**Required**: Add a formal *Preconditions* / *Postconditions* block to I3, following the pattern used in the foundations (e.g., T12, TA0).

### Issue 4: No frame condition for positions below p
**ASN-0082, Post-Insertion Shift**: I3 specifies the fate of every v ≥ p but is silent on v < p.
**Problem**: The ASN claims to capture "the permanent identity of every existing byte is invariant under insertion." But I3 only covers the shifted region. Positions below p should remain in dom(M'(d)) with unchanged I-addresses. Without this frame condition a consumer cannot conclude that content before the insertion point is preserved — I3 is half a specification.
**Required**: State the left-region frame: `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v < p : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`. Also state the cross-subspace and cross-document frame (positions outside subspace S and documents other than d are unchanged).

### Issue 5: Incorrect citation in subspace preservation argument
**ASN-0082, The Ordinal Shift**: "ordinal increment via TA5(c) modifies position m = #v"
**Problem**: TA5(c) defines `inc(t, 0)` — the hierarchical sibling increment. The shift operation uses TumblerAdd (⊕), not `inc`. These are distinct operations with different definitions. The correct justification is from TumblerAdd: for δₙ with action point k = m, positions i < k are copied from v, so when m ≥ 2 position 1 (the subspace identifier) is preserved.
**Required**: Replace the TA5(c) citation with TumblerAdd.

### Issue 6: Worked example does not verify the full postcondition
**ASN-0082, Worked Example**: The table covers only V-positions at or beyond p = [1, 3]. Positions [1, 1] and [1, 2] (below p) are absent from the after-state.
**Problem**: The example should verify every aspect of the postcondition the ASN introduces. Once the frame condition (Issue 4) is stated, the example should confirm it for the left region. As written, the example verifies I3 for three positions but leaves the frame unillustrated.
**Required**: Extend the table to include [1, 1] and [1, 2] in the after-state, confirming their I-addresses are unchanged.

## OUT_OF_SCOPE

### Topic 1: Postcondition for newly inserted positions
**Why out of scope**: I3's stated scope is the shift property for existing content. The mapping of new V-positions to freshly allocated I-addresses is a separate INSERT postcondition belonging in an operation ASN.

### Topic 2: Cross-subspace interference
**Why out of scope**: Whether an insertion in subspace 1 can affect link subspace 2 is an inter-subspace invariant belonging in the operation layer, not a span-algebra extension.

VERDICT: REVISE

---

# Review of ASN-0081

## REVISE

### Issue 1: Cross-ASN references to non-foundation ASN-0036
**ASN-0081, Contraction Setup**: "All V-positions in a given subspace share the same tumbler depth (S8-depth, ASN-0036)" and "positive by S8a (ASN-0036)"
**Problem**: ASN-0036 is not a foundation. Both properties are load-bearing: S8-depth is used in D-BJ's application of TA3-strict (#a = #b precondition), and S8a is used in D-SHIFT's well-definedness argument (ord(r) ≥ w_ord requires p₂ ≥ 1).
**Required**: State the needed properties as local axioms: (1) all V-positions within a subspace share the same tumbler depth; (2) the subspace identifier of every V-position is positive (≥ 1).

### Issue 2: Dangling reference to D-DP
**ASN-0081, Open Questions**: "contiguity preservation (D-DP)"
**Problem**: D-DP is referenced in the open question but is never defined in the ASN body or the statement registry. A reader encountering this label cannot locate its definition. The "Consequence" paragraph informally states what D-DP appears to mean (the gap closes exactly, with no overlap and no residual gap), but this is never formalized or registered.
**Required**: Either formalize the Consequence as a lemma with label D-DP and add it to the statement registry, or remove the D-DP reference from the open question.

### Issue 3: Depth restriction #p = 2 not in formal preconditions
**ASN-0081, Contraction Setup**: "Here p is a V-position in subspace S with #p = 2 (depth-2 V-positions, ordinal depth 1)"
**Problem**: This restriction is stated in setup prose but does not appear in the formal preconditions of D-SHIFT, D-BJ, or D-SEP. All three proofs rely on it: D-SHIFT's subtraction reduces to [vₘ] ⊖ [c]; D-BJ's TA3-strict application requires equal-length ordinals; D-SEP's TA4 verification requires the zero-prefix condition to be vacuously satisfied (k = 1). A formal consumer of these statements sees no depth restriction.
**Required**: Add `#p = 2` to the precondition blocks of D-SHIFT, D-BJ, and D-SEP, or state it once as a scoping axiom for the ASN and reference it from each statement.

### Issue 4: L and X regions have no formal postconditions
**ASN-0081, Three Regions / Shift Correctness**: The partition defines L (left), X (contracted), R (right), but only R receives a formal postcondition (D-SHIFT).
**Problem**: D-SEP claims gap closure — that the shifted right region abuts the left region with no gap. This claim requires L to be preserved unchanged in M'(d) and X to be removed. Neither is stated formally. Without L preservation, the gap-closure argument is ungrounded: "the left region ends just before ord(p)" assumes L's positions remain in dom(M'(d)). Without X removal, the contraction's effect is unspecified.
**Required**: Add postconditions: (1) L preservation: `(A v ∈ L : v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v))`; (2) X removal: `(A v ∈ X : v ∉ dom(M'(d)))`. Also state the cross-subspace and cross-document frame.

### Issue 5: Gap-closure consequence not formalized
**ASN-0081, Shift Correctness, Consequence**: "The gap closes exactly at p: the left region ends just before ord(p), and the shifted right region begins at ord(p). No overlap... and no residual gap."
**Problem**: This is the ASN's central result — that D-SHIFT + D-SEP together ensure the arrangement is intact at the contraction boundary — but it is stated only in prose. The formal statements stop at D-SEP (σ(r) has ordinal ord(p)), which is the key equation but not the full gap-closure property. The full property requires combining D-SEP with L preservation and X removal (Issue 4) to conclude that the post-state arrangement in subspace S has no new gap at the contraction point and no overlap between L and Q₃.
**Required**: Formalize the consequence as a lemma (this appears to be the intended content of the dangling D-DP label from Issue 2). State it as: L ∩ Q₃ = ∅ (no overlap) and there is no ordinal between max(L) and min(Q₃) that was in dom(M(d)) but is absent from dom(M'(d)) (no new gap).

## OUT_OF_SCOPE

### Topic 1: Generalization beyond depth-2 ordinals
**Why out of scope**: The open question already identifies this. At multi-component ordinal depth, TA4's zero-prefix condition is no longer vacuous and TA3-strict's equal-length precondition requires explicit verification. This is genuine new work.

### Topic 2: Promoting ord/vpos to a shared foundation
**Why out of scope**: These functions formalize what TA7a (ASN-0034) describes informally. Both ASN-0081 and ASN-0082 would benefit from shared definitions, but that is an architectural decision about foundation structure, not a defect in this ASN.

VERDICT: REVISE
