# Review of ASN-0045

I've worked through the predicate definitions, the Partition derivation, and the dependency citations. The ASN names four predicates (Node, Account, Document, Element) as T4c corollaries, with one substantive vocabulary decision (user → account) and one derived theorem (Partition).

Walking through the derivation:
- **Binding**: under T4-valid(t), Pₖ(t) ⟺ zeros(t) = k. Correct.
- **At-least-one**: T4c's Exhaustion gives zeros(t) ∈ {0,1,2,3}, hence one Pₖ holds. Correct.
- **At-most-one**: routes through T4c's biconditional `zeros(t) = k ↔ Lₖ(t)` and Pairwise extensional disjointness. The chain Pₖ ⟺ Lₖ combined with ¬(Lᵢ ∧ Lⱼ) yields ¬(Pᵢ ∧ Pⱼ). Correct.

Examples: positive cases hit each level once; counter-examples cover the three field-segment violations and a zeros(t) = 4 case. The load-bearing role of T4-valid(t) in Partition's antecedent is exhibited by the counter-example table.

Boundary cases verified: t = [1] (Node), [1,0,1] (Account), [0] (T4-invalid, all four false), zeros(t) > 3 (T4-invalid, all four false). Predicates are total on T because T4-valid and zeros are total.

Foundation references all resolve to ASN-0034 (T0, T4, T4b, T4c, NAT-zero, NAT-closure). No non-foundation cross-ASN references.

The rename equivalence for Account is derived explicitly, discharging the user → account vocabulary shift. T4b's projection symbol U is explicitly carved out as unchanged, so the rename's scope is bounded.

No hand-waves, no unjustified checkmarks, no skipped cases.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Projection presence correspondence
The predicates align one-to-one with T4b's *Presence pattern* postcondition (e.g., `Account(t) ⟺ T4-valid(t) ∧ t ∈ dom(U) ∧ t ∉ dom(D)`). The ASN doesn't surface this bridge.
**Why out of scope**: T4b already exhausts the presence pattern. Tying Node/Account/Document/Element to projection domains is a downstream connection (likely needed wherever a consumer wants to switch between "predicate classification" and "projection extraction"), not a gap in this ASN's stated naming-and-Partition scope.

### Topic 2: Length lower bounds per level
`Account(t) ⟹ #t ≥ 3`, `Document(t) ⟹ #t ≥ 5`, `Element(t) ⟹ #t ≥ 7` follow from T4a's segment non-emptiness conclusion. Not derived here.
**Why out of scope**: These are downstream T4a corollaries; introducing them would expand the ASN beyond level-predicate definitions into level-shape arithmetic.

VERDICT: CONVERGED
