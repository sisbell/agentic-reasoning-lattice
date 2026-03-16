# Review of ASN-0042

## REVISE

### Issue 1: O9 claims node-field equality but proof yields only prefix containment
**ASN-0042, Node-Locality**: "`nodeField(a) = nodeField(pfx(π))`"
**Problem**: The proof says "if `pfx(π) ≼ a`, then the leading components of `a` match those of `pfx(π)`, including the entire node field." This establishes that `pfx(π)`'s node field is a prefix of `a`'s node field, not that they are equal. A node-level principal with `pfx(π) = [1, 2]` (`zeros = 0`) satisfies `pfx(π) ≼ a` for `a = [1, 2, 3, 0, 5, 0, 7, 0, 1]`, yet `nodeField(a) = [1, 2, 3] ≠ [1, 2] = nodeField(pfx(π))`. This scenario is reachable: T10a's child increment `inc([1, 2], 1)` produces `[1, 2, 1]` (still `zeros = 0`), so addresses with longer node fields under the same node-level principal are structurally permitted.

Note that the claim *is* correct for account-level principals (`zeros = 1`): the prefix `N.0.U ≼ a` forces `a`'s first zero to align with the prefix's zero, which forces equal-length node fields. The failure is specific to node-level principals whose node field is a proper prefix of the address's node field.

**Required**: Weaken to `nodeField(pfx(π)) ≼ nodeField(a)`, or add a case split: equality when `zeros(pfx(π)) = 1`, prefix containment when `zeros(pfx(π)) = 0`. The conceptual claim (no cross-node ownership) survives either fix — a principal at node `[1]` cannot own addresses at node `[2]` — but the formal statement must match the proof.

### Issue 2: `≺` (strict prefix) used without definition
**ASN-0042, Delegation definition, condition (i)**: "`pfx(π) ≺ pfx(π')`"
**Problem**: The `delegated` relation uses `≺` in its first structural constraint. Neither this ASN nor the foundation ASN-0034 defines `≺`. ASN-0034 defines `≼` (T5) and `⋠` (T10) but not the strict variant. The meaning is universally understood (`p ≺ a ≡ p ≼ a ∧ p ≠ a`), but a formal definition introduces a symbol it does not define, and the delegation preservation proof of O1b and the Corollary both depend on the strict/non-strict distinction.
**Required**: Add a one-line definition: `p ≺ a ≡ p ≼ a ∧ p ≠ a` (equivalently, `p ≼ a ∧ #p < #a`).

### Issue 3: O8 proof cites O5 (allocation) for a delegation conclusion
**ASN-0042, Irrevocable Delegation**: "and by O5, only `π'` itself can perform such delegation"
**Problem**: The ASN explicitly separates allocation from delegation ("we must separate two concepts: *ownership delegation* ... and *allocation*"), and O5 is stated as a constraint on allocation ("Only the principal with the longest matching prefix may *allocate*"). The O8 proof then cites O5 to justify that only `π'` can *delegate* within `dom(π')`. The correct authority for delegation is condition (ii) of the `delegated` relation, which imposes the same "most-specific covering principal" constraint on delegators. The proof logic is sound — the conclusion follows from condition (ii) plus O12/O13 — but it cites the wrong property.
**Required**: Replace "by O5" with "by condition (ii) of the `delegated` relation" (or cite both O5 for allocation and condition (ii) for delegation, since the argument covers both).

## OUT_OF_SCOPE

### Topic 1: Authentication invariants for O0–O10 consistency
**Why out of scope**: O11 explicitly treats principal identity as axiomatic and the Scope section excludes "concrete authentication mechanisms." A future ASN could specify what invariants an authentication binding must satisfy to prevent property violations (e.g., that a session claiming `pfx(π)` must have been delegated that prefix per the `delegated` relation, ensuring O5 and O7 authorization constraints hold operationally, not just structurally).

### Topic 2: Principal activity vs. persistence
**Why out of scope**: O12 guarantees principal persistence but is silent on whether a persistent principal can become inactive or unreachable. The ownership model requires only that the principal *exists* in Π (for longest-match resolution); whether the principal can *act* is a separate concern that would require new state predicates. The open question about "content accessibility when the effective owner ceases to exist as a principal" gestures at this but does not frame it as a liveness property of ownership.

VERDICT: REVISE
