# Review of ASN-0117

I read the ASN as an abstract DELETE operation grounded in the foundation contraction (ASN-0082) with the content store held in frame. The displacement arithmetic (`σ(q_k) = q_{k−c}`, gap-closure `σ(q_{J+c}) = q_J`), the region partition, the count-based DEL-REMOVE (correctly robust against within-document sharing), the wp range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}`, and the worked boundaries (suffix delete, full delete, within-document sharing) all check out. The P2 suffix-delete vacuity is handled correctly via D-SEP(a) unconditional / D-SEP(b) conditional. One substantive issue remains.

## REVISE

### Issue 1: Referential-integrity conjunct contradicts the preservation of link positions
**ASN-0117, "The document remains one coherent sequence"**: "S3-post for referential integrity (`ran(M'(d)) ⊆ dom(C')`, which holds trivially since `ran(M'(d)) ⊆ ran(M(d))` and `C' = C`)."

**Problem**: The ASN operates on a two-subspace document — DEL-FSUB explicitly preserves the link-subspace positions `V_{s_L}(d)`, and DEL-LIMM keeps the link store fixed. Those preserved link positions map to addresses in `dom(L)`, which by store disjointness (SD, ASN-0093) are *not* in `dom(C)`. So for any document containing a link, `ran(M'(d)) ⊆ dom(C')` is literally false — the full-document range includes `dom(L)` images. The supporting reasoning (`ran(M'(d)) ⊆ ran(M(d))`, `C' = C`) is correct and is what actually preserves referential integrity, but the cited conjunct as written excludes the very link positions the operation claims to carry through unchanged. This is an internal inconsistency: the wp section relies on link-subspace images surviving (it carries `ran(M(d)\restriction V_{s_L}(d))` through the range identity), yet the well-formedness section asserts the whole range lies in `dom(C)`.

**Required**: State the preserved invariant as the two-subspace S3★ (GeneralizedReferentialIntegrity, ASN-0047): text V-positions resolve into `dom(C')`, link V-positions into `dom(L')`. Equivalently, restrict the `ran(M'(d)) ⊆ dom(C')` claim to the content subspace and add the link-subspace clause `ran(M'(d)\restriction V_{s_L}(d)) ⊆ dom(L')`, preserved by DEL-FSUB + DEL-LIMM. The preservation argument (`ran(M'(d)) ⊆ ran(M(d))`) already supports the corrected statement.

## OUT_OF_SCOPE

### Topic 1: Deletion at text depth m > 2 and deletion within the link subspace
**Why out of scope**: The operation is scoped to text-subspace, depth-2 positions (`S = s_C`, `m = 2`), mirroring the foundation contraction (ASN-0082), which is itself depth-2. A general-depth or link-subspace deletion would require a general-depth contraction foundation that does not yet exist; this is future territory, not an error in this ASN. The precondition states the restriction explicitly, so no claim here overreaches.

VERDICT: REVISE
