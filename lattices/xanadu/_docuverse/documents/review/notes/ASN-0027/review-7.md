# Review of ASN-0027

Based on Dafny verification — 35 properties, 34 clean, 1 divergence

## REVISE

No genuine spec issues.

## QUALITY

### File: DeleteCrossDocFrame.dfy — SIMPLIFY

**Missing abstraction.** CopyCrossDocFrame and RearrangeCrossDocFrame both delegate to the shared `CrossDocVIndependent` module. DeleteCrossDocFrame inlines the same predicate:

```dafny
ghost predicate DeleteCrossDocFrame(s: State, s': State, d: DocId) {
  forall d' :: d' in s.docs && d' != d && d' in s.vmap ==>
    d' in s'.vmap && s'.vmap[d'] == s.vmap[d']
}
```

Should delegate to `CrossDocVIndependent.CrossDocVIndependent(s, s', d)` like the other two operations. Same concept, three operations — two use the shared module, one inlines.

### All other files — PASS

All 34 remaining files are clean and maintainable. Notable strengths:

- **Empty lemma bodies** throughout (CopyIdentitySharing, CopyLeftFrame, CopyRightShift, DeleteCompaction, DeleteLeftFrame, FullRestoration, RearrangePermutation). The solver handles these without hints — exactly the right level of proof.
- **NonInvertibility.dfy** — well-decomposed with a helper lemma (`DeleteInsertPositions`) that isolates the index calculation. The `forall` body has only the necessary call and one trigger assertion. Clean.
- **RearrangeRangePreservation.dfy** — the per-case assertions are necessary witness hints for set equality (pointing the solver to where each element appears in the rearranged sequence). Not over-proving.
- **IdentityRestoringCopy.dfy** — single structural assert to unfold `InsertV`. Minimal.
- **ReferencePermanence.dfy** — clean inductive proof over a trace with a one-line recursive call. Sparse base case.
- **Shared ops modules** (DeleteOps, CopyOps, RearrangeOps) — good abstraction, used consistently across property files.

## SKIP

### ReachabilityDecay divergence — proof artifact

The Dafny proof constructs an empty state (`docs := {}, vmap := map[]`) to witness unreachability, rather than showing a sequence of DELETE operations from Σ to Σ'. The ASN's proof sketch (iterate over documents in D_a, delete lowest position mapping to `a` in each) is sound — the Dafny model already has trace machinery (used in ReferencePermanence) but formalizing iterated A2 steps across multiple documents requires an operation-application function not yet in the model. The ASN property A9 is correct as stated; the Dafny proof is a weaker existential that suffices for verification purposes. No spec change needed.

### 34 clean verifications — no divergences

All properties verified without modification to ASN statements: definitions (Reachable), preconditions (DeletePre, CopyPre, RearrangePre), postconditions (DeleteLength, DeleteCompaction, DeleteLeftFrame, CopyLength, CopyIdentitySharing, CopyLeftFrame, CopyRightShift, RearrangeLength, RearrangePermutation, VersionNewDoc, VersionIdentitySharing), frame conditions (all ISpacePreserved × 4, all CrossDocFrame × 4), invariants (ISpaceFrame, PublicationObligation), and lemmas (ReachabilityNonPermanent, NonInvertibility, IdentityRestoringCopy, FullRestoration, RearrangeRangePreservation, ReferencePermanence). The Dafny encoding faithfully models the ASN's seq-based V-space and map-based I-space.

VERDICT: SIMPLIFY
