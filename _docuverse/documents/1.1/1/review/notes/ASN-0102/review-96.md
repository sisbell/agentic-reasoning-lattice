# Review of ASN-0102

I read the full note, checked each X-claim's proof (especially the wp/S3★ reduction, the X16 tiling, and the X14 invariant discharge), and verified the worked examples against the boundary cases (empty subspace, append, prepend, self-transclusion, cross-origin, coalescing). The mathematics is sound: the tiling in X16 is explicit and gap-free, the wp computation in the "What is preserved" section genuinely reduces S3★ to the copied-region obligation, and the boundary/per-state distinction in X14 is handled correctly. I could not find a rigor error. The findings below are anti-bloat / presentation items, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: X2 restates ASN-0093's K.α allocation mechanics rather than using them
**ASN-0102, X2 (NoFreshAllocation)**: "K.α selects between two cases on the per-document content set `D_d`... When `D_d = ∅` the next address is the *first emission* `[d.0.s_C.1]`... When `D_d ≠ ∅` the next address is the *subsequent emission* `inc(a_prev, 0)` off the per-document frontier..."
**Problem**: The claim "COPY consumes no previously-unallocated address" is a one-line corollary of X1 (`dom(Σ'.C) = dom(Σ.C)`) and X6 (no origin altered): `D_d` is identical at `Σ` and `Σ'`, so any subsequent K.α behaves identically. The verbatim re-derivation of K.α's first-emission/subsequent-emission case split reproduces ASN-0093 foundation mechanics that the ASN should reference, not restate. It does not advance COPY's argument.
**Required**: Collapse to the corollary — "X1 and X6 leave `D_d = {a' ∈ dom(Σ.C) : origin(a') = d}` unchanged, so K.α's selection (whichever case) is identical at `Σ'` and `Σ`" — and drop the per-case anchor reconstruction.

### Issue 2: X14's label understates its scope, obscuring the invariant-maintenance argument
**ASN-0102, X14 (ContainmentRecording)**: a single claim body discharges (SL), J0/J1★/J1'★, P7, the entire `ExtendedReachableStateInvariants` per-state conjunction (S2, S3★, S3★-aux, S8a, S8★, D-CTG★/D-MIN★/D-SEQ★, S8-depth, S8-fin, the frame-trivial L-/C-/E-invariants, ...), the composite-boundary properties P4★/P4a/P7a, and the transition theorem P3.
**Problem**: A reader looking for "does COPY preserve S3★ / S8★ / P3?" must dig through a claim named *ContainmentRecording*. The breadth is necessary (every conjunct must be addressed), but bundling the full reachable-state and transition discharge under a containment label buries the load-bearing invariant-maintenance proof. The "Frame-trivial invariants" inventory and the boundary-property discharge are distinct concerns from the provenance write.
**Required**: Split the invariant-maintenance discharge (per-state + boundary + P3) into its own claim, leaving X14 to state only the containment recording and the step-local fact (SL); or rename X14 to reflect that it is the operation's invariant-preservation theorem.

## OUT_OF_SCOPE

### Topic 1: discoverability/identity under later displacement and unreachability (Open Questions)
**Why out of scope**: The four Open Questions (re-displacement and discoverability, transitive containment when a referencing document is itself a source, time-varying views, identity when the allocating document is unreachable) are genuine future-ASN territory — they concern link projection (ASN-0098 lineage) and reachability concepts this operation ASN correctly does not introduce. Properly left as open questions.

VERDICT: REVISE
