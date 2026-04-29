# Regional Review — ASN-0034/TA-Pos (cycle 1)

*2026-04-24 02:47*

### Nonstandard slot label "Complementarity" in TA-Pos
**Class**: REVISE
**Foundation**: n/a (structural)
**ASN**: TA-Pos, formal contract. The claim emits a slot `*Complementarity:* (A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`. No other claim in this ASN uses this label; NAT-zero and NAT-order both emit derived facts under `*Consequence:*`.
**Issue**: `Pos(t) ⟺ ¬Zero(t)` is a derived fact — the body proves it from the two Definition clauses via bounded DeMorgan. Under the project's slot conventions established by the neighboring claims it belongs in a `*Consequence:*` slot. Introducing a one-off label `*Complementarity:*` breaks the slot vocabulary that downstream tooling and reviewers rely on to distinguish posited content (Axiom, Definition) from derived content (Consequence).
**What needs resolving**: Settle whether the slot vocabulary is open (and if so, state the admissible labels) or closed to {Axiom, Definition, Consequence, Depends}. Under the closed reading, relabel the bullet as `*Consequence:*` (or fold it into the Definition slot as a second-order definitional fact, but that would obscure that it requires a DeMorgan step).

### TA-Pos opening paragraph is use-site inventory and typing defense
**Class**: REVISE
**Foundation**: n/a (meta-prose)
**ASN**: TA-Pos, first paragraph following the predicate definitions. Two consecutive passages:
(a) "The bound variable `i` is typed to ℕ because the projection `tᵢ` is defined by T0 only on the index domain `{1, …, #t} ⊆ ℕ` and the bounding relation `≤` is ℕ-typed; the explicit `i ∈ ℕ` keeps parity with the `(A n ∈ ℕ :: …)` form used by the sibling NAT axioms."
(b) "`tᵢ` itself is a natural number by T0's carrier, the literal `0` against which it is compared is the `0 ∈ ℕ` posited by NAT-zero, the numeral `1` bounding the quantifier range is the `1 ∈ ℕ` posited by NAT-closure, and the relation `≤` bounding that range is the non-strict companion of `<` defined on ℕ by NAT-order..."
**Issue**: Passage (a) is a defensive justification of a typing choice ("i is typed to ℕ because…"); passage (b) is a use-site inventory that names which dependency supplied every symbol. Neither establishes Pos or Zero — these are the reviser-drift patterns the review discipline names explicitly (defensive justifications, use-site inventories). The Depends list already records the dependencies; replaying them in prose degrades the argument and signals ongoing accretion.
**What needs resolving**: Either delete these two passages, or reduce them to a single sentence that states what the predicates mean (e.g., "Pos asserts at least one nonzero component; Zero asserts all components are zero"). The Depends slot carries the dependency trace.

### Meta-prose about structural slot choices
**Class**: REVISE
**Foundation**: n/a (meta-prose)
**ASN**: Three instances, each a body sentence that talks about the form of the contract rather than its content:
- NAT-zero: "The minimum predicate `(A n ∈ ℕ :: ¬(n < 0))` is therefore exported as a Consequence: of the formal contract, lifted from the axiom's disjunction by NAT-order's irreflexivity and transitivity (both branches collapse to `0 < 0`); NAT-order is declared in the Depends slot accordingly."
- NAT-order: "The axiom slot introduces `<` before constraining it… The Definition slot introduces the non-strict companion `≤` from `<` and logical equality, and the reverse companions `≥` and `>` as the converses of `≤` and `<` respectively."
- NAT-closure: "The axiom slot introduces `+` before constraining it: its first clause `+ : ℕ × ℕ → ℕ` posits the signature — fixing arity (binary) and codomain (ℕ)."
**Issue**: Each sentence explains where the reviser put things and why the slot is shaped the way it is, instead of what the axiom says. These are "essay content in structural slots" / "new prose around an axiom [that] explains why the axiom is needed rather than what it says" — patterns the discipline flags as compounding across cycles. The proof content in each claim is sound, but a reader must skip past the scaffolding sentences to reach it.
**What needs resolving**: Remove the sentences about "axiom slot introduces X before constraining it" and "exported as a Consequence… Depends slot accordingly." If the structural choice needs defense, that defense belongs outside the claim body (commit message, design note), not inside the axiom exposition.

VERDICT: REVISE
