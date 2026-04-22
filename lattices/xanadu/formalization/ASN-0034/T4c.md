**T4c (LevelDetermination).** Let `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` as in T4, with `|·|` the cardinality of a finite subset of ℕ (codomain ℕ, distinct from T0's tumbler-length `#·`); the indexed set is a subset of `{1, …, #t} ⊆ ℕ` by T0, so `zeros(t) ∈ ℕ`. On the T4-valid subset of `T` (tumblers satisfying `zeros(t) ≤ 3`, no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`), T4c defines four hierarchical level labels by zero count: `t` is a *node address* iff `zeros(t) = 0`, a *user address* iff `zeros(t) = 1`, a *document address* iff `zeros(t) = 2`, and an *element address* iff `zeros(t) = 3`.

The four biconditionals are the definition of the labels. The proof obligation reduces to: the four zero-count values exhaust the T4-valid subdomain, distinct values receive distinct labels, and each label is realised.

*Exhaustion.* By T4, every T4-valid tumbler satisfies `zeros(t) ≤ 3`, and by NAT-zero, `0 ≤ zeros(t)`. These bounds alone do not fix `zeros(t) ∈ {0, 1, 2, 3}` — without discreteness the segment could harbor intermediate values. NAT-discrete supplies the missing step: applied at `m ∈ {0, 1, 2}`, each instance promotes `m < zeros(t)` to `m + 1 ≤ zeros(t)`, so from `0 < zeros(t)` obtain `1 ≤ zeros(t)`, from `1 < zeros(t)` obtain `2 ≤ zeros(t)`, and from `2 < zeros(t)` obtain `3 ≤ zeros(t)`; the upper bound `zeros(t) ≤ 3` blocks any further promotion. Hence `zeros(t) ∈ {0, 1, 2, 3}`.

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
  - NAT-discrete (NatDiscreteness) — supplies the absence of values strictly between consecutive integers, promoting each strict inequality `m < zeros(t)` (for `m ∈ {0, 1, 2}`) to `m + 1 ≤ zeros(t)` so that the segment `0 ≤ zeros(t) ≤ 3` collapses to `{0, 1, 2, 3}`.
  - NAT-order (NatStrictTotalOrder) — supplies pairwise distinctness of `0, 1, 2, 3` for injectivity.
  - T4 (HierarchicalParsing) — supplies the T4-valid subdomain constraints, used in exhaustion and in validating the surjectivity witnesses.
- *Postconditions:* `(A t ∈ T : t is T4-valid :: (zeros(t) = 0 ↔ t is a node address) ∧ (zeros(t) = 1 ↔ t is a user address) ∧ (zeros(t) = 2 ↔ t is a document address) ∧ (zeros(t) = 3 ↔ t is an element address))`. The four labels are pairwise distinct, and each is realised by some T4-valid tumbler. Outside this subdomain, T4c assigns no level; consumers must discharge T4-validity before reading a level off `zeros(t)`.
