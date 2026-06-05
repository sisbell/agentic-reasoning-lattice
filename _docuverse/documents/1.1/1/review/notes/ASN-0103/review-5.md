# Review of ASN-0103

## REVISE

### Issue 1: `max(D_A)` well-definedness is never established

**ASN-0103, Effect One / CND.alloc / Worked Example**: "`d = inc(d_prev, 0)` otherwise, where `d_prev = max(D_A)`" and "`d_prev = max(D_A) = d1`".

**Problem**: The core definition of the operation in the non-empty case depends on `max(D_A)` existing, but the ASN never establishes that `D_A` is finite (equivalently, has a maximum). The cited invariant package supplies `C-fin` and `L-fin` but there is no entity-set finiteness invariant in `ExtendedReachableStateInvariants`, and none is cited or argued here. This is precisely the obligation the foundation discharges explicitly elsewhere — ASN-0093's K.α reads "The `max` is well-defined because the set is finite (C-fin restricted by `origin(·) = d`)." The analogous justification for `D_A` is absent, so the central allocation rule rests on an unproven existence claim.

**Required**: Add a one-line justification that `D_A ⊆ E` has a maximum at every reachable state — e.g., `E` is finite because `Σ₀.E = {n₀}` is finite and each transition (K.δ) adds at most one entity, so `D_A` is finite and `max(D_A)` exists. Without this, `CND.alloc` and the worked example invoke an operation that may be undefined.

### Issue 2: "next emission of `A_doc(A)`" overclaims relative to what is derived

**ASN-0103, Effect One**: "`D_A = {…}`, which is exactly the set of `A_doc(A)` emissions present in E" and "In both cases `d` is the next emission of `A_doc(A)`."

**Problem**: That `inc(max(D_A), 0)` is *the next emission* of the stream (rather than merely *an* address strictly past `max(D_A)`) requires `E_doc ∩ S(A, 2)` to be a contiguous initial prefix of the stream — otherwise a gap below `max(D_A)` would mean `d` skips stream positions. The contiguity is asserted but not derived. It is provable (by induction over K.δ, using P1 entity permanence plus the always-pick-the-frontier allocation discipline, analogous to B1's ContiguousPrefix over the registry), but the ASN works over `E` and supplies no such argument. The load-bearing properties (freshness, monotonicity, uniqueness) hold without contiguity, so this is a framing/rigor gap rather than a soundness failure — but the "exactly … emissions present in E" and "next emission" wording claims more than is shown.

**Required**: Either derive the contiguity of `E_doc ∩ S(A, 2)` (cite P1 + sequential frontier discipline) so "next emission" is justified, or weaken the prose to claim only what is needed (a fresh address strictly exceeding `max(D_A)`).

## OUT_OF_SCOPE

(none — the ASN confines itself to creation; CREATENEWVERSION appears only as contrast, with no claim defined for it, and the deferred ω-coupling is appropriately routed to a future registry-carrying ASN.)

VERDICT: REVISE
