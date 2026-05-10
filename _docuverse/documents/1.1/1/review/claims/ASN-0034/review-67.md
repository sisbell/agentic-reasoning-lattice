# Cone Review — ASN-0034/T9 (cycle 2)

*2026-04-16 03:43*

### T9's formal contract omits its dependency declarations

**Foundation**: (internal — foundation ASN)
**ASN**: T9 (ForwardAllocation), formal contract: "*Preconditions:* `a, b ∈ T` with `same_allocator(a, b) ∧ allocated_before(a, b)`. *Postconditions:* `a < b` under the tumbler order T1."
**Issue**: Every other theorem in the document declares its dependencies explicitly — T1 lists T0 and T3, T8 lists NoDeallocation, TA5 lists T1. T9's formal contract has Definitions, Preconditions, and Postconditions but no Depends clause. Yet the proof relies on three external properties: T10a ("By T10a, each allocator produces its sibling outputs exclusively by repeated application of `inc(·, 0)`"), TA5(a) ("By TA5(a), `inc(tᵢ, 0) > tᵢ`" — the base case), and T1(c) ("By transitivity of the strict order (T1(c))" — the inductive step). The `dom(A)` definition itself references `inc(·, 0)` and the restriction to sibling-only production, both of which originate in TA5 and T10a respectively. A formalizer working from the contract alone cannot reconstruct T9's dependency graph.
**What needs resolving**: A Depends clause in T9's formal contract listing T10a (allocator discipline — justifies the dom(A) definition), TA5(a) (strict monotonicity of inc — the base case), and T1(c) (transitivity — the inductive step).

---

### TA5's formal contract uses sig(t) without declaring its defining property as a dependency

**Foundation**: (internal — foundation ASN)
**ASN**: TA5 (HierarchicalIncrement), formal contract: "*Definition:* `inc(t, k)`: when `k = 0`, modify position `sig(t)` (TA5-SIG) to `t_{sig(t)} + 1`" and "*Depends:* T1 (LexicographicOrder)"
**Issue**: TA5's contract Definition references `sig(t)` with a parenthetical citation "(TA5-SIG)", and the proof opens with "Recall that `sig(t)` denotes the last significant position of `t`" — the word "recall" indicating a definition stated elsewhere. The summary table confirms TA5-SIG is a "separate property" with its own contract. Yet TA5's Depends clause lists only T1. The symbol `sig(t)` appears in the Definition (determining which position `inc` modifies for `k = 0`), in postcondition (b) (the agreement quantifier excludes `sig(t)`), and in postcondition (c) (the increment target). A formal dependency on TA5-SIG is required for any of these uses to resolve against a definition.
**What needs resolving**: TA5's Depends clause should include TA5-SIG, since `sig(t)` is load-bearing in TA5's definition and postconditions and is canonically defined in TA5-SIG.

---

### T10a's "full precondition of T10" claim is unreconciled with provable ancestor-descendant prefix-nesting

**Foundation**: (internal — foundation ASN)
**ASN**: T10a (AllocatorDiscipline), Justification: "T10 (PartitionIndependence), whose precondition — non-nesting prefixes — is the guarantee that T10a's discipline is designed to establish"; postcondition T10a.5: "Together with T10a.2, this delivers the full precondition of T10 across the entire allocator tree."
**Issue**: T10a.2 covers within-allocator prefix-incomparability; T10a.5 covers non-ancestor-related cross-allocator prefix-incomparability. Neither addresses the ancestor-descendant case — and in that case, prefix-nesting provably exists. When a parent spawns a child from output `tᵢ` via `inc(tᵢ, k')` with `k' > 0`, TA5(b) gives agreement on all positions `1..#tᵢ` and TA5(d) gives `#inc(tᵢ, k') > #tᵢ`, so `tᵢ` is a proper prefix of the child's base address. Since all child outputs preserve this prefix (by TA5(b) for `k = 0`), every element of the child's domain has the parent output `tᵢ` as a prefix. Thus for every parent-child allocator pair, there exist `x ∈ dom(parent)` and `y ∈ dom(child)` with `x ≺ y` — the prefix relation the Justification calls "nesting." The document describes T10's precondition as "non-nesting prefixes" without scope restriction, yet the postconditions only deliver prefix-incomparability for the non-ancestor case. The claim that T10a.2 + T10a.5 deliver the "full precondition" is either incorrect (if T10 requires universal prefix-incomparability) or relies on an unstated restriction in T10's precondition (that ancestor-descendant pairs are excluded).
**What needs resolving**: Either (a) explicitly state that T10's precondition restricts to non-ancestor-related allocator pairs and explain why the ancestor case is excluded (e.g., delegation semantics), or (b) qualify the "full precondition" claim to acknowledge that it covers only the non-ancestor-related scope that T10a.2 and T10a.5 address.
