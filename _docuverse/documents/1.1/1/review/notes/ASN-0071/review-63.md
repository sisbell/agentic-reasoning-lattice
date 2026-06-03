# Review of ASN-0071

## REVISE

### Issue 1: The central multi-vspec union is never exercised by a concrete example

**ASN-0071, A worked scenario / The query**: "A **vspec-set** is a finite set `Q = {q₁, q₂, ..., q_k}` of vspecs, possibly drawn from multiple source documents" and `iaddrs(Q)(Σ) := ⋃_{(d_s, σ) ∈ Q} iaddrs_one(d_s, σ)(Σ)`.

**Problem**: Every worked query is a *singleton* — `Q = {(d_A, σ_A)}`, `Q_D = {(d_D, σ_D)}`, `Q_E`, `Q_F` are all one-element sets. The "multi-address query" `Q_D` is one vspec resolving to two addresses, not a multi-vspec set. The defining feature of `iaddrs` — the union over several vspecs, including cross-source deduplication (two sources both resolving `a₁`) — is asserted but never traced against a state. The rubric requires the key construction to be verified against a specific scenario; the union operator is the construction and it is untested.

**Required**: Add a worked query with `Q = {(d_s, σ), (d_s', σ')}` drawn from two distinct sources whose resolutions overlap (e.g. both resolve `a₁`), showing the union dedups across sources and `find` reports each document once (F-DIST).

### Issue 2: Imprecise characterization of the relaxation of ASN-0058's ContentReference

**ASN-0071, The query**: "A vspec relaxes ASN-0058's `ContentReference (d_s, σ)`, retaining only its T12 condition on `ℓ` and dropping that definition's subspace-non-emptiness, depth-match `#ℓ = #u = m_C`, and full-coverage demands."

**Problem**: This is not accurate. (a) The vspec *retains* `#ℓ = #u` (stated as level-uniformity, ASN-0053 S6) — so it does not drop "depth-match `#ℓ = #u = m_C`"; it keeps `#ℓ = #u` and drops only the `= m_C` clause. (b) The vspec *strengthens* beyond T12: T12 names `actionPoint(ℓ) ≤ #u`, while the vspec imposes `actionPoint(ℓ) = #u` plus `actionPoint(ℓ) ≥ 2`. So "retaining only its T12 condition" undersells the precondition set. The vspec is a relaxation on some axes and a strengthening on others — describing it as a pure relaxation that keeps "only T12" misstates what is required.

**Required**: State precisely which ContentReference conjuncts are kept (Pos), which are strengthened (`actionPoint = #u`, `≥ 2`), which are retained (`#ℓ = #u`), and which are dropped (non-emptiness, `= m_C`, coverage).

### Issue 3: Unproven coincidence claim with `resolve`

**ASN-0071, Resolution**: "Where a vspec happens to be a well-formed `ContentReference`, the two coincide: `iaddrs_one(d_s, σ)(Σ)` is exactly the set of I-addresses appearing in `resolve(d_s, σ)`."

**Problem**: This is asserted, not derived. `resolve` yields run/width pairs from a maximally-merged decomposition (ASN-0058 C1a); `iaddrs_one` is a raw image set. Their equality "where well-formed" requires an argument that the I-addresses in the decomposition's runs are exactly `{M(d_s)(v) : v ∈ ⟦σ⟧}`. Either it is load-bearing (then derive it) or it is decorative bridging prose to the foundation (then it is the kind of use-comparison the anti-bloat pass should remove).

**Required**: Either give the one-line derivation (every I-address in a run is `M(d_s)(v)` for some covered `v`, and decomposition coverage is exact), or delete the sentence.

### Issue 4 (anti-bloat): Subspace confinement stated twice

**ASN-0071, The query** ("Its position-1 instance `t₁ = u₁` is subspace confinement, `subspace(t) = s_C`...") and **Resolution** ("*Subspace confinement.* For every `t ∈ ⟦σ⟧`, PC's position-1 instance (proven in *The query*) gives `t₁ = u₁ = s_C`...").

**Problem**: The same corollary (`subspace(t) = s_C` for all `t ∈ ⟦σ⟧`) is concluded in two sections. The Resolution restatement re-derives a result already named in The query.

**Required**: In Resolution, cite the corollary by name and apply S3★; do not re-derive `t₁ = u₁ = s_C`.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state result and provenance relation `R`

**Why out of scope**: The Open Questions correctly defer "What relationship between FINDDOCSCONTAINING's current-state result and the historical containment relation `R` must the system guarantee?" The Currency section is right to evaluate `find` purely at the query state; the historical/provenance bridge is a future ASN, not a defect here.

### Topic 2: Rejecting versus silently filtering unresolvable vspec positions

**Why out of scope**: F-FILT (silent filtering) is a deliberate semantic choice; whether the system should instead reject is an interface-policy question appropriately listed as an Open Question.

VERDICT: REVISE
