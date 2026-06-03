# Review of ASN-0102

I read the note as a specification of a single new state transition (COPY) with its precondition, five-component frame, and an invariant suite (X1–X16). I checked each derivation, the boundary cases, and the discharge of every conjunct of the foundation's reachable-state and transition invariants.

## Findings

The proofs hold up under scrutiny. Spot checks that matter:

- **X7 / X16 (no-overwrite, density).** The three-class tiling `[1,p) ∪ [p,p+W) ∪ [p+W,n_S+W] = [1,n_S+W]` is exact for all `1 ≤ p ≤ n_S+1`, including `p=1` (unmoved empty) and `p=n_S+1` (displaced empty). The no-overwrite conclusion correctly rests on range-disjointness of copied vs. displaced images, not on prior occupancy — and the note is careful to separate "freed slots" from "occupied portion of the copy region."
- **X8 (within-reference non-coalescence).** The two-step argument (V-contiguity ⟹ V-adjacency of maximal runs; then maximality ⟹ non-I-adjacency `a_{j+1} ≠ a_j + n_j`) is rigorous, not a "by maximality" hand-wave. The `≤ k, equality iff no inter-reference boundary I-adjacent` claim composes correctly even under chained same-origin references (no new I-adjacency is manufactured by a merge).
- **X14 (coupling discharge).** The New/Old split is sound. J1★ fires only on `New ⊆ A` (all recorded); J1'★'s Old branch correctly leans on P4★ at the pre-state, with the length-1-composite framing legitimately licensed by the explicit `ValidComposite★` amendment and the inductive availability of P4★ at a prior boundary. P7/P4★/P4a/P7a preservation and the P3 transition obligation are each derived from the frame, not asserted.
- **wp(COPY, S3★)** is a genuine non-trivial computation, reduced to the copied region and discharged by C1 — exactly the load-bearing dependence the content-subspace conjunct of P1 was added to secure.

Boundary coverage is complete for COPY-specific cases: empty target subspace (first-insertion depth choice), append (`p=n_S+1`, trailing boundary absent), self-transclusion (`Old ≠ ∅`, snapshot resolution via atomicity), cross-origin separation, and zero-width exclusion (`W ≥ 1`). Each is exhibited in a worked example with the relevant claims checked.

No REVISE items: no proof-by-checkmark, no skipped invariant conjunct, no undischarged boundary, and every cited ASN is a foundation ASN used (not reinvented).

## OUT_OF_SCOPE

### Topic 1: The four Open Questions (later re-displacement, transitive containment-of-references, time-varying views, unreachable allocating document)
Why out of scope: these concern subsequent operations and reachability dynamics beyond a single COPY transition; they are correctly posed as future work, not gaps in this note.

VERDICT: CONVERGED
