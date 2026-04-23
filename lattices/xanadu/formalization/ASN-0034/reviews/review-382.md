# Regional Review — ASN-0034/TA-Pos (cycle 1)

*2026-04-22 22:15*

### Closure clause is derivable from the `+` signature that precedes it
**Class**: REVISE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure formal contract: "`+ : ℕ × ℕ → ℕ` (`+` is a binary operation on ℕ); `1 ∈ ℕ` (one is a natural number); `(A m, n ∈ ℕ :: m + n ∈ ℕ)` (addition closure, restating the codomain commitment for direct citation)". Prose: "the closure clause `(A m, n ∈ ℕ :: m + n ∈ ℕ)` that follows restates that codomain commitment as an explicit universal, kept for direct citation by dependent axioms."
**Issue**: The signature clause `+ : ℕ × ℕ → ℕ` already states that for every `(m, n) ∈ ℕ × ℕ` the value `m + n` lies in ℕ — that is exactly what a codomain assertion means. The third clause `(A m, n ∈ ℕ :: m + n ∈ ℕ)` is therefore a logical consequence of the first, and the prose admits this openly ("restates that codomain commitment as an explicit universal"). This is the same defect the cycle-3 finding flagged for successor-closure: listing a derivable clause as a separate axiom misleads the reader into thinking it carries independent content. "Kept for direct citation" is not a mathematical justification for axiomatizing a derivable fact; downstream citations can cite the signature directly, or a lemma can be stated.
**What needs resolving**: Either drop the closure clause from the Axiom slot (the signature already suffices), or promote it to a stated consequence/lemma separate from the Axiom slot. The Axiom slot should contain only clauses that are not logical consequences of other clauses in the same slot.

### TA-Pos Definition slot leaves `t` unbound
**Class**: REVISE
**Foundation**: TA-Pos (PositiveTumbler)
**ASN**: TA-Pos formal contract: "*Definition:* `Pos(t)` iff `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`; `Zero(t)` iff `(A i ∈ ℕ : 1 ≤ i ≤ #t : tᵢ = 0)`; **Z** = {t ∈ T : Zero(t)}." Complementarity bullet by contrast: "`(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))`".
**Issue**: The Definition bullet writes `Pos(t)` and `Zero(t)` with a free `t`, never quantified or typed, while the sibling Complementarity bullet in the same formal contract binds `t ∈ T` explicitly. The prose above the contract does say "A tumbler `t ∈ T`", but the formal-contract slot is precisely where such implicit bindings should be eliminated so a mechanical reader can extract the claim without consulting surrounding prose. The cycle-6 finding already required the bound `i` to be typed `i ∈ ℕ` inside these same two clauses for the same reason; the `t` variable received no parallel treatment.
**What needs resolving**: Bind `t ∈ T` explicitly in the Definition bullet (e.g., `(A t ∈ T :: Pos(t) ⟺ (E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0)))` and likewise for `Zero`), so the formal contract contains no free variables.

### NAT-closure prose explains absences rather than stating content
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure prose: "The operation is posited directly on ℕ rather than derived from an earlier axiom — the same register NAT-order uses to posit `<` (with its axiom opening `< ⊆ ℕ × ℕ` before the strict-total-order clauses)." … "Successor closure `n + 1 ∈ ℕ` is not axiomatized separately: it is the instance of addition closure at `(m, n) := (n, 1)`, with `1 ∈ ℕ` from this very axiom supplying the right operand." … "The mirrored clause `n + 0 = n` is not axiomatized here; commutativity of `+` is not enumerated, so the right-identity form is not derivable from this axiom alone."
**Issue**: Three successive paragraphs explain *why* chosen clauses are present and *why* omitted clauses are absent — cross-referencing NAT-order's register, explaining that successor-closure is derivable, explaining that right-identity is not derivable. These are meta-justifications responding to prior findings rather than statements of the axiom's content. The "successor closure is not axiomatized separately" sentence in particular reads like a prior finding's remediation left in place as narration rather than silently resolved. A precise reader working the axiom has to skip past this apparatus to reach the claim.
**What needs resolving**: (OBSERVE only — logged for register).

VERDICT: REVISE
