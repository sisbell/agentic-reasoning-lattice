# Cone Review — ASN-0034/T8 (cycle 2)

*2026-04-14 01:36*

I've read the full ASN tracking definitions, quantifier scopes, and precondition chains across all properties. Two new findings.

---

### Roundtrip `a ⊕ (b ⊖ a) = b` fails when `#a > #b`, a regime the stated constraint does not address
**Foundation**: TumblerAdd (TumblerAdd) — postcondition `#(a ⊕ w) = #w`; TumblerSub (TumblerSub) — postcondition `#(a ⊖ w) = max(#a, #w)`
**ASN**: TumblerSub (TumblerSub) — "The roundtrip `a ⊕ (b ⊖ a) = b` therefore requires the additional constraint `zpd(b, a) ≤ #a` — equivalently, `a` is not a proper sequence-prefix of `b` — as established by D0."
**Issue**: The two result-length rules compose as `#(a ⊕ (b ⊖ a)) = #(b ⊖ a) = max(#a, #b)`, which equals `#b` only when `#a ≤ #b`. The stated constraint `zpd(b, a) ≤ #a` is automatically satisfied whenever `#a > #b` (because zpd cannot exceed `max(#a, #b) = #a`), so it provides no restriction in this regime — yet the roundtrip fails. Concretely: `a = [1, 0, 3, 0, 2, 0, 1, 100]` (`#a = 8`), `b = [1, 0, 3, 0, 5]` (`#b = 5`), `b > a` at position 5. Then `d = b ⊖ a = [0, 0, 0, 0, 3, 0, 0, 0]` (`#d = 8`), `zpd = 5 ≤ 8 = #a` (stated constraint satisfied), `actionPoint(d) = 5 ≤ 8 = #a` (TumblerAdd precondition satisfied). But `a ⊕ d = [1, 0, 3, 0, 5, 0, 0, 0]` has length 8, while `b` has length 5. By T3, `[1, 0, 3, 0, 5, 0, 0, 0] ≠ [1, 0, 3, 0, 5]`. The mechanism: TumblerSub copies the zero-padded minuend's tail (positions > zpd) into the displacement, including the zeros introduced by padding the shorter `b` to length `#a`; TumblerAdd then copies these trailing zeros into the result (positions > action point come from the displacement). The three trailing zeros propagate through both operations and inflate the result beyond `b`'s length. The two conditions — `zpd(b, a) ≤ #a` and `#a ≤ #b` — are independently necessary: the first ensures TumblerAdd's precondition; the second ensures the result length matches `b`. Neither implies the other (counterexample for each direction shown above and in finding #1).
**What needs resolving**: The roundtrip constraint must include `#a ≤ #b` alongside `zpd(b, a) ≤ #a`. The text's characterization "equivalently, `a` is not a proper sequence-prefix of `b`" captures only the zpd condition and is silent on the length condition. If D0 establishes the full conjunction, the TumblerSub description must reflect both conditions; if D0 establishes only the zpd condition, D0 itself is incomplete.

---

### TumblerAdd's formal contract omits the ordering guarantee that defines it as a position-advance operation
**Foundation**: TA5 (HierarchicalIncrement) — formal contract postcondition (a): "`t' > t` under T1"
**ASN**: TumblerAdd (TumblerAdd) — "Tumbler addition is not arithmetic addition — it is a **position-advance operation**"; formal contract postconditions: "`a ⊕ w ∈ T`, `#(a ⊕ w) = #w`"
**Issue**: The guarantee `a ⊕ w > a` (under T1) is the semantic core of "position-advance" and follows immediately from the construction: at the action point `k`, `(a ⊕ w)_k = a_k + w_k > a_k` (since `w_k ≥ 1` as the first nonzero component of a positive tumbler), and for `i < k` the components agree, so T1 case (i) witnesses `a < a ⊕ w`. The analogous operation TA5 includes this as an explicit postcondition — postcondition (a) — yet TumblerAdd's contract contains only membership and length. Any downstream property that needs `a ⊕ w > a` (span endpoint computation, displacement ordering, the position-advance semantics that TumblerSub's motivating description assumes when it says "the displacement from `a` to `b`") has no formal contract to cite. The gap is between TumblerAdd's descriptive text (which calls it position-advance) and its formal contract (which doesn't guarantee advancement).
**What needs resolving**: Add `a ⊕ w > a` (T1) as an explicit postcondition of TumblerAdd's formal contract, parallel to TA5's postcondition (a).
