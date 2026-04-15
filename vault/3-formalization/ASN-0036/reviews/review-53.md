# Cone Review — ASN-0036/ValidInsertionPosition (cycle 2)

*2026-04-13 17:38*

### ValidInsertionPosition formal contract extends `shift` to 0, contradicting OrdinalShift's precondition and S8-depth's explicit non-extension

**Foundation**: OrdinalShift (ShiftDefinition, ASN-0034) — precondition `n ≥ 1`
**ASN**: ValidInsertionPosition formal contract — "v = shift(min(V_S(d)), j) for 0 ≤ j ≤ N (where shift(min, 0) = min)"; S8-depth — "define v + 0 = v (identity) and v + k = shift(v, k) for k ≥ 1. OrdinalShift (ASN-0034) has precondition n ≥ 1; the extension to k = 0 is purely notational"
**Issue**: S8-depth explicitly states that OrdinalShift retains precondition `n ≥ 1` and introduces a separate wrapper notation `v + k` to handle `k = 0`. ValidInsertionPosition's formal contract ignores this, writing `shift(min, 0) = min` — extending `shift` itself to include 0. ValidInsertionPosition's own body text is consistent with S8-depth (it separates `v = min(V_S(d))` for `j = 0` from `v = shift(min, j)` for `1 ≤ j ≤ N`), but the formal contract merges the cases using the prohibited `shift(·, 0)`. The S8-depth correspondence run definition uses the `+` wrapper with explicit case split ("v + 0 = v, a + 0 = a, and for k ≥ 1, v + k = shift(v, k)"), confirming this is not an oversight but an intentional design — one that ValidInsertionPosition's formal contract violates.
**What needs resolving**: The formal contract for ValidInsertionPosition must either use the `v + k` wrapper notation introduced by S8-depth (writing `v = min(V_S(d)) + j` for `0 ≤ j ≤ N`), or separate the `j = 0` case as the body text already does. Alternatively, if the intent is to extend `shift` to `n ≥ 0` globally, OrdinalShift's precondition must be relaxed and S8-depth's commentary about the `n ≥ 1` restriction must be removed.

---

### S8-depth postcondition 3 cites S7c but omits the upstream chain establishing that `a` is an element-level address

**Foundation**: OrdinalShift (ShiftDefinition, ASN-0034) — prefix rule `shift(v, k)ᵢ = vᵢ` for `i < #v`
**ASN**: S8-depth formal contract — "Preconditions: Postcondition 3 requires S7c (`#fields(a).element ≥ 2`)"; S8-depth postcondition 3 — "E₁(a + k) = E₁(a)"
**Issue**: Postcondition 3 reasons about `E₁(a)` — the first component of `a`'s element field. For `fields(a).element` and `E₁(a)` to be meaningful, `a` must be an element-level address with a parseable four-field structure. This requires: (1) the correspondence run definition gives `M(d)(v) = a` at `k = 0`, (2) S3 (ReferentialIntegrity) gives `M(d)(v) ∈ dom(Σ.C)`, (3) S7b (Element-level I-addresses) gives `zeros(a) = 3`, confirming `a` has all four fields. Only then does S7c (`#fields(a).element ≥ 2`) apply. The formal contract cites S7c but not S3 or S7b — the upstream links that establish `a` is an address to which S7c is applicable. S8a (the immediately preceding property) does cite S3 and S7b for its own derivation, so both are available in the ASN; S8-depth simply omits them from its own precondition list.
**What needs resolving**: S8-depth's precondition list for postcondition 3 must include S3 and S7b (or cite S8a as an intermediary that provides the element-level address guarantee), making the chain from `a = M(d)(v)` through `a ∈ dom(Σ.C)` through `zeros(a) = 3` to `#fields(a).element ≥ 2` explicit.

---

### D-MIN minimum justification cites T0(a) for component positivity that comes from S8a

**Foundation**: T0(a) (UnboundedComponentValues, ASN-0034) — "Every component value of a tumbler is unbounded — no maximum value exists"; S8a (V-position well-formedness) — `v > 0` for all V-positions
**ASN**: D-MIN body — "any other position in subspace S shares the first component S but must differ at some subsequent component; at the first such component j, [S, 1, …, 1] has value 1 and the other position, having a positive natural (T0(a)) distinct from 1, has value strictly greater than 1 — making it strictly larger by T1(i)"
**Issue**: The argument that `[S, 1, …, 1]` is the least element of `V_S(d)` under T1 requires that every V-position component is a positive natural number (≥ 1), so any component distinct from 1 must be ≥ 2. The text attributes "positive natural" to T0(a), but T0(a) establishes that component values are unbounded natural numbers — it does not establish positivity. Natural numbers include 0, and T4 explicitly uses zero-valued components as field separators. The positivity of V-position components comes from S8a (`v > 0`), which derives it from T4's positive-component constraint via S8a's proof. Neither S8a nor T4 appears in D-MIN's precondition list or in the cited parenthetical. A reader or formalizer following the T0(a) citation finds only unboundedness — no mention of the `≥ 1` lower bound the argument requires.
**What needs resolving**: The minimum-justification paragraph should cite S8a (or T4's positive-component constraint through S8a) for the positivity claim, not T0(a). If the argument is considered load-bearing for the axiom's soundness, S8a should also appear in D-MIN's precondition list.
