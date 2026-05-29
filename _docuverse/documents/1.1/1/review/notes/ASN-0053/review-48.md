# Review of ASN-0053

I checked every proof. The mathematics is sound: WR, WF, S1–S11d discharge their foundation preconditions correctly, the level-uniformity hypotheses are genuinely load-bearing and consistently supplied, the SC exhaustiveness and S9 case split are complete, and the boundary cases (empty span-set, single span, equal/contained spans, separated/adjacent difference) are all handled. The S8 sweep-line invariant and the S9 uniqueness case-chase are rigorous, with no proof-by-"similarly" left standing — the symmetric cases (2b, 3a, 3b) are written out in full.

The findings below are the anti-bloat patterns the `review-mode.anti-bloat` classifier directs me to surface. They are accreted meta-prose, not mathematical errors.

## REVISE

### Issue 1: Dead restatement of a foundation definition
**ASN-0053, "The reach function"**: "the unique width w with a ⊕ w = b is the TumblerSub b ⊖ a, whose component formula (TumblerSub, ASN-0034) is `wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k` with k = divergence(a, b)."
**Problem**: TumblerSub is a foundation definition. The component formula is reproduced here but never consulted anywhere in this ASN — every downstream proof uses D0/D1/D2/WR abstractly, never the formula. It is prose the reader must skip. (Rule 7: ASNs may use foundation definitions without restating them.)
**Required**: Cite TumblerSub and write `w = b ⊖ a`; drop the reproduced formula.

### Issue 2: Reach-section paragraph previews WR; the divergence micro-argument is then re-derived twice more
**ASN-0053, "The reach function"**: "D0 ensures the displacement b ⊖ a is a well-defined positive tumbler... The displacement from a to b is recovered faithfully whenever the two endpoints share a length."
**Problem**: This is an informal preview of WR (`reach(σ) ⊖ start(σ) = width(σ)` for level-uniform σ). The same micro-derivation — "equal length excludes the prefix case, so divergence is type (i) with k ≤ #s" — is then performed a second time inside WR's proof and a third time inside WF's proof. WF is the lemma that packages exactly this fact, and S1/S3/S4/S11/S11c correctly cite WF instead of re-deriving. Stating the same content three times before WF exists is accreted duplication.
**Required**: Delete the prose preview. State the equal-length ⇒ type-(i) fact once (in WF, or hoist WF ahead of WR) and cite it; do not re-derive it in WR.

### Issue 3: Worked example forward-references a property defined later
**ASN-0053, S4 worked example**: "Verify S5: d ⊕ d' = [0,...,0,4] ⊕ [0,...,0,4]... Result = ... = ℓ."
**Problem**: S4's worked example verifies S5 before S5 is stated. A reader following S4 hits a reference to a claim that does not yet exist. The S5 verification belongs with S5's own statement, which carries its own worked check.
**Required**: Move the `d ⊕ d' = ℓ` verification to S5, or reorder so S5 precedes the combined example.

### Issue 4: Motivational essay in the introduction
**ASN-0053, intro**: "And he expects front-ends to manipulate them fluently: 'The manipulation of request sets is an important aspect of what front-end functions do...'"
**Problem**: This quote concerns front-end software design, not the span algebra the ASN defines. It is essay content that does not advance any claim. (The adjacent span-set quote and the Gregory merge-site grounding do carry weight — keep those.)
**Required**: Remove the front-end-manipulation quote.

## OUT_OF_SCOPE

### Topic 1: Span operations across hierarchical levels
The ASN restricts merge/split/intersection/difference to level-uniform, level-compatible spans. Intersection or split at a finer hierarchical level (different tumbler lengths) is genuinely new territory and is already named in the Open Questions — not a defect in this ASN.

META: not applicable — the ASN specifies abstract state (spans, span-sets), operations on it (merge, split, normalize, difference), and their invariants (convexity, partition, normalization uniqueness), all stated implementation-independently; it has not drifted.

VERDICT: REVISE
