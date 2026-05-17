**B_fin (Registry Finiteness).** `(A Σ : Σ reachable from Σ_init : Σ.B is finite)`.

*Proof.* This proof records the finiteness component of the joint induction with B_type stated above; B_type's Case 2 step appeals to the finiteness conclusion established here at the same precondition state, and conversely the joint hypothesis at each step carries both B_type and B_fin. We re-present the finiteness argument as a standalone derivation to attach a labelled invariant for downstream citation (next's well-definedness, Bop's well-definedness, B7, B8, B9), but the inductive structure is the same as B_type's.

*Base case.* In the initial state, Σ.B = B₀. By B₀ conf. (SeedConformance), B₀ is finite. The invariant holds at genesis.

*Inductive step.* Assume Σ.B is finite for state Σ with registry B. Consider a transition Σ → Σ' producing registry B'. By B0a (Baptismal Closure), either the transition is Σ.B-frame, in which case B' = B and B' is finite by the inductive hypothesis; or the transition is baptismal, in which case B' = B ∪ {a} for a single new element a, and B' is the union of a finite set with a singleton, hence finite. In both transition classes, B' is finite. By induction, Σ.B is finite in every reachable state. ∎

*Formal Contract:*
- *Invariant:* `(A Σ : Σ reachable from Σ_init : Σ.B is finite)`.
- *Base:* B₀ conf. — B₀ is finite.
- *Preservation:* B0a — every transition either leaves Σ.B unchanged or adds exactly one new element.

B_fin discharges the finiteness premise that surfaces wherever a proof appeals to max(children(Σ.B, p, d)) or treats children as a finite set. Concretely it is invoked at: next's preconditions (which require B finite for max to exist in the non-empty branch), Bop's well-definedness proof (which selects max(children(Σ.B, p, d)) on the sibling-increment branch), B10's Case 2 ("a non-empty finite subset of T"), and B7, B8, B9 (which appeal to children's cardinality via hwm). Each of these proofs is licensed by B_fin in the reachable states it ranges over; without it, finite-Σ.B would be silently assumed at every call site.

From B₀ conformance (T4 for seeds) and B6(i) (T4 for parents), we derive by induction on the baptism sequence that T4 validity is a registry-wide invariant:
