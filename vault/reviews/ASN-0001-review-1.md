# Review of ASN-0001

## REVISE

### Issue 1: T9 scope is too broad for the concurrent system T10 describes

**ASN-0001, T9 (Forward allocation)**: "Within any partition of the address space (any subtree identified by a fixed prefix), the allocation of new addresses is strictly monotonic."

**Problem**: T9 quantifies over "any partition," which includes server-level and node-level subtrees. These partitions span multiple independent allocators. T10 guarantees those allocators need no coordination. But T9 at the server level requires a total temporal ordering of all allocations under that server — including concurrent allocations by independent users. If user A (user number 1) allocates content at wall-clock time t₂ and user B (user number 2) allocates content at wall-clock time t₁ < t₂, then at the server-level partition, `allocated_before(b, a)` holds with `b > a`, violating T9.

The property the system actually needs is: each sequential allocator's output is monotonic within its own domain. Server-level monotonicity is then a *consequence* of (a) the server allocating user prefixes monotonically, (b) each user allocating within its prefix monotonically, and (c) T10 keeping the prefixes disjoint. Stating it as a universal quantification over arbitrary partitions conflates the axiom with its corollary and creates a contradiction with T10's coordination-freedom.

**Required**: Restrict T9 to single-allocator domains: "Within a single allocator's sequential allocation stream, new addresses are strictly monotonically increasing." Then derive server-level and node-level monotonicity as a theorem from T9 (restricted) + T10 + the prefix-ordering consequence of T1.

### Issue 2: "The zero tumbler" is not unique under T3

**ASN-0001, TA6**: "The zero tumbler `0 ∈ T` is less than every positive tumbler under T1, and is not a valid address."

**Problem**: T3 establishes that tumblers are equal iff they have the same length and same components. The tumblers `[0]`, `[0, 0]`, and `[0, 0, 0]` are therefore three distinct elements of T. By T1, `[0] < [0, 0] < [0, 0, 0]` (prefix rule). TA6 says "the zero tumbler" as if there is exactly one, but T3 forces there to be infinitely many all-zero tumblers. Which one is "the" sentinel? The formal statement `0 ∈ T` doesn't resolve this.

This cascades into TA0 and TA1, which use `w > 0` to mean "positive displacement." If `0` is ambiguous, "positive" is ambiguous. Is `[0, 0]` positive (it's greater than `[0]`)? If so, adding a zero-valued displacement should be a no-op, but TA0 says addition is defined for "positive" w and TA4 says `(a ⊕ w) ⊖ w = a` for `w > 0` — an all-zero displacement that qualifies as "positive" would make TA4 trivially true without constraining anything.

**Required**: Either (a) designate a specific zero tumbler (e.g., `[0]`, the length-1 sequence) and define "positive" as `t > [0]` under T1, acknowledging that `[0, 0]` is then "positive"; or (b) define "zero tumbler" as the equivalence class of all-zero sequences and explain how T3's strict length-sensitivity interacts with this class; or (c) define "positive" independently (e.g., "at least one component is nonzero") and separate it from the sentinel definition. Each choice has different consequences for TA0–TA4; the choice must be explicit.

### Issue 3: T5 proof omits the short-b case

**ASN-0001, T5 (Contiguous subtrees)**: "for if `b` diverged from `p` at some position `k ≤ #p`, then either `bₖ < pₖ` (contradicting `a ≤ b` since `aₖ = pₖ`) or `bₖ > pₖ` (contradicting `b ≤ c` since `cₖ = pₖ`)."

**Problem**: The proof assumes b has enough components to diverge from p at some position. It does not address the case `#b < #p`. In this case b cannot share prefix p (too short), and the "divergence at position k" framing doesn't directly apply. The case requires separate treatment: if `#b < #p`, then since `a ≤ b` and `#a ≥ #p > #b`, the first point of divergence `j ≤ #b` gives `aⱼ = pⱼ < bⱼ` (since a can't be a prefix of the shorter b). Then `bⱼ > pⱼ = cⱼ` contradicts `b ≤ c`. The conclusion holds, but the argument is structurally different from the one given — it relies on the length asymmetry, not on divergence within p's range.

**Required**: Add the `#b < #p` case explicitly. Two sentences suffice, but the case must be shown, not subsumed by "diverged from p."

### Issue 4: Density claim is incorrect

**ASN-0001, Representation and discreteness**: "At the abstract level, T is dense in the sense that T0 (unbounded components) allows arbitrarily many tumblers to be constructed between any two that differ in a component."

**Problem**: T is not dense, even in the hedged sense offered. The tumblers `[1, 3]` and `[1, 3, 0]` are adjacent under T1: `[1, 3] < [1, 3, 0]` by the prefix rule, and no tumbler lies strictly between them. Any `x` with `[1, 3] < x < [1, 3, 0]` would need to extend `[1, 3]` (by T5, anything between two extensions of a prefix shares that prefix), but the smallest such extension is `[1, 3, 0]` itself. Every tumbler and its minimal extension (appending a zero component) form an adjacent pair.

The qualifier "that differ in a component" excludes the prefix case, making the claim technically defensible but misleading. The immediately following analogy to floating-point and reals — "the abstract reals are dense, but the representable values are discrete" — implies T plays the role of the reals. It does not; T has the adjacent-pair structure from the start.

**Required**: State directly that T is not dense in the order-theoretic sense. Identify the adjacent-pair structure (a tumbler and its zero-extension are always adjacent). Then restate what T0 does provide: between any two tumblers that differ at a shared position (not related by prefix), there exist arbitrarily many intermediate tumblers. The floating-point analogy should be removed or corrected — the better analogy is to a tree's depth-first traversal order, which has adjacent pairs at every branch point.

