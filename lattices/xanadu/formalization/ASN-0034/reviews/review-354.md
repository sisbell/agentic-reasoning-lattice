# Regional Review — ASN-0034/ActionPoint (cycle 8)

*2026-04-21 23:35*

### TA-Pos's Depends list omits NAT-order and NAT-closure, though its Definition uses `≤` and `1`
**Foundation**: NAT-order (NatStrictTotalOrder) — introduces `<` and defines `≤`. NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ`.
**ASN**: TA-Pos formal contract — Definition: "`Pos(t)` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `Zero(t)` iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` … " Depends: "T0 (CarrierSetDefinition) … NAT-zero (NatZeroMinimum) — supplies `0 ∈ ℕ` for the literal appearing in `tᵢ = 0` and `tᵢ ≠ 0`."
**Issue**: TA-Pos's Definition uses three symbols drawn from NAT-* axioms: the literal `0` (cited to NAT-zero, correctly), the relation `≤` in the bounded-quantifier range `1 ≤ i ≤ #t`, and the numeral `1` in the same range. NAT-zero's addition to Depends resolved one of the three; the symmetric additions for `≤` (licensed by NAT-order) and `1` (licensed by NAT-closure) have not been made. The supporting prose "the equalities and inequalities in the two clauses are thus well-typed within ℕ" invokes `≤`/`<` well-typedness but the Depends list does not track back to NAT-order, which is what actually licenses `≤` on ℕ. The formal contract therefore still uses symbols the declared dependencies do not supply, in the same pattern the cycle that added NAT-zero was meant to close.
**What needs resolving**: Either extend TA-Pos's Depends list to cite NAT-order (for `≤`) and NAT-closure (for `1`), mirroring the NAT-zero citation pattern for `0`, or rewrite the Definition so the bounded-quantifier range uses only symbols already supplied by the declared dependencies.

---

### NAT-wellorder's body mentions `min(S)` but no claim in the ASN uses the `min` operator
**Foundation**: NAT-wellorder (NatWellOrdering) — formal contract: `(A S : S ⊆ ℕ ∧ S ≠ ∅ : (E m ∈ S :: (A n ∈ S :: m ≤ n)))`.
**ASN**: NAT-wellorder body, final sentence: "This least-element principle is what makes `min(S)` well-defined whenever `S` is nonempty."
**Issue**: ActionPoint was rewritten to avoid the `min` operator — its Definition now reads "actionPoint(w) is the unique `m ∈ S` such that `(A n ∈ S :: m ≤ n)`" and its derivation threads through the existential/uniqueness argument without naming `min`. No other claim in the ASN uses `min`. NAT-wellorder's body prose still announces that the principle makes `min(S)` well-defined, but the operator it gestures at appears nowhere downstream. This is a use-site inventory for an operator the ASN does not consume — the precise reader sees `min(S)` introduced in NAT-wellorder's body and finds no claim that cites it, leaving the sentence as dangling commentary about a notation the ASN does not deploy.
**What needs resolving**: Either drop the `min(S)` sentence from NAT-wellorder's body (leaving the least-element principle as the axiom's sole content), or identify a stated consumer and rewrite a downstream claim to use `min` so the body's mention lands on actual use. NAT-wellorder's formal-axiom slot should either carry content its consumers cite or name no operator its consumers do not use.

---

### T0 does not commit that component positions are natural numbers, though downstream claims quantify over indices via `1 ≤ i ≤ #t`
**Foundation**: T0 (CarrierSetDefinition) — formal contract: "T is the set of all nonempty finite sequences over ℕ, equipped with length `#· : T → ℕ` and component projection `·ᵢ` yielding `aᵢ ∈ ℕ` at each component position of `a ∈ T`."
**ASN**: TA-Pos Definition: "`Pos(t)` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` …". ActionPoint Definition and derivation: "S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}", and "a subset of ℕ because its elements are indices with 1 ≤ i ≤ #w".
**Issue**: T0's axiom commits that components take values in ℕ (`aᵢ ∈ ℕ`) and that length is in ℕ (`#· : T → ℕ`). It does not commit that the index domain of `·ᵢ` is ℕ — the phrase "at each component position" leaves the type of positions unsaid. TA-Pos's bounded quantifier `(E i : 1 ≤ i ≤ #t : …)` presupposes `i ∈ ℕ` for `≤` to be well-formed; ActionPoint's derivation explicitly invokes `S ⊆ ℕ` with the gloss "because its elements are indices with 1 ≤ i ≤ #w" — a justification that assumes, rather than derives, index ℕ-membership. The load-bearing step is ActionPoint's appeal to NAT-wellorder, whose precondition `S ⊆ ℕ` is exactly what this gap leaves unsecured. Component-position-is-ℕ is standard convention, but T0's axiom does not encode it, so consumers rest on an unstated premise.
**What needs resolving**: Either extend T0's axiom to state that the index domain of `·ᵢ` is ℕ (or equivalently that `·ᵢ : T × {1, …, #a} → ℕ` with `{1, …, #a} ⊆ ℕ`), or rewrite ActionPoint's derivation to cite whatever T0 content *does* license `S ⊆ ℕ`, so the NAT-wellorder precondition is discharged against stated axiom content rather than an implicit convention.

## Result

Regional review not converged after 8 cycles.

*Elapsed: 4281s*
