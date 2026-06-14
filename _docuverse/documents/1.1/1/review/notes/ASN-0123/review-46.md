# Review of ASN-0123

I checked the operation contract and the load-bearing proofs (VN-B1, V-WF, V3, the V8 coverer-set argument, the V9 severance theorem and its structural O5(ii) discharge, V10/V13, and both worked instances). The mathematics is sound: the case analyses are complete, the boundary case `n = 0` is handled, the cross-owner branch's freshness is correctly routed through ChildSpawnFreshness/FrontierEquivalence, and the worked instances' arithmetic (content addresses `[d.0.s_C.k]`, the position-4 divergence in the cross-owner instance) checks out. The findings below are confined to the meta-prose accretion the `anti-bloat` classifier flags.

## REVISE

### Issue 1: the J4 remark restates its own point

**ASN-0123, "Remark (relation to the foundation's fork composite)"**: "Where J4's bookkeeping ties its content operand to the version frontier, CREATENEWVERSION fixes the content operand to the named source at every invocation; the two coincide on first forks and whenever the source is unmodified between forks. The operation specified here follows the request's semantics: each call snapshots the document named in it."

**Problem**: The first clause ("fixes the content operand to the named source at every invocation") and the last sentence ("each call snapshots the document named in it") assert the identical fact — VERSION uses named-source rather than frontier-operand semantics. Only the middle clause (the coincidence condition) carries new content. The remark sits between the contract and V-WF; the reader skips the restatement to reach the proof.

**Required**: One sentence — the distinction from J4 is the named-source operand, true except where the source is unmodified between forks. Drop the third sentence.

### Issue 2: the P-tier precondition slot carries a downstream preview and a defensive aside

**ASN-0123, The Operation (P-tier comment)**: "...its first disjunct serves the owned fork at any forker tier, its second the cross-owner fork, restricted to an account-tier forker (zeros(pfx(π)) = 1) so the fork mints exactly one identity (reaching a document from a node prefix is an out-of-scope prior act). V0 carries the count over the two in-domain branches."

**Problem**: Inside the precondition slot, this re-explains what the identity clause (immediately below) shows and what V0 (count), V8 (owned ownership), and V9 (cross-owner) prove downstream — a use-site preview, not a statement of the precondition. The parenthetical "(reaching a document from a node prefix is an out-of-scope prior act)" is a defensive justification for the account-tier restriction. (The neighbouring "no authority over d_src is required" and "no condition is placed on M(d_src)" are statements of what the operation does *not* require and should stay.)

**Required**: Keep only the precondition's own content — P-tier is the domain delimiter, well-formed because PS makes `ω` total on `E`. The disjunct-to-branch mapping and the count are proved at V0/V8/V9; delete them and the out-of-scope parenthetical from the slot.

### Issue 3: V12's formal claim is buried in philosophical restatement

**ASN-0123, V12**: "The fork separates them at totality: a document whose every arranged byte was authored elsewhere is nonetheless a distinct document with a distinct, permanent address. That is the stronger refutation, because two identities cannot have been individuated by two contents when there is only one content. The boundary runs exactly where the state model put it: identity lives in the allocation tree (E), content in C, and the arrangement M ... is the relation between them."

**Problem**: V12's load-bearing content is the formal consequence (`d_src ≠ v` yet `M'(v) = M'(d_src)|...`, so the identity→content map is non-injective by construction) and the empty-vs-totality contrast that distinguishes a real boundary case. The quoted sentences then restate that conclusion three ways — "the stronger refutation," "individuated by two contents," "the boundary runs exactly where the state model put it" — adding no formal step. This is essay in a claim slot.

**Required**: Keep the non-injectivity claim and the empty/totality distinction; trim the triple paraphrase of "identity ≠ content."

### Issue 4: the copy-refutation is made twice

**ASN-0123, The Problem ("The copy") and G2**: The Problem — "a strap holding the original bytes holds no copy of them: every link made against the source's content comes up empty in the version (LP12)... attribution is forged: the copies' origin ... names the version." G2 — "the strap that holds a holds no copy of a... Under copying, coverage ∩ ran(Σ'.M(v)) = ∅ for every anchor in the source — carry-through fails totally... forges attribution (the copy's origin names the version, S7)."

**Problem**: The three-failure refutation (carry-through, correspondence, attribution) and the "strap holds no copy" image appear once qualitatively (The Problem) and once formally (G2). The motivate-then-derive structure justifies *some* overlap, but the identical metaphor and identical failure list in both is the "two paragraphs say the same thing in different words" pattern. (This is the softest of the four — the two-phase structure is a partial defense.)

**Required**: Let G2 carry the formal refutation; reduce The Problem's "The copy" to the bare assertion that copying fails, without pre-staging the three failures and the strap image.

## OUT_OF_SCOPE

### Deferred topics are correctly scoped, not missing
Windowing/source-tracking (touched in V11), version comparison, concurrent-fork serialization (the atomicity remark), and withdrawal/supersession are all routed to the Open Questions rather than specified here — appropriate, and not gaps in this ASN. The cross-owner branch's reliance on ASN-0047's document sub-allocator (rather than re-specifying CREATENEWDOCUMENT) keeps document-creation-from-scratch correctly out of scope while still admitting the cross-owner fork.

VERDICT: REVISE
