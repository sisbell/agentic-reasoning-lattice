# Channel Assignment — ASN-0086 review-23

**Date:** 2026-05-17 02:23

```
## Issue 1: R6's framing as "the substrate's own contribution" overstates what R6 actually claims
Reason: Fix is a reframing of which lemma carries the conceptual load (R6 vs. R6a + the active/audit distinction). Derivable from the ASN's own structure — the substantive content is already there, only its labeling needs adjustment.
```

```
## Issue 2: The Shared depth-1 element-field allocator derivation is dense and would benefit from being a named lemma
Reason: Fix is structural reorganization — lifting an existing derivation to a named lemma with explicit proof structure citing TA5(d), T10a, S7d from ASN-0034/0036. All inputs are already in the ASN family; no new content is needed.
```

```
## Issue 3: The worked sketch underexercises boundary cases relative to the abstract claims
Reason: Fix is adding concrete traces (alternate-d_retr; Observe_K invocation) that exercise definitions already present in the ASN. All needed semantics (Emit_K's caller-supplied home, Observe_K's hist/oper views) are fully specified internally.
```

```
## Issue 4: The Subspace-distinctness axiom's relationship to ASN-0043's L0/L0a partition is underspecified
Reason: The reviewer's analysis — that L0a's slice definition and L14's scoped disjointness presuppose s_C ≠ s_L — is verifiable by re-reading ASN-0043's L0/L0a/L14 statements. The reframing ("naming explicitly" rather than "axiom of this note") is internal expository work.
```

```
## Issue 5: R7's "stipulated half" framing could mislead about the reduction's scope
Reason: Fix is adding forward-references from R6(d) and the abstract paragraph to R7's existing Step 3 decomposition. The proven/stipulated decomposition is already in the ASN; only its visibility at earlier touch-points needs strengthening.
```

```
## Issue 6: R0a-Cor1's proof relies on the strengthened invariant as IH without explicitly noting the strengthening direction
Reason: Fix is adding one clarifying sentence distinguishing the inherited ⊆ direction (from R0a's sibling-stream invariant) from the strengthened ⊇ direction (contiguous prefix, no gaps). Pure exposition; the proof's inductive logic is unchanged.
```

```
## Issue 7: R0 Step 2 Case A's sibling-sweep argument relies on the sparse-allocator semantics established at the substrate primitive — the dependence could be more visible at the proof site
Reason: Fix is adding a local pointer from the sibling-sweep step back to the sparse-allocator paragraph (already established earlier in the note with both Nelson and Gregory grounding). The semantic commitment exists; only its non-local dependence needs flagging at the proof site.
```
