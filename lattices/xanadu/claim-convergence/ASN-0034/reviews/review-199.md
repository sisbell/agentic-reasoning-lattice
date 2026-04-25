# Cone Review — ASN-0034/TA0 (cycle 1)

*2026-04-17 20:55*

### NAT-closure and NAT-addcompat carry facts beyond what T0's prose enumerates

**Foundation**: T0 (CarrierSetDefinition), whose prose fixes the NAT-* axiom list as "closure under successor and addition, strict total order, discreteness, order compatibility of addition, well-ordering, zero as lower bound of ℕ, partial subtraction (…clauses…), additive cancellation (left, right, and summand absorption), and associativity of addition" — and further states "This list is exhaustive: the ASN states no NAT-* axiom outside it."

**ASN**: TumblerAdd's Depends attributes the *additive identity* `0 + wₖ = wₖ` to NAT-closure ("both invoke NAT-closure's additive identity (0 + wₖ = wₖ)"); the same Depends attributes the *strict successor inequality* `n < n+1` to NAT-addcompat ("NAT-addcompat's strict successor inequality (n < n + 1, instantiated at n = aₖ)"). ActionPoint's Depends similarly uses NAT-addcompat's strict successor inequality at `n = 0` together with the additive identity.

**Issue**: T0's description of NAT-closure is *closure* — ℕ closed under `+` and successor — not the algebraic law that `0` is a left identity for `+`. T0's description of NAT-addcompat is *order compatibility* (m ≤ n ⟹ m+p ≤ n+p and/or p+m ≤ p+n), not the distinct fact `n < n+1`. These attributions load two axioms with content T0's exhaustiveness claim says is absent. A reviser reading T0 as authoritative would strengthen NAT-closure to mere closure or NAT-addcompat to mere order compatibility and silently break TumblerAdd and ActionPoint. Because T0 explicitly asserts exhaustiveness and also explicitly excludes commutativity (in TumblerAdd's `aₖ + wₖ > wₖ` route argument), the readership is invited to scrutinise the list precisely — and the list, read at face value, does not license these uses.

**What needs resolving**: Either (a) extend T0's enumeration of NAT-closure and NAT-addcompat to state explicitly that they include the additive identity `0 + n = n` and the strict successor inequality `n < n+1` respectively (and update the PascalCase canonical names / their formal-contract scopes accordingly), or (b) introduce dedicated NAT-* axioms for these two facts (e.g., `NAT-addident`, `NAT-successor`) and re-route the TumblerAdd / ActionPoint citations through them. Either way, T0's exhaustiveness claim must line up with the set of facts downstream proofs actually consume.

---

### T3 in TA-Pos's Depends is only load-bearing for prose, not for the formal postcondition

**Foundation**: T3 (CanonicalRepresentation), cited by TA-Pos as a dependency with the rationale that T3's identity criterion discriminates `[0], [0,0], [0,0,0], …` as distinct elements of T.

**ASN**: TA-Pos's Depends entry for T3 reads: "the preamble's claim that `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T, from which the observation that there are infinitely many all-zero tumblers follows (and hence that the postcondition's universal quantification over zero tumblers `z ∈ T` of arbitrary length is substantive rather than collapsing to a single representative), invokes T3's biconditional…". The formal Postcondition is `(A t ∈ T, z ∈ T : Pos(t) ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) :: z < t)`. The proof uses T0, T1 (cases i and ii), NAT-wellorder, NAT-zero, NAT-order, NAT-discrete. It does not invoke T3.

**Issue**: A Depends entry is a claim that the listed property is load-bearing for the postcondition or its proof. T3 here supports only a prose observation ("there are infinitely many zero tumblers"); whether zero tumblers are distinct or collapse to one representative does not affect the truth of a universal quantifier — if two z's coincided as elements of T, the claim `z < t` would still need to hold, and the proof as written would still discharge it. A downstream tool trimming the Depends DAG to what truly licenses each postcondition will (correctly) drop T3 from TA-Pos; conversely, a reviser weakening T3 will (incorrectly) flag TA-Pos as broken. The discrepancy between "what the proof uses" and "what Depends lists" is exactly the kind of connective-tissue error cross-cutting review is meant to catch.

**What needs resolving**: Either remove T3 from TA-Pos's Depends (moving the distinctness observation to prose commentary outside the formal contract), or strengthen the postcondition/proof so that T3's identity criterion is genuinely consumed (for instance, a corollary explicitly using distinct zero tumblers as witnesses). The *Depends* clause should be exactly the set of properties without which the formal contract fails.
