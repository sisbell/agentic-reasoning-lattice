# Channel Assignment — ASN-0086 review-21

**Date:** 2026-05-17 01:17

```
## Issue 1: Seed-independence proof relies on an unestablished contiguous-prefix claim
Reason: The fix is internal — the discipline statement can be tightened (or an inductive sub-lemma added) using only the discipline definition and R0a's sibling-stream invariant. The existing udanax-green characterization (`lowerbound + 1`, already cited in the note) is sufficient evidence for tightening; no new information from Gregory or Nelson is required.
```

```
## Issue 2: R0a's "Symmetrically a' ⊀ a" remark is mislabeled
Reason: Purely presentational — the universal quantification already provides bidirectionality. Fix is to drop or rephrase the remark; no design intent or implementation evidence is needed.
```

```
## Issue 3: R0a's antichain conclusion in Case 1 uses T10a.2 without verifying its sibling-stream precondition
Reason: Internal citation fix. The bridge from "in the stream" to "siblings in A_{d.0.s_L.1}" requires only naming the allocator and invoking T10a.7 (already in this note's foundation citations).
```

```
## Issue 4: R6b "proof" is a single observation rather than a derivation
Reason: Internal structural choice — either redesignate R6b (DEF or COROLLARY) or expand the justification to a 2-3 step derivation from the Definition of `nullified(Σ)`. No external input needed.
```

```
## Issue 5: R0 Step 4's S-invariants summary argument cites preservation by "definitional identity of inputs"
Reason: Internal — the fix is to cite ASN-0036's signature (which excludes Σ.L) rather than asking the reader to enumerate S-invariants. This is a property of ASN-0036's documented signature, already inherited as a foundation in this note.
```

```
## Issue 6: The Definition of `nullified(Σ)` allows a degenerate case the note doesn't address
Reason: Internal design choice. R6 (active subset / retraction) is explicitly described in this note as the substrate's own contribution, not part of Nelson's link model; the asymmetry between syntactic and operational scope is a policy decision for this note alone.
```

```
## Issue 7: R7 Step 3's closure argument scope-shifts mid-paragraph
Reason: Purely structural — separate the derived half (L12/L12a/Frame entail class-(iii)) from the stipulated half (relational-layer commitment routes through Emit_K). No external input needed.
```

```
## Issue 8: Worked Sketch's Step 2 chain reuse claim needs explicit IH
Reason: Internal citation fix — invoke T10a's at-most-once axiom (already in foundation citations) to license uniqueness of the depth-2 allocator's opening spawn, then chain reuse follows directly.
```
