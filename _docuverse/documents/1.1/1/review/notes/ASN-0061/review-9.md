# Review of ASN-0061

## REVISE

### Issue 1: K.μ⁺ preconditions D-CTG and D-MIN not verified in composite transition

**ASN-0061, DELETE as Composite Transition, step (ii)**: "The new V-positions σ(v) satisfy S8a ... satisfying S8-depth. The domain remains finite (S8-fin) ... Frame: C' = C, E' = E, R' = R."

**Problem**: K.μ⁺ (ASN-0047) explicitly requires the resulting M'(d) to satisfy D-CTG and D-MIN. The composite transition section verifies S8a, S8-depth, S8-fin, referential integrity, and no V-position collisions for step (ii), but omits the two structural invariants that govern the shape of the V-position domain. Without this verification, the claim "DELETE is a valid composite" is incomplete — and D-DP's proof depends on that claim.

**Required**: Add explicit verification that the post-K.μ⁺ arrangement satisfies D-CTG and D-MIN. The argument is direct:

- **D-CTG**: L occupies ordinals below ord(p); Q₃ occupies ordinals from ord(p) onward (by D-SEP). At depth 2 these are consecutive natural-number ranges that abut with no gap (D-SEP) and no overlap (D-BJ + ordering). L ∪ Q₃ is therefore a single contiguous ordinal range.
- **D-MIN**: When L ≠ ∅, min(L ∪ Q₃) = min(L) = min(V_S(d)) = [S, 1, ..., 1] by D-MIN on the pre-state. When L = ∅, p = v_min = [S, 1, ..., 1] (D-MIN on pre-state), so σ(r) has ordinal ord(p) = [1, ..., 1], giving min(Q₃) = [S, 1, ..., 1].

The same argument should be noted for step (i): K.μ⁻ removes the suffix from p onward, leaving L — a prefix of the original contiguous range — which satisfies D-CTG and D-MIN (or is empty, satisfying both vacuously).

---

### Issue 2: D-MIN preservation absent from D-DP, invariant verification, and Properties Introduced

**ASN-0061, D-DP**: "DELETE preserves D-CTG — follows from ArrangementInvariantsLemma once DELETE is shown valid"

**Problem**: ArrangementInvariantsLemma (ASN-0047) establishes that valid composites preserve both D-CTG **and** D-MIN. The ASN singles out D-CTG for an explicit lemma (D-DP) while leaving D-MIN entirely implicit. This creates three gaps:

1. D-DP's statement names D-CTG but not D-MIN.
2. The invariant preservation section verifies P0–P8, S0–S8-fin individually but never mentions D-MIN (even though it appears in ReachableStateInvariants alongside D-CTG).
3. The Properties Introduced table lists D-DP as "DELETE preserves D-CTG" with no D-MIN counterpart.

D-MIN is a co-equal arrangement invariant. An arrangement that is contiguous but starts at [S, 5] instead of [S, 1] would violate D-MIN while satisfying D-CTG, so the two are independent.

**Required**: Either expand D-DP to cover both D-CTG and D-MIN (e.g., "D-DP — ArrangementStructurePreservation: DELETE preserves D-CTG and D-MIN"), or introduce a separate D-DM lemma for D-MIN. Update the invariant preservation section and Properties Introduced table accordingly.

---

## OUT_OF_SCOPE

### Topic 1: Extension to the extended state model (C, L, E, M, R)

**Why out of scope**: The ASN works with the basic state Σ = (C, E, M, R), which is a self-consistent model defined by ASN-0047. The extended state adds the link store L and introduces additional invariants (L0, L1, L1a, L3, L12, L14, CL-OWN, S3★, S3★-aux) and amended transitions. DELETE trivially preserves L (no elementary transition in the composite modifies it), and all L-related invariants follow from L' = L. But verifying this belongs to an ASN that integrates DELETE with the full extended state, not to this one.

VERDICT: REVISE
