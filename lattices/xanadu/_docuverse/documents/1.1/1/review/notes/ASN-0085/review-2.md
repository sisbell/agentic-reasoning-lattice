# Review of ASN-0085

## REVISE

### Issue 1: Inverse claims stated in prose, not in formal contracts
**ASN-0085, vpos definition**: "These are inverses: ord(vpos(S, o)) = o and vpos(subspace(v), ord(v)) = v."
**Problem**: The inverse relationship is the most structurally important property of the decomposition, but it appears only in body text — neither ord nor vpos includes it as a formal postcondition. The second direction requires v to satisfy S8a (so that `subspace(v) ≥ 1` and all components of `ord(v)` are positive, meeting vpos's preconditions), but this precondition is unstated. Without formal postconditions, downstream consumers cannot cite the inverse property by label.
**Required**: Add formal postconditions (to vpos, or introduce a joint lemma) establishing both directions with explicit preconditions: (a) For `S ≥ 1` and `o ∈ S`: `ord(vpos(S, o)) = o`. (b) For `v` satisfying S8a with `#v ≥ 2`: `vpos(subspace(v), ord(v)) = v`.

### Issue 2: w_ord actionPoint postcondition not conditioned on w > 0
**ASN-0085, w_ord formal contract, postconditions**: "actionPoint(w_ord) = actionPoint(w) - 1"
**Problem**: Stated unconditionally, but actionPoint is defined only for positive tumblers (TA0: "For a positive displacement w..."). The preconditions admit `w = [0, 0, ..., 0]`, for which neither actionPoint is defined. The positivity postcondition is correctly conditioned ("When `w > 0`, `w_ord > 0`"), but the actionPoint postcondition is not.
**Required**: Condition: "When `w > 0`: `actionPoint(w_ord) = actionPoint(w) - 1`."

### Issue 3: No concrete example
**ASN-0085, OrdAddHom**: The proof is component-by-component but purely symbolic.
**Problem**: No concrete numerical verification of the central result. A worked instance would confirm the component indexing and ground the proof.
**Required**: Add at least one instance, ideally two covering distinct action-point positions. For example: (a) `v = [1, 3, 5]`, `w = [0, 0, 2]` (action point 3): `v ⊕ w = [1, 3, 7]`, `ord([1, 3, 7]) = [3, 7]`; `ord(v) ⊕ w_ord = [3, 5] ⊕ [0, 2] = [3, 7]`. (b) `v = [1, 3, 5]`, `w = [0, 4, 0]` (action point 2): `v ⊕ w = [1, 7, 0]`, `ord([1, 7, 0]) = [7, 0]`; `ord(v) ⊕ w_ord = [3, 5] ⊕ [4, 0] = [7, 0]`. Case (b) is particularly instructive — the result `[7, 0]` falls outside S, illustrating the TA7a S-membership boundary.

### Issue 4: TA7a connection claimed but not derived
**ASN-0085, introduction**: "connecting these definitions to TA7a's closure guarantees on S"
**Problem**: OrdAddHom is proved entirely from TumblerAdd; TA7a is never invoked in any proof or postcondition. The claimed connection is conceptual only. The key consequence — that S-membership of `ord(v ⊕ w)` is governed by TA7a's postconditions applied to the decomposed operands — is unstated. Since `ord(v) ∈ S` (by ord's postcondition under S8a), TA7a's detailed S-membership conditions for `⊕` apply to the right-hand side of OrdAddHom, and by the homomorphism they govern the left-hand side. This is the bridge the introduction promises.
**Required**: Add a corollary or note within OrdAddHom: by OrdAddHom, `ord(v ⊕ w) = ord(v) ⊕ w_ord`; since `ord(v) ∈ S`, TA7a's `⊕` postconditions apply — specifically, `ord(v ⊕ w) ∈ S` when all components of `w_ord` after its action point are positive. This is one sentence of derivation but makes the connection explicit and citable.

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism
**Why out of scope**: The ASN's own open questions flag this. TA7a's subtraction postconditions are conditional and case-split-heavy (S-membership depends on action point position, divergence, and relative lengths). This requires its own treatment.

### Topic 2: S8a preservation under within-subspace addition
**Why out of scope**: The full statement — "v satisfying S8a and w a subspace-preserving displacement implies v ⊕ w satisfies S8a under conditions C" — combines the Issue 4 TA7a connection with the subspace-identifier preservation argument. It is a downstream consumer of this ASN's results, not a missing component of the decomposition itself.

VERDICT: REVISE
