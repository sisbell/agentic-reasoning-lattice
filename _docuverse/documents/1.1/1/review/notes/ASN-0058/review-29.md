# Review of ASN-0058

## REVISE

### Issue 1: M16a's T4-validity derivation has an unjustified descendancy step
**ASN-0058, M16a (OriginInvarianceUnderShift)**: "Therefore the element-level allocator whose output is a — a descendant of the document-level allocator within the T10a allocator tree — is itself T10a-conforming."

**Problem**: The argument routes T4-validity of `a` through the chain S7d → T10a recursive closure → T10a.4. The step "a descendant of the document-level allocator within the T10a allocator tree" is asserted, not derived. S7d only establishes T10a-conformance for document tumblers; the assertion that the element-level allocator producing `a` is in 𝒯 (as a descendant of A_D) requires either citing T10a.5 (CrossAllocatorIncomparability — contrapositive: prefix-containing outputs imply lineage) or acknowledging an architectural assumption about all I-address allocations falling within 𝒯.

**Required**: Simpler route — cite S7b directly. S7b's postcondition states "The projections N(a), U(a), D(a), E(a) supplied by T4b are all well-defined," which implies `a` is in T4b's domain (the T4-valid subset of T), giving T4-validity without invoking the T10a-closure chain.

### Issue 2: Four-step structural skeleton is duplicated across M2, M7-cov, M12a
**ASN-0058, M2 reverse inclusion**, **M7-cov**, **M12a "Equal starts"**: The same four claims — (1) subspace agreement, (2) depth equality via S8-depth, (3) prefix agreement via TumblerAdd, (4) component-m reduction — recur three times with the explicit acknowledgement "The same four-claim skeleton recurs in M7-cov claims (1)–(4) and M12a's 'Equal starts' argument."

**Problem**: The reuse is flagged but not factored. Each instance restates the skeleton verbatim with minor variations, adding ~30 lines of repeated reasoning. This obscures the underlying fact (that for any `v_1, v_2 ∈ dom(M(d))` with `v_1 < v_2 < shift(v_1, n_1)` under standing S8a/S8-depth preconditions, `v_2 = v_1 + k` for some `1 ≤ k < n_1`).

**Required**: Extract a single tumbler-interval-characterization lemma stated abstractly over the foundation preconditions (S8a, S8-depth, TumblerAdd, T1) that M2, M7-cov, and M12a can each invoke in one line.

### Issue 3: M12a's "Equal widths" sub-case relies on a hidden symmetry argument
**ASN-0058, M12a**: "Suppose WLOG n_1 < n_2. Then v_1 + n_1 ∈ V(R_2)... contradicts condition 3 of R_1. The symmetric case n_2 < n_1 contradicts condition 3 of R_2 by the same argument."

**Problem**: The "by the same argument" elision is acceptable here (the symmetry is genuine — swap subscripts), but the proof relies on having already established `v_1 = v_2` in the "Equal starts" sub-case. The trichotomy that resolves `n_1 < n_2`, `n_1 = n_2`, `n_2 < n_1` is implicit. The `n_1 = n_2` case is the conclusion we want — it should be stated as the residual case after both strict-inequality branches are refuted, not left implicit.

**Required**: Add one sentence: "By NAT-order trichotomy on (n_1, n_2), the surviving case is `n_1 = n_2`, giving `(v_1, a_1, n_1) = (v_2, a_2, n_2)`."

### Issue 4: M16a's k=0 case in (b) of M-sub is asymmetric with k=0 case in (a)
**ASN-0058, M-sub clause (a)** "At k = 0, v + 0 = v by OrdinalShiftBase, so subspace(v + 0) = subspace(v) trivially." **Clause (b)**: "At k = 0, a + 0 = a by OrdinalShiftBase."

**Problem**: Both clauses dispose of `k = 0` via OrdinalShiftBase, but clause (a) carries a sharpness note for `#v = 1` while clause (b) carries no analogous sharpness note for the I-side. If `#a = 1`, would `subspace_I(a + k)` equal `subspace_I(a)` for `k ≥ 1`? By S7b every `a ∈ dom(C)` has `zeros(a) = 3`, so `#a ≥ 8` (as M16a itself derives) — `#a = 1` is impossible. The asymmetry should either be explained (S7b precludes `#a ≤ 7`) or made symmetric (drop the sharpness note in (a) as architecturally irrelevant since S8a forces `#v ≥ 2`).

**Required**: Add a one-line note in clause (b) acknowledging that S7b's `zeros(a) = 3` plus S7c's `#E(a) ≥ 2` makes the `#a ≥ 8` bound implicit (no `#a = 1` sharpness case to consider).

## OUT_OF_SCOPE

None — the open questions section appropriately defers further structural inquiries (lattice ordering of decompositions, depth relationships, multi-source resolution ordering) to future work without claiming them.

VERDICT: REVISE
