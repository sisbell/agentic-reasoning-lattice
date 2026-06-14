# Review of ASN-0131

I read this as a query-operation note: `RE(W, d, Σ)` surfaces the role-tagged endsets of addressable links whose coverage overlaps a content region's image, withholding link identity. I checked the definition, every derived claim, the worked instance, and the stability suite.

**Correctness is sound.** I could not break any proof:

- RE-DEF, RE-LOC, RE-OVL, RE-BND, RE-SND, RE-CMP are correct reads of the definition; the `I ⊆ dom(Σ.C)` step is correctly discharged by S3★ under the `W ⊆ s_C` obligation.
- RE-ADDR's antichain argument (R0a + unit-depth to-set ⟹ only a self-emitter-retraction covers `ℓ_new`) is valid, and the `Σ.L`-evolution bridge legitimately imports the ASN-0086 lemmas it leans on.
- The worked instance is faithful: `coverage(e₁)` first span = `{t : a₂ ≤ t < a₄}` (via `shift(a₂,2)=a₄`), the `e₃`/to-set field-agreement disjointness arguments are rigorous (3 separators transfer, forcing `E(c)₁ = E(ℓ)₁ ≠ s_C`), and `RE = {(1,e₁)}` exercises RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT correctly.
- RE-UDIST is correct; RE-UDIST-∩'s two counterexamples (one non-injective, one *injective* via split touch-witnesses) genuinely show no arrangement restriction recovers `⊇`, and the necessary-and-sufficient touch-implication is right.
- RE-CWP and RE-RET are the most intricate and both hold: the wp pullback (`coverage(e) ∩ Δ ≠ ∅ ⟹ coverage(e) ∩ I_R ≠ ∅`) is the correct "nothing dropped" condition, strictly finer than D-CWP's per-link form; "drops iff sole addressable bearer" survives both directions under the flagged net-removal hypothesis (R-Scope confines the new nullification to `ℓ`; L12 + frame keep any other bearer alive).

No correctness or missing-case REVISE items. The remaining findings are anti-bloat only — the note carries the `review-mode.anti-bloat` classifier, and trace meta-prose has accreted.

## REVISE

### Issue 1: Forward-reference parenthetical interrupting the extent argument
**ASN-0131, "Extent: the surfaced endset, whole and unclipped"**: "(That every returned pair is a *genuine* slot-`i` endset of an addressable link touching the region — its provenance — is the soundness direction, established below as RE-SND; here we sharpen the separate question of **extent**.)"

**Problem**: This is meta-prose the extent argument does not consume — a forward reference to RE-SND ("established below") whose only function is to pre-delimit the section against a claim made two sections later. The section's own opening sentence ("not an approximation of it, and not a fragment of it trimmed to the region") already fixes the extent focus, so the precise reader skips the parenthetical to reach the load-bearing RE-CLIP/RE-WHOLE distinction. This is exactly the "skip past meta-prose to follow the claim" pattern.

**Required**: Delete the parenthetical. The extent focus is carried by the surrounding prose without it.

### Issue 2: Redundant restatement of the `addressable` definition
**ASN-0131, "Under retraction"**: "a retraction marks it nullified (ASN-0086), and we range only over `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`."

**Problem**: The full formula `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)` was already defined in "The unit of the answer: anchoring without names" ("the **addressable** links: `addressable(Σ) = dom(Σ.L) ∖ nullified(Σ)`"). Re-writing the formula verbatim at the retraction section is the "two paragraphs say the same thing" pattern — by this point the reader knows `addressable`; "we range only over the addressable links" suffices. A secondary throat-clear in the same neighbourhood ("for one shared reason worth isolating") signals structure rather than advancing it.

**Required**: Recall `addressable` by name at the retraction section rather than restating its definition; drop the "worth isolating" filler.

## OUT_OF_SCOPE

The note's own Open Questions (rendered-mode answers OQ3, type-slot-vs-content matches OQ6, link-subspace regions `W ⊆ s_L` OQ7, the weakest structurally-restricted intersection-equality condition OQ4) are correctly deferred — each is genuine future territory, not a gap in this note. The whole-vs-touching-spans choice (RE-WHOLE, OQ1) is honestly held provisional while RE-CLIP stands firm, which is the right separation. These should not be pulled in as REVISE work.

VERDICT: REVISE
