# Review of ASN-0034

## REVISE

### Issue 1: `divergence(a, b)` used without formal definition

**ASN-0034, TA1-strict**: "`a ⊕ w < b ⊕ w`, where `k` is the action point of `w` and `divergence(a, b)` is the first position at which `a` and `b` differ"

**Problem**: `divergence(a, b)` appears as a formal condition in TA1-strict and TA3-strict, but is never given a formal definition — particularly for the prefix case. When `a` is a proper prefix of `b`, there is no position `k ≤ min(#a, #b)` where the components differ; the divergence is that `a` runs out of components. The TA1 verification implicitly handles this (Case 1 erases the prefix divergence, giving equality), but TA1-strict's statement is ambiguous: does `divergence([1,1], [1,1,5])` equal 3 (zero-padded interpretation), `∞` (no shared-position divergence), or undefined? The answer determines whether TA1-strict's condition `k ≥ divergence(a,b)` is satisfiable for prefix-related pairs.

**Required**: Formal definition of `divergence(a, b)` that covers both T1 case (i) (component divergence at a shared position) and T1 case (ii) (prefix relationship). State explicitly what TA1-strict and TA3-strict say (or don't say) about the prefix case.

### Issue 2: T0 prose claims two dimensions but the formal statement captures one

**ASN-0034, T0**: "T0 is required doubly: each component is unbounded (unlimited siblings at any level) AND the number of components is unbounded (unlimited nesting depth). Together these make the address space infinite in two dimensions"

**Problem**: T0's formal statement `(A t ∈ T, i : 1 ≤ i ≤ #t : (A M ∈ ℕ :: (E t' ∈ T :: t' agrees with t except t'.dᵢ > M)))` captures component-value unboundedness only. It quantifies over positions within a given tumbler and shows values at those positions are unbounded. It says nothing about the existence of tumblers with more components. Length unboundedness — that for every `n` there exists a tumbler of length ≥ `n` — is a consequence of T's definition as the set of all finite sequences over ℕ, not of T0. The prose attributing both dimensions to T0 is factually incorrect: T0 contributes one dimension, T's carrier-set definition contributes the other.

**Required**: Either (a) add a formal statement for length unboundedness (e.g., `(A n ∈ ℕ : n ≥ 1 : (E t ∈ T :: #t ≥ n))`) as a separate property or as T0(b), or (b) correct the prose to state that component unboundedness is T0 and length unboundedness is definitional from the carrier set. The minimality table should reflect whichever choice is made.

### Issue 3: TA3 verification, Case 0 (prefix subcase) under-argued

**ASN-0034, Verification of TA3, Case 0**: "both subtractions produce the same result on positions 1, ..., max(#a, #w) (since a and b agree on these positions)"

**Problem**: This assertion skips the component-level argument. The subtraction algorithm zeroes positions before the divergence, subtracts at the divergence, and copies the minuend's tail after. For the two subtractions `a ⊖ w` and `b ⊖ w` to agree on positions 1 through `max(#a, #w)`, you need: (i) the divergence points `d_a` and `d_b` are identical within the shared range, (ii) at the divergence, `a_d - w_d = b_d - w_d` (which holds since `a_d = b_d` for `d ≤ #a`), (iii) the tails copied from the respective minuends agree (which holds since `a_i = b_i` for `i ≤ #a`). None of these steps are shown. The subsequent claim that "a ⊖ w is shorter than b ⊖ w and is a prefix of it" also needs explicit justification: the longer result's extra positions `max(#a,#w)+1, ..., max(#b,#w)` come from `b`'s components beyond `#a`, which are copied from the minuend in the tail-copy phase.

**Required**: Show that the divergence points coincide within the shared range, that the formula produces identical values at shared positions, and that the longer result's extra positions come from the longer minuend's tail. The argument is straightforward but must be explicit — this is a novel subtraction algorithm, not standard arithmetic.

### Issue 4: Global uniqueness theorem, Case 4 — scope narrower than needed

**ASN-0034, Theorem (Global uniqueness), Case 4**: "This arises when a parent and child allocator both produce addresses at the same hierarchical level."

**Problem**: The case covers "different allocators with nesting prefixes and the same zero count," which includes all ancestor-descendant pairs, not just parent-child. The length-separation argument (`γ₁ + k' > γ₁`) applies at each nesting level: a grandchild's outputs have length `γ₁ + k₁' + k₂'`, still strictly greater than the grandparent's `γ₁`. But the proof text only argues one level of nesting ("the child's outputs are strictly longer than the parent's"). A reader could reasonably ask: what about an allocator three levels deep whose accumulated length extension happens to equal a cousin allocator's extension at a different branch? The answer is that cousins have non-nesting prefixes (Case 2), and all ancestor-descendant pairs have strictly increasing lengths — but this should be stated.

**Required**: Note that Case 4 covers arbitrary nesting depth. A one-sentence addition suffices: "The length separation is additive across nesting levels — each `inc(·, k')` with `k' ≥ 1` adds at least one component, so a descendant `d` nesting levels below has output length at least `γ₁ + d > γ₁`. Non-ancestor allocators at different branches have non-nesting prefixes and are handled by Case 2."

### Issue 5: Worked example does not verify TA1 or TA4 against the concrete scenario

**ASN-0034, Worked example section**

**Problem**: The worked example verifies T4, T1, T5, T6, T7, T9, TA5, T12, and TA7a — good coverage. But the two most delicate arithmetic properties are absent:

(a) **TA1 (order preservation under addition)**: The example has `a₂ < a₃` and displacement `ℓ = [0,0,0,0,0,0,0,3]`. It should check `a₂ ⊕ ℓ ≤ a₃ ⊕ ℓ` — compute both results and verify the order holds. Since the action point `k = 8 = divergence(a₂, a₃)`, TA1-strict predicts strict inequality. Showing this concretely validates both the weak and strict claims.

(b) **TA4 (partial inverse)**: The ordinal-only check `[5] ⊖ [2] = [3]` is trivially a single-component case. The interesting case is full addresses. The example should compute `(a₂ ⊕ ℓ) ⊖ ℓ` and show it does NOT equal `a₂` — then verify TA4's preconditions: `k = 8 = #a₂`, `#ℓ = 8 = k`, but `a₂` has `a₂₁ = 1 ≠ 0`, violating the zero-prefix condition. This concretely demonstrates the limitation and makes the restrictive preconditions tangible.

**Required**: Add both verifications to the worked example. For TA1, show two additions and compare results. For TA4, show the full-address round-trip, identify which precondition fails, and contrast with the ordinal-only case where all preconditions hold.

## OUT_OF_SCOPE

### Topic 1: Span operations (intersection, union, containment testing)

**Why out of scope**: The ASN defines what a span IS (T12) but not operations ON spans. How to test whether two spans overlap, compute their intersection, or merge adjacent spans is new territory requiring its own treatment — likely involving conditions on action-point alignment and the many-to-one property of addition.

### Topic 2: Shift composition conditions

**Why out of scope**: The ASN explicitly identifies this as an open question: "Under what conditions can shift composition hold — when does `(a ⊕ w₁) ⊕ w₂ = a ⊕ (w₁ ⊕ w₂)`?" This is not an error in the current ASN — the non-associativity is correctly stated, and the conditions for limited associativity are genuine future work.

### Topic 3: Zero-tumbler edge cases in span arithmetic

**Why out of scope**: The ASN identifies this as an open question: "What must the system guarantee about the zero tumbler's interaction with span arithmetic?" Span endpoints that are zero sentinels require convention (unbounded spans, uninitialized markers) that goes beyond the algebra defined here.

VERDICT: REVISE
