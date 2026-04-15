# Cone Review — ASN-0036/S8 (cycle 3)

*2026-04-14 17:19*

### S8a: `v > 0` overloads `>` with a meaning not defined in the shared vocabulary

**Foundation**: T1 (defines `<` and derived `>` as a total lexicographic order on T)
**ASN**: S8a formal axiom: `"(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)"` with gloss `"The conjunct v > 0 — every component is strictly positive"`
**Issue**: Throughout the ASN and its foundations, `>` is T1's lexicographic total order on T. In S8a's axiom, `v > 0` is glossed as componentwise positivity — a different relation that is never formally defined. Under T1's interpretation, `v > 0` would mean `v > [0]`, which reduces to `v₁ ≥ 1` (the second conjunct, already stated). Under the intended componentwise interpretation, `v > 0` means every component is ≥ 1, which is equivalent to `zeros(v) = 0` (the first conjunct, already stated). Either reading makes the third conjunct redundant with one of the other two, and S8's own formal preconditions silently acknowledge this by citing S8a as `"zeros(v) = 0 ∧ v₁ ≥ 1"` — dropping `v > 0` entirely. A formalizer encounters an axiom containing a symbol (`>` applied componentwise to a scalar) that has no definition in the specification's vocabulary, whose intended meaning duplicates a conjunct already present.
**What needs resolving**: Either define the componentwise order used by `v > 0` as a distinct relation from T1's `>`, or replace `v > 0` with the already-present equivalent (`zeros(v) = 0`). If the three conjuncts are intentionally stated for emphasis (as the text suggests for `v₁ ≥ 1`), the axiom should note which conjuncts are consequences of which, so a formalizer knows the independent content.

---

### S8-vdepth: derivation path claimed but neither shown nor obviously valid

**Foundation**: T0 (components ∈ ℕ), OrdinalShift (prefix preservation requires `i < #v`)
**ASN**: S8-depth preconditions: `"S8-vdepth establishes this bound as a theorem (from S8a, S3, S7c) for every V-position in dom(M(d))"`. S8 preconditions: `"#v ≥ 2 for all V-positions (S8-vdepth, a theorem from S8a, S3, S7c)"`
**Issue**: Both S8 and S8-depth cite S8-vdepth (`#v ≥ 2`) as load-bearing — without it, S8-depth's postcondition 1 (subspace preservation) is false at `#v = 1`, and S8's `m = 1` case analysis changes from vacuous to live. Both describe S8-vdepth as a *theorem* derivable from S8a, S3, and S7c. But the derivation is never given, and the claimed path is non-obvious: S8a constrains V-position component values (`zeros(v) = 0`, `v₁ ≥ 1`); S3 constrains M(d)'s range (referential integrity to `dom(Σ.C)`); S7c constrains I-address element-field depth (`δ ≥ 2`). None of these directly constrain V-position *length*. The step from "the I-address mapped to by v has element-field depth ≥ 2" to "v itself has ≥ 2 components" requires an additional connection — either a model constraint relating V-position depth to I-address structure, or a separate argument — that is absent from the ASN.
**What needs resolving**: Either provide the explicit derivation from S8a + S3 + S7c (showing which step connects I-address structure to V-position depth), or reclassify S8-vdepth as an axiom with its own formal statement. The current status — a theorem whose proof is claimed but never shown, over a derivation path that doesn't obviously close — leaves a gap that both S8 and S8-depth build on.
