# Cone Review — ASN-0036/D-CTG (cycle 2)

*2026-04-15 07:23*

I've read all current property files and YAML dependencies. Let me trace the cross-cutting chains against the foundation statements and previous findings.

The critical comparison is between properties that use the same inductive proof pattern. S8-depth, S8-fin, and D-CTG all establish invariants by induction over the operation history, citing AX-1 for the base case and AX-5 for the inductive case split.

---

### D-CTG's YAML dependency list omits AX-1 and AX-5, which its inductive proof explicitly cites — inconsistent with every sibling invariant that uses the same proof pattern

**Foundation**: AX-1 (InitialEmptyState) — provides the base case for every inductive invariant; AX-5 (ClosedWorldTransition) — provides the case split over Op for every inductive step
**ASN**: D-CTG (VContiguity), body text: "*Base case.* By AX-1 (InitialEmptyState), `dom(Σ₀.M(d)) = ∅` for every document `d`, so `V_S(d) = ∅` for every subspace `S`." and "*Inductive step.* … by AX-5 (ClosedWorldTransition), some op ∈ Op produces Σ' from Σ." D-CTG YAML depends: `[Sigma-M, V-S, SubspaceIdentifier, S8a, T1, T0, S8-depth, OrdinalShift]`.
**Issue**: Three ASN-0036 properties establish invariants by identical inductive structure: base case via AX-1, case split via AX-5, per-operation obligation deferred. S8-depth and S8-fin both include AX-1 and AX-5 in their YAML `depends` lists (S8-depth: `[Sigma-M, AX-1, AX-5]`; S8-fin: `[Sigma-M, AX-1, AX-5]`), establishing the convention that proof-infrastructure dependencies — not just formal preconditions — appear in the dependency declaration. D-CTG uses the same proof pattern and cites both axioms by name in its body text, but its YAML `depends` list omits both. The formal contract's preconditions section also omits them (listing only V_S, Σ.M(d), and T1), but this is consistent with S8-depth and S8-fin, whose formal preconditions likewise omit AX-1 and AX-5 — the convention places proof dependencies in YAML, not in the preconditions section. D-CTG violates only the YAML convention. A formalization tool constructing the build order from YAML dependency declarations would not know that D-CTG's verification requires AX-1 and AX-5 to be established first. Since D-CTG is a transitive dependency of D-SEQ, S8-crun, and ValidInsertionPosition, the gap propagates through the dependency DAG: any tool resolving transitive dependencies for VIP's verification would miss the induction-framework axioms needed at the D-CTG level.
**What needs resolving**: D-CTG's YAML `depends` must include AX-1 and AX-5, matching the convention established by S8-depth and S8-fin for invariants proved by induction over the operation history.
