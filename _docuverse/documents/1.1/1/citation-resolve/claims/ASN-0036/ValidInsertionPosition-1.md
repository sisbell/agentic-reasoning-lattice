# Citation Resolve — ASN-0036/ValidInsertionPosition — run 1

*2026-06-25T20:24:52Z*
*Model: sonnet*

## Output

All the ASN-0034 label files are cross-referenced but stored under a different node version. I have enough from the prose and the same-ASN files I read to classify all labels. Every reference in this claim's proof and formal contract consumes a symbol or result supplied by the cited claim — none are navigation pointers to downstream elaborations.

```
CLASSIFICATIONS:
- label: S8-depth
  direction: depends
  bullet: "- S8-depth (FixedDepthVPositions) — supplies the common V-position depth `m` of V_1(d) asserted in the preconditions and used throughout the proof to fix the tumbler length"

- label: S8a
  direction: depends
  bullet: "- S8a (ArrangementDomainRestriction) — supplies the `m ≥ 2` lower bound on depth, invoked in the preconditions, and the zero-free / componentwise-positive predicate verified on each satisfying `v` in the postconditions"

- label: D-MIN
  direction: depends
  bullet: "- D-MIN (VMinimumPosition) — supplies `min(V_1(d)) = [1, …, 1]` of depth `m`, the base position from which all satisfying `v` are constructed in both the definition and the proof"

- label: OrdinalShift
  direction: depends
  bullet: "- OrdinalShift (ASN-0034) — supplies the `shift` operator and its expansion `shift([1,…,1], j) = [1,…,1, 1+j]`, the key step in deriving the satisfying-set formula in the proof and formal contract"

- label: OrdShiftHom
  direction: depends
  bullet: "- OrdShiftHom (OrdinalShiftPreservation) — supplies part (a) `subspace(shift(v, n)) = subspace(v)`, invoked to establish `v₁ = 1` as the text subspace identifier for every satisfying position (postcondition)"

- label: T3
  direction: depends
  bullet: "- T3 (ASN-0034) — supplies the distinctness criterion for length-`m` tumblers that differ at any component, used to conclude the `N + 1` satisfying positions are pairwise distinct"

- label: NAT-order
  direction: depends
  bullet: "- NAT-order (ASN-0034) — supplies the strict total order on natural numbers, used to establish `1 + j ≠ 1 + j'` for `j ≠ j'`, driving the distinctness count in the proof and postconditions"

RETRACTIONS: []
```
