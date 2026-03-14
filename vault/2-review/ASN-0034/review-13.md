# Review of ASN-0034

## REVISE

### Issue 1: Off-by-one in TA5/T4 preservation analysis
**ASN-0034, TA5 preserves T4**: "the address format has exactly four fields with three separators, so at most two new separators can be introduced from a node address"
**Problem**: Starting from a node address (zeros = 0), three `inc(·, 2)` operations are permitted: 0→1 (node→user), 1→2 (user→document), 2→3 (document→element). Each satisfies the stated constraint `zeros(t) ≤ 2`. The result is three new separators, not two.
**Required**: Change "at most two" to "at most three," or clarify what "from a node address" means if a different reading was intended. No reading of the sentence produces "two" as the correct count.

### Issue 2: TA7a stated only for single-component ordinals
**ASN-0034, TA7a**: "a position in subspace S with identifier N and ordinal x is represented as the single-component tumbler [x] for arithmetic purposes"
**Problem**: Element fields can have sub-structure (the ASN's own T4 defines the element field as `E₁. ... .Eδ` with `δ ≥ 1`). A span from `[1, 3, 2]` to `[1, 5, 7]` requires a multi-component displacement `[0, 2, 7]` acting at position 2 within the ordinal. The subspace closure holds in this case — the constructive definition copies position 1 (ordinal prefix) unchanged whenever the action point is at position 2 or later — but the formal statement of TA7a restricts to `[x] ⊕ [n]` and `[x] ⊖ [n]`, covering only single-component ordinals and single-component displacements.
**Required**: Either generalize TA7a to state that for any ordinal `o = [o₁, ..., oₘ]` and displacement `w` whose action point `k ≥ 1`, the result preserves all ordinal components before `k` (trivially, by the constructive definition); or justify why single-component ordinals are sufficient for all element-level shift arithmetic, with an explicit statement that deeper element structure is addressed elsewhere.

### Issue 3: Result length of ⊕ used without statement
**ASN-0034, Constructive definition of ⊕**: "The result `a ⊕ w = [r₁, ..., rₚ]` has length `p = max(k - 1, 0) + (n - k + 1)`"
**Problem**: The formula simplifies to `p = n = #w` for all `k ≥ 1`, meaning the result of tumbler addition always has the same length as the displacement. This fact is load-bearing: the reverse inverse proof asserts "The equal-length condition holds: `#a = k = #(y ⊕ w)`" without justification — it relies on knowing `#(y ⊕ w) = #w = k`. The TA4 verification similarly depends on the result having length `#w`. The formula is present in the constructive definition but is never simplified or stated as a property.
**Required**: State as a remark or lemma that `#(a ⊕ w) = #w` (for `w > 0` with action point `k ≤ #a`), and cite it where the reverse inverse proof and TA4 verification rely on it.

### Issue 4: T9 status inconsistency
**ASN-0034, Properties Introduced table**: "T9 | ... | introduced"
**Problem**: The text labels T9 as `[lemma]` and derives it from T10a and TA5(a): "Since `inc` produces a strictly greater tumbler at each step (TA5(a)), it follows that within each allocator's sequential stream, new addresses are strictly monotonically increasing." But the Properties Introduced table lists T9's status as "introduced," conflicting with its derived nature.
**Required**: Change T9's status in the Properties Introduced table from "introduced" to "lemma" or "derived from T10a + TA5(a)," consistent with the body text.

## OUT_OF_SCOPE

### Topic 1: T4 preservation under ⊕ and ⊖
When shifting span endpoints, the result must remain a valid address. Whether ⊕ preserves T4's constraints (positive components, ≤ 3 zeros, no adjacent zeros) depends on the specific operands and action point, and would require a separate analysis of which displacements produce valid addresses from valid addresses.
**Why out of scope**: This is an interaction property between the algebra and the address format — a constraint on span operations, not a property of the tumbler algebra itself.

### Topic 2: Formal definition of "allocated"
T8 uses "allocated" as a predicate over system history ("If tumbler `a ∈ T` has been allocated at any point in the system's history") without defining what constitutes an allocation event. The concept depends on system state — which addresses have been produced by `inc` operations and accepted by the system.
**Why out of scope**: "Allocated" is a system-level predicate, not an algebraic one. Its formal definition belongs in a system-state ASN.

### Topic 3: Span action-point semantic constraint
T12 requires `k ≤ #s` for well-formedness, but a span `(a₂, [3])` satisfies this (k=1 ≤ 8) yet produces a node-level address `[4]` — semantically nonsensical. The constraint that the action point of the span length must match the hierarchical level of the start address is noted in the worked example but not formalized.
**Why out of scope**: Semantic span constraints belong in a span-operations ASN, not the algebra.

VERDICT: REVISE
