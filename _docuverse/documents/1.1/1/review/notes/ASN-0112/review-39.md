# Review of ASN-0112

I worked the arithmetic in multiple configurations (single content position, single subspace, cross-subspace equidepth, and the depth-divergent `m_C=3>m_L=2` variant) and the coverage proofs (V2 via D0/D1), the tightness distinction (V3 vs V-ReachTight), origin permanence (V8/V18), and the exact-cover/bounding-box split (V5/V6) all hold. The two-case structure on `#origin_d` vs `#reach_d` is genuinely exhaustive and correctly avoids assuming level-uniformity. One precision defect remains in the weakest-precondition analysis.

## REVISE

### Issue 1: wp is computed over a universally-valid biconditional, not a contingent property

**ASN-0112, Preconditions and well-definedness**: "The companion reach property factors the same way along the orthogonal endpoint axis, via V-ReachTight (vacuously true on the `⟨⟩` result): `wp(RETRIEVEDOCVSPAN(d), V-ReachTight) = (O(d) = ∅ ∨ #origin_d ≤ #reach_d)`."

**Problem**: V-ReachTight is defined (Claims table; "The constructed endpoint…" paragraph) as the biconditional `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d`, and it is *proved to hold in every state* (D1 closes the round-trip, D0 makes it fail otherwise). A theorem that holds in all reachable states is, as a postcondition, always satisfied — so `wp(op, V-ReachTight)` is trivially `true` (the entire pre-state space), **not** the stated `(O(d) = ∅ ∨ #origin_d ≤ #reach_d)`.

The condition `(O(d) = ∅ ∨ #origin_d ≤ #reach_d)` is the weakest precondition of the *contingent* property `reach(σ_d) = reach_d` (reach attains the constructed endpoint), which is true in some states and false in others. The Exact case is handled correctly precisely because `Exact` is named as a contingent state-property; the reach case borrows the *theorem* name instead of the analogous contingent property. The asymmetry is the tell.

**Required**: Introduce a contingent tightness predicate (analogous to `Exact`), e.g. `Tight ≡ "reach(σ_d) = reach_d"`, and compute `wp(RETRIEVEDOCVSPAN(d), Tight) = (O(d) = ∅ ∨ #origin_d ≤ #reach_d)`, deriving forward (via D1) and converse (via D0) exactly as the Exact factoring does via V5/V6. Reserve "V-ReachTight" for the universally-valid biconditional it actually denotes.

## OUT_OF_SCOPE

### Topic 1: Multi-subspace extent-to-count relation
The first Open Question asks what invariant relates extent to occupied count in the cross-subspace case. Correctly deferred — it concerns a relation this single-span query cannot express, and the honest negative (count not recoverable, V12 restricted to single-subspace) is already stated.

### Topic 2: Per-subspace exact reporting
Faithful per-subspace decomposition belongs to RETRIEVEDOCVSPANSET / ASN-0113, explicitly out of scope; this ASN correctly limits itself to the single bounding span and proves the bounding-box degradation (V6) rather than attempting fragmentation.

VERDICT: REVISE
