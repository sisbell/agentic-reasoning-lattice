# Review of ASN-0061

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Depth generalization is harder than the open question suggests
The round-trip property D-SEP relies on TA4 at ordinal depth 1, where the zero-prefix precondition `(A i : 1 ≤ i < k : aᵢ = 0)` is vacuously satisfied. At ordinal depth > 1, D-SEQ positions have the form `[1, ..., 1, k]` — the intermediate components are 1, not 0, so TA4 fails. Concretely: `[1, k+c] ⊖ [0, c]` diverges at position 1 (where `1 ≠ 0`), producing `[1, k+c]` rather than `[1, k]`. TumblerSub copies the tail from the minuend past the divergence point, so the width is silently discarded. Generalization requires either a restricted subtraction that operates only on the last component, or a new algebraic identity. The open question correctly identifies this but understates the obstacle.
**Why out of scope**: This is new algebraic work, not an error in the depth-2 proofs.

### Topic 2: Link-endset reachability after orphaning
When DELETE orphans I-addresses that are referenced by link endsets, the links remain immutable (L12) but their endset spans point to content unreachable through any current arrangement. Characterizing this "dangling endset" state and its effect on link traversal belongs in a future link-semantics ASN.
**Why out of scope**: Link traversal semantics are explicitly deferred.

VERDICT: CONVERGED

---

I verified every proof step, every invariant conjunct, every edge case (L=∅, R=∅, full delete, width-1 deletion), the composite transition decomposition, and the coupling constraints. The proofs are explicit, the block case analysis is exhaustive (six cases, all with interior-point validity checked), and the worked example correctly exercises case (f). The shift σ is shown order-preserving via TA3-strict, gap-closing via TA4 at depth 1, and compatible with block consistency via natural-number commutativity. All 27 invariants from ExtendedReachableStateInvariants are addressed — the frame-dominated ones (P0, P1, P2, L-series, CL-OWN) via D-CF, and the arrangement-sensitive ones (S2, S3★, S8a, S8-depth, S8-fin, D-CTG, D-MIN, P4★) via direct argument.
