# Review of ASN-0100

This is a thorough, genuinely rigorous operation spec. The substrate decomposition is correct, the three-region partition is proved disjoint and exhaustive, the closed-interval D-CTG★ reduction handles the live `m≥3` off-prefix case (and the deep-subspace example exercises it concretely), and the invariant coverage is complete (S2, S3★, S4, S7*, S8*, D-*, L*, P*, J*, P3, plus the composite-boundary trio). The wp analysis hits two non-trivial cases. No correctness or missing-case gaps found. The findings below are the prose-accretion patterns the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Chain-index/V-position decoupling stated twice within one example
**ASN-0100, §A Worked Example — "Re-insertion into a cleared content subspace"**: the example body states "the decoupling of the V-position index from the I-address chain index: the I-addresses resume the chain at indices 3 and 4 (the chain never restarts), yet the V-positions restart at `[s_C, 1]`," and then the closing paragraph restates it whole: "The chain index advances monotonically across the document's whole history ... while the V-position numbering is re-pinned to `[s_C, 1, …, 1]` on every re-insertion into an emptied subspace. The two indices are independent."
**Problem**: The closing paragraph adds no new content over the example body's own statement of the same point — two paragraphs, same claim. This is the "two paragraphs say the same thing in different words" pattern.
**Required**: Drop the closing paragraph; the concrete walk-through (indices 3,4 vs. V-positions `[1,1],[1,2]`) already carries the decoupling.

### Issue 2: Residual-content branch-selection mechanism developed twice
**ASN-0100, §Effect One: Allocation**: the branch-selection nuance is fully developed in prose — "The branch selection keys on the *content store*, not the *arrangement* ... an empty content subspace `V_{s_C}(d) = ∅` does not entail an empty content store ... So when residual content persists ... the *subsequent*-emission branch selected above off the persisted frontier `a_prev` is the one that fires — continuing `A_C(d)`'s chain rather than restarting it — even though `V_{s_C}(d)` is empty." The "Re-insertion into a cleared content subspace" example then re-narrates the identical mechanism in prose ("By S0/P0 the addresses ... persist in `dom(Σ.C)`, so although `V_{s_C}(d) = ∅`, the residual set ... ≠ ∅ with frontier `a_prev` ...") before its concrete walk-through.
**Problem**: The mechanism is explained at length in Effect One and re-explained in the example's preamble. The example's *concrete* content (addresses `[d.0.s_C.3]`, `[d.0.s_C.4]`) is legitimate; the prose preamble restating Effect One's principle is the accretion.
**Required**: Keep the principle in one place (Effect One), reduce the example to its concrete instantiation, or vice versa — not both narrated in full.

## OUT_OF_SCOPE

(none — the "Bounding the Scope" section lists DELETE/COPY/REARRANGE/version/BEBE as excluded, which matches the declared scope; the ASN defines no claims for them, so no flag is warranted.)

VERDICT: REVISE
