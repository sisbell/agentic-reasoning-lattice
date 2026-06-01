# Review of ASN-0047

## REVISE

### Issue 1: J4 fork — k=0 subsequent-version content source asserted but unverified, no concrete example

**ASN-0047, *Coupling and isolation*, J4 / Definition (Fork)**: "Fork is version creation on d_src's version chain `A_v(d_src)`, uniform across first and subsequent versions" and step (ii): "K.μ⁺ populating M'(d_new) from d_src's content subspace under transclusion: `ran(M'(d_new)) ⊆ ran(M(d_src)|_{V_{s_C}(d_src)})`".

**Problem**: The definition fixes the transclusion source as `d_src` for *all* sub-cases, but the k=0 sub-case's operand is `prev_version` (a prior version on `A_v(d_src)`'s frontier), not `d_src`. For a chain `d_src → v1 → v2` where `v1` was edited (K.α + K.μ⁺ added content not present in `d_src`), creating `v2 = inc(v1, 0)` under J4 transcludes `d_src`'s *original* content, silently excluding `v1`'s additions. Whether this is intended (every sibling version forks `d_src`'s base content) or an error (should snapshot `prev_version`) is never stated. The claim of uniformity across k=1 and k=0 is asserted but never exercised: the *Worked example: fork with subsequent insertion* performs only the k=1 first-version case (`d₂ = inc(d₁, 1)`). The k=0 subsequent-version fork — and the discharge of S2/S3★/D-CTG★/D-MIN★ and J1★/J1'★ against the `ran ⊆ ran(M(d_src)|...)` bound — is verified nowhere.

**Required**: Either (a) state explicitly that all sibling versions on `A_v(d_src)` fork `d_src`'s content (so a version building on `v1`'s edits must instead fork `v1` via k=1 on `A_v(v1)`), and add a concrete k=0 worked example verifying the invariants; or (b) correct step (ii) so the k=0 case transcludes from `prev_version` and re-derive the range bound. As written, the uniformity claim fails the "concrete example mandatory" and "depth mandatory" standards for a key postcondition.

### Issue 2: Operational-depth paragraph restates the re-pinning fact three times

**ASN-0047, *Elementary transitions*, "V-position depth (operational)"**: "`m_S(d)` is well-defined only while `V_S(d) ≠ ∅`; it is constant within a contiguous non-empty stretch but is *not* a permanent per-document constant. K.μ⁻ admits full clearance ... after which S8-depth is again vacuous and the next insertion ... re-pins `m_S(d)` from scratch — at any value `≥ 2` by S8a, not necessarily the prior depth. The depth therefore tracks the live arrangement, not a value fixed at first-ever insertion."

**Problem**: The single load-bearing fact — "depth is not a permanent constant; clearing the subspace lets the next insertion re-pin it" — is stated three times in one paragraph ("not a permanent per-document constant," "re-pins `m_S(d)` from scratch ... not necessarily the prior depth," "tracks the live arrangement, not a value fixed at first-ever insertion"). This is the anti-bloat "same thing in different words" pattern; the precise reader must verify each restatement carries no new content.

**Required**: Collapse to one statement of the rule (definedness only while `V_S(d) ≠ ∅`; re-pinning to any `m ≥ 2` after clearance). The S8a lower bound and the "from scratch" mechanism are the only substantive additions; the rest is repetition.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal / tombstoning mechanism
The Open Questions note that D-CTG★/D-MIN★ confine K.μ⁻ to link-subspace suffix truncation, so withdrawing an interior link requires an out-of-K.μ⁻ mechanism. This is correctly deferred — it is new territory (a withdrawal primitive or status-flag state), not a defect in the present transition set.

### Topic 2: Concurrent link allocation under a shared home document
The serialization/coordination guarantees for concurrent K.λ events targeting one document are raised as Open Questions and belong to a future concurrency ASN, not this single-event-sequential model.

VERDICT: REVISE
