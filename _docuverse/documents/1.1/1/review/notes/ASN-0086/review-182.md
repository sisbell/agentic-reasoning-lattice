# Review of ASN-0086

I checked every proof (R0, R0a, R1–R7a, L-ContiguousPrefix, the wp analysis, and the worked sketch's tumbler arithmetic) against the foundation contracts. The logical content is sound: boundary cases (first emission, subsequent emission, self-nullification, nullifying a non-link address, empty homed-set) are all covered, the worked sketch's arithmetic verifies, the wp is genuinely non-trivial, and consequences are derived. I found **no correctness or missing-case defects**.

The note carries the `review-mode.anti-bloat` classifier, and the two findings below are accretion, not correctness. Both impede a precise reader who must skip past prose that no downstream claim consumes.

## REVISE

### Issue 1: Implementation aside between a definition and R7a advances no part of R7a's reasoning
**ASN-0086, after "Definition — substrate-conforming layer"**: "In udanax-green every link-writing operation adds exactly one fresh link key: CREATELINK is the only operation that writes links, and although it issues several spanf writes per call, all but one are endpoint *index* entries (LINKFROMSPAN/LINKTOSPAN), not new link keys — so the decomposition runs at `m = 1` for every present operation."

**Problem**: R7a is proved for arbitrary `m ≥ 1`, and its decomposition is used by R6d only as a finite K-step chain — neither consumes the fact that current implementations happen to run at `m = 1`. The sentence is a standalone aside sitting in a structural slot between the substrate-conforming-layer definition and R7a; to follow R7a one skips it. (Implementation grounding that feeds a premise — as in T0(a), TA4 — is legitimate; this one feeds nothing.)

**Required**: Drop the paragraph, or relocate the `m = 1` observation to a non-load-bearing remark explicitly marked as illustration, so it is not read as setup for R7a.

### Issue 2: The relational-layer reduction corollary front-loads an R7a-applicability argument its core claim disclaims needing
**ASN-0086, "Corollary (reduction to Emit_K)" proof**: Paragraph 1 checks the layer against *Definition — substrate-conforming layer*, concludes "R7a's pre-state hypothesis is then met from the outset," and derives that every reached state is substrate-conforming. Paragraph 2 then states: "The relational layer's own reduction follows directly from its *Definition*, **without invoking R7a** ... So every `Σ.L`-affecting step the layer takes simply *is* an `Emit_K` call — at `m = 1`, with nothing to decompose."

**Problem**: The corollary's stated claim (reduction of the layer's state-affecting operations to `{Emit_K}`) is established entirely by Paragraph 2's first half, which the proof itself flags as not invoking R7a. The whole of Paragraph 1 (substrate-conformance + R7a-hypothesis-meeting) is consumed only by Paragraph 2's final sentence ("R7a additionally covers composite extensions"). A reader tracking the corollary's actual claim skips Paragraph 1.

**Required**: Move the R7a-applicability setup into the single "composite extensions" sentence it serves (or cut it if composite extensions are out of scope here), leaving the corollary's proof to the direct one-line reduction.

## OUT_OF_SCOPE

The Open Questions (cross-`L_K`/`Σ.M` visibility invariants, multi-arity relations `L_K^{(n)}`, concurrency/atomicity model for Observe vs. Emit, cardinality bounds on `nullified`, dynamic type-address coordination) are correctly deferred — they concern relations the substrate does not yet define and belong in successor notes, not in this revision.

VERDICT: REVISE
