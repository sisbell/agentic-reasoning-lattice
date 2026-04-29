# Regional Review — ASN-0034/Divergence (cycle 3)

*2026-04-24 05:33*

Reading the ASN as a system, checking claim boundaries, precondition chains, and prose discipline.

### Meta-prose about symbol provenance recurs across NAT-addcompat, NAT-cancel, and NAT-discrete
**Class**: REVISE
**Foundation**: (internal)
**ASN**: Three parallel paragraphs, each sitting between the top-of-axiom statement and the Formal Contract:
- NAT-addcompat: "The left/right compatibility clauses invoke the non-strict `≤` *defined* in NAT-order (by `m ≤ n ⟺ m < n ∨ m = n`) and the binary addition closed over ℕ by NAT-closure; the strict successor inequality uses NAT-order's primitive strict relation `<` together with that same closed addition and NAT-closure's `1 ∈ ℕ`."
- NAT-cancel: "Two primitives appear in these clauses that are not introduced here. The binary operation `+` is the one posited by NAT-closure's signature clause `+ : ℕ × ℕ → ℕ`; all clauses use `+` at exactly that arity. The literal `0` appearing on the right-hand side of the absorption conclusion is the `0 ∈ ℕ` posited by NAT-zero — NAT-cancel introduces no constant of its own, so without NAT-zero supplying the symbol the absorption conclusion `n = 0` would reference an ungrounded literal."
- NAT-discrete: "The axiom body invokes two symbols beyond ℕ's primitive `<` and `=`: the non-strict companion `≤`, *defined* in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`, and the successor term `m + 1`, whose summand `1 ∈ ℕ` and closure `m + 1 ∈ ℕ` are posited by NAT-closure."
**Issue**: Each paragraph inventories which symbol comes from which dependency and why that dependency is named. The prior cycle flagged the specific closing-sentence variants ("Both foundations are declared in the Depends slot…" and "matching the precedent NAT-closure uses to declare NAT-zero…"), and those exact sentences are gone. What remains is the same pattern in different paragraphs — defensive justification for the Depends list rather than claim development. The Depends citations under Formal Contract already state the supplied symbol and its use; these paragraphs restate that content outside the contract. The NAT-cancel instance goes furthest ("so without NAT-zero supplying the symbol … would reference an ungrounded literal") — counterfactual reasoning about what would happen if the Depends were different is exactly the reviser-drift pattern.
**What needs resolving**: Remove the three "axiom body invokes symbol X from dependency Y" paragraphs. Keep the Depends citations, which already name the supplied symbol and its use site. Substantive derivations (NAT-cancel's walk from cancellation to summand absorption; NAT-discrete's forward-walk to the no-interval form; NAT-order's exactly-one-trichotomy derivation) stay.

### Divergence Definition assigns the function's value from an existential
**Class**: REVISE
**Foundation**: (internal)
**ASN**: Divergence, *Formal Contract → Definition*: "(i) if `∃ k : 1 ≤ k ∧ k ≤ #a ∧ k ≤ #b` with `aₖ ≠ bₖ` and `(A i : 1 ≤ i < k : aᵢ = bᵢ)`, then `divergence(a, b) = k`".
**Issue**: This is the function-defining clause, but it introduces `k` existentially and then assigns the function's value to that `k` — the form `(∃k. P(k)) ⟹ f(a,b) = k` leaves `k` unbound on the right side and does not, as stated, designate a unique value. The Postconditions line later supplies the designating description ("`divergence(a, b) = k` is the unique least index satisfying …"), which is the form the Definition itself ought to carry. Uniqueness *is* derivable from the conjunction `aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`, but the Definition does not state the derivation and does not state the unique/least choice. A function definition should not require the reader to consult the Postconditions to learn which `k` is meant.
**What needs resolving**: Rewrite case (i) of the Definition as a designating description — "`divergence(a, b)` is the (unique / least) `k` satisfying `1 ≤ k ∧ k ≤ #a ∧ k ≤ #b ∧ aₖ ≠ bₖ ∧ (A i : 1 ≤ i < k : aᵢ = bᵢ)`" — so the Definition itself designates a value. If the "least" formulation is chosen, the NAT-wellorder Depends citation should follow suit and name existence rather than carrying the "distinct role" framing previously flagged.

VERDICT: REVISE
