# Review of ASN-0069

## REVISE

### Issue 1: V1's IsDocument argument for the subsequent-fork sub-case is implicit

**ASN-0069, V1**: "In either case `d_new ∈ E'_doc`, `d_new ∉ E_doc` (pre-fork), `IsDocument(d_new)` (by KDeltaZerosK01, ASN-0047, which preserves zeros at both k = 0 and k = 1)"

**Problem**: KDeltaZerosK01 preserves zeros but does not establish that zeros equals 2. For the first-fork sub-case (k=1, t=d_src), zeros(d_src) = 2 follows from V0's precondition `d_src ∈ E_doc`. For the subsequent-fork sub-case (k=0, t=d_prev), the argument needs zeros(d_prev) = 2, which requires d_prev ∈ E_doc — and this in turn requires an inductive argument that all prior emissions of A_v(d_src) have IsDocument. The "in either case" treatment elides this induction. The V0 verification section (K.δ sub-case B) does spell out the induction: "zeros preserved at the first emission by KDeltaZerosK01 at k = 1, and preserved at each subsequent emission by KDeltaZerosK01 at k = 0" — but V1's standalone proof should not depend on the reader cross-referencing the verification section.

**Required**: V1 should state explicitly: "For the subsequent-fork sub-case, d_prev ∈ E_doc by P1 (entity permanence) applied to its prior K.δ event, so zeros(d_prev) = 2; KDeltaZerosK01 at k = 0 gives zeros(d_new) = 2, hence IsDocument(d_new). For the first-fork sub-case, the base case is direct from d_src ∈ E_doc." Equivalently, frame the IsDocument claim as an induction on A_v(d_src)'s emission count (parallel to V2's structural-ancestry induction).

### Issue 2: V8b's membership criterion elides the domain conjunct

**ASN-0069, V8b**: "Membership of `v ∈ Π_g` is determined by the current arrangements alone: by `v ∈ F` (a fixed condition) and by `M_g(d_src)(v) = M_g(d_new)(v)` (evaluated at `Σ_g`)."

**Problem**: The precise definition `Π_g := F ∩ Corr_g` requires three conditions for membership: (i) `v ∈ F`, (ii) `v ∈ dom(M_g(d_src)) ∩ dom(M_g(d_new))` (inherited from Corr_g), (iii) `M_g(d_src)(v) = M_g(d_new)(v)`. The text-level summary lists only (i) and (iii), eliding (ii). For partial functions, the equality (iii) is not well-defined when either side is undefined; the domain conjunct is load-bearing. This matters because the subsequent discussion of "K.μ⁻ on either side may remove `v`" depends specifically on whether `v` leaves dom(M_g(d_src)) ∩ dom(M_g(d_new)) — the domain change is the mechanism, not the equality.

**Required**: Either restate the membership criterion as "by `v ∈ F` AND by `v ∈ dom(M_g(d_src)) ∩ dom(M_g(d_new)) ∧ M_g(d_src)(v) = M_g(d_new)(v)`", or note explicitly that the equality is taken under the convention that "f(v) = g(v) is false when either f or g is undefined at v" so the domain conjunct is implicit in the predicate.

## OUT_OF_SCOPE

None. The ASN stays within scope (the CREATENEWVERSION operation as a state transition); Open Questions correctly defer future-ASN topics (concurrent forking, snapshot vs. living forks, fork of a transclusion, etc.) without claiming current coverage.

VERDICT: REVISE
