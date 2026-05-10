# Review of ASN-0040

## REVISE

### Issue 1: B10 dependency on B1 creates a cycle in the dependency graph

**ASN-0040, Properties Table and B10 proof**: B10 lists `B1` and `B2` among its dependencies; B1 lists `B10` among its dependencies.

**Problem**: The dependency graph contains a cycle: B1 → B10 → B1. The B10 proof introduces this by citing B1 to identify the element being incremented: "By B1 (Contiguous Prefix), children(B, p, d) = {c₁, ..., cₘ}, so cₘ ∈ B." But B10's argument does not require knowing *which* stream element is being incremented — only that the input to `inc(·, 0)` is in B and satisfies T4.

The B10 Case 2 argument works without B1:

> Let t = max(children(B, p, d)). By definition of children, t ∈ children(B, p, d) ⊆ B. By the inductive hypothesis (B10 for B), t satisfies T4. The new element a = inc(t, 0). TA5a with k = 0 preserves T4 unconditionally. Therefore a satisfies T4.

No contiguous prefix structure is consulted — only set membership (`t ∈ B`) and the inductive hypothesis. Similarly, B2 is used only to label the new element as `c_{m+1}`, which is irrelevant to T4 preservation.

**Required**: (a) Revise the standalone B10 proof's Case 2 to derive `max(children) ∈ B` from the set definition rather than from B1. (b) Remove B1 and B2 from B10's dependency list in the Properties Table. This eliminates the cycle: B10 becomes independently provable, and B1 can then cite B10 without circularity.

### Issue 2: Bop freshness argument applies B7 without verifying its precondition

**ASN-0040, Bop correctness proof, Freshness section**: "In any other namespace (p', d') ≠ (p, d): by B7 (Namespace Disjointness), S(p, d) ∩ S(p', d') = ∅"

**Problem**: B7's formal contract requires both (p, d) and (p', d') to satisfy B6. The freshness argument applies B7 to all (p', d') ≠ (p, d) without verifying that the other pair is B6-valid. An element of Σ.B could belong to children(Σ.B, p', d') for a non-B6-valid (p', d') — the stream identity proved in the B1 argument (S(p, 1) = S(p', 2) when p' ends in zero) demonstrates that T4-valid elements can inhabit non-B6-valid streams. B7 says nothing about such pairs.

The three-class partition is also imprecise: the third class is described as "elements belonging to no sibling stream" but should be "elements not belonging to any B6-valid sibling stream." The argument ultimately works (by B0a, non-seed elements are in B6-valid streams; T4-valid seeds of length ≥ 2 are in B6-valid streams; length-1 seeds are in no stream), but these steps are not shown.

A simpler argument establishes freshness without B7: By B1, children(Σ.B, p, d) = {c₁, ..., cₘ}. Since children(Σ.B, p, d) = Σ.B ∩ S(p, d) and c_{m+1} ∈ S(p, d), showing c_{m+1} ∉ children suffices to conclude c_{m+1} ∉ Σ.B. And c_{m+1} ∉ {c₁, ..., cₘ} because m + 1 > i for all 1 ≤ i ≤ m, and S0 gives distinct stream indices map to distinct elements.

**Required**: Either (a) replace the three-class partition with the simpler one-step argument from B1 (which needs only B1 and S0, no B7), or (b) make the partition precise by establishing that every element of Σ.B is in some B6-valid stream or in no stream at all (citing B0a for non-seeds, and the natural-parent construction for T4-valid seeds of length ≥ 2).

## OUT_OF_SCOPE

### Topic 1: Per-subspace contiguous prefix property
The sibling stream under a document parent mixes subspaces — c₁ lands in subspace 1, c₂ in subspace 2, etc. Whether the contiguous prefix property should hold independently within each subspace (so that text elements and link elements each form gap-free sequences) is a question for a future ASN on subspace structure, not an error in this ASN's stream definition.

**Why out of scope**: The current ASN defines baptism at the stream level, not the subspace level. Subspace-aware allocation discipline is new territory that depends on the link ontology and content mapping ASNs.

VERDICT: REVISE
