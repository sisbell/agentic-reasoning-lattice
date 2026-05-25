# Channel Assignment — ASN-0069 review-5

**Date:** 2026-05-25 13:15

## Issue 1: V8b monotonicity is incorrect — counterexample via K.μ⁻ + K.μ⁺ round-trip
Reason: The fix is derivable from ASN-0047's transition semantics already cited in ASN-0069. Either restrict V8b's scope to "in the absence of further K.μ⁺ on either side" or replace with the trivial invariant Π_g ⊆ F, both arguable from existing ASN content.

## Issue 2: V8b's proof cites P3 for a property P3 does not provide
Reason: P3's scope (C, E, R, L only — explicitly excluding M) is documented in ASN-0047 references already invoked elsewhere in ASN-0069. The fix is to drop the P3 citation and either supply a correct argument for whatever weakened claim survives or excise V8b — purely internal.

## Issue 3: V11 inductive step relies on inclusion not justified by V4
Reason: The fix is a formulation choice between restricting V11 to chains without intermediate non-fork transitions or rewriting the IH around "v propagated through the chain" as a primitive. Both options can be argued from V4, V5a, and the existing framing without external consultation.

## Issue 4: V2 derivation uses unintroduced notation
Reason: Pure editorial fix — introduce `d¹` explicitly as the first-fork output `inc(d_src, 1)` or use `d_new` consistently with the base case. No external context required.

## Issue 5: V4b's derivation appeals to J4 for a domain restriction J4 does not provide
Reason: ASN-0069's own §"The Arrangement Layer" already states that J4 constrains only the range and that V4 strengthens this to literal domain inheritance. The fix is to cite V0 or V4 as the source of "exactly V_{s_C}(d_src)" rather than J4 — internal recitation.

## Issue 6: V0's first-fork freshness verification chain has a redundant step
Reason: The clarification distinguishes the parent allocator's K.δ event (which placed A_v(d_src)'s base inc(d_src, 1) into E) from A_v(d_src)'s own subsequent sibling-stream emissions. Both invocations of T10a are already cited; the fix is rephrasing to make the constraint attribution explicit.
