**AX-6 (MinimumPresence).** For every document d and subspace S, if V_S(d) is non-empty then the all-ones position belongs to V_S(d):

`V_S(d) ≠ ∅  ⟹  [S, 1, …, 1] ∈ V_S(d)`

where the tuple has length m, the common depth of V-positions in subspace S (S8-depth), with m ≥ 2 (S8-vdepth). The tuple [S, 1, …, 1] is a finite sequence of m naturals, hence a member of T by T0 (CarrierSetDefinition, ASN-0034). Every post-subspace component equals 1, satisfying S8a.

This is a design requirement on valid arrangements. Every operation that populates or modifies V_S(d) must ensure that the resulting set, if non-empty, contains [S, 1, …, 1]. An INSERT creating the first position in a subspace must place it at [S, 1, …, 1]; a DELETE must not remove [S, 1, …, 1] while other positions remain. Each operation specification must individually discharge this obligation.

*Formal Contract:*
- *Axiom:* `V_S(d) ≠ ∅ ⟹ [S, 1, …, 1] ∈ V_S(d)` — for any non-empty subspace, the absolute minimum position is present. Operations must preserve this invariant.
