# Regional Review — ASN-0034/TA-Pos (cycle 5)

*2026-04-22 16:47*

### "Exactly one of" in trichotomy is English glue inside a formal-contract slot
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: NAT-order formal contract: "`(A m, n ∈ ℕ :: exactly one of m < n, m = n, n < m)` (trichotomy)."
**Issue**: The phrase "exactly one of" is natural-language shorthand sitting where every other axiom in the contract uses fully symbolic logic (`¬`, `∧`, `∨`, `⟹`). A TLA+-style reader cannot mechanically translate "exactly one of A, B, C" without choosing between several expansions (pairwise-exclusive disjunction, indicator-sum, etc.). Sibling axioms in this very contract — irreflexivity and transitivity — are given as closed formulas; trichotomy regresses to prose. The asymmetry matters because trichotomy is the axiom that downstream reasoning (e.g., the `n < 0` reductio in NAT-zero) will cite case-by-case.
**What needs resolving**: Express the trichotomy axiom as a closed formula in the same symbolic register as irreflexivity and transitivity — e.g., an explicit disjunction of the three mutually-negated conjuncts — so the contract contains no English connectives.

### NAT-order's formal contract omits the *Depends* slot entirely
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: NAT-order formal contract lists only an *Axiom:* bullet; there is no *Depends:* bullet of any kind. Every sibling contract in the ASN (T0, NAT-zero, NAT-closure, TA-Pos) carries an explicit *Depends:* slot.
**Issue**: The reader cannot distinguish "NAT-order depends on nothing" from "the Depends slot was forgotten." For a review pipeline that inspects contracts uniformly, a silently absent slot is operationally different from an explicit `(none)`. The asymmetry also weakens the claim that NAT-order is genuinely foundational — that is a structural assertion worth recording, not inferring.
**What needs resolving**: Make the absence explicit by adding a *Depends:* bullet with `(none)` (or equivalent) so every contract in the ASN has the same slot structure and NAT-order's root position is declared rather than implied by omission.

### TA-Pos prose argues about a length-0 case that T0 excludes
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos prose: "…irrespective of whether the index range `{i : 1 ≤ i ≤ #t}` is empty; at a hypothetical length-`0` tumbler `Pos` would reduce to `False` and `Zero` to `True`, and the biconditional `False ⟺ ¬True` would still hold."
**Issue**: T0's nonemptiness axiom `(A a ∈ T :: 1 ≤ #a)` already removes length-0 tumblers from `T`, and the very next paragraph of TA-Pos invokes that axiom to establish the partition is non-vacuous. Discussing the biconditional's behavior "at a hypothetical length-`0` tumbler" is defensive justification for a case that cannot arise in the carrier — essay content explaining away a non-issue. The precise reader must skip this aside to reach the actual claim.
**What needs resolving**: Drop the parenthetical about the length-0 case. The complementarity argument needs only DeMorgan plus the definitions; whatever would happen "outside T" is not a statement TA-Pos needs to make.

### Variable flip in T0 prose breaks local reference
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: T0 prose: "The nonemptiness of each `a ∈ T` is formalized as `(A a ∈ T :: 1 ≤ #a)`… The inequality `1 ≤ #a` is thus well-typed within ℕ, and with it the index domain `{1, …, #a}` is never empty, so bounded quantifiers of the form `(Q i : 1 ≤ i ≤ #t : …)` range over a nonempty set rather than collapsing to vacuity."
**Issue**: The paragraph binds `a` throughout, then switches to `#t` in the closing clause without introducing `t`. A precise reader has to decide whether `t` is a typo for `a`, a forward reference to the TA-Pos variable name, or a separate object. In a document whose central discipline is "every symbol has one meaning," an un-introduced variable in a justification clause is a small but real consistency failure.
**What needs resolving**: Use a single variable throughout the paragraph (either keep `a` consistently, or bind `t ∈ T` explicitly before the closing clause).
