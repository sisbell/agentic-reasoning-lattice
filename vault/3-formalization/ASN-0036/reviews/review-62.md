# Cross-cutting Review — ASN-0036 (cycle 3)

*2026-04-13 00:03*

Looking at the ASN and foundation statements carefully, checking cross-property consistency, precondition chains, and definition coherence.

### S8 correspondence run definition requires S3 but S8 omits it from dependencies

**Foundation**: S3 (Referential integrity) — `(A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))`
**ASN**: S8-depth section defines a correspondence run as "a triple `(v, a, n)` with `v ∈ dom(Σ.M(d))`, `a ∈ dom(Σ.C)`, and `n ≥ 1`." S8's postcondition: "the arrangement … can be decomposed into a finite set of correspondence runs {(vⱼ, aⱼ, nⱼ)}." S8's table entry: "theorem from S8-fin, S2, S8a, S8-depth, T1, T3, T5, T10, TS4, OrdinalShift (ASN-0034)." S8's formal contract preconditions list S8-fin, S2, S8a, S8-depth — no S3.
**Issue**: The correspondence run definition requires `a ∈ dom(Σ.C)`. S8's proof constructs singleton runs `(v, M(d)(v), 1)` and claims they are correspondence runs. For `M(d)(v) ∈ dom(Σ.C)` to hold — making the singleton a valid correspondence run per the definition — S3 is required. Without S3, the constructed triples satisfy postconditions (a) and (b) as pure equalities but do not meet the correspondence run definition's domain condition on `a`. The dependency chain S8 → correspondence run definition → `a ∈ dom(Σ.C)` → S3 is unbroken in the mathematics but undeclared in both the table entry and formal contract.
**What needs resolving**: S8's dependency list (table entry and formal contract) must include S3, or the correspondence run definition must be restructured so that the `a ∈ dom(Σ.C)` condition is a separately-stated consequence of S3 rather than a definitional requirement.

---

### S8-depth formal contract attributes correspondence-run prerequisites to the axiom

**Foundation**: S8-vdepth (MinimalVPositionDepth) — `#v ≥ 2` for all V-positions; S7c (Element-field depth) — `#fields(a).element ≥ 2` for all content addresses
**ASN**: S8-depth formal contract structure: "*Preconditions:* S8-vdepth — every `v ∈ dom(Σ.M(d))` satisfies `#v ≥ 2` … S7c — every `a ∈ dom(Σ.C)` satisfies `#fields(a).element ≥ 2` … *Axiom:* `(A d, v₁, v₂ : … : #v₁ = #v₂)` *Definition:* A *correspondence run* …"
**Issue**: The S8-depth axiom (fixed depth within a subspace) is a standalone design requirement with no logical dependencies. S8-vdepth and S7c are needed for the correspondence run definition's shift semantics (subspace preservation under ordinal shift for V-positions and I-addresses respectively) and the I-address shift discussion co-located in the same section — not for the axiom. Placing these as "Preconditions" before the "Axiom" in the formal contract creates the reading that the axiom depends on S8-vdepth and S7c. Any property that declares S8-depth as a dependency (S8, D-CTG-depth, D-SEQ) would inherit spurious transitive dependencies on S8-vdepth and S7c through the formal contract, inflating import requirements for downstream ASNs that need only the depth-uniformity axiom.
**What needs resolving**: The S8-depth formal contract must separate the axiom's scope from the correspondence run definition's prerequisites — either by splitting into distinct formal contracts or by clearly scoping the preconditions to the definition rather than the axiom.

---

### S8 table entry lists T5 but proof applies it only at m ≥ 2 without declaring the m = 1 alternative

**Foundation**: T5 (ContiguousSubtrees, ASN-0034) — `p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c ⟹ p ≼ b`
**ASN**: S8's cross-subspace uniqueness proof splits into two cases: for `m ≥ 2`, it uses T5 to show all tumblers in `[v, v+1]` extend `[S₁]`; for `m = 1`, it gives a direct argument that every tumbler `t` in `[[S₁], [S₁+1])` satisfies `t₁ = S₁` without invoking T5. The direct m = 1 argument relies on T1(i) and T1(ii) case analysis on `t₁` relative to `S₁` and `S₁ + 1`.
**Issue**: S8's table entry lists T5 as a dependency, but the proof's m = 1 case — which is the case S8 must handle precisely because it does not declare S8-vdepth — uses an independent argument based on T1 case analysis, not T5. For T5 to apply at m = 1 with prefix `[S₁]`, the proof would need `[S₁] ≼ v` and `[S₁] ≼ (v+1)`. At m = 1, `v = [S₁]` and `v + 1 = [S₁+1]`; since `[S₁]₁ = S₁ ≠ S₁+1 = [S₁+1]₁`, `[S₁] ⋠ [S₁+1]` — T5's precondition fails. The proof correctly avoids T5 at m = 1, but this means the m = 1 path uses foundation properties (T1 cases (i) and (ii) applied to mixed-depth comparisons) that are not separately declared in the table. A verifier checking the table against the proof would find T5 used only in the m ≥ 2 branch and undeclared reliance on T1(ii) for the m = 1 prefix-ordering argument.
**What needs resolving**: Either S8 should declare S8-vdepth as a dependency (eliminating the m = 1 case and simplifying the proof), or the table entry should note that T5 applies only at m ≥ 2 and that the m = 1 argument relies on T1's prefix case (ii) for mixed-depth cross-subspace exclusion.
