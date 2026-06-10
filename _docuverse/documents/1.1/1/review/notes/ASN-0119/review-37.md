# Review of ASN-0119

I verified the substance first. The invariant discharge is comprehensive: I checked the full ExtendedReachableStateInvariants conjunct list against the note's coverage and every conjunct is accounted for (the frame-frozen closure rule, the key-set ride-along, the positive S8★ argument via R-BLK/R-CANON, the per-subspace S3★ derivation, and the explicit P4★/P4a/P7a boundary work). The worked pivot (`A B C D E ↦ A C D E B`) and swap (`A B C D E F ↦ A E F C D B`) check out arithmetically — destination ordinals tile, ranges are invariant, the middle's `+1` displacement equals `w_β − w_α`. The four link-contiguity configurations are correct, and the P4a trace-quantified argument is rigorous (the non-REARRANGE-final-composite case is genuinely part of establishing P4a at Σ′, not over-reach — I checked). No correctness or completeness gap survives.

The note carries `review-mode.anti-bloat`, and the residue is meta-prose: two spots where a precise reader must skip past framing to reach the claim.

## REVISE

### Issue 1: S3★ discharge leads with presentation-rationale and method pre-announcement
**ASN-0119, "What is preserved: I-address correspondence" (the S3★ paragraph)**: "We state it per-subspace rather than as the plain `ran(M'(d)) ⊆ dom(C)` because a document's arrangement carries link-subspace V-positions as well... Both inclusions are inherited, but the inheritance runs through the inverse permutation, not through any claim that a position keeps its image — inside the affected interval the image filed at a key generally *does* change..."

**Problem**: Two of these clauses are skippable before the actual proof. (a) "We state it per-subspace rather than..." re-justifies a framing ASN-0047 already fixed (S3★ is stated per-subspace in the foundation) — the note doesn't need to relitigate the foundation's framing choice. (b) "the inheritance runs through the inverse permutation, not through any claim that a position keeps its image" pre-announces the proof method, and the derivation that immediately follows ("Take a text position `v`... `M'(d)(v) = M(d)(π⁻¹(v))`...") demonstrates exactly that, making the pre-announcement redundant. The genuinely informative content — link positions map into `dom(L)`, and `M'(d)(v) ≠ M(d)(v)` inside the interval (a statement of what the operation does, which is fine) — survives in one clause. A reader must wade through ~3 sentences of framing to reach a clean 3-line derivation.

**Required**: Drop straight from the per-subspace statement to the derivation, keeping at most one clause noting link positions map to `dom(L)` (not `dom(C)`) and that images change inside the interval. The `π⁻¹` mechanism speaks for itself in the derivation.

### Issue 2: Foundation-connective meta-commentary that does not advance its local claim
**ASN-0119, "Links" section**: "(This derivation re-proves inline, for REARRANGE, ASN-0098's coverage invariance LP3 and reordering bijection LP11.)"

**Problem**: The RA7a derivation above this parenthetical is complete and self-contained. The note also insists REARRANGE is "distinct from and not reducible to" K.μ~ — so LP11 (stated for K.μ~) does not apply, and RA7a is an *independent* result for a different operation, not literally a re-proof of LP11. The parenthetical is a connective note that neither advances RA7a nor is needed by any downstream claim; it is precisely "meta-prose around a forward reference." A related instance sits in the opening: the parenthetical decomposing K.μ~ — "(a `K.μ⁻ + K.μ⁺` pair that necessarily passes through a content-removed intermediate)" — is exposition of a *foundation* operation's mechanism, and the load-bearing point (REARRANGE ∉ ASN-0047's vocabulary, hence added as an atomic primitive) is established precisely later in the obligations paragraph where it is actually used.

**Required**: Delete the LP3/LP11 parenthetical. In the opening, keep the "what REARRANGE does not do" content (realizes the net change "without ever vacating content") but trim the K.μ~ internal-mechanism exposition; let the obligations paragraph's vocabulary-extension passage carry the atomicity point at the site that needs it. (Minor relative to Issue 1.)

## OUT_OF_SCOPE

### Topic 1: Cross-document boundary-hood, concurrent rearrangement, content-index/fragmentation invariant, prior-arrangement recoverability, closed-form displacement guard
**Why out of scope**: These are correctly captured in the note's own Open Questions and belong to future ASNs (inter-document boundary semantics, concurrency, discovery-index maintenance, version recovery, and the implementation-layer arithmetic guard). The note does not define claims for any of them — it defers them — which is the right disposition. No action needed.

VERDICT: REVISE
