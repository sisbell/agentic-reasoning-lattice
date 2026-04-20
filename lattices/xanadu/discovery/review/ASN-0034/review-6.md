# Review of ASN-0034

## REVISE

### Issue 1: TA5 preservation of T4 — structural constraint omitted

**ASN-0034, TA5 section**: "TA5 preserves T4 when `zeros(t) + k - 1 ≤ 3`. ... When `t` is a node address (`zeros(t) = 0`), `k ≤ 4`."

**Problem**: The analysis checks only the zero-count bound but T4 also requires no adjacent zeros (equivalently, every present field has at least one component). For `k ≥ 3`, the appended sequence `[0, ..., 0, 1]` contains adjacent zeros, creating empty fields that violate T4 regardless of the total zero count.

Concrete counterexample: `inc([1], 3)` produces `[1, 0, 0, 1]`. Zero count is 2 (≤ 3), satisfying the stated bound. But positions 2 and 3 are adjacent zeros. Parsing: node field `[1]`, separator, **empty user field**, separator, document field `[1]`. The empty user field violates T4's non-empty-field constraint. The claim "k ≤ 4 for node addresses" is wrong.

**Required**: The preservation condition must include the structural constraint: T4 is preserved by `inc(t, k)` when `k ≤ 2` **and** `zeros(t) + k - 1 ≤ 3`. The bound `k ≤ 2` ensures each increment appends at most one separator, which is flanked by the existing last-field component (positive, by T4) and the new child component (1). For `k = 1`: zero new separators, T4 trivially preserved. For `k = 2`: one new separator between two positive components, no adjacent zeros. For `k ≥ 3`: adjacent zeros, T4 violated. The effective constraints are: `k = 0` (always valid), `k = 1` (always valid), `k = 2` (when `zeros(t) ≤ 2`). The note "the hierarchy itself enforces this" is directionally correct but the arithmetic does not match.

### Issue 2: TA3 proof Case 0 — false intermediate claim and missing sub-case

**ASN-0034, Verification of TA3, Case 0, sub-case `a > w`**: "If `a > w` by T1 case (ii), `w` is a proper prefix of `a`, and the divergence falls at `#w + 1 ≤ #a`."

**Problem**: The zero-padded divergence falls at the first position `> #w` where `a` differs from zero, not necessarily at `#w + 1`. Counterexample: `a = [1, 0, 3]`, `w = [1]`. After padding `w` to `[1, 0, 0]`, positions 1 and 2 agree (both 1, both 0); divergence is at position 3, not `#w + 1 = 2`.

Additionally, the sub-case where all of `a`'s components beyond `#w` are zero — making `a = padded_w` after padding, so no divergence exists — is not identified. In this sub-case (`a = [1, 0]`, `w = [1]`, padded `w = [1, 0]`, identical), `a ⊖ w = [0, 0]` (the zero tumbler). The proof then references `dₐ` as if it exists ("Since `bᵢ = aᵢ` for all `i ≤ #a` and `dₐ ≤ #a`..."), but `dₐ` is undefined when there is no divergence.

The conclusion `a ⊖ w ≤ b ⊖ w` is correct in all cases — when no divergence exists, `a ⊖ w` is a zero tumbler, and zero tumblers are ≤ everything (TA6 + T1). But the proof path through the false intermediate claim and undefined `dₐ` is broken.

**Required**: Split the `a > w` (T1 case ii) sub-case into: (a) at least one `aᵢ > 0` for `i > #w` — divergence exists at some `d` with `#w < d ≤ #a`, proceed with existing argument using `d` not `#w + 1`; (b) all `aᵢ = 0` for `i > #w` — no divergence, `a ⊖ w` is a zero tumbler of length `#a`, which is `≤ b ⊖ w` since zero tumblers precede all positive tumblers and are prefixes of longer zero tumblers.

### Issue 3: Partition Monotonicity theorem — statement does not capture what the proof establishes

**ASN-0034, Theorem (Partition monotonicity)**: "Within any prefix-delimited partition of the address space, the set of allocated addresses is totally ordered by T1, and this order is consistent with the allocation order of any single allocator within that partition."

**Problem**: The first clause (totally ordered by T1) is trivially true — any subset of a totally ordered set is totally ordered. The second clause (consistent with any single allocator's order) is T9 restated. The theorem adds nothing beyond T9. But the proof establishes a non-trivial structural result: sibling sub-partitions have non-nesting prefixes of uniform length (via T10a + TA5(c)), and by the Prefix Ordering Extension lemma, every address under an earlier sibling prefix precedes every address under a later sibling prefix. This cross-allocator ordering is the actual content of the theorem, but the statement does not capture it.

**Required**: The theorem statement should include the cross-allocator claim: for non-nesting sibling prefixes `p₁ < p₂` within the partition, every address extending `p₁` precedes every address extending `p₂` under T1. This is what the Prefix Ordering Extension lemma establishes and what makes the theorem non-trivial.

## OUT_OF_SCOPE

### Topic 1: Finite-model constraints for implementation representations
**Why out of scope**: The ASN correctly identifies this as an open question. Determining what bounded representation can satisfy T0 without reachable-state violations is a separate analysis requiring a model of the system's allocation patterns, not a property of the abstract algebra.

### Topic 2: Multi-allocator discovery and prefix tree management
**Why out of scope**: T10 and T10a specify what allocators must satisfy, not how they are created or coordinated. The operational protocol for establishing ownership prefixes and delegating sub-prefixes is a system-level concern that belongs in a future ASN on allocation machinery.

VERDICT: REVISE
