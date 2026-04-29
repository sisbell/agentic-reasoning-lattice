# Cone Review — ASN-0034/TA-Pos (cycle 1)

*2026-04-25 16:58*

Reviewing this foundation ASN for internal consistency. Working through each section's grounding and the connections between them.

### ℕ is used as a set throughout but never declared
**Class**: REVISE
**Foundation**: (none — internal review)
**ASN**: All four NAT-* claims, plus T0 and TA-Pos. Examples: NAT-order's axiom `< ⊆ ℕ × ℕ`; NAT-closure's `+ : ℕ × ℕ → ℕ` and `1 ∈ ℕ`; NAT-zero's `0 ∈ ℕ` and `(A n ∈ ℕ :: 0 < n ∨ 0 = n)`; T0's `aᵢ ∈ ℕ` and the index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}`.
**Issue**: The symbol `ℕ` carries the entire weight of the foundation — every Cartesian product `ℕ × ℕ`, every membership `x ∈ ℕ`, every set-builder `{j ∈ ℕ : ...}` presupposes `ℕ` is a set. Yet no axiom in any of the four NAT-* claims (or T0) establishes `ℕ` as a carrier. T0 by contrast does state "T is the set of nonempty finite sequences over ℕ" before axiomatizing `T`. The four NAT-* claims jump straight to operations and constants on a never-introduced ℕ. A reader walking the dependency DAG bottom-up encounters `< ⊆ ℕ × ℕ` (NAT-order, no deps) without `ℕ` ever having been declared.
**What needs resolving**: Either (a) add a primitive declaration that `ℕ` is a set (the carrier on which the NAT-* claims operate), placed at or before NAT-order, or (b) state explicitly somewhere in the ASN's preamble that `ℕ` is taken as a meta-level primitive denoting the natural numbers, and reference that commitment from each NAT-* claim that uses it.

### NAT-closure bundles constant-introduction with addition primitives
**Class**: OBSERVE
**Foundation**: (none — internal review)
**ASN**: NAT-closure (NatArithmeticClosureAndIdentity). Its Axiom block conjoins five clauses: `+ : ℕ × ℕ → ℕ`, `1 ∈ ℕ`, `0 < 1`, `(A n ∈ ℕ :: 0 + n = n)`, `(A n ∈ ℕ :: n + 0 = n)`.
**Issue**: The clauses `1 ∈ ℕ` and `0 < 1` introduce a named constant and locate it in the strict order — they have nothing to do with closure or additive identity. Their bundling means T0, which only needs `1 ∈ ℕ` for its nonemptiness bound `1 ≤ #a`, transitively imports addition and the additive-identity laws even though it consumes neither. TA-Pos has the same exposure: it cites NAT-closure solely for `1`. The name "ArithmeticClosureAndIdentity" undersells the included `1 ∈ ℕ`/`0 < 1` clauses, which a reader chasing the dependency for `1` would not look for under that title.

### TA-Pos prose "the universal is not vacuous" mislabels what nonemptiness rules out
**Class**: OBSERVE
**Foundation**: (none — internal review)
**ASN**: TA-Pos prose: "Pos(t) demands a nonzero component (the existential is not vacuous) and Zero(t) forces every component to equal `0` (the universal is not vacuous)."
**Issue**: A bounded universal `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` over an empty index range is vacuously *true*, not vacuously empty. The prose seems to use "not vacuous" in two different senses across the two halves of the sentence — for the existential, it correctly means "the witness must really exist"; for the universal, it informally means "the constraint really constrains every component," but a reader expecting symmetric meaning may parse it as the existential's sense applied to `Zero`, which would mislead. The point being made is sound; the phrasing conflates two distinct readings of vacuity.

VERDICT: REVISE
