# Review of ASN-0069

## REVISE

### Issue 1: Composite verification re-derives freshness that foundation lemmas supply directly

**ASN-0069, §"The Fork Composite", K.δ sub-case A and sub-case B**: The sub-case A discharge of `e ∉ E` runs a three-step argument "(i) within the parent allocator's spawning event… (ii) within the parent allocator's other spawning events… (iii) within A_v(d_src)'s subsequent sibling stream and across every other allocator," and sub-case B runs a parallel three-step argument for `inc(d_prev, 0) ∉ E`.

**Problem**: ASN-0047 (foundation) supplies two lemmas built precisely for this. **ChildSpawnFreshness** gives `inc(t, k') ∉ Σ.E ⟺ the (t, k') child-spawn has not yet been performed` for `k' ∈ {1, 2}` — directly applicable to the first fork (`t = d_src`, `k' = 1`), reducing the entire (i)–(iii) argument to the one-line observation that sub-case A's predicate ("A_v(d_src) has emitted no prior version") *is* "the (d_src, 1) spawn has not fired." **FrontierEquivalence** gives `inc(t, 0) ∉ Σ.E ⟺ t is the frontier of A's (t, 0)-branch` — directly applicable to the subsequent fork (`t = d_prev = max(dom(A_v(d_src)))` is the frontier). The ASN cites neither lemma (the Dependency Audit lists K.δ, Allocator hierarchy, SubAllocatorBundle, SequentialTransitionAxiom — not these two), and instead re-proves both from T10a/T10a.6/T10a.7/P1/SequentialTransitionAxiom. This is re-proving a foundation result rather than consuming it.

**Required**: Replace the (i)–(iii) freshness derivations with citations to ChildSpawnFreshness (k = 1 branch) and FrontierEquivalence (k = 0 branch), connecting each to the sub-case predicate in one line. If the lemmas are deliberately avoided, state why.

### Issue 2: "Correspondence triple" notation overloads the S8/S8★ run structure

**ASN-0069, §"Worked Example"**: "Reading this equality pointwise across the three positions yields the correspondence triple `([s_C, 1], [s_C, 1], 3)` — three pointwise-corresponding positions."

**Problem**: S8 (ASN-0036) and S8★ (ASN-0047) define a *correspondence run* as a triple `(v, a, n)` whose middle element is an **I-address**. The example's triple `([s_C, 1], [s_C, 1], 3)` has a **V-position** in the middle slot — it is a cross-document V-position alignment `(v_src, v_new, length)`, a different object. Reusing the established term "correspondence triple" for a differently-shaped tuple invites confusion with the foundation's run structure.

**Required**: Rename the worked-example object (e.g., "intercomparison alignment `(v_src, v_new, length)`") or drop the triple notation and state the alignment in prose, so it is not mistaken for an S8 run.

## OUT_OF_SCOPE

None. The Open Questions section appropriately defers concurrent-fork semantics, descendant enumeration, snapshot-vs-living forks, transcludent sources, and counterpart correspondence to future ASNs.

VERDICT: REVISE
