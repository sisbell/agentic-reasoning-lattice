# Review of ASN-0042

## REVISE

### Issue 1: O10 Form B argument locally redefines S(p, d) creating notation conflict

**ASN-0042, O10 non-coverage analysis (Form B)**: "Hence `pfx(π).0.U^{(i)}_1 ∈ Σ.B`, so `U^{(i)}_1 ∈ S(pfx(π), 2) ∩ Σ.B` (where `S(pfx(π), 2)` denotes the set of admissible depth-2 child indices under `pfx(π)`), and therefore `U^{(i)}_1 ≤ hwm_0` by definition of hwm."

**Problem**: ASN-0040 defines `S(p, d)` as a sequence of tumblers (the sibling stream `c₁, c₂, c₃, …`). The proof here locally redefines `S(pfx(π), 2)` as "the set of admissible depth-2 child indices" — a set of natural numbers, not tumblers. The membership statement `U^{(i)}_1 ∈ S(pfx(π), 2) ∩ Σ.B` is then type-incorrect under either reading: `U^{(i)}_1` is a natural number, so it cannot be an element of a tumbler-sequence; and `Σ.B` is a set of tumblers, so its intersection with a set of indices is not well-formed without an embedding.

**Required**: Use consistent notation. Either keep `S(pfx(π), 2)` as ASN-0040 defines it and write `pfx(π).0.U^{(i)}_1 ∈ S(pfx(π), 2) ∩ Σ.B`, or introduce a separate symbol (e.g., `idx(Σ.B, pfx(π), 2)`) for the set of allocated indices and write `U^{(i)}_1 ∈ idx(Σ.B, pfx(π), 2)`. The argument is sound either way; the proof as written is confusing.

### Issue 2: O10's conclusion that π is the unique longest match elides the non-sub-delegate covering-chain argument

**ASN-0042, O10 non-coverage analysis**: "In both `zeros(pfx(π)) = 0` and `zeros(pfx(π)) = 1` cases, no sub-delegate covers `a'`. Hence `π` itself achieves the unique longest matching prefix in `Π_Σ` for `a'`, and `ω_{Σ'}(a') = π`."

**Problem**: The "Hence" jumps from "no sub-delegate covers a'" to "π is the unique longest match in Π_Σ" without addressing the other covering principals in Π_Σ — principals whose prefix is a proper prefix of `pfx(π)` (ancestors-via-delegation, when they exist in Π_Σ) and non-nesting principals. The full argument requires showing: (i) π covers a' (by construction); (ii) sub-delegates of π don't cover a' (Form A/B, proved); (iii) any non-sub-delegate covering principal π_x has #pfx_x < #pfx(π), via the covering-chain lemma applied to pfx_x and pfx(π) as common prefixes of a', followed by O1b to rule out equality. Step (iii) is exactly what O2's proof (Step 2) develops at length, but O10 doesn't cite or restate it.

**Required**: Make the covering-chain argument explicit in the O10 conclusion, or cite O2's Step 2 as the warrant. Without it, the "Hence" hides the load-bearing case analysis.

### Issue 3: O7(c) chain construction text inaccurate for k=0→k=1

**ASN-0042, O7 postcondition (c), chain construction**: "Define `pfx(π_0) = [1]` (zeros = 0, T4 satisfied) and for `k ≥ 1`, `pfx(π_k) = [1, 0, 1, 1, ..., 1]` with `k + 2` total components ... For every k, `pfx(π_k) ≺ pfx(π_{k+1})` (strict extension by one user-field component, satisfying (i))."

**Problem**: For k=0 → k=1, the extension is from `[1]` (length 1) to `[1, 0, 1]` (length 3) — two new components are appended (the zero separator AND the first user-field component), not "one user-field component". The "strict extension by one user-field component" phrasing is accurate only for k ≥ 1 transitions, where the separator already exists in pfx(π_k). The strict-prefix relation still holds for k=0 → k=1, but the prose mischaracterizes the structural shape of that link.

**Required**: Either treat k=0 separately ("for k=0 → k=1, the extension introduces the user-field separator and the first user-field component; for k ≥ 1, the extension adds one user-field component"), or restructure the chain so every link extends by exactly one component (e.g., start at `pfx(π_0) = [1, 0, 1]` and have π_N be a bootstrap node-level principal that delegates to π_0).

### Issue 4: AccountLevelPermanence formal contract postcondition has free π'

**ASN-0042, AccountLevelPermanence Formal Contract**: "Postconditions: `(E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ delegated_Σ(π_d, π'))` where π' ∈ Π_{Σ'} ∖ Π_Σ is the new principal causing the ownership change."

**Problem**: The body of the property correctly states the postcondition with nested existentials: `(E π_d ∈ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ (E π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π')))`. The formal contract slot leaves π' as a free variable with an English gloss, which is a different statement (under the typical reading, π' would have to be supplied as input). The contract and the proved postcondition should match.

**Required**: Update the formal contract to use the nested-existential form, matching the body. Either: `Postconditions: (E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π) ≼ pfx(π_d) ∧ delegated_Σ(π_d, π'))`, or describe π' as quantified rather than free.

## OUT_OF_SCOPE

None. The scope boundary at the end of the ASN appropriately enumerates the deferred topics, and the ASN's content stays within the ownership model.

META: The ASN stays on the ownership predicate, the effective-owner function, delegation, and the structural invariants of state — domain-neutral properties an alternative implementation would also need to satisfy.

VERDICT: REVISE
