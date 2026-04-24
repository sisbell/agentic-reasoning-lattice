# Regional Review — ASN-0034/T4 (cycle 1)

*2026-04-24 12:02*

### NAT-card depends on T0 only for a disambiguation aside
**Class**: REVISE
**Foundation**: NAT-card (NatFiniteSetCardinality)
**ASN**: NAT-card. The Axiom ends "`|·|` acts on subsets of ℕ and is distinct from T0's tumbler-length `#·`, which acts on sequences." The Depends list then includes "T0 (CarrierSetDefinition) — supplies the tumbler-length operator `#· : T → ℕ` referenced in the disambiguation remark distinguishing `|·|` from `#·`."
**Issue**: The substantive axioms of NAT-card (strictly-increasing-function characterisation, upper bound) are pure statements about subsets of ℕ and do not reference T, `#·`, or anything from T0. T0 is named only to sustain a cautionary note that `|·|` is a different symbol from `#·`. This couples a ℕ-only claim to the tumbler carrier for cosmetic reasons, and matches the reviser-drift pattern "new prose around an axiom explains … rather than what it says." Downstream, T4 acquires a diamond in the DAG (T4 → NAT-card → T0 and T4 → T0) that carries no mathematical content.
**What needs resolving**: Either remove the `#·`-disambiguation from the Axiom (and the corresponding T0 entry from Depends) so NAT-card's contract contains only what it asserts about ℕ-subsets, or move the disambiguation to a non-contractual prose slot that does not induce a dependency edge.

### ℕ⁺ notation introduced in T4 prose but unused
**Class**: OBSERVE
**ASN**: T4. Prose: "write `ℕ⁺ = {n ∈ ℕ : 0 < n}` for the strictly positive naturals".
**Issue**: The symbol `ℕ⁺` is introduced in the body but is not referenced anywhere else in T4's prose, Definition, Axiom, Consequence, Preconditions, or Depends list. The positivity facts `0 < Nᵢ`, `0 < Uⱼ`, `0 < Dₖ`, `0 < Eₗ` are stated directly with `<`, not as membership `∈ ℕ⁺`. Either the notation is intended for downstream use (T4a/T4b/T4c), in which case it should be introduced there at first use, or it is residue from an earlier draft.

### Canonical-form schema in T4 Axiom is derivable, not independent
**Class**: OBSERVE
**ASN**: T4 Axiom: the per-`k` schema `k = 0`: `t = N₁. … .Nₐ`; …; `k = 3`: `t = N₁. … .Nₐ . 0 . U₁. … .Uᵦ . 0 . D₁. … .Dᵧ . 0 . E₁. … .Eδ`, with positivity at every position present.
**Issue**: Given `zeros(t) = k`, the field-segment constraint (no adjacent zeros; `t₁ ≠ 0`; `t_{#t} ≠ 0`) together with NAT-zero's dichotomy on each non-separator component already determines the written form with nonempty fields. The schema clauses add no constraint beyond what the field-segment constraint + `zeros(t) = k` already entail; they are display-form restatements. Presenting them as part of the Axiom (alongside the independent field-segment constraint) blurs which clauses are primitive and which are consequences.

### Forward-reference paragraph for T4a/T4b/T4c
**Class**: OBSERVE
**ASN**: T4, paragraph beginning "Three downstream claims — T4a (SyntacticEquivalence), T4b (UniqueParse), and T4c (LevelDetermination) — build on T4 with additional foundations."
**Issue**: This paragraph is scaffolding: it describes what downstream claims will do without adding anything T4 itself asserts. It is also a sibling to the earlier prose about T4c being "the single definitional site" for the four address labels. Scaffolding of this kind is not harmful but is the kind of meta-prose a precise reader reads past; if the downstream claims appear in the same document when assembled, the forward references can be trimmed.

VERDICT: REVISE
