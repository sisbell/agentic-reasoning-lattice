# Review of ASN-0042

## REVISE

### Issue 1: Inconsistent count of structural axioms

**ASN-0042, *State Axioms* introduction**: "The ownership model rests on seven structural axioms (O12, O13, O14, O15, O5, O16, O18) together with the primitive allocation relation `allocated_by_Σ`..."

**Problem**: The Properties Introduced table marks O1a and O1b additionally as "axiom" — yielding nine, not seven. Worse, the Delegation section establishes O1a/O1b as *invariants preserved* by induction: the base case is O14 (clauses 3, 4, 5), the inductive step uses O15 conditions (iv) and (v). If O1a/O1b are truly axioms, the inductive preservation arguments are redundant; if they are invariants, the table mislabels them.

**Required**: Either (a) classify O1a/O1b as derived properties (analogous to FiniteRegistry, NestingByDelegation, O17, PrefixBaptismCoupling), revising the intro to "seven structural axioms" → "seven transition-discipline axioms plus two pfx structural constraints (O1a, O1b)"; or (b) explicitly justify why O1a/O1b are axioms despite being inductively derivable (e.g., framing them as constraints on the primitive `pfx` function).

### Issue 2: ω(a) definition omits state subscript

**ASN-0042, ω(a) (EffectiveOwner) definition**: "`ω(a) = π ≡ pfx(π) ≼ a ∧ (A π' ∈ Π : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`"

**Problem**: The definition quantifies over bare `Π`, but `Π` is state-relativized (`Π_Σ`). The "Notation (state-relativization of ω and Π)" paragraph acknowledges this informally, but the formal definition should be self-contained. Without explicit `Π_Σ`, the definition is implicitly state-dependent in a way that requires external context to disambiguate — for proofs (O3, O8, OwnershipDomainPermanence) that compare `ω_{Σ'}(a)` to `ω_Σ(a)`, the bare quantifier is load-bearing in a way the formal statement doesn't disclose.

**Required**: Write the definition as `ω_Σ(a) = π ≡ pfx(π) ≼ a ∧ (A π' ∈ Π_Σ : π' ≠ π ∧ pfx(π') ≼ a : #pfx(π) > #pfx(π'))`, and clarify the domain restriction `ω_Σ : Σ.B → Π_Σ` formally rather than only in the notation paragraph.

### Issue 3: O8 proof relies tacitly on trajectory including the witnessed delegation

**ASN-0042, O8 proof, *The delegate persists with an unchanged prefix***: "The remaining delegation case must be the transition that witnesses `delegated_{Σ_d}(π, π')` — namely `Σ_d → Σ_d^{post}`."

**Problem**: This step conflates two facts: (a) `delegated_{Σ_d}(π, π')` witnesses an actual transition `Σ_d → Σ_d^{post}` (historical reading), and (b) the trajectory `Σ_d →⁺ Σ'` includes this specific transition. The "double reading" of `delegated_Σ` (historical vs. structural) explicitly permits both interpretations, but the proof needs the historical one to conclude that the trajectory's introducing transition for `π'` *coincides* with `Σ_d → Σ_d^{post}`. The argument from O15 uniqueness and O12 monotonicity establishes that `π'` has a unique introduction event, but to identify that event with `Σ_d → Σ_d^{post}` requires the historical reading.

**Required**: Make the historical reading explicit in the hypothesis structure of O8 — e.g., "`delegated_{Σ_d}(π, π')` is the historical witness of the transition `Σ_d → Σ_d^{post}` that introduced `π'`" — or argue explicitly that the trajectory's introducing transition must coincide with the witnessed one (rather than just being "some delegation transition").

### Issue 4: Covering-chain lemma not in Properties Introduced

**ASN-0042, *Ownership Domains* section**: "**Covering-chain lemma (PrefixesOfCommonAddressAreComparable).** Any two tumbler prefixes of a common address are `≼`-comparable..."

**Problem**: The lemma is named, stated, and proved inline, then cited by O2 (Step 2), O7(a), OwnershipDomainPermanence (Step 3), NestingByDelegation, DelegatorAllocatesPrefix, and O10 (non-coverage). For such a load-bearing named result, omission from the Properties Introduced table makes the dependency graph incomplete and increases the burden on readers tracking what's been established.

**Required**: Add the covering-chain lemma to the Properties Introduced table with its derivation (`from Prefix, T3`) and the multiple consumer properties cited.

### Issue 5: O3's "no spontaneous activation" hypothesis structure

**ASN-0042, O3 proof, derivation of `π' ∈ Π_{Σ'} ∖ Π_Σ`**: "The chain `#pfx(π') > #pfx(ω_Σ(a)) ≥ #pfx(π)` holds: the second inequality follows because `π ∈ Π_Σ` covers `a`..."

**Problem**: This appears in the proof of OwnershipDomainPermanence, not O3 itself. In O3's body, the case-split on `#pfx(π') ≤ #pfx(ω_Σ(a))` is dispatched by O1b in one sentence ("ties cannot occur — by O1b... and hence be equal, contradicting distinctness"). The argument is correct but compressed: it relies on the fact that two prefixes of the same length both covering `a` must coincide componentwise via the prefix relation's definition. For a property as foundational as O3, this step warrants the explicit two-line argument it gets in OwnershipDomainPermanence Step 2 rather than being elided to a parenthetical.

**Required**: In O3's body, expand the rejection of `#pfx(π') = #pfx(ω_Σ(a))` to explicitly show: two prefixes of equal length both covering `a` agree componentwise with `a` on their shared length and hence with each other, so are equal as tumblers, then O1b forces principal identity.

### Issue 6: O7(c) chain construction skips the k=0→k=1 boundary

**ASN-0042, O7(c) proof, recursive chain construction**: "Each `pfx(π_k)` has `zeros(pfx(π_k)) = 1` (account level, satisfying (iv)) and satisfies T4..."

**Problem**: The construction defines `pfx(π_0) = [1]` with `zeros = 0`, then `pfx(π_k) = [1, 0, 1, …, 1]` with `zeros = 1` for `k ≥ 1`. The blanket claim "Each `pfx(π_k)` has `zeros = 1`" is false at `k = 0`. More importantly, the transition `π_0 → π_1` is structurally different from subsequent transitions: it opens the user field (adding both the zero separator and the first user-field component), whereas `π_k → π_{k+1}` for `k ≥ 1` only appends a user-field component. The verification that condition (i)'s strict extension holds at the boundary case is implicit.

**Required**: Either restrict the chain construction to `k ≥ 1` (with `π_1` as the base of the chain, a separately-verified bootstrap principal), or explicitly verify the boundary step `pfx(π_0) = [1] ≺ pfx(π_1) = [1, 0, 1]` separately from the inductive extensions.

## OUT_OF_SCOPE

None. The ASN keeps strictly within ownership-model territory; cross-cutting topics (content storage, links, baptism mechanism) are correctly delegated to ASN-0040 and downstream ASNs, and the *Scope* section is properly observed.

VERDICT: REVISE
