# Regional Review — ASN-0034/TA-Pos (cycle 6)

*2026-04-22 16:55*

### Bound index `i` in TA-Pos quantifiers is not typed
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos formal contract: "`Pos(t)` iff `(E i : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`; `Zero(t)` iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`". T0 prose: "bounded quantifiers of the form `(Q i : 1 ≤ i ≤ #t : …)`".
**Issue**: The bound variable `i` is never typed. The relation `≤` supplied by NAT-order is defined on ℕ, so `1 ≤ i ≤ #t` is well-typed only when `i ∈ ℕ`; likewise the projection `tᵢ` is defined only for `i ∈ {1, …, #t} ⊆ ℕ`. Sibling axioms in this very ASN (NAT-zero, NAT-order, NAT-closure) all type their bound variables explicitly (`(A n ∈ ℕ :: …)`). TA-Pos breaks that convention, leaving a precise reader to infer the type of `i` from the bounding predicate it appears in — exactly the inference TLA+-style discipline is designed to remove.
**What needs resolving**: Either explicitly type `i` in the quantifier (e.g., `(E i ∈ ℕ : 1 ≤ i ≤ #t : …)`) or state once, where T0 introduces the index domain, that bounded `i`-quantifiers in this ASN range over ℕ by convention. The fix should restore parity with how NAT-order/NAT-zero/NAT-closure type their variables.

---

### `+` is used in NAT-closure without being introduced
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure formal contract: "`(A m, n ∈ ℕ :: m + n ∈ ℕ)` (addition closure); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity)." Prose: "ℕ is closed under addition, with `0` as the left additive identity."
**Issue**: The binary symbol `+` first appears in the addition-closure axiom and is then used in the left-identity axiom, but no clause introduces it as a binary operation on ℕ. NAT-order is explicit about its primitive ("The binary relation `<` on ℕ is a strict total order"); NAT-closure is silent about `+`. A reader cannot tell whether the closure axiom is *asserting totality of an existing primitive* `+` or *introducing* `+` by side-effect of asserting `m + n ∈ ℕ`. Either way, the symbol's signature (`+ : ℕ × ℕ → ℕ`?) is never stated.
**What needs resolving**: Introduce `+` as a named primitive operation on ℕ (signature stated) before the axioms that constrain it, in the same explicit register NAT-order uses for `<`. The closure and identity clauses can then constrain a symbol the contract has actually introduced.

---

### TA-Pos still discusses a length-0 case that T0 excludes
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos prose: "A length-`0` tumbler would satisfy `Zero(t)` vacuously, since the universal over an empty index range holds trivially; T0's clause removes that degenerate case from `T`."
**Issue**: The previous review flagged defensive justification for a hypothetical length-0 tumbler in the complementarity paragraph; the response moved it to the content-of-partition paragraph rather than dropping it. The pattern is the same: TA-Pos imagines an object outside `T` and explains why its absence is good. The substantive claim — that under T0's nonemptiness clause `Zero(t)` and `Pos(t)` carry non-vacuous content — needs only to *cite* T0's clause, not to re-litigate what would happen if the clause failed.
**What needs resolving**: Drop the length-0 sentence. The non-vacuity statement should rest on T0's `(A a ∈ T :: 1 ≤ #a)` directly without rehearsing the failed alternative.

---

### "Zero(t) witnesses the existence of a component equal to 0" misframes a universal as existential
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos prose: "T0's clause `(A a ∈ T :: 1 ≤ #a)` guarantees that every `t ∈ T` has at least one index in range, so `Pos(t)` witnesses the existence of a nonzero component and `Zero(t)` witnesses the existence of a component equal to `0`."
**Issue**: `Pos(t)` is defined existentially, so calling it a "witness of existence" is exact. `Zero(t)` is defined universally — it asserts *every* component equals `0`, a strictly stronger fact than the existence of one such component. The prose flattens both into the same existential shape, which loses the asymmetry the definitions deliberately encode. A precise downstream reader who later needs "all components are zero" will not find that statement here in plain form.
**What needs resolving**: State the two consequences asymmetrically, mirroring the definitions: `Pos(t)` exhibits a nonzero component; `Zero(t)` makes every component equal to `0` (and, given `#t ≥ 1`, this also implies at least one component equal to `0` is exhibited, if the existential corollary is what's wanted downstream).
