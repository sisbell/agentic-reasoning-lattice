# Cross-cutting Review — ASN-0036 (cycle 1)

*2026-04-13 01:24*

I've read the full ASN-0036 and its ASN-0034 foundation statements, tracing every precondition chain, checking quantifier scope, verifying case exhaustiveness, and confirming definition consistency across properties. Three issues found, all in the S8 (correspondence-run decomposition) dependency structure.

---

### S8 property table omits S3 dependency
**Foundation**: S3 (ReferentialIntegrity) — `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
**ASN**: S8-depth definition of correspondence run: *"A correspondence run in document d is a triple (v, a, n) with v ∈ dom(Σ.M(d)), **a ∈ dom(Σ.C)**, and n ≥ 1"*; S8 proof, Existence step: *"form the singleton run (v, a, 1) — a valid correspondence run per the S8-depth definition, since v ∈ dom(Σ.M(d)), a ∈ dom(Σ.C), and n = 1 ≥ 1"*
**Issue**: The S8 proof constructs singletons `(v, M(d)(v), 1)` and claims they are valid correspondence runs. The correspondence-run definition requires `a ∈ dom(Σ.C)`. The proof establishes this via `M(d)(v) ∈ dom(Σ.C)`, which is exactly S3. Yet the property table lists S8 as *"theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TS4, OrdinalShift (ASN-0034)"* — S3 is absent. The formal contract correctly includes S3, creating an inconsistency between the two dependency declarations.
**What needs resolving**: The property table entry for S8 must include S3 among its dependencies, matching the formal contract and the proof's actual reliance on referential integrity for singleton run construction.

---

### S8 property table omits S8-vdepth dependency
**Foundation**: TS4 (ShiftStrictIncrease), T5 (ContiguousSubtrees), T10 (PartitionIndependence) — all from ASN-0034
**ASN**: S8 proof, Uniqueness across subspaces: *"By S8-vdepth, #v ≥ 2, so the common depth m (from S8-depth) satisfies m ≥ 2. The successor v + 1 therefore also extends [S₁]: OrdinalShift gives (v + 1)ᵢ = vᵢ for all i < m"*
**Issue**: The cross-subspace uniqueness argument invokes T5 with prefix `[S₁]`, requiring `[S₁] ≼ (v + 1)`. This holds only when `shift(v, 1)` preserves the first component — i.e., when the action point `m` satisfies `m ≥ 2`, so TumblerAdd copies position 1 from `v`. At `m = 1`, `shift([S], 1) = [S+1]` and `[S] ⋠ [S+1]`, breaking the T5 application entirely. The proof obtains `m ≥ 2` from S8-vdepth (via S8-depth), yet the property table omits S8-vdepth. The formal contract correctly includes it.
**What needs resolving**: The property table entry for S8 must include S8-vdepth, since without `m ≥ 2` the T5/T10 cross-subspace argument cannot be constructed — it is not merely a convenience but a load-bearing precondition for the prefix-containment step.

---

### S8 formal contract includes D-CTG, contradicting the proof's own analysis
**Foundation**: S8-depth (Fixed-depth V-positions) — *"Within a given subspace S of document d, all V-positions share the same tumbler depth"*
**ASN**: S8 proof, exhaustiveness aside: *"The key restriction is #v = #u: since u ∈ V_S(d) has depth m by S8-depth, D-CTG's constraint becomes #v = m, so only depth-m tumblers can be forced into V_S(d). The following case analysis on depth-m tumblers therefore covers all members of V_S(d)."*; S8 formal contract: *"Preconditions: … V-positions within each subspace form a contiguous ordinal range — D-CTG"*
**Issue**: The proof's own exhaustiveness analysis concludes that S8-depth alone guarantees the case analysis covers all members of `V_S(d)` — D-CTG's `#v = #u` restriction means it can only "force" depth-m tumblers into `V_S(d)`, which S8-depth already ensures. The singleton decomposition works for *any* finite set of V-positions with uniform depth per subspace, regardless of contiguity. The proof never invokes D-CTG's contiguity guarantee in any step. Yet the formal contract lists D-CTG as a precondition. This creates an internal contradiction within the S8 section: the prose establishes that D-CTG is not needed, then the formal contract asserts it is. The property table correctly omits D-CTG, but the formal contract's inclusion falsely suggests the decomposition theorem requires contiguous arrangements — obscuring the fact that S8 holds even for fragmented (D-CTG-violating) states.
**What needs resolving**: The formal contract's precondition list must be reconciled with the proof's analysis. If D-CTG is not used in any proof step, it should not appear as a precondition of S8.

## Result

Converged after 2 cycles.

*Elapsed: 2956s*
