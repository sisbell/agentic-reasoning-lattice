# Review of ASN-0001

## REVISE

### Issue 1: T4 field non-emptiness is implicit and never verified against TA5

**ASN-0001, Hierarchical structure**: "t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ where each Nᵢ, Uⱼ, Dₖ, Eₗ > 0"

**Problem**: The constraint that every field component is strictly positive is embedded in the structural form but never stated as a named property. This constraint is load-bearing — it is what makes the zero-count-to-level correspondence injective (zeros appear *only* as separators). Without it, a tumbler like `[1, 0, 0, 3]` has two zeros but ambiguous parse: is it a user address with user field `[0, 3]` (violating positivity) or something else? More critically, the ASN never verifies that TA5 preserves this constraint. The verification is straightforward — `inc(t, 0)` increments a positive component (keeping it positive), and `inc(t, k>0)` sets the final component to 1 — but "straightforward" is not "shown."

**Required**: (a) State the positive-component constraint as a named property or explicit conjunct of T4: every component of every field in a valid I-space address is strictly positive. (b) Verify that TA5 preserves this constraint for both `k = 0` and `k > 0`, citing the specific parts of TA5(c) and TA5(d) that guarantee it.

### Issue 2: Global Uniqueness Case 4 mischaracterizes the child allocator

**ASN-0001, Global uniqueness proof, Case 4**: "The parent allocator produces addresses by inc(t, 0) at the document level, yielding document fields of some length γ. The child allocator produces addresses by inc(t', k) with k > 0 within the parent's partition, yielding document fields of length γ' > γ (since child allocation extends the tumbler by TA5(d))."

**Problem**: The child allocator does not produce every address by `inc(t', k)` with `k > 0`. It uses a *single* deep increment to establish its prefix (e.g., `inc(1.0.3.0.2, 1)` to create version space `1.0.3.0.2.1`), then produces subsequent addresses by `inc(·, 0)` — shallow sibling increments within that prefix. The proof's conclusion is correct (child outputs are longer because TA5(c) preserves the length established by the initial deep increment), but the stated mechanism is wrong. A reader following the proof literally would conclude that every child allocation extends the tumbler by `k` positions, which contradicts TA5(c).

**Required**: Restate: the child allocator's *prefix* was established by a single `inc(parent, k)` with `k > 0`, giving it length `#parent + k`. Subsequent allocations within the child's stream use `inc(·, 0)`, which preserves this length by TA5(c). Parent outputs have length `#parent`; child outputs have length `#parent + k > #parent`. Different lengths, so T3 gives `a ≠ b`.

### Issue 3: Worked example does not verify subspace confinement (TA7)

**ASN-0001, Worked example**: "We instantiate the algebra on a concrete scenario."

**Problem**: The example has five text-subspace characters but no link-subspace positions. It verifies T1, T4, T5, T6, T9, TA1, TA4, and T8/T11 — but TA7a (subspace closure) and TA7b (subspace frame) are among the hardest properties to get right, and the example is silent on them. The review instructions are explicit: "the ASN should verify its key postconditions against at least one specific scenario." TA7 is a key postcondition.

**Required**: Add at least one link address to the example (e.g., `ℓ₁ = 1.0.3.0.2.0.2.1` in subspace 2) and verify that the INSERT of width `[2]` in text subspace 1 leaves `ℓ₁`'s V-space position unchanged (TA7b), and that `a₃ ⊕ [2]` remains in subspace 1 (TA7a).

### Issue 4: Partition Monotonicity proof — first sibling produced by deep increment, not shallow

**ASN-0001, Partition monotonicity proof**: "sub-partition prefixes are produced by a single parent allocator using inc(t, 0) (sibling allocation within its sequential stream). By TA5(c), inc(t, 0) preserves the length of t: #inc(t, 0) = #t."

