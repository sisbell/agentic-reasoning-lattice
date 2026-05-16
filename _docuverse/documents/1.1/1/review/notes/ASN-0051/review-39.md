# Review of ASN-0051

## REVISE

### Issue 1: Notation note's description of shift conflicts with the OrdinalShift definition
**ASN-0051, opening Notation paragraph**: "`a + k = shift(a, k)`, the k-th ordinal advance of a within its parent's sequence (TumblerAdd applied at the position one past a's last nonzero component; at k = 1 the result is the next sibling under a's prefix)"
**Problem**: ASN-0034's OrdinalShift defines `shift(v, n) = v ⊕ δ(n, #v)`, where δ has its action point at position #v. TumblerAdd modifies position #v (the last position), not one past it. For T4-valid v, `sig(v) = #v`, so the action point IS the position of v's last nonzero component, not one past it. "One past v's last nonzero component" would be position #v + 1, which doesn't exist in v's representation — and would actually correspond to `inc(v, 1)`, which appends a new component producing v's *child*, not its next sibling. The phrasing therefore conflates shift (last-component value increment) with inc (depth-extending append), while the parenthetical's own conclusion ("the next sibling under a's prefix") correctly describes shift. The same notation note appears in subsequent uses (`a + 5 = a₅ + 1` in worked example) where shift's "modify last component" behaviour is what's actually used.
**Required**: Replace "TumblerAdd applied at the position one past a's last nonzero component" with "TumblerAdd applied at the position of a's last nonzero component (position #a for T4-valid a)" or equivalent — matching ASN-0034's OrdinalShift definition and the sibling-result claim that follows.

### Issue 2: Apparent circularity in SV6's T4-validity verification of t
**ASN-0051, SV6 proof, T4-validity of t paragraph, "t₁ ≠ 0" sub-bullet**: "Position 1 lies in [1, k − 1] (since k > p₃ ≥ 6, so k ≥ 7 ≥ 2). (`p₃ ≥ 6` follows from T4-validity: `t₁ ≠ 0` gives `p₁ ≥ 2`, no adjacent zeros gives `p₂ ≥ 4` and `p₃ ≥ 6`.) Conclusion (b) gives t₁ = s₁, and s is T4-valid, so t₁ = s₁ ≠ 0."
**Problem**: The parenthetical cites "`t₁ ≠ 0`" as a premise in the derivation chain `p₁ ≥ 2 → p₂ ≥ 4 → p₃ ≥ 6`, but the surrounding step is itself titled "For t₁ ≠ 0" — t₁ ≠ 0 is the very claim being established here. The valid argument runs through s's T4-validity (which IS a precondition of SV6): s's leading-nonzero conjunct gives `s₁ ≠ 0`, hence `p₁ ≥ 2`; s's no-adjacent-zeros conjunct gives `p₂ ≥ p₁ + 2 ≥ 4` and `p₃ ≥ p₂ + 2 ≥ 6`. The bound `p₃ ≥ 6` thus follows from s's T4-validity alone, and `t₁ ≠ 0` is then derived (in the sentence immediately after the parenthetical) via Conclusion (b) plus s's T4-validity. As written, the prose presents the dependency backwards.
**Required**: Replace the parenthetical's "T4-validity: `t₁ ≠ 0` gives `p₁ ≥ 2`" with "T4-validity of s: `s₁ ≠ 0` gives `p₁ ≥ 2`" — breaking the apparent circularity and explicitly grounding `p₃ ≥ 6` in s's T4-validity (a precondition) rather than t's (which is being proved).

## OUT_OF_SCOPE

None. The ASN's scope is well-defined: broader-level spans (k ≤ p₃) and link-subspace contributions to projection are explicitly deferred to ASN-0034's address-hierarchy treatment and a future Link Subspace ASN respectively, with adequate scope notes. The eight open questions appropriately identify future work without leaving load-bearing gaps in the present claims.

VERDICT: REVISE
