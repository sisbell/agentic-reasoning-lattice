# Citation Resolve — ASN-0036/D-CTG-depth — run 1

*2026-06-25T20:27:01Z*
*Model: sonnet*

## Output

I now have all the information needed. The claim references eight labels: `S8-depth`, `T1(i)`, `S8a`, `D-CTG`, `T0(a)`, `T3`, `S8-fin` (all in proof steps), and `T4` (in the post-∎ expository paragraph).

```
CLASSIFICATIONS:
- label: S8-depth
  direction: depends
  bullet: "- S8-depth (FixedDepthVPositions) — supplies the shared depth `m` for all positions in V_1(d), consumed as the proof's starting invariant that all elements have a common depth before the contradiction is constructed"

- label: T1(i)
  direction: depends
  bullet: "- T1(i) (LexicographicOrder, ASN-0034) — supplies the component-comparison clause of the lexicographic order; invoked at three points in the proof to derive u < w and w < x from the first differing component"

- label: S8a
  direction: depends
  bullet: "- S8a (ArrangementDomainRestriction) — supplies the well-formedness predicate (`#p ≥ 2 ∧ (A i : 1 ≤ i ≤ #p : pᵢ > 0)`) that the constructed intermediate w must satisfy before D-CTG can require w ∈ V_1(d)"

- label: D-CTG
  direction: depends
  bullet: "- D-CTG (VContiguity) — supplies the contiguity axiom applied to force w ∈ V_1(d) from u < w < x with matching subspace, depth, and S8a well-formedness; the claim's contradiction rests on producing infinitely many such w"

- label: T0(a)
  direction: depends
  bullet: "- T0(a) (UnboundedComponentValues, ASN-0034) — supplies, for any bound M, a witness n > M; consumed to construct the strictly increasing sequence n₁ < n₂ < … of admissible intermediates that contradicts S8-fin"

- label: T3
  direction: depends
  bullet: "- T3 (CanonicalRepresentation, ASN-0034) — supplies tumbler equality as component-wise identity; used to conclude that distinct values of n yield distinct depth-m positions w (differing at component j + 1)"

- label: S8-fin
  direction: depends
  bullet: "- S8-fin (FiniteArrangement) — supplies finiteness of dom(M(d)); the proof is by contradiction, and the infinite sequence of distinct positions in V_1(d) contradicts this finiteness"

- label: T4
  direction: forward
  bullet: "- T4 (HierarchicalParsing, ASN-0034) — cited as the structural reason zero is unavailable as a V-position component (zero is a field separator), grounding the 1-based ordinal convention for V-positions stated after the main proof"

RETRACTIONS: []
```
