# Cross-cutting Review — ASN-0036 (cycle 2)

*2026-04-12 23:34*

### S8 table entry cites TA5 but proof uses TS4 and OrdinalShift

**Foundation**: TA5 (HierarchicalIncrement, ASN-0034) — defines `inc(t, k)`; TS4 (ShiftStrictIncrease, ASN-0034) — `shift(v, n) > v`; OrdinalShift (ShiftDefinition, ASN-0034) — `shift(v, n) = v ⊕ δ(n, m)`
**ASN**: S8 table entry: "theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TA5 (ASN-0034)". S8 proof: "v + 1 = shift(v, 1) > v by TS4" and "By OrdinalShift, v + 1 = shift(v, 1) = v ⊕ δ(1, m) satisfies #(v + 1) = m and differs from v only at position m."
**Issue**: The S8 partition proof does not use TA5 (HierarchicalIncrement) anywhere. TA5 defines `inc(t, k)`, which is an allocation operation; S8's proof is about partitioning existing V-positions into runs and uses only the shift operation. The actual ASN-0034 properties invoked are TS4 (to establish `v + 1 > v`, the strict increase needed for singleton interval non-emptiness) and OrdinalShift (to establish that `v + 1` has the same depth as `v` and differs only at the last component). TA5 appears in S8-depth's *motivational* discussion of why non-trivial runs arise in practice ("TA5(c) guarantees the successor has the same depth"), but this discussion is not part of any formal derivation. The dependency graph connecting S8 to the foundation through TA5 is spurious, while the actual connections through TS4 and OrdinalShift are undeclared.
**What needs resolving**: S8's table entry must replace TA5 with the foundation properties actually used in the proof: TS4 (ShiftStrictIncrease) and OrdinalShift (ShiftDefinition), along with OrdinalDisplacement if transitive dependencies are tracked.

---

### S7a table entry omits S7b dependency required for well-formedness

**Foundation**: T4 (HierarchicalParsing, ASN-0034) — field decomposition defined for address tumblers; `fields(a).document` exists only when `zeros(a) ≥ 2`
**ASN**: S7a table entry: "design; uses Prefix, T4, T4c (ASN-0034)". S7a formal contract: "Preconditions: `a ∈ dom(Σ.C)`, `zeros(a) = 3` (S7b: every content address sits at the element level, ensuring all four fields of `fields(a)` are well-defined)." S7a axiom statement references `(fields(a).node).0.(fields(a).user).0.(fields(a).document)`.
**Issue**: S7a's axiom references `fields(a).document`, which T4's field correspondence defines only when `zeros(a) ≥ 2`. Without S7b — which constrains `zeros(a) = 3` for every `a ∈ dom(Σ.C)` — the expression `fields(a).document` is potentially undefined: if some `a ∈ dom(Σ.C)` had `zeros(a) = 0` (node-level), the document field would not exist and S7a's axiom would reference an undefined quantity. The formal contract correctly identifies S7b as a precondition, but the table lists only ASN-0034 dependencies (Prefix, T4, T4c) and omits S7b entirely. A downstream ASN importing S7a by reading the table would not know it must also import S7b for the axiom to be well-formed.
**What needs resolving**: S7a's table entry must list S7b among its dependencies, since S7b provides the structural guarantee (`zeros(a) = 3`) that makes `fields(a).document` well-defined for all content addresses.

---

### S8a proof text uses "v > 0" to mean "every component positive," inconsistent with PositiveTumbler definition

**Foundation**: PositiveTumbler (ASN-0034) — "A tumbler `t ∈ T` is *positive*, written `t > 0`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`." This is an existential condition.
**ASN**: S8a proof: "The conjunct `v > 0` — every component of v is strictly positive — follows directly from T4's positive-component constraint." Then: "The conjunct `v₁ ≥ 1` is a specialisation of `v > 0` to the first component."
**Issue**: The foundation defines `t > 0` existentially (at least one nonzero component). The S8a proof glosses `v > 0` as "every component of v is strictly positive" — the universal condition. Under the foundation's definition, "specialising `v > 0` to the first component" is not valid: an existential guarantee that *some* component is nonzero cannot be specialised to a *specific* component. The actual derivation of `v₁ ≥ 1` proceeds through T4's positive-component constraint applied to position 1, not through the `v > 0` conjunct. The universal property ("every component positive") is correctly captured by the separate conjunct `zeros(v) = 0` — which, for natural-number components, is equivalent to `(A i : 1 ≤ i ≤ #v : vᵢ > 0)`. The term `v > 0` thus carries less information than the proof text attributes to it. No downstream property relies on the incorrect reading — all properties that need "all components positive" access it through `zeros(v) = 0` — but the two meanings of `v > 0` within the document (existential at the foundation, universal in S8a's proof) create a terminological inconsistency that a formal verification tool would reject.
**What needs resolving**: The S8a proof text must attribute "every component positive" to `zeros(v) = 0`, not to `v > 0`. The derivation of `v₁ ≥ 1` must cite T4's positive-component constraint directly rather than characterising it as a specialisation of the existential `v > 0`.
