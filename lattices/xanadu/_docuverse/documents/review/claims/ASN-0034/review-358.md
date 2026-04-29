# Regional Review — ASN-0034/T4a (cycle 1)

*2026-04-22 00:21*

### T3 (CanonicalRepresentation) cited without statement
**Foundation**: none — this is a foundation ASN
**ASN**: T4's Formal Contract Preconditions: "T4b requires T3 (CanonicalRepresentation) for fixed component sequences"; T4b Depends: "T3 (CanonicalRepresentation) — fixed component sequences license uniqueness of the parse"; T4b Preconditions: "`t` satisfies T3 (CanonicalRepresentation) and the T4 constraints."
**Issue**: T3 is named four times as a precondition/dependency, but no T3 (CanonicalRepresentation) claim appears anywhere in the ASN, and the ASN has no declared depends. The uniqueness argument in T4b explicitly leans on it ("T3 fixes the components of `t`, so the separator positions are uniquely determined…"). Without T3 in scope, the chain from "T4-valid `t`" to "the components of `t` are fixed" is broken; one could in principle have two distinct component sequences satisfying T4 and disagree on parses.
**What needs resolving**: Either include T3 in this ASN, declare it as an external dependency with its export quoted, or rewrite the uniqueness argument so it does not require an unstated lemma.

### T4b case analysis omits first/last segment non-emptiness for k = 2 and k = 3
**Foundation**: T4 positional conditions (i)–(iii)
**ASN**: T4b proof, "*Case k = 2.* … Interior non-emptiness from no-adjacent-zeros (`s₂ ≥ s₁ + 2`).  *Case k = 3.* … `s₂ ≥ s₁ + 2`, `s₃ ≥ s₂ + 2`."
**Issue**: Case k = 1 carefully cites both ends: `t₁ ≠ 0 ⇒ s₁ ≥ 2` and `t_{#t} ≠ 0 ⇒ s₁ ≤ #t − 1`. Cases k = 2 and k = 3 give only the *interior* inequalities. The non-emptiness of `N(t)` (needs `s₁ ≥ 2`) and of `D(t)` or `E(t)` at the tail (needs `s_k ≤ #t − 1`) is never derived in those cases, even though T4b's Postconditions claim each of those fields is non-empty.
**What needs resolving**: Either restate cases k = 2 and k = 3 to discharge first- and last-segment non-emptiness explicitly, or factor non-emptiness through T4a so the case work need only fix boundaries.

### "Absence" used as a primitive notion in T4b without definition
**Foundation**: T4a's stated postcondition concerns segment non-emptiness, not absence
**ASN**: T4b prose: "By T4a, for each `X ∈ {N, U, D, E}` and every T4-valid `t`, `X(t) = ε` iff field `X` is absent in `t`." T4 Preconditions: "T4b requires … T4a (SyntacticEquivalence) for the absence-marker unambiguity clause."
**Issue**: T4a's postcondition is "the three positional conditions hold iff every field segment is non-empty" — it never mentions absence, never relates ε to anything, and never partitions the four labels into present/absent. Meanwhile "absent" is nowhere defined in T0–T4c; the only operational notion of "field X is absent" comes from T4b's own case construction (which assigns ε in cases where `zeros(t)` is too small). So the cited biconditional reduces to "ε iff ε" and the appeal to T4a is doing no work.
**What needs resolving**: Pin down what "field X is absent in `t`" means independently of T4b's own assignment (e.g., as a level-driven predicate keyed to `zeros(t)` via T4c), and verify the iff against that definition rather than citing T4a.

### `>` and `ℕ⁺` notation used though only `<`, `≤` are defined
**Foundation**: NAT-order defines `<` and (derivatively) `≤`; nothing introduces `>` or `≥`
**ASN**: T4 axiom: "where each `Nᵢ, Uⱼ, Dₖ, Eₗ > 0`"; T4 prose: "write `ℕ⁺ = {n ∈ ℕ : n > 0}`"; T4b: "`Seq(ℕ⁺) × Seq(ℕ⁺) × …`"; T4 prose: "non-zero components are field components" but elsewhere "`tᵢ > 0`".
**Issue**: NAT-order only introduces `<` (with `≤` derived). The recent revision history records explicit elimination of `>`/`≥` on ℕ, yet the carrier of every projection in T4b is defined via `n > 0`, T4's axiom uses `> 0`, and `ℕ⁺` itself is defined with `>`. A precise reader cannot tell whether `>` is meant as the un-introduced symbol or as an unstated abbreviation for `0 < ·`.
**What needs resolving**: Either introduce `>` and `≥` formally as the converses of `<` and `≤`, or restate every occurrence (`Nᵢ > 0`, `ℕ⁺ = {n ∈ ℕ : 0 < n}`, `tᵢ > 0`, etc.) using the available relations.

### `Seq(·)` used as a type without definition; clash with T0's nonempty restriction
**Foundation**: T0 defines `T` as nonempty finite sequences over ℕ
**ASN**: T4b: "`fields : T ⇀ Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺)`"; absent fields represented by ε.
**Issue**: `Seq(·)` is never defined. The only sequence-type construct in scope is T (nonempty finite sequences over ℕ). For `ε` to inhabit `Seq(ℕ⁺)`, the codomain must include the empty sequence — i.e. `Seq(ℕ⁺)` must be the *possibly empty* finite sequences over ℕ⁺. That construct is never given a contract, and its relationship to T (nonempty) is not stated.
**What needs resolving**: Either introduce a sequence-type constructor `Seq(·)` (specifying whether the empty sequence is included and how it relates to T's "nonempty" stipulation), or restate the codomain of `fields` in terms already in scope.

### T4 Formal Contract Preconditions slot describes other claims' preconditions
**Foundation**: structural — Preconditions of a claim should be that claim's preconditions
**ASN**: T4 Formal Contract: "*Preconditions:* T4b requires T3 (CanonicalRepresentation) for fixed component sequences, and T4a (SyntacticEquivalence) for the absence-marker unambiguity clause. T4c requires no inter-consequence precondition."
**Issue**: T4's own preconditions are never stated; the slot is filled with meta-prose about its dependents' preconditions. A reader looking up "what must hold to invoke T4" finds only commentary on T4b/T4c, which themselves carry their own Preconditions slots.
**What needs resolving**: State T4's own preconditions (likely "`t ∈ T`") in this slot and move the inter-claim commentary out, or remove the slot entirely if T4 is purely axiomatic.
