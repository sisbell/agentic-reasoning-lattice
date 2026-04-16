# Cone Review — ASN-0034/TA1 (cycle 1)

*2026-04-15 23:32*

I'll read the full content carefully and review for cross-cutting issues.

### PositiveTumbler undefined; `w > 0` admits tumblers that break TumblerAdd
**Foundation**: T1 (LexicographicOrder), case (ii) — prefix rule
**ASN**: TumblerAdd, formal contract and body: "By PositiveTumbler, the precondition `w > 0` means `(E i : 1 ≤ i ≤ n : wᵢ ≠ 0)`"
**Issue**: The symbol `>` is defined by T1 as lexicographic comparison. Under T1, `[0] < [0, 0]` by case (ii) (prefix rule), so `[0, 0] > [0]`, i.e., `[0,0] > 0` holds under T1 ordering. But `[0, 0]` has no nonzero component, so the action point set `{i : wᵢ ≠ 0}` is empty and `actionPoint(w)` is undefined — TumblerAdd's piecewise construction cannot execute. PositiveTumbler is cited as an external property but never defined in this ASN. Its characterization (`∃ nonzero component`) is strictly narrower than T1-positivity (`w > [0]`): every PositiveTumbler-positive tumbler is T1-positive, but not conversely. All-zero tumblers of length ≥ 2 pass the T1 gate but crash the construction. This propagates to every downstream consumer: TA0's proof opens with "Since `w > 0`, at least one component of `w` is nonzero" — true under PositiveTumbler, false under T1. TA1 inherits the same precondition.
**What needs resolving**: Either define PositiveTumbler as a named predicate distinct from T1 ordering and stop writing it as `w > 0` (since `>` already has a meaning), or prove the equivalence (which requires restricting T to exclude all-zero multi-component tumblers), or add an explicit precondition that `w` has at least one nonzero component without overloading the `>` symbol.

---

### TA0 stated before the definition it depends on
**Foundation**: N/A — document structure
**ASN**: TA0 (WellDefinedAddition), proof: "By TumblerAdd, each component of the result lies in ℕ and `#(a ⊕ w) = #w ≥ 1`"; formal contract: "actionPoint(w) ≤ #a"
**Issue**: TA0 appears under "Well-definedness of addition" before the "Tumbler arithmetic" section where TumblerAdd defines `⊕` and `actionPoint`. The statement `a ⊕ w ∈ T` requires `⊕` to have a meaning; the precondition `actionPoint(w) ≤ #a` requires `actionPoint` to be defined. Neither exists at the point TA0 is stated. The proof explicitly delegates to TumblerAdd ("By TumblerAdd"), confirming the dependency runs forward. This is not merely a presentation preference — TA0's formal contract contains terms (`⊕`, `actionPoint`) that are undefined when the reader encounters them, making the contract uninterpretable without reading ahead.
**What needs resolving**: TumblerAdd's definition (at minimum the piecewise construction and the `actionPoint` definition) must precede TA0, or TA0 must be reframed as a consequence of TumblerAdd rather than a precursor to it.

---

### TA1 quantifier binds free variable `k` only via informal "where" clause
**Foundation**: N/A — quantifier scoping
**ASN**: TA1 (OrderPreservationUnderAddition), statement: "`(A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a, #b) : a ⊕ w ≤ b ⊕ w)`, where `k` is the action point of `w`"
**Issue**: In the quantified formula, `k` appears free — it is not bound by the universal quantifier over `a, b, w`. The binding `k = actionPoint(w)` is supplied only by an informal "where" clause outside the formula. A reader (or a TLA+ translator) encountering the bare formula could interpret `k` as an additional universally quantified variable, which would change the meaning: "for every `k ≤ min(#a, #b)`, ..." is a strictly weaker statement than "for the specific `k` that is the action point of `w`, ...". The formal contract correctly writes `actionPoint(w) ≤ min(#a, #b)`, but the primary statement and the quantified formula disagree on whether `k` is free or functionally determined.
**What needs resolving**: The quantified statement should either substitute `actionPoint(w)` directly in place of `k`, or bind `k` with a `LET` construct inside the quantifier body, so the formula is self-contained.
