# Review of ASN-0131

I checked each introduced claim against its proof and against the foundations. The technical content is sound: RE-NCD's cross-subspace disjointness argument (separator-zero coincidence forcing `E(c)₁ = E(s)₁`), RE-ADDR's fresh-output addressability (antichain + P-tgt + self-retraction case split), RE-UDIST and the one-sided RE-UDIST-∩ with both obstruction constructions, RE-CWP's weakest-precondition derivation against the D-CWP bridge, and the forward/backward halves of RE-RET (R-Scope confinement, L12 value-fixity, image-fixity) all hold. The worked instance computes correctly and exercises every distinctive postcondition. Boundary cases (empty image, empty `W`, no addressable links, empty endset slot, `coverage(∅)`) are covered by RE-BND. Soundness and completeness are honest reads of the biconditional. No technical REVISE.

The note carries `review-mode.anti-bloat`, and two residual prose duplications remain after the prior cycle's tightening.

## REVISE

### Issue 1: Unit-depth confinement rationale stated twice
**ASN-0131, RE-NCD lemma block and §Stability (retraction)**: The lemma block closes with "The reduction to the prefix relation `s ≼ c` is what confines the lemma to unit-depth spans." The retraction subsection then makes the same point where it is actually used: "RE-NCD is confined to unit-depth spans, where coverage reduces to the prefix relation `s ≼ c`; across the interior of a *wide* span `(s, ℓ_s)` that argument fails...".
**Problem**: The closing sentence at the lemma's own site is a forward-looking remark with no local use — the confinement matters only at the type-slot discussion, where it is re-derived. A reader meets the same "unit-depth because coverage reduces to `s ≼ c`" claim twice, the first occurrence purely foreshadowing the second.
**Required**: Drop the RE-NCD closing sentence; the retraction subsection supplies the confinement fact at its point of use without loss.

### Issue 2: "No injectivity-style restriction recovers ⊇" previewed, then proved, then restated
**ASN-0131, §Composing regions (intersection)**: The reverse-inclusion paragraph opens "The reverse inclusion, by contrast, **fails in general** — and, decisively, *no injectivity-style structural restriction on the arrangement recovers it*." This is specifically obstruction 2's result, but it is asserted *before* obstruction 1 (which concerns non-injectivity, a different route). Obstruction 2 then restates it ("*no injectivity-style restriction escapes it*") and the construction concludes it ("The `⊇` direction fails with `Σ.M(d)` **injective**").
**Problem**: The opening headline duplicates the conclusion obstruction 2 earns, and sits ahead of obstruction 1, which establishes a distinct point. The "no injectivity helps" meta-claim is thereby stated three times; following the failure argument requires skipping past the preview to reach the construction that proves it.
**Required**: Remove the preview clause "and, decisively, *no injectivity-style structural restriction on the arrangement recovers it*" from the opening sentence (keep "fails in general"); let obstruction 2 carry the injectivity headline once, where the injective construction earns it.

## OUT_OF_SCOPE

None to add. The seven Open Questions and the Scope declaration appropriately defer the touching-spans return value (Q1), multiplicity preservation (Q2), V-rendered answers (Q3), the structural intersection-equality condition (Q4), cross-store completeness (Q5), type-slot-against-content semantics (Q6), and link-subspace regions (Q7), and correctly route FINDLINKSFROMTOTHREE / pagination / READLINK / traversal / creation to their sibling ASNs.

VERDICT: REVISE
