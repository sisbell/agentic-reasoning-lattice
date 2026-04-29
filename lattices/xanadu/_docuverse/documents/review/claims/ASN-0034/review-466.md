# Regional Review — ASN-0034/NAT-card (cycle 1)

*2026-04-24 01:28*

### Nondistinctness of `0` and `1` is consistent with the axioms
**Class**: REVISE
**Foundation**: NAT-closure (`1 ∈ ℕ`), NAT-zero (`0 ∈ ℕ`, `0 < n ∨ 0 = n`), NAT-order
**ASN**: T0's nonemptiness clause "`(A a ∈ T :: 1 ≤ #a)`: every tumbler has at least one component"; NAT-card's initial segment `{1, 2, …, n}`.
**Issue**: Nothing in the declared axioms forces `0 ≠ 1`. The trivial model ℕ = {0}, `+` trivial, `<` empty, with the numeral `1` interpreted as `0`, satisfies every NAT-* clause: irreflexivity/transitivity/trichotomy hold vacuously or at `0 = 0`; `+ : ℕ×ℕ → ℕ` and `1 ∈ ℕ` hold; both additive-identity clauses hold at `n = 0`; `0 ∈ ℕ` and `0 < n ∨ 0 = n` hold at `n = 0`. In that model, `1 ≤ #a` in T0 degenerates to `0 ≤ #a`, which is trivially true and no longer forces the prose's "at least one component" reading — T could admit `#a = 0`. NAT-card's `{1, 2, …, n}` is likewise destabilised at `n = 0`, since the distinction between empty and non-empty initial segments relies on `0 < 1`.
**What needs resolving**: Either add a clause that distinguishes `1` from `0` (e.g., `0 < 1`, or `1 ≠ 0`, at NAT-closure or NAT-order) so T0's nonemptiness bite and NAT-card's initial-segment anatomy are secured; or re-express T0's nonemptiness using a primitive that does not depend on `0 ≠ 1` and adjust NAT-card accordingly.

### Free variable `S` in NAT-card's codomain quantifier
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-card Axiom first clause: "`(A n ∈ ℕ : S ⊆ {1, 2, …, n} :: |S| ∈ ℕ)` (conditional codomain)".
**Issue**: The Dijkstra quantifier binds `n` only; `S` appears free in both the range `S ⊆ {1, 2, …, n}` and the body `|S| ∈ ℕ`. The intended reading is "for every `n ∈ ℕ` and every `S ⊆ {1, …, n}`, `|S| ∈ ℕ`", which requires binding `S` as well. As written, the clause is malformed (or silently depends on an outer binder the contract does not state). The same shape recurs in the upper-bound clause `(A n ∈ ℕ : S ⊆ {1, 2, …, n} :: |S| ≤ n)`.
**What needs resolving**: Bind `S` in both clauses, e.g. `(A n ∈ ℕ, S : S ⊆ {1, …, n} :: |S| ∈ ℕ)` / `… :: |S| ≤ n`, or otherwise make the quantification over `S` explicit.

### NAT-card axiom prose is dominated by meta-justification
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-card body and Axiom / Depends slots — the long passages beginning "Existence of such an enumeration for every `S`, the postulate's selection of a single `k` per `S`, and the upper bound `|S| ≤ n` are all clauses of the axiom, not derivations…", continuing through "Uniqueness of `k` is therefore posited rather than derived…", "The upper bound `|S| ≤ n` is similarly posited rather than derived…", and the matching paragraph in the NAT-order Depends bullet ("Neither trichotomy nor any other NAT-order property is appealed to in deriving uniqueness of `k` or the upper bound `|S| ≤ n`…").
**Issue**: These paragraphs explain *why* clauses are posited rather than derived, referencing sketches of inductive proofs that are not in scope (`s_i ≥ i` by stepping, minimum-extraction on `S \ {s_1, …, s_{i-1}}`). This is the reviser-drift pattern the instructions flag: prose around an axiom explaining why the axiom is needed rather than what it says. The actual axiom content — enumeration existence, `k`-uniqueness, upper bound — is stated once and then re-litigated across multiple paragraphs with hypothetical derivations that are explicitly not performed. A downstream reader has to skip past the meta-argument to recover the posit.
**What needs resolving**: Reduce NAT-card to what the postulate *asserts*. A single short note that uniqueness and the upper bound are axiom clauses (not consequences) suffices; the sketches of would-be inductive proofs and the enumeration-of-what-the-foundations-lack catalogue can be removed or compressed to one line.

### NAT-card depends on T0 solely for a disambiguation remark
**Class**: OBSERVE
**Foundation**: —
**ASN**: NAT-card Depends: "T0 (CarrierSetDefinition) — supplies the tumbler-length operator `#· : T → ℕ` referenced in the disambiguation remark distinguishing `|·|` from `#·`."
**Issue**: NAT-card is pure arithmetic about subsets of initial segments of ℕ; nothing in its Axiom uses `T`, `#·`, or any T0 construct. The dependency is declared only so that a disambiguation sentence can name `#·`. This inverts the natural layering (arithmetic depending on the tumbler carrier) and inflates NAT-card's dependency surface. The symbols `|S|` (set bars, set argument) and `#a` (hash, sequence argument) are already notationally and type-theoretically distinct.
**What needs resolving**: (OBSERVE — optional) Consider dropping the T0 dependency and either removing the disambiguation or relocating it to T0's side where the two operators first coexist.

VERDICT: REVISE
