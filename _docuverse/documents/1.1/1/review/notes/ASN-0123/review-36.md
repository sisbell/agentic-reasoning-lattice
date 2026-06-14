# Review of ASN-0123

I checked the load-bearing proofs (SA, VN-B1, V-WF, V0, V4, V8, V9's severance/maximality, V9w, V10, V13) against their preconditions and the cited foundation contracts. The mathematics is sound and the edge cases the topic demands are covered: the empty source (`n = 0`) is handled explicitly throughout, the owned/cross-owner branches are both discharged, and the cross-owner severance is a genuine theorem rather than a stipulation. The non-injective worked instance (`|A| = 2 < n = 3`) correctly exercises shared-address provenance counting. I found no correctness gap and no non-foundation cross-ASN reference.

The note carries `review-mode.anti-bloat`. The findings below are forward-reference accretion, not correctness.

## REVISE

### Issue 1: V-WF and V9 circularly cross-cite and duplicate the cross-owner stream-form derivation

**ASN-0123, V-WF (cross-owner branch of Clause 1) and V9 (preamble)**:

V-WF derives the cross-owner allocation as a single document K.δ in `A_doc(pfx(π)) = S(pfx(π), 2)`, establishes the `k=2`/`k=0` frontier and its freshness, then: *"The produced `v` is the frontier of `S(pfx(π), 2)` (just shown), whence `Document(v)` by V9."*

V9's preamble *independently re-derives the same stream form* — *"`pfx(π) ∈ E` … carries the document sub-allocator `A_doc(pfx(π))` … the sibling stream `S(pfx(π), 2)` — first emission `inc(pfx(π), 2)`, thereafter `inc(·, 0)` … every member of the stream … has the form `v = [pfx(π)₁, …, 0, k]`"* — and then cites back: *"`π` creates `v` there as a single document-level K.δ in its own namespace (V-WF; the within-stream index is immaterial …)."*

**Problem**: The citations form a loop — V-WF → V9 for `Document(v)`, V9 → V-WF for "single K.δ" — and the identity clause *also* defers `Document(v)`/O5 to V9 (*"discharging what the identity clause deferred"*). A reader assembling the cross-owner case is bounced between the two claims and re-reads the same `A_doc(pfx(π)) = S(pfx(π), 2)` development twice. The circle is purely expository: both facts are actually proven in both places (V9 derives `Document(v)` from `zeros(v)=zeros(pfx(π))+1=2` and B6(a) without needing V-WF; V-WF establishes the single K.δ itself), so neither citation is load-bearing. This is exactly the "multiple paragraphs defer to the same downstream location" + duplication pattern.

**Required**: Give the cross-owner stream-form derivation one owner and cite it one-directionally. V-WF already holds `v ∈ S(pfx(π), 2)`, from which `zeros(v) = zeros(pfx(π)) + 1 = 2` and T4-validity (B6(a)) yield `Document(v)` directly — drop "by V9". Remove the reciprocal "(V-WF)" in V9's preamble (V9 derives the stream membership itself). Preserve V9's O5(ii) maximality derivation unchanged — this finding is about the citation structure and the duplicated setup, not the maximality math.

### Issue 2 (minor): VD states the registry-decides-derivation result twice, plus a third time in the table

**ASN-0123, VD**: *"Restricted to `v ∈ S(d, 1)`, the registry decides derivation: `derives(v, d) ⟺ v ∈ E`. … Equivalently, writing `derives_addr(v, d) := derives(v, d) ∧ d ≼ v` for address-encoded derivation, the registry decides exactly that fragment: `derives_addr(v, d) ⟺ v ∈ E ∩ S(d, 1)`."* The claims table restates it a third time: *"(equivalently `derives_addr(v, d) ⟺ v ∈ E ∩ S(d, 1)`)."*

**Problem**: The "Equivalently …" reformulation says the same thing as the restricted biconditional, and the introduced `derives_addr` is consumed nowhere else — only by the restatement itself and the table row. It is an alternate phrasing carried for its own sake.

**Required**: Keep one formulation (either the prose restriction `derives(v,d) ⟺ v ∈ E` for `v ∈ S(d,1)`, or the `derives_addr` form), and drop the redundant other plus its table echo.

## OUT_OF_SCOPE

None. The note scopes correctly: comparison, content/link operations, windowing, withdrawal, and replication are excluded in the "Scope." paragraph and surface only as Open Questions, not as claims.

VERDICT: REVISE
