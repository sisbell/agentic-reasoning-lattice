# Review of ASN-0129

## Verification performed

Before the verdicts, the load-bearing checks, since a CONVERGED verdict needs to show its work:

**The worked trace, recomputed end-to-end.** I re-derived all five states: gate verdicts (Sh-conf Binary at Σ₁/Σ₂, Unary at Σ₄), frontier addresses `a₁`–`a₄` against FrontierUnification, C2/C3 at each deposit (C3 at Σ₄ checked both ways — via DR's surface-discipline argument and concretely via R0a: `a₄ = inc³(a₁,0)` is same-length as `a₂`, hence outside `subtree(a₂)`), single-tuple scope at Σ₃, and every predicate value. The active-view sequence ⊤,⊥,⊤,⊥,⊥, the default-view sequence ⊤,⊥,⊤,⊥,⊤, and `ever_res`'s ⊥,⊥,⊤,⊤,⊤ all check out. The Σ₄ default-view computation correctly applies BH1's rewrite formula (J = retired ≠ cmt) and correctly leaves `is_cmt(c₁)` unrewritten. Even the unstated corner (if `t` were an extension of `c₁`, making `t` filtered) does not change any stated verdict, since the default-view filter's base is already empty at Σ₄.

**PD0, rule by rule against the step effects.** Grow-only is correct for `L_K` (R3 via B2/RP-b), `L_dom` (step effects), audit `M_K` (union over growing index of immutable values, L12), filters with ST bodies (membership persists: base growth plus the induction hypothesis), and step-constant domains. The polarity discipline is right where it is easiest to get wrong: `count(D) ≤ c` correctly placed in SF only, `count(D) = c` correctly in neither class, T1-extrema correctly excluded (the ⊥-at-empty verdict and extremum movement do make their polarity conditional). The deliberate omissions are also correct: ∀ over a grow-only domain with ST body is *not* claimed ST, ∃ with SF body is *not* claimed SF. The absence of a PC2-composition rule is acknowledged incompleteness (the classes are explicitly spelling-level; OQ5), and the step-constant quantifier clauses cover the bound-argument idiom the worked ST example uses.

**PD2's active-view clause against the born-nullified corner.** A deposit of type J ∉ 𝒦, J ≁ R, can land born-nullified inside an existing retraction's coverage, which *does* change `nullified(Σ)` — but the fresh address carries type J, is not in any `L_K` for K ∈ 𝒦, so `A_K` is unchanged. The clause survives the corner; the three named exceptions (retraction, BH4 home-chain traffic, `targets_keyed`'s cross-type footprint) are exactly the right three.

**V-IDX's vacuity argument.** Checked against R-C1 and S1–S3: `[K_R]` is mandatory with behaviors = ∅, so no behavior family is universally attached at any constructible registry; the shape and idem clauses independently block BH2/BH3 (retired is Unary) and BH4 (all three designates are idem = ⊤). The conclusion — no `Reg`-quantified body applying a class-indexed behavior atom is ever a PL term — is sound, and the `targets_keyed`/`·[K]` escape routes are correctly typed.

**PC6's converse at its one non-trivial leaf.** The QD-filter spelling of `Observe_K(Σ, F̂, Ĝ, view)` matches ASN-0086's definition exactly (`F̂ ⊆ coverage(F)` unfolds to the finite conjunction of per-element coverage tests on the F slot). The reverse-lookup reconstruction `⋃({x ∈ A_K : target ∈ coverage_G(x)}, addrs_F)` is term-for-term BH3's `sources_to`. The registry-lookup discharge by constant-folding under R1 is sound. The relativization is honestly priced (the costs paragraph), and the three conjectures are correctly held at conjecture status with the FO-citation route correctly rejected as unsound for this language (the walk atoms, counting, and built-in orders each genuinely break it).

**Citation hygiene.** All cross-references are to foundation ASNs; the transfer chains (L12/L12a/R3 across B2 with RP-b; P6 via RP-a; FrontierUnification via RP-a; RangeSterilization via RP-b) each use the correct transfer lemma for the claim's quantification shape. `M_K` and `L_dom` are fenced object-language aliases required by the domain grammar, not reinvented notation.

**Anti-bloat scan, per the classifier.** The deferrals present (QD-audit → C-emit; QD-audit/PC4/PC6 → Structural reads only) are single-clause pointers whose content exists exactly once at the target; the `Reg` restriction's four appearances are application sites with back-citations, not restatements; no ordering-justification prose, no orphaned relocated findings, no case analysis of precondition-excluded cases (V-IDX's vacuity is a derived exclusion doing load-bearing work, not an imagined case). COD's "every entry is realized" sentence is the closest thing to a use-site inventory, but it doubles as the intro/elim accounting for `Seq_fin(T)` and `Map_fin`, which the typing judgment needs; I do not flag it.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Discharging the three inexpressibility conjectures
**Why out of scope**: C-reach, the parity candidate, and C-emit each require an invariance argument over branchy, cardinality-balanced state families in a counting-plus-order regime — including the age-bearing obligation both PC6 and C-emit correctly identify. The note records the obligation (Open Question 6) and correctly refuses the unsound citation shortcut; the proofs are a future ASN's work, not a defect here.

### Topic 2: Mechanical certification of the dynamics classes
**Why out of scope**: PD0 is sound but deliberately spelling-level and incomplete — e.g., it has no PC2-composition rule, so some extensionally monotone spellings receive no certificate. A completeness-or-decidability result for class membership (Open Question 5) is new theory, not an error in the classification shipped.

### Topic 3: Joint dynamics with the editing vocabulary
**Why out of scope**: PD0–PD2 are proven relative to `→_sh`. If a composed system ever evaluates PL over a transition system that also includes ASN-0127's editing steps (K.δ, K.μ⁻, K.μ~), the stability theory needs re-derivation against that vocabulary — straightforward in prospect, since no PL footprint reaches arrangement bindings or content, but it is a new transition system and belongs to the ASN that composes the layers.

VERDICT: CONVERGED
