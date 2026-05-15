# Review of ASN-0082

This is a thorough analysis. Let me document what I checked and where, if anywhere, the proofs leave gaps.

## REVISE

(No items.)

After working through the proofs and edge cases systematically, I did not find issues warranting revision. Specifically I verified:

**I3 (post-insertion shift):**
- The eight clauses (I3, I3-L, I3-X, I3-D, I3-V, I3-C, I3-CS, I3-CX) are pairwise consistent — the consistency check at "Shifted vs left/shifted/cross-subspace" and "Vacated vs assignment regions" is correct.
- I3-V's exclusion clause `v ∉ {shift(u, n) : ...}` correctly handles the overlap case (worked example: [1,5] is both an original position and shift([1,3], 2)).
- The wp derivation for I3-VP cleanly surfaces the three pre-state obligations and discharges each.
- I3-S2's seven-case wp analysis is exhaustive across the four region pairings.
- Boundary cases (insert at start with p = [1,1], insert past end p = [1,6], empty document) all verify.
- Cross-subspace examples exercise both S=1 active / S=2 frame and S=2 active / S=1 frame correctly.

**D-SHIFT (post-contraction shift):**
- The depth scoping `#p = 2` justification via TA4 is mathematically sound — constraints (i), (ii), and (iv) of TA4 do collide jointly with S8a positivity at deeper depths.
- D-SEP(a)'s reduction to TA4 at depth 1 with vacuous zero-prefix holds.
- D-SEP(b)'s Case 2 use of D-CTG with `u = [1, p₂ + c − 1]` to establish r ∈ V_1(d) is valid; the containment precondition discharges u ∈ V_1(d).
- D-CTG-post's closed-form derivation V_1(d') = {[1, k] : 1 ≤ k ≤ N − c} covers all four boundary configurations (L empty, R empty, both empty, both non-empty).
- The NAT-sub chains deriving `n + ℓₘ = ℓₘ + n` (I3-S) and `(s₂ + c') − c = (s₂ − c) + c'` (D-S) explicitly avoid commutativity-of-+, which the foundation does not provide.
- PositiveOffsetExceeds correctly handles both left and right summand forms without commutativity.

**Cross-cutting:**
- All cross-ASN references are to foundation ASNs only (0034, 0036, 0053).
- OrdinalOrderEquivalence derivation from T1 is correct, including the k = 2 boundary where ord's pre-divergence range is empty.
- All structural preservation lemmas (I3-VD/VP/S3/S2/fin/S7 and S8-depth-post / S8a-post / D-CTG-post / D-MIN-post / D-SEQ-post / S8-fin-post / S2-post / S3-post / S7-post) cite only earlier results, no circularity.

## OUT_OF_SCOPE

### Topic 1: Full INSERT operation (content placement at gap)
**Why out of scope**: The ASN explicitly scopes I3 to the shift sub-operation and defers content allocation at [p, shift(p, n)) to a future INSERT ASN. The handoff to S0-weakening is clearly stated.

### Topic 2: Non-text subspace contraction (tombstoning)
**Why out of scope**: The ASN's subspace scoping axiom S = 1 is justified by the foundation's text-only D-CTG/D-MIN/D-SEQ. Link-subspace mutation uses tombstoning, deferred to a future ASN.

### Topic 3: Deeper-depth contraction
**Why out of scope**: Explicitly raised in Open Questions. Generalization requires either strengthening TA4 or a separate derivation from TumblerAdd/TumblerSub.

### Topic 4: External reference update across shifts
**Why out of scope**: Listed in Open Questions. Concerns external state bookkeeping rather than arrangement semantics.

### Topic 5: Span behavior under shift when span straddles the cut point
**Why out of scope**: I3-S and D-S are restricted to spans wholly within the shifted/right region. Straddling spans need separate treatment.

### Topic 6: Concurrent INSERT/DELETE interaction, COPY, MAKELINK, link preservation
**Why out of scope**: Separate ASNs.

VERDICT: CONVERGED
