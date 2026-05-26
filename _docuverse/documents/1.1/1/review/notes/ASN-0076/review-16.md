# Review of ASN-0076

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Supersession-type convention (τ_sup designation)
**Why out of scope**: The ASN explicitly defers fixing a canonical supersession-type tumbler to a future ASN on type-endset conventions. The composite correctly admits `τ_sup` as a caller-supplied input with only `#τ_sup ≥ 1`, and L4/L9 license this generality.

### Topic 2: Authorization model
**Why out of scope**: The "informal motivation" in E6 hedges all discussion of who is authorized to fire K.λ on which document. The link model has no executor field; this is a future ASN.

### Topic 3: Cycle detection / acyclicity of supersession chains
**Why out of scope**: Listed in Open Questions. The link model imposes no acyclicity invariant; whether one should be added is a future design decision.

### Topic 4: Reader-side resolution policy
**Why out of scope**: E5 admits arbitrary fan-out; how readers choose among competing successors is policy. The illustrative appendix is honest about its limitations.

### Topic 5: Higher-arity supersession links and many-to-one/one-to-many supersession
**Why out of scope**: The current composite produces arity-3 supersession links. Extensions belong to a future ASN.

### Topic 6: Notification mechanisms for original owner
**Why out of scope**: E10 explicitly establishes non-notification as structural, citing pull-model architecture. Push notification belongs to a future ASN if at all.

---

Notes on what was checked and found correct:

- E0's discharge of K.λ preconditions, including the length-preservation/zero-preservation/#E-preservation induction under inc(·, 0) via TA5(c) + TA5(b) + TA5-SigValid + T4 field-segment constraint.
- E0's identification of `max{...}` at Σ_1 via T10a.7 strict monotonicity on the initial-segment enumeration.
- T12 discharge for the three supersession spans via OrdinalDisplacement (n=1, m=#x).
- ValidComposite★ status via vacuous J0/J1★/J1'★ (K.λ frame preserves C and M).
- E2's pairwise distinctness via SequentialTransitionAxiom + L11a, with the redundant per-step freshness confirmation.
- E5's induction: base case vacuity, IH structure, conclusion (d) pairwise distinctness across all 2k events.
- E4 + E7's structural witness via PrefixSpanCoverage + L13.
- L12 inheritance across both K.λ steps for E1, E8, E9.
- Worked example arithmetic: zeros at positions 2/4/6 of [3.0.5.0.7.0.2.1] give zeros=3; sig=#ℓ at 8 by TA5-SigValid yields ℓ_sup = [4.0.2.0.3.0.2.2].
- Foundation-invariant inheritance via ExtendedReachableStateInvariants and ExtendedTransitionInvariants.
- No non-foundation cross-ASN references; no notational reinvention.
- Boundary cases for first-vs-subsequent emission, `d_new = home(ℓ_old)` vs not, multiple parallel supersessions, and minimum tumbler depths are all handled.

VERDICT: CONVERGED
