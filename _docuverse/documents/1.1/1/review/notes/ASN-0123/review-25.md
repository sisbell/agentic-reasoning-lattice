# Review of ASN-0123

This is a strong, unusually careful note. The local apparatus (VN-B1, SA, nextv) is reproved over ASN-0047's K.δ vocabulary rather than imported from ASN-0040's transition system — exactly the right instinct, and the proofs hold. VN-B1's induction is airtight (the k=0 case correctly forces the operand to be `c_{j-1}` and pins `j = m+1`; the k=2 and Node cases are correctly excluded). The severance theorem's structural derivation of O5(ii) maximality from the depth-2 stream form, O1a, and Z-mono is genuinely elegant and correct, as is the worked-out divergence at position 4 in the cross-owner instance. The owned-branch freshness, transcription, source frame, and link carry-through all check out, and the foundation-invariant delegation to ExtendedReachableStateInvariants is legitimate since VERSION decomposes into the ASN-0047 atomic vocabulary and V-WF discharges ValidComposite★.

One derivation gap remains, and it is exactly the asymmetry the standard targets: the owned case proves its key precondition meticulously while the cross-owner case asserts the same precondition.

## REVISE

### Issue 1: The cross-owner branch's freshness precondition is asserted, not derived

**ASN-0123, Identity clause and V-WF clause 1**: In the identity clause, "Every member of that stream has the form `[pfx(π), 0, k]` (ASN-0040), whence Document(v), **v ∉ E**, pfx(π) ≼ v (O5(i))"; and in V-WF, "The produced v then satisfies Document(v), **v ∉ E**, and — established structurally at V9 from that stream form (ASN-0040) with O1a and Z-mono — pfx(π) ≼ v (O5(i))".

**Problem**: `v ∉ E` is grouped under "whence [the stream form]," but the stream form `[pfx(π), 0, k]` establishes `Document(v)` (zeros = 2) and `pfx(π) ≼ v` — it does **not** establish freshness. Freshness is a *precondition* of the allocating K.δ (`e ∉ E` in K.δ case (ii)), and for V-WF's clause-1 discharge to be complete, the note must show that precondition is *satisfiable* — i.e., that a fresh document exists in `S(pfx(π), 2)` and the operation allocates one. The owned branch does exactly this work ("freshness `v ∉ E` by the nextv choice (VN-B1 — the realized children are exactly `{c₁,…,c_hwm}`, so its successor `c_{hwm+1}` lies outside E)"); the cross-owner branch skips it. This is the precise shape of "showing the common case works does not establish the edge case does."

The gap is compounded by the framing "Which sibling of `S(pfx(π), 2)` v is — the frontier detail — stays out of scope." That is true for the *guarantees* (V9's maximality and severance use only the form `[pfx(π), 0, k]`, valid for any `k ≥ 1`), but it is **not** true for freshness: the sibling must be a *fresh* one. The note cannot leave "which sibling" entirely unconstrained and simultaneously rely on `v ∉ E`.

A secondary omission in the same clause: V-WF discharges `parent(v) ∈ E` explicitly for the owned branch ("parent(v) = parent(d_src) ∈ E by K.δ-ID.parent-0/1 and P8") but not for the cross-owner K.δ, where K.δ case (ii) also requires it (`parent(v) = pfx(π) ∈ E` by K.δ-ID.parent-2 and PS incumbency).

**Required**: Discharge the cross-owner K.δ's freshness precondition with the same explicitness as the owned branch. The materials are available in the foundation: the operation allocates the frontier of `A_doc(pfx(π)) = S(pfx(π), 2)`, fresh by ASN-0047's **ChildSpawnFreshness** (for the first document, `inc(pfx(π), 2) ∉ E` iff the `(pfx(π), 2)` child-spawn has not been performed) and **FrontierEquivalence** (for later documents, `inc(max, 0) ∉ E` since `inc(max, 0) > max` by TA5(a) and namespace disjointness places it outside `E`). Reconcile "which sibling is out of scope" with this: the sibling must be the (fresh) frontier; only the document-number *assignment* is immaterial to VERSION's guarantees. Also state `parent(v) ∈ E` for the cross-owner K.δ.

## OUT_OF_SCOPE

None. The note respects the stated scope: it uses K.δ as a foundation primitive to allocate its identity (it does not redefine document-creation-from-scratch), characterizes the version's editability via the foundation's K.μ family without defining the edit operations, and routes link carry-through entirely through foundation projections (LP12). The remaining boundaries — concurrent-fork serialization, derivation-direction recovery, version-namespace discipline for non-VERSION clients, location-fixed windowing — are correctly deferred to the Open Questions rather than asserted.

VERDICT: REVISE
