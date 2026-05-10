# Regional Review — ASN-0034/T4 (cycle 1)

*2026-04-23 17:22*

### `zeros(·)` and "T4-valid" used in T4 contract without exposed definitions
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4's Formal Contract opens *Axiom:* with "Valid address tumblers satisfy: `zeros(t) ≤ 3`; …" and the *Consequence:* states "`zeros(t) ∈ {0, 1, 2, 3}` for every T4-valid tumbler `t`". Both `zeros(·)` and the "T4-valid" predicate are central to the contract, but neither has a *Definition:* slot. `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` lives only in the prose preamble, and "T4-valid" is implicitly defined as "satisfies the four axiom clauses" without a named predicate. A consumer reading only the Formal Contract cannot interpret `zeros(t)` or determine what `T4-valid` denotes — they must consult the surrounding narrative. Sibling claims (AllocatedSet's missing "Activated" / "Frontier" definitions) drew the same kind of finding in cycle 1.

### Symbol `k` overloaded in T4's per-`k` Axiom schema
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4's *Axiom:* writes "for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, the form is — `k = 0`: …; `k = 3`: `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`. In every case, `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present." The variable `k` serves both as the zero-count selector binding the case enumeration and as a position-index into the document field `Dₖ` in the strict-positivity clause. Disambiguation is straightforward from context, but a precise reader has to re-interpret `k` mid-sentence.

### NAT-card *Axiom:* slot interleaves clauses with derivation-defense prose
**Class**: OBSERVE
**Foundation**: NAT-card (NatFiniteSetCardinality)
**ASN**: NAT-card's *Axiom:* bullet contains three clauses (conditional codomain, enumeration characterisation, upper bound) interleaved with multi-line parenthetical justifications: "— both existence of the enumeration for every such `S` and the selection of a single `k` per `S` are clauses of the postulate, since the declared foundations supply no induction principle …", and "(upper bound — posited as an independent clause of the axiom since deriving it from the enumeration characterisation would require an induction on `i` establishing `s_i ≥ i` across all indices `1 ≤ i ≤ k` plus a discrete-successor step on ℕ, neither supplied …)". This is meta-prose explaining *why* each clause is posited rather than derived — content that belongs in the surrounding narrative (where it also already appears, almost verbatim). A reader scanning *Axiom:* for the actual clauses must filter past defensive justification embedded inside the bullet.

### T4 Exhaustion's `m = 0` step ignores NAT-zero's exported Consequence
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing); NAT-zero exports `(A n ∈ ℕ :: ¬(n < 0))` as a *Consequence:*
**ASN**: T4's Exhaustion derivation says "At `m = 0`: the case `zeros(t) < 0` is excluded by `0 ≤ zeros(t)` via the exactly-one route just described". The "exactly-one route" — unfolding `0 ≤ zeros(t)` to `0 < zeros(t) ∨ 0 = zeros(t)` and invoking trichotomy's exactly-one clause to forbid `zeros(t) < 0` — is genuinely needed at `m ∈ {1, 2, 3}` (where no analogous direct Consequence is available), but at `m = 0` NAT-zero already exports `¬(n < 0)` as a Consequence that excludes `zeros(t) < 0` in one step. The chosen "uniformity" of route adds derivation steps where a one-line citation of an upstream Consequence would do. Not incorrect — the longer route arrives at the same conclusion — only redundant.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 223s*