### Issue 5: TA4 states one direction; the reverse is derivable but not derived

**ASN-0001, TA4 (Inverse)**: "`(A a, w : w > 0 : (a ⊕ w) ⊖ w = a)`."

**Problem**: The reverse direction, `(a ⊖ w) ⊕ w = a` for `a ≥ w`, is not stated. It is derivable from TA1, TA3, and TA4: let `y = a ⊖ w`; then `(y ⊕ w) ⊖ w = y` by TA4. If `y ⊕ w ≠ a`, then `y ⊕ w > a` or `y ⊕ w < a`; applying ⊖ w (order-preserving by TA3) to both sides yields `y > a ⊖ w` or `y < a ⊖ w`, either of which contradicts `y = a ⊖ w`. So `(a ⊖ w) ⊕ w = a`.

This reverse direction is needed for DELETE-then-INSERT to restore V-positions — the symmetric scenario to INSERT-then-DELETE (which TA4 covers). Leaving it unstated leaves the reader to wonder whether the algebra is symmetric in this respect.

**Required**: State and prove the reverse direction as a derived consequence of TA1, TA3, and TA4. Three lines suffice.

### Issue 6: T12 justification cites wrong dependencies

**ASN-0001, T12 (Span well-definedness)**: "Contiguity follows from T5 (contiguous subtrees) and the order-preservation of addition (TA1)."

**Problem**: T12 defines a span as the set `{t ∈ T : s ≤ t < s ⊕ ℓ}`. This is an interval in a totally ordered set. Intervals in totally ordered sets are contiguous by definition — if `s ≤ x < y < s ⊕ ℓ`, then any `z` with `x ≤ z ≤ y` satisfies `s ≤ z < s ⊕ ℓ`. No appeal to T5 or TA1 is needed.

T5 establishes that *prefix-defined* sets are contiguous intervals. That is a non-trivial property. T12 defines *interval-defined* sets, which are trivially contiguous. Citing T5 here obscures the distinction between the two kinds of sets and suggests the proof is non-trivial when it is definitional.

TA1 is relevant to establishing that `s ⊕ ℓ > s` when `ℓ > 0` (so the interval is non-empty), but the ASN doesn't make this the explicit purpose of the citation.

**Required**: Replace the justification. State that contiguity of intervals in a total order is definitional. If the intent is to establish non-emptiness, cite TA1 for that purpose explicitly. Reserve T5 for claims about prefix-defined sets (e.g., "all content under server 2 forms a contiguous interval").

### Issue 7: Span length type is unspecified

**ASN-0001, T12**: "A span is a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ` is a length."

**Problem**: The type of `ℓ` is never stated. T12 uses `s ⊕ ℓ`, which by TA0 requires both operands to be tumblers, implying `ℓ ∈ T`. But `ℓ` is called a "length," which connotes a non-negative integer. These are different — the tumbler `[1, 3]` and the integer `13` are not the same kind of object. The ASN's earlier discussion of addition treats the second operand as a "displacement" (a tumbler), not a scalar. If span lengths are tumblers, this should be stated. If they are integers embedded into T by some convention (e.g., the integer `n` becomes the tumbler `[n]`), that embedding must be specified.

**Required**: State explicitly that `ℓ ∈ T` (or whatever the type is). If span lengths are single-component tumblers `[n]`, say so. If they can be multi-component, explain what a multi-component length means for the range calculation.

### Issue 8: No concrete worked example

**ASN-0001, throughout**: The ASN gives fragmentary illustrations (e.g., "1.1.0.3 becomes 1.1.0.4") but never walks through a complete scenario verifying multiple properties simultaneously.

**Problem**: A worked example is not decorative — it is a consistency check. The properties T0–T12 and TA0–TA8 must cohere. The easiest way to expose contradictions is to instantiate them on a specific case and verify that all claimed properties hold simultaneously.

**Required**: Add at least one scenario — e.g., "Server 1, user 3, document 2, element subspace 1, positions 1 through 5" — and verify T1 (ordering), T4 (parsing), T5 (contiguity), T6 (containment), and T9 (allocation monotonicity) against concrete tumbler values. Show the tumbler arithmetic TA0–TA4 on a specific V-space shift.

## DEFER

### Topic 1: Associativity of ⊕ and composition of shifts
**Why defer**: The ASN acknowledges this as an open question. Whether `(a ⊕ w₁) ⊕ w₂ = a ⊕ (w₁ ⊕ w₂)` matters for operation composition, which is a topic for the ASN that formalizes multi-step editing, not for the tumbler algebra itself.

### Topic 2: Crash recovery and allocation counter durability
**Why defer**: The ASN establishes the abstract monotonicity requirement (T9). How to maintain monotonicity across crashes is an operational concern that depends on persistence mechanisms not yet specified.

### Topic 3: Zero-length spans
**Why defer**: T12 restricts to `ℓ > 0`. Whether the system needs zero-length spans (for empty endsets, deleted ranges, etc.) is a question about the link and editing models, not about the tumbler algebra.

### Topic 4: Detailed semantics of mixed-length tumbler arithmetic
**Why defer**: TA0–TA4 state axiomatic properties of ⊕ and ⊖ without specifying behavior for operands of different lengths or depths. The algebra admits cases like `[1, 3] ⊖ [1, 0, 0, 0, 0]` where the precondition `a ≥ w` holds lexicographically but the operation's meaning is non-obvious. A future ASN on V-space arithmetic should pin down these cases.
