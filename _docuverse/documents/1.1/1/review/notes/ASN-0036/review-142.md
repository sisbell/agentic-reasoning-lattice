# Review of ASN-0036

## REVISE

### Issue 1: The δ/TumblerAdd action-point fact is restated five times
**ASN-0036, multiple sections**: The single foundation fact "δ(·, m) has action point m, so TumblerAdd copies positions 1..m−1 unchanged and advances the last component" is spelled out in full at least five times:
- S8 "Uniqueness across subspaces" ("since δ(1, m) has action point m, TumblerAdd's prefix rule copies every component at positions i < m...");
- S8 lemma, Case j = m ("the action point of δ(1, m) is m, so all components at positions i < m are copied...");
- the derivation paragraph after the two ValidInsertion definitions ("since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1...");
- the ValidFirstInsertionPosition prose ("For m ≥ 2, δ(n, m) has action point m > 1, so TumblerAdd copies component 1 unchanged...");
- the worked example ("action point 2; component 1 copied unchanged, component 2 receives 1 + 1 = 2").

**Problem**: This is the "two paragraphs say the same thing in different words" pattern, compounded across cycles. A reader re-derives the same TumblerAdd consequence each time. It is noise the precise reader must skip.
**Required**: State the consequence once (e.g., a one-line lemma: "for a depth-m V-position, shift(v, j) preserves components 1..m−1 and sets the last to v_m + j"), then cite it. Remove the inline re-derivations at the four downstream sites.

### Issue 2: Decorative weakest-precondition blocks restate their own axioms
**ASN-0036, S0**: "`wp(op, (A a : a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a)))` must hold in every reachable state."
**ASN-0036, S3**: "`wp(op, S3) ⟹ a ∈ dom(Σ'.C)` — the I-address must exist in the post-state."
**Problem**: Operations (INSERT/DELETE/COPY) are out of scope for this ASN, so there is no operation against which to compute a genuine wp. Both blocks therefore reduce to restating the invariant in wp notation — the trivial case the review standard explicitly disqualifies as analysis. They advance no reasoning.
**Required**: Either drop the wp framing and keep the plain consequence sentence ("every operation must leave C(a) fixed or write only fresh addresses"), or move the wp obligation to the operations ASN where a non-trivial wp can actually be computed. As written it is depth-signalling, not depth.

### Issue 3: Implementation-mechanics prose in S1 does not bear on the abstract guarantee
**ASN-0036, S1**: "Gregory's evidence shows the reclamation machinery was built but deliberately deactivated — the reference-counted deletion call is commented out (`/*subtreefree(ptr);*/`) — so S0 and S1 are upheld by design choice rather than architectural impossibility."
**Problem**: Whether the invariant holds by design choice or by impossibility is irrelevant to the abstract guarantee; an alternative implementation satisfies S1 iff its Σ contains no removal operation, which is the abstract argument already given two sentences earlier ("none of the seventeen FEBE commands modifies Istream content"). The commented-out-call detail is implementation mechanics dressed as a refinement of the invariant.
**Required**: Cut the `/*subtreefree(ptr);*/` sentence, or compress to a one-clause evidentiary note. The load-bearing claim is the absence of a removal op in Σ, already stated.

### Issue 4: S0 motivational preamble and the "Read directionally" remark explain why the axiom is needed rather than what it says
**ASN-0036, S0**: The "Suppose `C(a)` could change from value `w` to `w'`..." paragraph plus the trailing "Read directionally, the frame is the two-stream separation: an arrangement-only transition... cannot alter C, since S0 holds unconditionally."
**Problem**: The "Read directionally" remark re-asserts the frame already given in the Formal Contract ("No condition on arrangements... holds for arbitrary `Σ'.M(d)`"). It is the "new prose explains why the axiom is needed" pattern. The counterfactual preamble is acceptable as the ASN's derivation method, but the directional restatement adds nothing past the frame line.
**Required**: Delete the "Read directionally" sentence; the frame clause already carries it.

## OUT_OF_SCOPE

### Topic 1: S5 witness states do not satisfy S7b/S8a
S5's constructions use an arbitrary I-address `a` and so do not satisfy S7b (`zeros(a) = 3`) or tie V-positions to S8a. This is correct as a narrow consistency result (S5's frame discloses "witnesses are not claimed to satisfy later invariants"), and strengthening the witness to also satisfy S7b/S8a is an enhancement, not a defect — not required for the independence claim.

### Topic 2: Subspace-alignment between subspace(v) and the element-field component of M(d)(v)
The ASN correctly defers (Open Questions) the obligation that `subspace(v)` match the first element-field component of `M(d)(v)`. This is an operations-layer preservation property; its absence as a state invariant is appropriate.

VERDICT: REVISE
