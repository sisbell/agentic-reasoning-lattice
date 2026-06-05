# Review of ASN-0115

## REVISE

### Issue 1: R6 (SilentGapFiltering) has no concrete worked instance for the partial-delivery boundary

**ASN-0115, R6 / §"Partial delivery"**: "A named position with no binding in the consulted arrangement … contributes nothing to the delivery and causes no failure."

**Problem**: R8, R10, and R11 each get a worked instance, but R6 — the partial-delivery boundary, which is exactly the boundary case rigor demands (clip, overrun, present-and-absent named positions in one request) — gets none. The §"Exactness" prose promises "an implementation must clip to the interval exactly," yet no scenario verifies a delivery where the named interval reaches past the bound range and the overrun positions are filtered. The core resolution/exactness/order claims (R1, R3 lower bound, R5) are exercised only incidentally inside the advanced revelations; the ordinary "deliver a multi-position content span, with a boundary overrun" case is never shown end-to-end.

**Required**: Add a worked instance: e.g. a content subspace with `V_1(d) = {[1,k] : 1 ≤ k ≤ 4}`, a spec naming `[1,2]..[1,7]`, delivering `⟨content,Σ.C(M(d)([1,2]))⟩,…,⟨content,Σ.C(M(d)([1,4]))⟩` and filtering `[1,5],[1,6]` silently — checking R1, R3 (both bounds), R5, and R6 against the result.

### Issue 2: R6 establishes silent filtering but does not explore where gaps can occur

**ASN-0115, R6**: "the unbound region is represented by its absence."

**Problem**: An established postcondition with an unexplored consequence. The substrate fixes per-subspace contiguity — D-CTG / D-SEQ (ASN-0036) and D-CTG★ / D-SEQ★ (ASN-0047) make each subspace's active V-positions the contiguous prefix `{[S,1,…,1,k] : 1 ≤ k ≤ n_S}`. It follows that within the consulted arrangement an *interior* named position can never be unbound: a gap inside `[s, s⊕ℓ)` is impossible, and every unbound named position is necessarily a boundary overrun past `n_S`. R6 is stated as if interior gaps were possible ("the unbound region"), missing this sharpening. This is the derivation that connects R6 to the §"Exactness" clip remark and tells the reader the gap is always a tail, never a hole.

**Required**: Derive, from D-SEQ★/D-CTG★, that the unbound portion of `⟦σ⟧` is always a terminal overrun of the subspace's contiguous range, and restate R6 with that precision.

### Issue 3: No frame statement that RETRIEVEV leaves the state unchanged

**ASN-0115, R0 / §"What … delivery is"**: `deliver(R, Σ)` is introduced as a function returning material.

**Problem**: The ASN never states that the operation produces no state transition — that `Σ.C`, `Σ.L`, `Σ.M`, and the rest are untouched by delivery. The project's other query operation states this explicitly (ASN-0086, Observe: "Observe leaves Σ unchanged"), so the convention is to record purity as a frame, not leave it implicit in the functional notation.

**Required**: Add a one-line frame/purity statement that RETRIEVEV reads state and produces no transition (no component of Σ is modified).

## OUT_OF_SCOPE

### Topic 1: Relationship between spec-start depth `#s` and the consulted subspace depth `m_{s₁}(d)`

**Why out of scope**: The V-spec imposes `#s ≥ 2` and ordinal-level but does not require `#s = m_{s₁}(d)` (S8-depth). A depth-mismatched spec still yields a well-defined, exact `act` by T1 (R3 holds tautologically; `item` stays total), so no invariant is violated — selection is mechanical. What a depth-`#s` interval *should mean* against a depth-`m` arrangement is an addressing-semantics question for a future ASN, not a defect here.

VERDICT: REVISE
