# Cone Review — ASN-0034/D2 (cycle 5)

*2026-04-18 19:05*

### D2 Step 2 never discharges TumblerSub's own precondition `b ≥ a` for the subtraction `b ⊖ a`

**Foundation**: TumblerSub's Preconditions list `a ≥ w (T1)` as its entry condition — invoking TumblerSub at operand pair `(b, a)` (i.e., computing `b ⊖ a`) requires `b ≥ a`. D1's parallel TumblerSub invocation discharges this explicitly in its Depends: "TumblerSub (TumblerSub) — supplies component formulas for w = b ⊖ a, establishes w ∈ T from b ≥ a".

**ASN**: D2 Step 2 — "TumblerSub at `k = zpd(b, a)` yields `(b ⊖ a)ᵢ = 0` for i < k (the agreement prefix copied as zeros) and `(b ⊖ a)ₖ = bₖ − aₖ`...". D2's T1 Depends entry reads only "invoked in Step 2 to derive `bₖ > aₖ` at the divergence position from `a < b`", and the TumblerSub Depends entry enumerates only component formulas and the action-point/Pos identifications.

**Issue**: The subtraction `b ⊖ a` requires `b ≥ a` for TumblerSub to apply; this is supplied by `a < b` via T1 (strict-to-weak). Neither the proof prose nor the Depends lists records this discharge. A reader verifying precondition chains has no signal that T1 is consumed for this role and that TumblerSub's first precondition is satisfied.

**What needs resolving**: Either note in Step 2 that `b ≥ a` follows from the precondition `a < b` via T1 before invoking TumblerSub's component formulas, and extend D2's T1 and TumblerSub Depends entries to enumerate this role, matching D1's treatment.

---

### D2 Step 2 never explicitly concludes `b ⊖ a ∈ T`, a precondition of TA-LC

**Foundation**: TA-LC's Preconditions include `a, x, y ∈ T` alongside `Pos(x), Pos(y), actionPoint(x) ≤ #a, actionPoint(y) ≤ #a`. TumblerSub's Postconditions supply `a ⊖ w ∈ T`.

**ASN**: D2 Step 2 establishes, for the `b ⊖ a` branch, `Pos(b ⊖ a)` ("Hence Pos(b ⊖ a)") and `actionPoint(b ⊖ a) = k ≤ #a` ("Since k ≤ #a, TA0's preconditions are satisfied"), then Step 3 applies TA-LC. TA-LC's precondition list includes `a, x, y ∈ T` — here `y = b ⊖ a`.

**Issue**: The membership `b ⊖ a ∈ T` is needed for TA-LC (and for TA0 through TA-LC) but is never stated. Step 2 walks through positivity and action-point derivations but skips the carrier-membership claim that TumblerSub's postcondition supplies. D1's parallel structure calls this out ("First, w ∈ T: by hypothesis b ∈ T and a ∈ T, and since a < b implies b ≥ a, TumblerSub's preconditions are satisfied for minuend b and subtrahend a, and its postcondition gives w = b ⊖ a ∈ T"). D2 omits the analogous sentence.

**What needs resolving**: Add the `b ⊖ a ∈ T` conclusion to Step 2 (tied to TumblerSub's postcondition), matching the three-property check (∈ T, Pos, action-point) that D1 performs and that TA-LC's preconditions require.
