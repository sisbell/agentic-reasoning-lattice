# Channel Assignment — ASN-0086 review-49

**Date:** 2026-05-18 03:31

```
## Issue 1: R7a's proof gap for ↝-steps that add documents
Reason: The fix is internal — choosing among (a) restricting R7a's scope, (b) reformulating to allow interleaved class-(i)/(ii) setup steps, or (c) adding a proof obligation is a structural decision about R7a's claim, derivable from the frame conditions and L1a already in the note.
```

```
## Issue 2: R0 Step 4's grouped L-invariant verification
Reason: Each L-invariant is defined in ASN-0043; per-invariant discharge requires only reading those definitions and writing one line each. No design intent or implementation evidence needed.
```

```
## Issue 3: Inconsistency between State transition relation and Substrate emission primitive
Reason: The fix is to make the note's own internal labeling consistent — class (iii) should be named uniformly as either the disciplined or broader primitive. The note already articulates the "most natural reading"; clarification is editorial.
```

```
## Issue 4: Convention — RetractionDirectionality is load-bearing without principled rationale
Reason: Option (a) requires understanding whether retraction has a canonical direction in the design intent; option (b) is internal symmetric restatement. Nelson can clarify whether the design intends a directional retraction semantics or treats it symmetrically.
Nelson question: In the design of typed relations with retraction semantics, did Nelson intend a canonical direction (to-set carries retraction targets) or treat retraction as direction-symmetric over the link's endsets?
```

```
## Issue 5: Emit_K's seed-independence is conditional on the trajectory, not on the state
Reason: Option (a) elevates the sibling-frontier discipline to a substrate-level guarantee — a design decision needing both intent (Nelson) and implementation evidence (Gregory) to determine if this is feasible and faithful. Option (b) is internal restructuring.
Nelson question: Was the sibling-frontier emission pattern intended as a substrate-level invariant of link allocation, or as an implementation choice on top of a broader address-emission primitive?
Gregory question: Does udanax-green's link allocation primitive (e.g., `findisatoinsertmolecule`) unconditionally enforce sibling-frontier placement, or can callers/code paths produce link addresses that are strict prefix-extensions of existing link addresses?
```

```
## Issue 6: Meta-prose accretion flagged by the review-mode.anti-bloat classifier
Reason: Pure stylistic cleanup. Removing meta-prose, terminology notes, hypothesis classifications, and forward-reference rationales requires only editing the note itself.
```

```
## Issue 7: R5's Stage 2 use-site inventory
Reason: The reduction is internal — replacing the exhaustive enumeration with a single load-bearing statement uses only L4(c), L13, and R0, all already named in Stage 1.
```

```
## Issue 8: Multiple "see X below" / "deferred to Y" patterns
Reason: Internal restructuring — linearizing cross-references requires only reorganizing the note's own prose, no external input.
```

```
## Issue 9: Worked Sketch covers one cycle without `↦`-transition example
Reason: Either extending the sketch with an `↦`-step or dropping R6c-Corollary is a decision derivable from the note's own definitions of `↦`, arrangement modifications (ASN-0036), and `A_K`'s dependence on `Σ.L`.
```

```
## Issue 10: SharedDepthOneAllocator lemma's step (d) is asserted, not proved
Reason: T10a's at-most-once axiom is defined in ASN-0034; the additional sentence citing it and deriving `(d.0.s_C, 1) ≠ (d.0.s_L, 1)` from the subspace-distinctness hypothesis is internal.
```
