# Cone Review — ASN-0034/TA7a (cycle 1)

*2026-04-18 17:36*

### Undefined symbol `Z` in TA7a
**Foundation**: TA-Pos (PositiveTumbler) — defines the *predicates* `Pos(t)` and `Zero(t)`, not a set.
**ASN**: TA7a proof and postconditions — "We have `[0, 2] ∈ T` (confirming the T-closure claim) but `[0, 2] ∉ S ∪ Z`"; "`[x] ⊖ [n] ∈ Z` when `x = n`"; "For `⊖` on single-component ordinals (`#o = 1`, `#w = 1`): the result is in `S ∪ Z`".
**Issue**: The symbol `Z` is used as if it were a set of zero tumblers, but TA-Pos introduces only the predicate `Zero(t)`. No set-form definition `Z = {t ∈ T : Zero(t)}` appears anywhere in the ASN. TA7a's S-membership claims and the final postcondition clauses `S ∪ Z` reference an undefined object.
**What needs resolving**: Either define `Z` explicitly (likely at the TA-Pos definition site, paralleling the paired predicate introduction) and cite it in TA7a's Depends, or rewrite the TA7a postconditions in terms of the `Zero(·)` predicate rather than a set `Z`.

---

### TA7a uses `max` as primitive, contradicting the ASN's established dispatch convention
**Foundation**: TumblerSub's Definition and Postconditions, TA2's Definition and Postconditions — both explicitly replace `max(#a, #w)` with a NAT-order trichotomy dispatch on `(#a, #w)` so that `L` is named by the selected sub-case, "rather than by a primitive binary-maximum operator on ℕ".
**ASN**: TA7a Conjunct 2 proof — "zero-pad to length `max(#o, #w)`"; Preliminary case — "TumblerSub produces a result of length `max(m, #w) = #w > m`".
**Issue**: TumblerSub and TA2 go to considerable length to eliminate `max` as an unsourced primitive, routing through NAT-order trichotomy and listing `L` explicitly in sub-cases (α), (β), (γ). TA7a consumes TumblerSub's result-length postcondition but writes `max(m, #w)` and `max(#o, #w)` directly, reintroducing the primitive the ASN has taken pains to avoid. The convention is cross-cutting: every operator in a Definition must be Depends-backed.
**What needs resolving**: Rewrite TA7a's length-dispatch steps in terms of the same NAT-order trichotomy (or cite TumblerSub's dispatch directly via its postcondition `#(a ⊖ w) = L`) rather than invoking `max` as a primitive.

---

### `o₁ − 0 = o₁` in TA7a Case `k ≥ 2` routes through the wrong NAT-closure/NAT-sub combination
**Foundation**: NAT-closure axiom — `(A n ∈ ℕ :: 0 + n = n)` (left additive identity only); NAT-sub right-telescoping — `(A m, n ∈ ℕ :: (m + n) − n = m)`. T0's exhaustive NAT-* enumeration omits commutativity, and TumblerAdd's Depends explicitly flags this (e.g., "differ by a commutativity step absent from the enumeration").
**ASN**: TA7a Case `k ≥ 2` — "`r₁ = o₁ - 0 = o₁` — the identity `o₁ - 0 = o₁` is NAT-sub's right-telescoping clause at `n = 0` combined with NAT-closure's additive identity".
**Issue**: Right-telescoping at `m = o₁, n = 0` yields `(o₁ + 0) − 0 = o₁`. To reduce this to `o₁ − 0 = o₁`, one needs `o₁ + 0 = o₁` (the *right* additive identity). NAT-closure supplies only `0 + o₁ = o₁`. Without commutativity of addition on ℕ — which T0's enumeration explicitly excludes, and which TumblerAdd's own Depends discipline relies on — right-telescoping + left-identity does not close this identity. The correct route is NAT-sub's *left-inverse characterisation* `n + (m − n) = m` at `m = o₁, n = 0` (under `o₁ ≥ 0` from NAT-zero), yielding `0 + (o₁ − 0) = o₁`, then NAT-closure's left additive identity at `n = o₁ − 0` rewriting the left-hand side to `o₁ − 0`, giving `o₁ − 0 = o₁`.
**What needs resolving**: Either bundle `n + 0 = n` into NAT-closure's axiom as a right-additive-identity clause (with the analogous propagation to NAT-closure's Formal Contract), or rewrite TA7a's Case `k ≥ 2` derivation to route through NAT-sub's left-inverse characterisation rather than right-telescoping — whichever aligns with the rest of the ASN's subtraction-identity discipline.

---

### TA7a's ⊖ proof opening drops `Pos(w)` from the recited preconditions
**Foundation**: TA2's preconditions — `a ∈ T, w ∈ T, a ≥ w` (no `Pos(w)`); TA7a's Formal Contract preconditions for `⊖` — `o ∈ S, w ∈ T, Pos(w), o ≥ w`.
**ASN**: TA7a Conjunct 2 opening — "The precondition gives `o ∈ T`, `w ∈ T`, and `o ≥ w`. These are exactly the preconditions of TA2 (well-defined subtraction)."
**Issue**: The Formal Contract declares `Pos(w)` as a precondition for `⊖`, and the proof body uses `w`'s action point `k` (defined only when `Pos(w)`) throughout the case split ("Case `k ≥ 2`", "Case `k = 1`, divergence `d = 1`", etc.). But the Conjunct 2 opening lists only `o ∈ T, w ∈ T, o ≥ w` when matching against TA2, creating a minor inconsistency: either `Pos(w)` is a precondition of `⊖` (as the contract says, and as the action-point case split requires) or it is not (as the TA2 handoff line implies). The second paragraph of the proof then proceeds to use `k = actionPoint(w)` without having re-justified `Pos(w)`'s presence at this step.
**What needs resolving**: Reconcile the contract's `⊖` precondition list with the Conjunct 2 proof opening — either drop `Pos(w)` from the `⊖` precondition list and justify the action-point use differently (or restrict it to cases where `w` is positive), or add `Pos(w)` to the recited preconditions at the TA2 handoff and note explicitly that it is *additional* to TA2's needs but required for the subsequent action-point case analysis.
