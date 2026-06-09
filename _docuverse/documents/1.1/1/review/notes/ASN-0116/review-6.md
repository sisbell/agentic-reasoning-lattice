# Review of ASN-0116

I read the ASN as the composition K.α (×n) + ASN-0082's I3 post-insertion shift + the INSERT-specific block fill (I-NEW), and checked each cited clause, the per-position block attribution, the well-formedness re-derivations, the four-part witness decomposition, and the worked example including both boundaries. The construction is careful and largely correct: the per-position attribution (I3-V where the block position pre-existed, I3-CS where it did not), the explicit non-inheritance of I3-S3/I3-S7 because INSERT breaks the I3-C content frame, the k=0 vs k≥1 split for OrdShiftHom, the bijection-not-inclusion witness map, and the containment (not emptiness) weakest precondition are all sound. I verified `ran(M'(d)) = ran(M(d)) ∪ A_new`, the disjoint consecutive index intervals `{1..J-1}, {J..J+n-1}, {J+n..N+n}`, and the resurrection-vs-already-discoverable distinction in the worked example. All cross-references are to foundation ASNs.

One precondition-completeness gap remains.

## REVISE

### Issue 1: Inserted content values are never typed in the precondition
**ASN-0116, INSERT Precondition / I-ALLOC**: the operation signature is `INSERT(d, p, w₀ … w_{n-1})` and the Effect writes `C'(shift(a, k)) = w_k`, but the Precondition constrains only `d`, `n`, `p`, `S`, `m`, and the validity of the insertion position — never the inserted units `w_k`.
**Problem**: INSERT is the n-fold composition of K.α (ContentAllocation, ASN-0093), whose contract requires `v ∈ Val` for the value it commits. If any `w_k ∉ Val`, the underlying K.α step is undefined, yet the stated precondition admits the call. The precondition is therefore strictly weaker than the operation it specifies — it fails to assume an input the composite depends on.
**Required**: Add `(A k : 0 ≤ k < n : w_k ∈ Val)` to the precondition (or equivalent typing of the inserted span), so the K.α value-well-formedness obligation is discharged at the boundary rather than left implicit.

## OUT_OF_SCOPE

### Topic 1: Provenance coupling (J1★) of the allocation
**Why out of scope**: INSERT is specified against the `(C, M)` substrate of ASN-0093/0036, which carries no provenance relation `R`. In the full ASN-0047 transition model, a content-allocating composite must satisfy J1★ (every range-new content-subspace I-address records `(a, d) ∈ R'`). The ASN deliberately works in the two-layer substrate and defers this to its own open question ("What invariant relates the fresh I-addresses of an insertion to the document's recorded provenance…"). This is appropriate deferral, not an error in this ASN — provenance integration belongs to a later layering, not to the insertion mechanics specified here.

VERDICT: REVISE
