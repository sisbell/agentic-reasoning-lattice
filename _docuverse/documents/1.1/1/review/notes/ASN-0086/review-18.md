# Review of ASN-0086

## REVISE

### Issue 1: "Sparse-allocator interpretation" is a substrate-level commitment that strengthens ASN-0034 but its relationship is under-specified
**ASN-0086, Substrate emission primitive section**: "the substrate primitive's atomic class-(iii) step implicitly extends `Act(s)` and `n_s` for every allocator on the L1c witness chain to whatever values are required to witness T10a's T2 admissibility at each intermediate spawn pair, in one indivisible action. The substrate exposes no separate allocator-activation transition..."

**Problem**: ASN-0034's T10a defines T1 (sibling-increment), T2 (child-spawn), T3 (non-allocating) as *separate* transition shapes — each `op ∈ Σ` is one shape, and `s → s'` is one op. ASN-0086 collapses sequences of these into a single atomic substrate-`→` step (e.g., R0 Step 2 Case A's chain `(d,2) → s_L−1 sibling sweeps → (d.0.s_L,1)` is treated as one class-(iii) transition extending `Act(s)`/`n_s` correspondingly). This is a *layering* commitment: ASN-0086's `→` is coarser than ASN-0034's. The ASN flags this informally but never explicitly characterizes the coarsening relationship: is ASN-0086's `→` *the* canonical substrate-level abstraction over ASN-0034, or one of several admissible layerings? Without this, a downstream ASN can't tell whether an alternative implementation that exposes intermediate allocator-state transitions is conforming.

**Required**: Add an explicit "Coarsening" statement: ASN-0086's `→` is the equivalence-class projection of ASN-0034's transition relation under "compose all T1/T2 sequences with no exposed effect on `(dom(Σ.C), dom(Σ.M), dom(Σ.L))`". State whether this is normative for the substrate model or one admissible choice among several.

### Issue 2: R0 Step 2 Case A's "subspace 1" labeling implicitly assumes `s_C = 1`
**ASN-0086, R0 proof, Step 2 Case A**: "(i) `t₁ = inc(d, 2)` → `d.0.1` — at element-field depth 1, subspace 1"

**Problem**: The label "subspace 1" describes the address `d.0.1` having first element-field component 1. The ASN doesn't formally fix `s_C = 1` (only `s_C ≠ s_L`). The construction works for any `s_C, s_L ≥ 1`, but the comment reads as if it's identifying this address with the content subspace. A reader checking whether the chain validly traverses subspaces will be confused when `s_C ≠ 1` (e.g., a system with `s_C = 3, s_L = 2`), where step (i) lands at subspace 1 which is neither content nor link.

**Required**: Either fix `s_C = 1` as a convention adopted by ASN-0086 (consistent with udanax-green; this would also discharge "step (i) lands at content subspace" cleanly), or rewrite the parenthetical as "at position 1 of the first element-field component" without invoking subspace labels.

### Issue 3: R0 Step 4's L11a verification is redundant
**ASN-0086, R0 proof, Step 4**: "L11a (LinkUniqueness, ASN-0043): L11a's antecedent (distinct allocation events) is discharged by Step 4's freshness argument; L11a's conclusion then gives that `a` is distinct from every prior link address."

**Problem**: The freshness argument `a ∉ dom(Σ.L)` already directly establishes `a ≠ a'` for all `a' ∈ dom(Σ.L)` — that's exactly what `∉` means. The L11a invocation traverses "freshness → distinct allocation event → distinct address" to reach a conclusion freshness already provides. This is circuitous and may make a reader wonder whether L11a is doing real work here (it isn't).

**Required**: Rewrite the bullet as "L11a (LinkUniqueness): preserved trivially. Prior pairs satisfy L11a at Σ; the new event's address `a ∉ dom(Σ.L)` is distinct from all prior addresses by freshness." Drop the chain through L11a's conclusion.

### Issue 4: R6c's bridge to broader transition vocabulary is buried in a parenthetical
**ASN-0086, R6c**: "(The relation `Σ ⊑ Σ'` is the reflexive-transitive closure of the dom-extending `→`, and so the formal quantifier above ranges over dom-extending reachability only; ... The user-facing reading 'every future active subset' is intended in the *broad* sense — across both dom-extending and arrangement-modifying successors — and the claim extends to that broader relation without further work, via the following dependency chain. [...])"

