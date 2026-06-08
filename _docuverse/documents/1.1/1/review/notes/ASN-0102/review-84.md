# Review of ASN-0102

## REVISE

### Issue 1: Composite-coupling deferral stated three times in X14
**ASN-0102, X14 (ContainmentRecording)**: the claim that the composite couplings (J0, J1★, J1'★) and boundary properties (P4★, P4a, P7a) are not COPY's obligation is asserted three times in different words:
- "they are that composite's obligation, not the elementary step's, and we do not re-prove them here with a private boundary apparatus."
- "composite-wide coupling validity then follows from (SL) and ValidComposite★'s own boundary evaluation across the embedding composite."
- "they are evaluated only at composite boundaries, so an embedding composite discharges them from (SL) plus ValidComposite★'s boundary evaluation, not COPY's elementary step."

**Problem**: This is the anti-bloat "multiple paragraphs defer to the same downstream location" pattern. The deferral is announced up front, restated mid-paragraph (J0/J1★), and restated again at the P4★ sentence. Only the J0/J1★ work (J0 vacuous via X1; J1★ via SL) advances the argument; the surrounding deferral framing is the same point thrice. The phrase "we do not re-prove them here with a private boundary apparatus" is additionally defensive residue describing what the note *no longer does* (a stripped prior structure), not what COPY establishes.
**Required**: State the composite/elementary obligation split once (where SL is introduced), give the J0-vacuous and J1★-via-SL facts, and delete the up-front announcement and the closing P4★ restatement. Drop "with a private boundary apparatus."

### Issue 2: Self-transclusion well-definedness argued twice in prose
**ASN-0102, source-designation intro and X10(b)**:
- intro: "This single pre-state pinning is what makes self-transclusion (`d_s = d`) well-defined: the copied span is read from the frozen pre-state image even as `d` is simultaneously displaced."
- X10(b): "the guarantee that holds here is not non-alteration but *pre-state resolution*: for `d_s = d`, the target-as-source is read at the pre-state `Σ` and is itself displaced by `· + W`."

**Problem**: Both passages make the identical well-definedness argument in different words. The intro sets the resolution convention; X10(b) restates the same justification rather than relying on the convention already fixed. (The worked-example restatement is exempt — it is a concrete demonstration, not duplicated reasoning.)
**Required**: Fix the convention once (intro) and have X10(b) state the guarantee by reference to it, without re-deriving the snapshot rationale.

## OUT_OF_SCOPE

None. The note correctly confines INSERT/DELETE/version/link topics to comparisons and open questions, defining no out-of-scope claims. The invariant discharge in X14 is complete (every conjunct of ExtendedReachableStateInvariants and P3 is addressed), the X16 tiling and S2/S8a arguments are rigorous, and the worked examples exercise the boundary cases (empty subspace, append, self-transclusion overlap, coalescing merge). The remaining issues are prose-level repetition, not correctness gaps.

VERDICT: REVISE
