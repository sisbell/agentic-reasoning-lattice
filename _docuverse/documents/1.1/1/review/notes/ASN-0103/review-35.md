# Review of ASN-0103

This ASN is mathematically sound. The `D_A = E ∩ S(A, 2)` lemma proves both inclusions explicitly, the freshness argument (`d ∈ S(A,2) \ E`) is clean, the version/document length filter is genuinely load-bearing and demonstrated concretely in the worked example, and every conjunct of `ExtendedReachableStateInvariants` is discharged (directly, vacuously, or by frame). The proofs hold. My findings are confined to the meta-prose patterns the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: S3★ discharged twice via forward reference
**ASN-0103, Effect Two / Invariants Maintained**: Effect Two states "We note one consequence immediately, to be discharged as an invariant below: with `ran(M'(d)) = ∅`, referential integrity ... holds vacuously for `d`." The Invariants section then re-derives it: "*Referential integrity (S3★...).* For `d`: `ran(M'(d)) = ∅ ⊆ dom(C')`, vacuously."
**Problem**: This is a forward-reference deferral ("to be discharged as an invariant below") whose content is then restated in full at the downstream location — the exact accretion pattern flagged for this review. The Effect Two aside does not advance Effect Two's reasoning (which is about emptiness); it previews a discharge that the Invariants section already owns.
**Required**: Discharge S3★ once, in the Invariants section. Drop the Effect Two preview, or if a plain-language consequence is wanted there ("an empty document cannot dangle"), keep that sentence without the "to be discharged below" deferral and without the duplicate vacuity derivation.

### Issue 2: Editorializing exhaustiveness clause in the freshness argument
**ASN-0103, Effect One, "Freshness and distinctness"**: "... whence `d ∉ E` — closing freshness against nodes, accounts, documents, and versions at once, with no case split."
**Problem**: The substantive claim (`d ∉ E`) is fully established by the preceding `d ∈ S(A,2) \ E` step. The trailing clause is an exhaustiveness/economy claim editorializing about the proof ("at once, with no case split") rather than advancing it — noise the reader steps past after the conclusion is already reached.
**Required**: End the sentence at `d ∉ E`. The fact that `E` comprises nodes/accounts/documents/versions needs no restatement here, and "with no case split" is self-congratulation, not reasoning.

## OUT_OF_SCOPE

(none — the CREATENEWVERSION contrast in "What Distinguishes Creation From Forking" is a statement of what the operation does *not* do, which the anti-bloat criteria explicitly exclude from meta-prose; CND.no-sharing is an in-scope claim about the created document.)

VERDICT: REVISE
