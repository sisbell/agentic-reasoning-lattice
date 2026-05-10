# Cross-cutting Review — ASN-0034 (cycle 5)

*2026-04-17 07:42*

### Vocabulary declares `fields` total on T while T4b only establishes well-definedness on T4-valid tumblers
**Foundation**: (foundation ASN; internal consistency review)
**ASN**: Vocabulary entry for `fields(t)` and T4b (UniqueParse).
**Issue**: The Vocabulary declaration reads:

> "**fields(t)** — total function fields : T → Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) × Seq(ℕ⁺) with fields(t) = (N(t), U(t), D(t), E(t)); absent fields are represented by the empty sequence ε, unambiguous because every present field segment is non-empty (T4a). Presence pattern by zeros(t): 0 → only N; 1 → N, U; 2 → N, U, D; 3 → all four"

This asserts `fields` is a *total function* on `T`. T4b, however, is the property that licenses the function, and its Preconditions require "`t` satisfies T3 (CanonicalRepresentation)" and "`t` satisfies the T4 constraints (at most three zero-valued components, field-segment constraint — no two zeros adjacent, `t₁ ≠ 0`, `t_{#t} ≠ 0`)" — T4b's postcondition only states `fields` is "well-defined and uniquely determined by `t`" under those preconditions. Two classes of tumblers in `T` fall outside T4b's scope:

- Tumblers with `zeros(t) ≥ 4` (T violates `zeros(t) ≤ 3` only at T4-validity, not at T0-carrier). The Vocabulary's "Presence pattern by zeros(t)" lists only zero counts 0, 1, 2, 3 — so for `t ∈ T` with `zeros(t) = 4`, the presence pattern has no case, and `fields(t)` has no stated value.
- Tumblers violating the field-segment constraint but with `zeros(t) ≤ 3` — e.g., `[0, 1, 0, 2]` (violates `t₁ ≠ 0`) or `[1, 0, 0, 2]` (violates no-adjacent-zeros). T4b does not apply, and the Vocabulary's presence pattern alone (`zeros(t) = 1` → N, U non-empty) gives no well-defined answer for where the separator sits or whether an "empty user" is admitted.

Downstream consumers interpret `fields` as total: T6's proof in Ingredient 1 says "By T4(b), `fields(t) = (N(t), U(t), D(t), E(t))` is well-defined and uniquely determined by `t` alone", and the three-stage pattern "extract — presence check — componentwise compare" assumes that `fields(a)` and `fields(b)` yield values for any `a, b` satisfying T6's precondition "a, b ∈ T are valid tumblers satisfying T4" — which is fine locally but relies on T4's preconditions being enforced by every caller. A reader navigating from the Vocabulary would believe `fields` is total on `T` rather than a partial function sourced from T4b's T4-gated postcondition.

**What needs resolving**: Either revise the Vocabulary entry to state that `fields` is defined on T4-valid tumblers (with a forward pointer to T4b), remove the word "total", and restrict the presence pattern's scope explicitly to that subdomain; or strengthen T4b to extend `fields` to all of `T` with a stipulated value (e.g., `ε × ε × ε × ε`) on non-T4-valid inputs and carry that through the presence pattern. Either way, the Vocabulary's current declaration and T4b's gated postcondition should not disagree about the function's domain. The issue is closely related to Previous Findings' T7 finding (quantification range vs. T4b) but distinct: it lives at the Vocabulary level where every consumer reads the signature, not only in one corollary's quantifier.