**Problem**: The *first* sub-partition prefix is produced by `inc(parent, k)` with `k > 0` — a deep increment, not a sibling increment. The ASN's own description of TA5 says: "Creating a new account under a server uses a deep increment (k > 0) to produce the first child. Allocating successive documents under an account uses a shallow increment (k = 0) to produce the next sibling." The proof claims all sibling prefixes come from `inc(·, 0)`, contradicting this. The equal-length conclusion survives — the first child has length `#parent + k`, and `inc(·, 0)` preserves that length for all subsequent siblings — but the proof as stated has a false premise.

**Required**: Acknowledge that the first sub-partition prefix `t₀` is produced by `inc(parent, k)` with `k > 0`, giving `#t₀ = #parent + k`. Then note that subsequent prefixes `t₁ = inc(t₀, 0), t₂ = inc(t₁, 0), ...` all have length `#t₀` by TA5(c). The equal-length property holds for all siblings; the non-nesting and disjointness conclusions follow unchanged.

### Issue 5: TA5 domain and subspace-boundary interaction unstated

**ASN-0001, TA5 (Hierarchical increment)**: "For tumbler t ∈ T and level k ≥ 0, there exists an operation inc(t, k) producing tumbler t'..."

**Problem**: TA5 is stated for *any* tumbler `t ∈ T` and *any* `k ≥ 0`, with no domain restriction. For valid I-space addresses, `sig(t)` always falls on a field component (the last nonzero position is within some field, since field components are positive and trailing positions within a field are positive). But TA5 as written also applies to non-address tumblers, and the ASN never states the invariant that makes `sig(t)` safe for addresses. Specifically: for a valid element-level address, `sig(t) = #t` (the last component `Eδ > 0`), so `inc(t, 0)` increments within the element field, safely. But this is a *consequence* of T4's positive-component constraint, not stated or derived.

**Required**: State explicitly: for valid I-space addresses, `sig(t)` falls within the last populated field (because that field's components are positive by T4, so the last nonzero component is in the last field). Therefore `inc(t, 0)` modifies only the last field, preserving the hierarchical structure. This closes the gap between TA5 (arbitrary tumblers) and T4 (structured addresses).

### Issue 6: Global Uniqueness Case 4 — parenthetical claim about zero separators

**ASN-0001, Global uniqueness proof, Case 4**: "each child address extends the parent's document identifier by at least one zero separator and one new component"

**Problem**: For `k = 1`, TA5(d) says `#t' = #t + 1`, with `k - 1 = 0` intermediate zero positions and one final component set to 1. There are *no* zero separators for `k = 1` — just one new component. The parenthetical claim "at least one zero separator and one new component" is false for the `k = 1` case. The mathematical argument (`#t' > #t` for any `k > 0`) is correct regardless, but the descriptive claim is wrong.

**Required**: Replace the parenthetical with an accurate description: "each child address extends the parent's document identifier by `k` positions (TA5(d)), so `#t' = #t + k > #t`."

## OUT_OF_SCOPE

### Topic 1: Concrete semantics of ⊕ for multi-component operands

The ASN axiomatizes `⊕` and `⊖` via TA0–TA4 without defining what they compute for multi-component inputs. The worked example uses only single-component V-space positions. For multi-component operands, the result is constrained by the axioms but not determined by them. This is a valid abstract-specification choice, but a future ASN defining the POOM or enfilade operations will need to instantiate `⊕` concretely, or prove that the axioms suffice.

**Why defer**: The current ASN establishes the algebraic contract. Concrete instantiation is implementation-level, or belongs in an ASN on V-space operations.

### Topic 2: Allocation protocol — which `k` values are used at each level

The ASN describes `inc(t, 0)` for siblings and `inc(t, k>0)` for children but doesn't specify the exact protocol: who calls `inc` with what `k`, in what sequence, at each level of the hierarchy. The proofs reference the protocol informally ("creating a new account under a server uses a deep increment") but don't formalize it.

**Why defer**: The allocation protocol is an operation-level concern. This ASN establishes the algebraic properties that any correct protocol must satisfy.

### Topic 3: Crash recovery and allocation counter durability

Listed as an open question. A correct answer requires defining the system's persistence model, which is outside the scope of the tumbler algebra.

**Why defer**: This is a system-level concern, not an algebraic property.
