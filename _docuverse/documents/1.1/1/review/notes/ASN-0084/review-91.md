# Review of ASN-0084

## REVISE

### Issue 1: Merge definition is padded with consumer-enumeration and deferral meta-prose
**ASN-0084, "Correspondence-Run Decomposition Transformation" / Merge**: "This ASN uses Merge only as a definition — to identify mergeable pairs in the worked examples and to state CanonicalRunDecomposition. The verification that the merged run satisfies S8-cons under A belongs to the recovery of the canonical partition, which this ASN does not undertake (see Open Questions), and is deferred to the ASN resolving that question."

**Problem**: Neither sentence advances the meaning of Merge. The first enumerates downstream consumers ("used... in the worked examples and to state CanonicalRunDecomposition"); the second is a deferral that explains what the ASN *does not* do and points forward. This is exactly the forward-reference/consumer-enumeration accretion the precise reader must skip past. The definition itself — V-adjacency, I-adjacency, the merged triple — is complete without it.

**Required**: Delete both sentences. If a deferral is genuinely needed, the single Open Question on canonical recovery already records it; one pointer suffices, not a restatement at the definition site.

### Issue 2: R-BLK's "agrees with processing each cut against the original B" is an incorrect justification
**ASN-0084, R-BLK, "Interaction between successive cuts"**: "Processing cuts in index order against the progressively refined partition therefore agrees with processing each cut against the original B."

**Problem**: The literal claim is false. Take one run with ordinal extent {1,2,3,4,5} and cuts at ordinals 2 and 4. Progressive processing yields {1},{2,3},{4,5}. But "processing each cut against the original B" gives, for the cut at 4 applied to the *unsplit* original run, the boundary {1,2,3}|{4,5} — a partition the progressive result does not contain. The two procedures do not "agree" in the stated sense. What is actually true (and all that Phase 2 needs) is that splitting is order-independent: the final boundary set is the union of B's run boundaries and the cut set, so no run straddles any cut. The "agrees with the original B" phrasing is a hand-wave standing in for that argument.

**Required**: Replace the sentence with the order-independence / common-refinement statement, or drop it and rely directly on the conclusion already stated ("After all cuts are processed, no run straddles any cut position c_i") — which follows because Phase 1 splits at every cut.

### Issue 3: "Canonical decomposition" reinvents S8's maximality criterion without linking them
**ASN-0084, "Correspondence-Run Decomposition Transformation" / Canonical decomposition**: "The *canonical run decomposition* of an arrangement is the partition of its V-positions into *maximal* runs — runs that cannot be extended by merging with a V-adjacent, I-adjacent neighbor."

**Problem**: S8 (ASN-0036) already defines the maximal correspondence-run decomposition, with maximality given by non-extendability (no run `(v,a,n+1)`, no lockstep predecessor). This ASN restates maximality via a *different* criterion — merge-non-extendability — and then asserts in the properties table that CanonicalRunDecomposition "Names the S8-unique (ASN-0036) maximal-run partition." For the name to attach to S8's object, merge-non-extendability and S8's extension-non-extendability must coincide; the ASN neither uses S8's definition directly nor shows the two agree. Per standard 7, this is inventing notation for something the foundation already defines.

**Required**: Either define canonical decomposition as S8's maximal-run partition outright (citing the foundation), or add the one-line equivalence: a forward/backward lockstep extension of `(v,a,n)` is precisely a V-adjacent, I-adjacent neighbor, so the two maximality criteria coincide.

## OUT_OF_SCOPE

### Topic 1: Recovery of the canonical (maximal) partition from B' and confluence of merging
**Why out of scope**: The Open Questions already isolate this (merge S8-cons verification, termination, confluence). R-BLK correctly produces a *valid* partition B' and the post-state canonical partition's existence/uniqueness is discharged via direct application of foundation S8 — the constructive recovery is legitimately future work, not a gap in this ASN.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: New territory captured in Open Questions; the pivot/swap pair is a self-contained primitive class.

VERDICT: REVISE
