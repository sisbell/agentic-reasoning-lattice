**AX-5 (ClosedWorldTransition).** Every state transition is produced by one of six operations. Let Op = {INSERT, DELETE, COPY, MOVE, REARRANGE, APPEND}. For every pair of consecutive reachable states Σ, Σ' in a system trace, there exists an op ∈ Op such that Σ' = op(Σ).

This is the closed-world assumption on the transition relation. The system state Σ = (C, M) (comprising the content store Σ.C and the arrangement Σ.M(d) for each document d) evolves only through these six operations — no other mechanism modifies any component of Σ. In TLA+ terms, this axiom corresponds to the `Next` predicate: `Next ≡ INSERT ∨ DELETE ∨ COPY ∨ MOVE ∨ REARRANGE ∨ APPEND`.

Every invariant proof that proceeds by induction over the operation history depends on Op being exhaustive. The inductive step must show that the invariant is preserved by each op ∈ Op; if Op failed to enumerate all transitions, the inductive step would not cover every possible Σ → Σ', and the invariant could not be established for all reachable states. This axiom provides the single formal anchor that those proofs cite.

*Formal Contract:*
- *Axiom:* `(A Σ, Σ' : Σ' is a successor of Σ in a system trace : (E op : op ∈ Op : Σ' = op(Σ)))` — every state transition is produced by an operation in Op.
- *Definition:* `Op = {INSERT, DELETE, COPY, MOVE, REARRANGE, APPEND}` — the complete, closed set of state-modifying operations.