**Problem**: R6c's load-bearing user-facing guarantee — that arrangement-modifying transitions also leave the nullified set untouched — is in a parenthetical aside spanning the four-step Steps 1–4 derivation. The formal claim quantifies only over `⊑`, but the practically interesting consequence (which the ASN names explicitly: "every future active subset") requires the broader bridge. A reader scanning R6c may miss the broader reading or treat it as informal commentary.

**Required**: Promote the broader-transition bridge to a labeled corollary or post-script directly under R6c. State both "(formal): R6c on `⊑`" and "(corollary): R6c on `⊑ ∪ arrangement-modifying`" as separate, equally prominent claims, each with its own derivation pointer.

### Issue 5: R0a's statement omits the antichain's failure mode under the substrate primitive in isolation
**ASN-0086, R0a Statement**: "*Hypothesis: every class-(iii) `→`-transition along the reachability chain respects the sibling-frontier discipline (above).* Under that hypothesis, for every state Σ reachable from an initial Σ_0 with `dom(Σ_0.L) = ∅` via finitely many such `→`-transitions, no two link addresses in `dom(Σ.L)` are prefix-comparable"

**Problem**: The statement doesn't characterize what holds *without* the discipline. The "Breadth of the primitive vs. the discipline" remark earlier exhibits `a' = a₁.1` as a primitive-permissible emission that falsifies the antichain, but R0a itself doesn't carry a contrapositive: the user can't tell whether non-disciplinary substrates fail R0a *immediately* on the first non-disciplinary emission, or only in some subsequent state. The Nullify P3 precondition relies on R0a's reachable-state antichain; if a system is partially disciplined (early disciplined, late non-disciplined), Nullify's behavior at intermediate states is unspecified.

**Required**: Add a "Necessity" or "Failure modes" clause stating: (a) one non-disciplinary class-(iii) transition is sufficient to break the antichain *permanently* (since L12 keeps the bad pair in dom(Σ.L) forever); (b) Nullify's single-tuple-scope therefore fails *immediately* at any post-`Σ` state where the discipline is broken, regardless of whether the specific `a` being nullified is the broken party.

## OUT_OF_SCOPE

### Topic 1: Higher-arity links and their active subsets
The ASN restricts to standard-triple links. Multi-arity active subsets `A_K^{(n)}` need their own machinery.
**Why out of scope**: Flagged in Open Questions; the strand of work that would extend `L_K` to higher arities is separate from the standard-triple foundation here.

### Topic 2: Concurrency, ordering, and atomicity of Emit/Observe
What consistency model holds between Emit and Observe under concurrent invocation?
**Why out of scope**: Flagged in Open Questions; concurrency semantics belong to a substrate-layer ASN.

### Topic 3: L14's scoped form without the Setup hypothesis
The Setup hypothesis is global; R0/R4/R5 are Setup-required. The slice-wise reformulation under L14's native scoped form requires its own treatment.
**Why out of scope**: Flagged in Open Questions; substantial work to redo R0's L14a-preservation step against the slice.

### Topic 4: Strengthening R0a to substrate-level (discipline as primitive guarantee)
Tightening Emit_K or the substrate primitive itself to enforce prefix-incomparability with `dom(Σ.L)`.
**Why out of scope**: Flagged in Open Questions; would require revising the substrate emission primitive's specification, which is broader than ASN-0086's scope.

### Topic 5: Bound on |nullified(Σ)| vs. |dom(Σ.L)|
Whether the substrate guarantees any structural ratio between retracted and total tuples.
**Why out of scope**: Flagged in Open Questions.

### Topic 6: Crafted-span retractions with broader-coverage to-spans
The ASN scopes Nullify to unit-depth spans; broader retraction policy (subtree-retraction) is admitted by the primitive but not modeled here.
**Why out of scope**: A higher-layer policy concern, not a substrate-level guarantee.

VERDICT: REVISE
