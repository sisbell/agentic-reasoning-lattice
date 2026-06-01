# Review of ASN-0047

## REVISE

### Issue 1: D-CTG★/D-MIN★ "Justification" does not justify the strengthening
**ASN-0047, *Amendments to existing transitions*, D-CTG★/D-MIN★**: "*Justification.* The strengthening drops ASN-0036's link-subspace exemption, requiring D-CTG★/D-MIN★ to hold on `V_{s_L}(d)` as well as `V_{s_C}(d)`."

**Problem**: This is a restatement of the strengthening, not a justification of it. The exemption being dropped exists in the foundation for a documented architectural reason — Nelson's tombstoning design (LM 4/9), cited two sentences earlier as the very thing the exemption "accommodates." The ASN then asserts the opposite (links must be dense/contiguous/suffix-truncatable) and labels the assertion "Justification." This is load-bearing: it forces K.μ⁻ to admit only link-subspace suffix removal, so withdrawing an interior link requires withdrawing every later link (the ASN itself confirms this in worked-example Step 5 and OQ #10). A strengthening that reverses a foundation invariant's documented purpose needs an actual argument for why contiguity is the right contract for the link subspace, not a one-sentence reassertion.

**Required**: Either supply a genuine justification for imposing contiguity on the link subspace, or relabel the strengthening as a provisional modeling choice and state plainly that the tombstoning tension (OQ #10) is unresolved at the point the invariant is introduced — not only in the Open Questions list.

### Issue 2: J4 narrative duplicates Definition (Fork) step (ii)
**ASN-0047, *Coupling and isolation*, J4 intro vs. Definition (Fork) step (ii)**: The J4 paragraph states "The transcluded content source in each case is the K.δ operand, not invariably the base d_src; this is established once in step (ii) of the Definition below," then step (ii) states "The content source is the K.δ operand `d_op`, not invariably `d_src`... This matches Nelson's CREATENEWVERSION... and Gregory's `docreatenewversion`."

**Problem**: Two paragraphs make the identical operand-tracking-content-source point, with the same Nelson (LM 4/66) and Gregory citations, in different words. The J4 paragraph even announces "this is established once in step (ii)" while itself establishing it — the announcement is self-falsifying. This is the "two paragraphs say the same thing" pattern the anti-bloat classifier names.

**Required**: State the operand-tracking content source once (in the Definition box, where it is load-bearing) and reduce the J4 intro to a pointer or a single non-duplicating sentence.

### Issue 3: K.δ freshness mechanism stated in two places with a deferral
**ASN-0047, K.δ case (ii) "*Per-k freshness mechanism (stated once here)*" vs. §*K.δ case (ii) discharge and parent-allocator activation***: The definition's per-k paragraph describes the freshness discharge (frontier check at k=0 via FrontierEquivalence, direct per-`(t,k')` uniqueness at k∈{1,2}); the later section re-describes the same k=0/k∈{1,2} freshness discharge under "parent-allocator activation."

**Problem**: The "stated once here" marker is contradicted by the later section repeating the freshness split; the definition defers parent-allocator activation downstream while restating the freshness half it claims to own. This is the "multiple paragraphs defer to the same downstream location" + restated-mechanism pattern, compounding an already very large K.δ definition.

**Required**: Keep the freshness mechanism in exactly one location and have the other reference it without re-deriving the per-k split.

## OUT_OF_SCOPE

### Topic 1: Tombstoning / interior link withdrawal mechanism
**Why out of scope**: The reconciliation of D-CTG★/D-MIN★ with Nelson's tombstoning (a status flag / retraction mechanism enabling interior link removal) is correctly deferred to OQ #10 and belongs in a future ASN. Only the *justification gap at the point of introduction* (Issue 1) is in scope here.

VERDICT: REVISE
