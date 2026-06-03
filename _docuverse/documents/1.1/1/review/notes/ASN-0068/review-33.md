# Review of ASN-0068

I checked every claim's proof, the boundary cases (empty restriction, subspace-minimum V-position, differing depths, self-comparison, restriction-gap fragmentation, link subspace), and the central CV-MAX existence/uniqueness argument. I also audited for forward-reference accretion per the anti-bloat classifier.

## Findings on rigor

The hard proofs hold up.

- **CV-MAX existence**: the left/right walks are well-defined, the combined triple `R = (v_a − j, v_b − j, j + n_R)` is verified as a correspondence run by a correct two-region split (left region via the predecessor inverse + M-aux, right region via M-aux), and both maximality directions are discharged against the walk maximality of `j` and `n_R`. Left-walk termination via D-SEQ★/S8a (last-component bound `(v_a)_{m_a} − 1`) is sound and does not improperly lean on global finiteness.
- **CV-MAX uniqueness**: the lockstep reduction `δ = j²_a − j¹_a = j²_b − j¹_b = k¹ − k²` is correctly derived per-side via OrdinalShift's last-component formula + T3, and survives `m_a ≠ m_b` because each side reduces internally to its own depth. Both cases (`δ = 0`, `δ > 0`) reach the maximality contradiction with the range bounds (`0 ≤ δ−1 < n¹`) correctly established. Offset uniqueness is separately discharged. The `δ < 0` branch is covered by the WLOG swap.
- **CV-PRED**: existence (`v_m ≥ j+1`), uniqueness (TS2 at common amount/depth), and the inverse property are each proved, not asserted. The short-circuit reading of the maximality disjunctions (first disjunct fires when a predecessor is undefined) is consistent throughout.
- **CV-SPAN-VIEW / CV-FIN / CV-ATOM / CV-SYM / CV-RO / CV-DETERM**: each carries an explicit derivation; CV-SPAN-VIEW's T12 discharge (`actionPoint(δ(n,m)) = m = #v`) and CV-FIN's injective `run ↦ starting-pair` map are both correct.

Every claim has a proof or derivation; the five worked examples concretely verify the key postconditions (aggregation, self-transclusion independence, self-comparison diagonal, depth mismatch, restriction-induced fragmentation). No "by similarly," no checkmark-as-proof, no missing conjunct. The only cross-ASN references are to the foundation set (0034/0036/0047/0053/0058), which is permitted.

I found no rigor gap, no missing edge case, no hand-wave, and no clear meta-prose accretion that obstructs the argument. The degenerate-case claims (CV-SELF, CV-LINK-*, CV-IN-N) are derived consequences with proofs, which the depth standard requires rather than forbids; CV-IN-N mirrors the foundation's own T10a-N necessity pattern.

## OUT_OF_SCOPE

### Topic 1: Concurrent arrangement modification mid-comparison
**Why out of scope**: Correctly deferred to an Open Question. CV-RO/CV-DETERM establish snapshot semantics against a fixed `Σ`; concurrency invariants are new territory, not a defect here.

### Topic 2: Replication equivalence and multi-document correspondence composition
**Why out of scope**: Listed as Open Questions; these require BEBE/inter-server machinery and a composition algebra not yet introduced. Not errors in this pairwise operation.

VERDICT: CONVERGED
