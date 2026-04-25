# Regional Review — ASN-0034/T5 (cycle 1)

*2026-04-24 07:52*

### Redundant "#p ≥ 1" and informal "tumbler prefix" in T5 preconditions
**Class**: OBSERVE
**Foundation**: T5 (ContiguousSubtrees) Formal Contract; T0 (CarrierSetDefinition) axiom
**ASN**: T5 prose opens with "Let `p` be a tumbler prefix with `#p ≥ 1`"; the Formal Contract's Preconditions list states "`p` is a tumbler prefix with `#p ≥ 1`" but does not assert `p ∈ T`.
**Issue**: The term "tumbler prefix" is not formally defined. Since `≼` is defined only on `T × T` (via Prefix, whose carrier is T), `p` must be in `T`. T0 already guarantees `1 ≤ #t` for every `t ∈ T`, so the clause "with `#p ≥ 1`" is redundant. The precondition would be cleaner as `p ∈ T` with the length clause dropped. No soundness issue — every use of `p` in the proof is consistent with `p ∈ T`.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 378s*
