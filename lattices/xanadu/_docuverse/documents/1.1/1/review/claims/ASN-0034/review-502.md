# Regional Review — ASN-0034/T4a (cycle 1)

*2026-04-24 07:21*

### T4a uses "Postconditions" slot where "Consequence" is expected
**Class**: REVISE
**Foundation**: T4a (SyntacticEquivalence)
**ASN**: T4a Formal Contract: "*Postconditions:* The three positional conditions (i), (ii), (iii) hold if and only if every field segment of `t` is non-empty."
**Issue**: The biconditional is the derived theorem of T4a, proved in the prose. Every other claim in this ASN (T4, NAT-sub, NAT-addbound, NAT-zero, NAT-order) files proved statements under *Consequence:*, reserving *Axiom:* for posited content. T4a instead exposes its main result as *Postconditions:*, a slot not used anywhere else in the ASN. A downstream consumer reading the contract cannot tell whether the equivalence is posited (like T4's field-segment axiom) or derived (like T4's exhaustion consequence). The epistemic status of the claim's headline result should not be inferable only by reading the prose.
**What needs resolving**: Restate the equivalence in a slot whose semantics is consistent with the rest of the ASN — either *Consequence:* (with the existing prose as the derivation) or split it into two implications under whichever slot(s) fit the ASN's convention. "Postconditions" should not appear unless it is adopted uniformly and its semantics documented.

### T4 Axiom: variable `k` overloaded as both zero-count and D-field position subscript
**Class**: OBSERVE
**Foundation**: T4 (HierarchicalParsing)
**ASN**: T4 Formal Contract, *Axiom:* — "for each `k ∈ ℕ` with `0 ≤ k ≤ 3` at which `zeros(t) = k`, the form is — … `k = 3`: `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ`. In every case, `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position present."
**Issue**: The variable `k` is bound in the outer schematic quantifier as the zero-count, then reused inside `0 < Dₖ` as a position subscript ranging over D-field positions `1..γ`. A precise reader must reconstruct from context that the two `k`'s are different bindings. The same overload appears in the earlier Hierarchical-structure prose where `Dₖ` is introduced before `k` is bound, but it re-enters scope inside a clause where `k` is already the zero-count.

### T4a Reverse-interior-segment: range of condition (i) not established at `s_i`
**Class**: OBSERVE
**Foundation**: T4a (SyntacticEquivalence)
**ASN**: T4a Reverse *Interior segments* — "Condition (i) forbids `s_{i+1} = s_i + 1`"
**Issue**: Condition (i) is stated at range `1 ≤ i < #t`, so applying it at renamed index `s_i` (to rule out `t_{s_i} = 0 ∧ t_{s_i+1} = 0`) requires `1 ≤ s_i < #t`. The proof uses this without witnessing `s_i < #t`. The bound follows from condition (iii) (`t_{#t} ≠ 0` forces `s_k ≠ #t`, hence `s_k < #t` by NAT-order) together with strict monotonicity `s_i < s_k` for `i < k`, but the proof elides this step. A one-line derivation inside the Interior case — or an upfront lemma stating `s_k < #t` under (iii) — would make the applicability of condition (i) at `s_i` explicit.

VERDICT: REVISE
