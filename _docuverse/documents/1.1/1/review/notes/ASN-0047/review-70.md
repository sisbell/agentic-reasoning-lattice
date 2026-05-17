# Review of ASN-0047

## REVISE

### Issue 1: Inconsistent discharge of `e ∉ E` for k=0 siblings on a ghost chain

**ASN-0047, K.δ case (ii) "Operational T10a allocator" paragraph + Worked example 4 Step 2**

The K.δ definition lists three discharge paths for the `e ∉ E` precondition:
1. T10a's GlobalUniqueness for live-operand case (ii)
2. K.δ precondition + TA5 determinism for ghost-operand k=1
3. NodeUniqueAllocation for case (i)

The *Operational T10a allocator* paragraph claims for k=1: "A new version sub-allocator `A_v(t)` activated at the K.δ event under the same standard spawning machinery." But T10a's T2 rule (ASN-0034) requires `parent(A) ∈ Act(s)` AND `spawnPt(A) ∈ domₛ(parent(A))`. For a ghost t, t is by stipulation outside every entity allocator's tracked domain, so the spawnPt precondition fails. T10a's standard machinery does *not* admit A_v(t) activation for ghost t.

Worked Example 4 Step 2 then writes: "e₂ ∉ E by T10a's GlobalUniqueness on the version sub-allocator `A_v(1.0.1.0.5)` activated at Step 1's K.δ event." But Step 1 allocated from ghost t = 1.0.1.0.5, so under the K.δ definition's own analysis, A_v(t) cannot have been validly activated in Act(s). Invoking GlobalUniqueness on a non-active allocator is unsound.

**Problem**: The ASN simultaneously asserts (a) ghost-base k=1 needs no T10a extension and (b) T10a's GlobalUniqueness on A_v(t) discharges subsequent k=0 sibling freshness. These cannot both hold.

**Required**: Pick one consistent story. Either (a) explicitly extend T10a to admit ghost-base A_v(t) activation (parallel to SubAllocatorAxiom's treatment of content/link sub-allocator pairs), updating the *Operational T10a allocator* paragraph to acknowledge the extension; or (b) extend discharge path 2 to cover the *entire* ghost chain — all subsequent k=0 siblings discharge via K.δ precondition + TA5 determinism, and Example 4 Step 2's "T10a's GlobalUniqueness on A_v" attribution must be replaced with the precondition+TA5 reading.

### Issue 2: D-SEQ★ structural-form notation errors in worked examples

**ASN-0047, Worked example 3 (initial state and Step 1) and Worked example 5 (Step 2 and Step 5)**

The D-SEQ★ form `{[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` contains m_S − 2 intermediate 1s. At m_S = 2 (used throughout these examples), the inner range is empty and the form reduces to `{[S, k] : 1 ≤ k ≤ n_S}`. The examples write forms with extra 1s that don't match the actual V-position depth:

- Example 3 initial state: `{[s_C, 1, k] : 1 ≤ k ≤ 4}` would yield 3-component tuples `{[1, 1, 1], [1, 1, 2], ...}` but the V-positions are `{[1, 1], [1, 2], [1, 3], [1, 4]}` (2-component, depth 2). Should be `{[s_C, k] : 1 ≤ k ≤ 4}`.
- Example 3 Step 1 verification: `V_{s_C}(d_int) = {[s_C, 1, 1]}` — V-position is `[1, 1]` (2-component). Should be `{[s_C, 1]}`.
- Example 5 Step 2 verification: `{[s_L, 1, 1, k] : 1 ≤ k ≤ 2}` (4-component form) for V-positions `{[2, 1], [2, 2]}` (2-component). Should be `{[s_L, k] : 1 ≤ k ≤ 2}`.
- Example 5 Step 5 verification: `V_{s_L}(d') = {[s_L, 1, 1, 1]}` for V-position `[2, 1]`. Should be `{[s_L, 1]}`.

**Problem**: The notation introduces extra "1"s pushing the form to wrong depth. Mathematics is correct; notation is wrong.

**Required**: Rewrite the structural forms with the correct number of intermediate 1s (zero for m_S = 2).

### Issue 3: K.δ k=1 sub-case prose buries the freshness-discharge incompatibility

**ASN-0047, K.δ case (ii) k=1 "Scope, base-liveness, and discharge" paragraph**

This paragraph runs ~700 words and intermixes (i) the relaxation rationale, (ii) the consultation evidence, (iii) the per-step liveness chain analysis, (iv) the discharge mechanism for ghost vs live operands, and (v) deferred semantics. The crucial claim — that for the ghost-operand sub-case, T10a's GlobalUniqueness is *unavailable* and freshness comes from "K.δ precondition + TA5 determinism" alone — is stated once near the end and is easy to lose track of when subsequent text (including Example 4) implicitly relies on T10a applying.

**Problem**: A load-bearing axiomatic dependency is hidden inside an explanatory paragraph, making it easy for downstream proofs to drift back to T10a-based discharge (as Example 4 Step 2 demonstrates).

**Required**: Hoist the layered discharge table (path 1 for live-operand, path 2 for ghost-operand, path 3 for nodes) into its own named subsection or numbered axiom, with explicit per-case rules. Subsequent proofs should cite the path by number.

## OUT_OF_SCOPE

### Tombstone-style interior link withdrawal
The ASN explicitly notes that D-CTG★/D-MIN★ forbid interior link-subspace removal (Nelson LM 4/9 design). The mechanism (status flag, tombstone marker, retraction link) is deferred to a future ASN. **Why out of scope**: This is a deliberate scope deferral with an acknowledged open question; the current K.μ⁻ contract is internally consistent.

### Version-management semantics
The arrangement-transition invariants between successive versions, content-allocator linkage between version base and version, provenance flow, and version-lineage acyclicity are explicitly deferred. **Why out of scope**: The current ASN's K.δ k=1 contract is structurally complete; semantic version contracts belong to a separate ASN.

### Account-level k=1 admissibility
The IsDocument restriction at k=1 is a deliberate scope exclusion. **Why out of scope**: Acknowledged as a deliberate scope decision in the Open Questions.

### Non-T10a allocators
Admitting allocators not conforming to T10a (beyond the NodeUniqueAllocation node case) is deferred. **Why out of scope**: Acknowledged as a deferred topic.

VERDICT: REVISE
