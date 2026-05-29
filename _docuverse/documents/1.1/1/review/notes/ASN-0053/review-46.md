# Review of ASN-0053

## REVISE

### Issue 1: WF intro paragraph imagines a case the precondition excludes

**ASN-0053, "Well-formed spans from endpoints" (paragraph before WF)**: "The level_compat precondition is what excludes the troublesome cross-level case: a deeper-level point such as [1, 3, 0, 1] relative to start [1, 3] has divergence([1, 3], [1, 3, 0, 1]) = 3 ... so D0 fails ... When start and reach are level-compatible this case cannot arise..."

**Problem**: This is precondition-justification prose — it elaborates the `#s ≠ #r` cross-level failure that WF's stated precondition `#s = #r` already excludes. It explains *why the precondition is needed* rather than advancing what WF claims. This is the accretion pattern "a paragraph imagines a case the claim's precondition already excludes." A reader following WF must skip past it.

**Required**: Delete the motivating paragraph. WF's `s < r ∧ #s = #r` precondition is self-evident from the claim. If one boundary illustration is retained, keep only the bare counter-instance, not the "this is what excludes the troublesome case" framing.

### Issue 2: S10 Nelson paragraph restates the proof

**ASN-0053, S10 (trailing paragraph)**: "Nelson argues this is structurally guaranteed: 'spans are intervals on a total order. Combining intervals on a total order is set union, which is commutative and associative.'"

**Problem**: The S10 proof has *just* established commutativity/associativity by reducing to set union. The Nelson paragraph then says the same thing in different words — "two paragraphs in the same document say the same thing." It does not advance the argument beyond the four-line proof above it.

**Required**: Drop the restatement, or compress to a single source-citation tag if grounding is wanted. Do not re-argue the proof in prose.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound

The ASN bounds single-span difference (S11–S11d) but not `normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)` for span-sets. This is correctly deferred — Open Question 7 already names it. Not an error here; it belongs to a future ASN.

### Topic 2: Stability of normalized form under allocation

Whether a normalized span-set remains valid/minimal as new addresses are baptized (Open Questions 1, 6) touches allocation dynamics, which this static algebra need not cover.

VERDICT: REVISE
