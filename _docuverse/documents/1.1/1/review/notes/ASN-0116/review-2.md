# Review of ASN-0116

## REVISE

### Issue 1: New-block well-formedness is not discharged by the cited ASN-0082 lemmas

**ASN-0116, "The document remains one coherent sequence"**: "We do not re-prove well-formedness: it is exactly ASN-0082's post-insertion preservation family — … I3-VD (depth uniformity) and I3-VP (S8a) for the positions, I3-S2 for single-valuedness, I3-fin for finiteness, I3-S3 for referential integrity."

**Problem**: ASN-0082's I3 family explicitly excludes the new content positions. I3-CS (PostInsertionSubspaceClosure) characterizes `dom(M'(d)) ∩ subspace S` as *left positions ∪ shifted positions only* — the block `{shift(p,k) : 0 ≤ k < n}` is withheld (I3-V). Consequently ASN-0082's M'(d) is the *gapped*, room-made arrangement, and its preservation lemmas (I3-VP, I3-VD, I3-S2, I3-fin, I3-S3) establish well-formedness only for the left+shifted regions. They say nothing about the new block. INSERT's filled post-state adds `{shift(p,k)}` mapped to `{shift(a,k)}`, and these positions need their own discharge: S8a (via OrdShiftHom on `p`), depth uniformity (`#shift(p,k) = m`), single-valuedness (disjointness from the shifted/left images — the gap intervals), and referential integrity (`shift(a,k) ∈ dom(C')` by I-ALLOC). None of these is inherited; each is an INSERT obligation.

**Required**: State and prove well-formedness for the new-block positions explicitly, rather than attributing it to ASN-0082 lemmas that demonstrably cover only the gapped arrangement.

### Issue 2: Contiguity is miscited; the lemmas named are contraction lemmas

**ASN-0116, same paragraph**: "it is exactly ASN-0082's post-insertion preservation family — D-SEQ-post/D-MIN-post (min(V_S(d')) = q_1)/D-CTG-post (contiguity) for the dense run …"

**Problem**: In ASN-0082, D-SEQ-post, D-MIN-post, and D-CTG-post are **contraction** (D-family) lemmas — D-SEQ-post is literally `V_1(d) = {[1,k] : 1 ≤ k ≤ N − c}`, where `c` is the contraction amount. They are not insertion lemmas. Moreover there *cannot* be an insertion-side contiguity lemma to inherit: ASN-0082's post-insertion arrangement is gapped (`{q_1,…,q_{J-1}} ∪ {q_{J+n},…,q_{N+n}}`, hole at `{q_J,…,q_{J+n-1}}`), so it *fails* D-CTG until the new block is filled. Contiguity of INSERT's filled run is INSERT's own theorem. The ASN in fact proves it (the consecutive/disjoint interval argument yielding `V_S(d') = {q_1,…,q_{N+n}}`), but frames that proof as a mere "restatement" of inherited lemmas. It is the actual obligation.

**Required**: Drop the D-*-post citations (they are contraction-side and inapplicable), and present the interval argument as the load-bearing contiguity/D-SEQ proof for the filled post-state, not as a restatement.

### Issue 3: Precondition permits a subspace mismatch between position and allocation

**ASN-0116, INSERT precondition**: "`S = subspace(p)`; `m := #p ≥ 2` …"

**Problem**: The precondition places no constraint forcing `S = s_C`, yet the allocation is **K.α (ContentAllocation)**, which always yields `subspace_I(a) = s_C`. If `p` sits in the link subspace (`S = s_L`), then I-NEW maps link-subspace positions `shift(p,k)` (subspace `s_L`, preserved by OrdShiftHom) to content addresses `shift(a,k)` (subspace `s_C`). This violates generalized referential integrity (S3★, ASN-0047), which requires `subspace(v) = s_L ⟹ M(d)(v) ∈ dom(L)`. INSERT-as-content-insertion is only well-defined for the text subspace.

**Required**: Add `S = s_C` to the precondition (or otherwise reconcile the allocation subspace with the insertion-position subspace). The cited I3-S3 does not cover this, as it concerns the unchanged left/shifted images, not the new block.

### Issue 4: P4's stated resolved-witness set is incomplete

**ASN-0116, P4 (LinkSurvival)**: "Hence the post-insert resolved-witness set of `e` in `d` is the shifted-suffix witnesses together with any such new-block witnesses — a superset of the prior set, equal to it iff `coverage(e) ∩ A_new = ∅`."

**Problem**: The resolved-witness set is `project(e, d, Σ') = {v ∈ dom(M'(d)) : M'(d)(v) ∈ coverage(e)}`. This also contains (a) **left-position witnesses** `v < p` whose image lies in `coverage(e)` (these are preserved verbatim by I-LEFT), and (b) **cross-subspace witnesses** in subspaces `S' ≠ S` (a link's coverage may include images of `d`'s positions in another subspace, preserved by F-SUB). The stated characterization "is the shifted-suffix witnesses together with new-block witnesses" omits both. The superset/equality conclusion happens to survive (left and cross-subspace witnesses are common to prior and post sets), but the explicit set identity in a named claim is wrong.

**Required**: Correct P4 to characterize the post-insert witness set as left witnesses ∪ shifted-suffix witnesses ∪ cross-subspace witnesses ∪ (new-block witnesses iff `coverage(e) ∩ A_new ≠ ∅`).

## OUT_OF_SCOPE

### Topic 1: Intra-composite coupling (J0) and provenance recording

**Why out of scope**: Whether each fresh I-address is coupled to an arrangement placement at the composite boundary, and the relation to the provenance relation R, lives in the ASN-0047 coupling/transition layer. The ASN correctly works at the ASN-0036 two-layer level and flags provenance as an open question; this is a future ASN concern, not a defect here.

VERDICT: REVISE
