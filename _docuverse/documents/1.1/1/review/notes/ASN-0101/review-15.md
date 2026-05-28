# Review of ASN-0101

## REVISE

### Issue 1: Confusing partition phrasing in D8 Group (iii) P4★ argument

**ASN-0101, D8 Group (iii) P4★ justification**: "When d'' = d, D0's effect partitions v ∈ dom(M'(d)) into Λ ⊎ Q ⊎ V_{S'}(d) for S' ≠ s_C (where S may equal s_C or s_L)"

**Problem**: The qualifier "for S' ≠ s_C" does not unambiguously characterize S'. The intended meaning is that S' is the unaffected subspace (i.e., S' ≠ S), but the literal reading "S' ≠ s_C" specifically picks out S' = s_L, which would force S = s_C and contradict the parenthetical "(where S may equal s_C or s_L)". The subsequent case analysis (v ∈ Λ, v ∈ Q, v ∈ V_{S'}(d) with S' = s_C and S ≠ s_C) makes the intended partition clear only after the reader has deciphered the prose; the partition expression itself is muddled.

**Required**: Rephrase as "Λ ⊎ Q ⊎ V_{S'}(d), where S' = {s_C, s_L} \ {S} is the unaffected subspace" or equivalent unambiguous wording that ties S' to its role as the complement of the affected subspace S, not to s_C.

### Issue 2: Incorrect citation of TS2 in D1 proof

**ASN-0101, D1 Justification, "Order preservation" paragraph**: "The middle case is excluded by TS2 (ShiftInjectivity, ASN-0034): u₁ = u₂ would force shift(u₁, n) = shift(u₂, n), i.e., v₁ = v₂, contradicting v₁ < v₂."

**Problem**: The step "u₁ = u₂ ⟹ shift(u₁, n) = shift(u₂, n)" is an application of *functionality* of shift (well-definedness as a function), not its *injectivity*. TS2 (ShiftInjectivity, ASN-0034) states the converse: shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂. The argument as written does not use TS2's injectivity direction; it uses the fact that equal inputs yield equal outputs, which is functionality. To use TS2 correctly, the proof would derive u₁ ≠ u₂ from v₁ ≠ v₂ (which follows from v₁ < v₂ by T1 irreflexivity) via TS2's contrapositive.

**Required**: Either restructure the argument to use TS2 correctly ("By T1 (a) irreflexivity v₁ ≠ v₂; by TS2's contrapositive, u₁ ≠ u₂, ruling out the middle case of trichotomy"), or replace the TS2 citation with a citation of OrdinalShift's definition (ASN-0034), which is what actually licenses the functionality step.

### Issue 3: "Vacuously at length 1" misnomer in S8★ justification

**ASN-0101, D8 Group (i) justification of S8★**: "S8's condition (a) holds by construction (each post-state V-position is its own length-1 run), and condition (b) holds vacuously at length 1"

**Problem**: At n_j = 1, condition (b) ranges over k ∈ {0}, which is non-empty. Condition (b) holds *trivially* at k = 0 (because shift(v_j, 0) = v_j by OrdinalShiftBase, so the equation reduces to M(d)(v_j) = a_j, the run's defining equation), not *vacuously*. Vacuous discharge requires an empty quantifier range; here the range is the singleton {0}.

**Required**: Replace "vacuously at length 1" with "trivially at length 1" or "by the run's defining equation at k = 0 (using OrdinalShiftBase)".

## OUT_OF_SCOPE

(none — the ASN's scope is well-bounded; topics adjacent to DEL such as INSERT undoing DEL, recoverability mechanisms, and version reconstruction appear only in the Open Questions section, which is the appropriate place for them)

VERDICT: REVISE
