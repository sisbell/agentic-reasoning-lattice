**T4c (LevelDetermination).** Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`. On the T4-valid subset of `T` (tumblers satisfying `zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`), T4c defines four hierarchical level labels by zero count: `t` is a *node address* iff `zeros(t) = 0`, a *user address* iff `zeros(t) = 1`, a *document address* iff `zeros(t) = 2`, and an *element address* iff `zeros(t) = 3`.

The four biconditionals are the definition of the labels. The proof obligation reduces to: the four zero-count values exhaust the T4-valid subdomain, distinct values receive distinct labels, and each label is realised.

*Exhaustion.* By T4, every T4-valid tumbler satisfies `zeros(t) ≤ 3`. By NAT-zero, `0 ≤ zeros(t)`. Hence `zeros(t) ∈ {0, 1, 2, 3}`.

*Injectivity.* The values `0, 1, 2, 3` are pairwise distinct by NAT-order trichotomy, and `zeros(t)` is single-valued. Therefore distinct zero counts induce distinct labels.

*Surjectivity.* Each zero count is realised by a T4-valid witness:

  - `(1)`: `zeros = 0` — *node address*.
  - `(1, 0, 1)`: `zeros = 1` — *user address*.
  - `(1, 0, 1, 0, 1)`: `zeros = 2` — *document address*.
  - `(1, 0, 1, 0, 1, 0, 1)`: `zeros = 3` — *element address*.

Each witness is checked against T4's field-segment clauses directly. ∎

*Formal Contract:*
- *Preconditions:* `t` satisfies the T4 constraints (`zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`).
- *Depends:*
  - T0 (CarrierSetDefinition) — fixes ℕ as the codomain of `zeros(t)` and the component domain of the witnesses.
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ zeros(t)` for the exhaustion step.
  - NAT-order (NatStrictTotalOrder) — supplies pairwise distinctness of `0, 1, 2, 3` for injectivity.
  - T4 (HierarchicalParsing) — supplies the T4-valid subdomain constraints, used in exhaustion and in validating the surjectivity witnesses.
- *Postconditions:* `(A t ∈ T : t is T4-valid :: (zeros(t) = 0 ↔ t is a node address) ∧ (zeros(t) = 1 ↔ t is a user address) ∧ (zeros(t) = 2 ↔ t is a document address) ∧ (zeros(t) = 3 ↔ t is an element address))`. The induced map `zeros(t) → hierarchical level` is a bijection `{0, 1, 2, 3} → {node, user, document, element}` on the T4-valid subdomain. Outside this subdomain, T4c assigns no level; consumers must discharge T4-validity before reading a level off `zeros(t)`.
