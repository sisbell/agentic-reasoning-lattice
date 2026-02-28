# Review of ASN-0001

## REVISE

### Issue 1: TA4 stated unconditionally but violated by the constructive definition

**ASN-0001, Verification of TA4**: "TA4 holds exactly when `a`'s trailing structure below the action point matches `w`'s trailing structure, or when `a` has no components below the action point."

**Problem**: TA4 is stated as `(A a, w : w > 0 : (a ⊕ w) ⊖ w = a)` — universally quantified, no precondition. The constructive definition then demonstrates a concrete failure mode: when the action point `k < #a`, trailing components of `a` at positions `k+1, ..., #a` are discarded by addition (replaced by `w`'s trailing structure) and cannot be recovered by subtraction.

Concrete counterexample: let `a = [1, 5]`, `w = [1, 3]`. Action point of `w` is position 1. Addition: `[1, 5] ⊕ [1, 3] = [2, 3]` (position 1: `1+1=2`, position 2: copy from `w` = `3`). Subtraction: `[2, 3] ⊖ [1, 3]` — first divergence at position 1 (`2 ≠ 1`), result `[2-1, 3] = [1, 3] ≠ [1, 5]`.

The ASN acknowledges this — "This reveals a subtle but important constraint" — but does not revise TA4. The axiom and its constructive realization contradict each other. The resolution ("in the editing use case, the action point is at the deepest level") is stated informally and does not appear in the axiom's quantifier.

**Required**: Either (a) add a precondition to TA4 restricting it to cases where the action point `k ≥ #a` (equivalently, `a` has no components below the action point), or (b) revise the constructive definition to satisfy the axiom unconditionally. If (a), the Reverse Inverse corollary must inherit and state the same precondition — it currently derives from unrestricted TA4 without noting the restriction.

### Issue 2: TA1 strict inequality fails under the constructive definition

**ASN-0001, Verification of TA1**: "TA1 in the `≤` sense holds universally. TA1 in the strict `<` sense requires `k ≥ j`."

**Problem**: TA1 is stated as `(A a, b, w : a < b ∧ w > 0 : a ⊕ w < b ⊕ w)` with strict inequality. The verification's Case 1 (`k < j`, where `k` is the action point and `j` is the first divergence between `a` and `b`) shows `a ⊕ w = b ⊕ w` — equality, not strict inequality. Both operands agree at position `k`, both get the same `wₖ` added, and both copy the same tail from `w` afterward. The original divergence at position `j > k` is erased.

Example: `a = [1, 3]`, `b = [1, 5]` (diverge at position 2), `w = [2]` (action point at position 1). Then `a ⊕ w = [3]`, `b ⊕ w = [3]`. So `a < b` but `a ⊕ w = b ⊕ w`. TA1 (strict) is violated.

The ASN says "In the editing use case... Case 2 always applies." This is an informal domain restriction that does not appear in the axiom.

**Required**: Either (a) weaken TA1 to `≤` and document that strict preservation requires `k ≥ divergence(a, b)`, or (b) add the precondition `k ≥ divergence(a, b)` to the strict version. In either case, state explicitly which version the editing operations rely on and why their use satisfies the precondition.

### Issue 3: TA0 well-definedness contradicted by the constructive precondition

**ASN-0001, Constructive definition of ⊕**: "**Precondition:** `k ≤ m` — the displacement's action point must fall within the start position's length."

**Problem**: TA0 states `a ⊕ w` is well-defined for any `a, w ∈ T` with `w > 0`. The constructive definition requires `k ≤ #a` — the displacement cannot have more leading zeros than `a` has components. For example, `[1] ⊕ [0, 0, 3]` is undefined: the action point of `[0, 0, 3]` is position 3, but `#[1] = 1`. TA0 claims this is well-defined; the constructive definition says it is not.

**Required**: Add the precondition `k ≤ #a` (where `k` is the action point of `w`) to TA0, or provide a constructive extension that handles `k > #a`. Propagate the precondition to every property that depends on TA0 (TA1, TA-strict, TA4, T12).

### Issue 4: TA5 verification of T4 preservation omits the zero-count constraint

**ASN-0001, TA5 verification**: "We verify that TA5 preserves the positive-component constraint of T4... So `t'` satisfies T4's positive-component constraint."

**Problem**: T4 has two constraints: (i) every field component is strictly positive (the positive-component constraint), and (ii) an I-space address contains *at most three* zero-valued components. The verification checks (i) but not (ii). When `k > 0`, `inc(t, k)` appends `k - 1` zero-valued components plus a final `1`. If `t` already has three zeros (an element address) and `k ≥ 2`, the result has at least four zeros, violating T4.

Example: `t = 1.0.3.0.2.0.1.3` (three zeros, element address). `inc(t, 2)` produces `1.0.3.0.2.0.1.3.0.1` (four zeros). This is not a valid I-space address under T4.

**Required**: Either (a) add a precondition to TA5 restricting `k` based on the current zero count of `t` (e.g., `zeros(t) + (k - 1) ≤ 3`), or (b) explicitly state that TA5 can produce tumblers outside the valid I-space address set and document which combinations of `t` and `k` preserve T4. The verification must address both T4 constraints.

### Issue 5: Case 4 of global uniqueness assumes allocator discipline not established by axioms

**ASN-0001, Global uniqueness, Case 4**: "The parent allocator produces addresses by `inc(t, 0)` at the document level, yielding document fields of some length `γ` (TA5(c) preserves this length across all sibling allocations)."

**Problem**: The proof assumes that a parent allocator produces its direct outputs exclusively via shallow increment `inc(t, 0)`, and creates child allocators via deep increment `inc(t, k > 0)`. This is a behavioral constraint on allocators — it says an allocator partitions its actions into "produce siblings" (shallow) and "spawn children" (deep), and never mixes them in a way that produces same-length outputs from both parent and child.

No axiom establishes this discipline. T9 requires monotonicity. T10 requires prefix disjointness for non-nesting prefixes. TA5 defines the increment operation. None of them constrains how an allocator chooses between `k = 0` and `k > 0` across its allocation sequence. An allocator that intermixed shallow and deep increments — e.g., producing `inc(t, 0)` then `inc(t', 2)` then `inc(t'', 0)` — could produce outputs of varying lengths, and the proof's length-based uniqueness argument would not apply.

**Required**: Either (a) introduce an axiom constraining allocator behavior (e.g., each allocator uses a fixed `k` for all its sibling allocations), or (b) revise the proof to handle allocators that mix shallow and deep increments, or (c) demonstrate from existing axioms that mixed-depth allocation cannot produce collisions.

### Issue 6: Self-correction within a proof

**ASN-0001, Verification of TA1, case `k > j`**: "Both results have `wⱼ` at position `j` (copied from the displacement's leading zeros, since `j < k`). But `wⱼ = 0` (before the action point), so `(a ⊕ w)ⱼ = aⱼ` and `(b ⊕ w)ⱼ = bⱼ`, wait — positions before `k` copy from the start..."

**Problem**: The proof makes an incorrect claim ("both results have `wⱼ` at position `j`"), catches the error mid-sentence ("wait — positions before `k` copy from the start"), and corrects course. The correction is right, but a proof should not contain its own drafts. The initial error (confusing "positions before `k` copy from `w`" with the actual rule "positions before `k` copy from the start") suggests the case analysis was improvised rather than derived from the constructive definition.

**Required**: Rewrite the `k > j` case cleanly. The argument is straightforward: for `i < k`, `(a ⊕ w)ᵢ = aᵢ` and `(b ⊕ w)ᵢ = bᵢ`. Since `j < k`, the divergence at position `j` is preserved: `(a ⊕ w)ⱼ = aⱼ < bⱼ = (b ⊕ w)ⱼ`. State it once, correctly.


## DEFER

### Topic 1: Formal definition of "allocator"

**Why defer**: The ASN uses "allocator" as a primitive concept — an entity that controls a prefix and produces addresses monotonically. A future ASN should define what an allocator is (its state, its interface, its behavioral constraints — particularly whether it may mix shallow and deep increments, as Issue 5 reveals). This is new territory requiring its own treatment, not an error in ASN-0001's tumbler algebra.

### Topic 2: Span operations (splitting, intersection, merging)

**Why defer**: ASN-0001 defines what a span IS (T12) but not what operations act on spans. Span splitting (when an INSERT falls within a span), intersection (for link search), and merging (for compacting POOMs) are distinct operations that require their own treatment. The algebra of spans is downstream of the tumbler algebra.

### Topic 3: Crash recovery and allocation monotonicity

**Why defer**: The open question about allocation counter durability across crashes is a systems-level concern. T9 demands monotonicity; how that survives a crash (write-ahead log, checkpointing, etc.) is a recovery protocol, not a property of the tumbler algebra.
