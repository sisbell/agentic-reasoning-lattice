# Review of ASN-0116

This is a careful, well-structured operation note. INSERT is correctly cast as a valid ASN-0047 composite `K.α(×n) → K.μ⁻ → K.μ⁺ → K.ρ(×n)`, the K.μ⁻/K.μ⁺ pairing is properly motivated (a single K.μ atomic cannot both rewrite suffix images and grow the domain), the I3-gapped-arrangement-plus-block-fill composition is sound, the block-disjointness index argument is correct, the boundary cases (front, append, empty, re-insertion) are genuinely worked, and the IP6 weakest-precondition (containment-not-emptiness) is a real analysis with the right distinction. The findings below are precision/justification slips and one accreted-prose pattern — none touches the core mechanics.

## REVISE

### Issue 1: IP4 asserts a universal non-inclusion that fails (and contradicts its own count formula)

**ASN-0116, IP4 (LinkSurvival)**: "INSERT maps these injectively into the post-insert set: left and cross-subspace verbatim, suffix by the bijection `v ↦ shift(v, n)` (I-SHIFT). The two sets are therefore **not** in a set-inclusion relation — the shifted witnesses occupy new V-positions".

**Problem**: The blanket "not in a set-inclusion relation" is false whenever `e` has no shifted-suffix witness. Concretely:
- If `coverage(e)` meets only left-region or cross-subspace images and `coverage(e) ∩ A_new = ∅`, then left and cross-subspace witnesses are preserved verbatim and there is no suffix part, so `project(e, d, Σ) = project(e, d, Σ')` — equality, which *is* a set-inclusion relation.
- If `e` has only left witnesses plus a new-block witness, then `project(e, d, Σ) ⊊ project(e, d, Σ')`.

The non-inclusion holds only when at least one suffix witness actually shifts. The justification clause "the shifted witnesses occupy new V-positions" is vacuous in the suffix-free case, so the conclusion does not follow there. Worse, the claim is in direct tension with IP4's own count formula immediately below it: `|project(e, d, Σ')| = |project(e, d, Σ)| + |{shift(p, k) : … ∧ shift(a, k) ∈ coverage(e)}|` "with equality in both iff the new-block part is empty" — at empty new-block and empty suffix this gives equal *sets*, contradicting "not in a set-inclusion relation."

**Required**: Condition the non-inclusion on the presence of a shifted suffix witness — e.g., state that `project(e, d, Σ) ⊆ project(e, d, Σ')` holds exactly when no suffix witness shifts, and the two sets are incomparable precisely when some suffix witness is present. The bijection-onto statement and the count/content-monotonicity formulas are correct and can stand unchanged.

### Issue 2: IP3 justifies content-membership via a false whole-range inclusion

**ASN-0116, IP3 (PositionImpermanence)**: "the same slot now resolves to freshly minted content, since `shift(a, k−J) ∈ A_new` is fresh (IP0) while `M(d)(q_k) ∈ ran(M(d)) ⊆ dom(C)`."

**Problem**: `ran(M(d)) ⊆ dom(C)` is false in general. `M(d)` arranges both subspaces; by S3★ (GeneralizedReferentialIntegrity) link-subspace V-positions map into `dom(L)`, so any document with arranged links has `ran(M(d)) ∩ dom(L) ≠ ∅` and hence `ran(M(d)) ⊄ dom(C)`. The intended conclusion `M(d)(q_k) ∈ dom(C)` is nonetheless true, but for a different reason: `q_k` is a *content*-subspace block slot (`subspace(q_k) = s_C`), so S3★ places its image in `dom(C)`. The cited route (membership in the full range, then a false subset step) does not establish it.

**Required**: Replace "`∈ ran(M(d)) ⊆ dom(C)`" with the content-subspace referential-integrity step: `M(d)(q_k) ∈ dom(C)` by S3★, since `subspace(q_k) = s_C`. (RAN already states the range gain correctly as "new to the *content-subspace* range," so this is a localized slip, not a systematic one.)

### Issue 3: Provenance coupling is proved once and then re-asserted, with a forward-pointer lead-in

**ASN-0116, "INSERT as a valid composite" (Clause 2) vs. "Provenance coupling…" paragraph vs. PROV**: Clause 2 proves J0/J1★/J1'★ via the RAN range identity (the correct location for the coupling proof). The later "Provenance coupling — the obligation allocation incurs" paragraph then forward-points — "The coupling that allocation-with-placement incurs — J0, J1★, J1'★, and the boundary coverage P7a/P7 — is carried by PROV below" — and PROV re-asserts "which discharges the coupling constraints J0, J1★, J1'★ of ASN-0047 between the composite's initial and final states."

**Problem**: The carries-PROV-below sentence is a pure deferral, and PROV's coupling-discharge clause restates what Clause 2 already proved, in different words. The `R' = R ∪ {(shift(a,k), d)}` record statement appears in I-PROV (Effect), the lead paragraph, PROV, and the worked example. (The worked-example *trace* of J0/J1★/J1'★ is a concrete verification and is appropriate; the issue is the lead-paragraph forward pointer plus PROV's re-assertion adding no proof content beyond Clause 2.) PROV's only non-duplicative content is the P7a/P7 conclusion and the "atomically-with-allocation, not deferred" framing.

**Required**: Drop the "is carried by PROV below" forward pointer; let PROV cite Clause 2 for the J0/J1★/J1'★ discharge rather than restating it, retaining only the P7a/P7 conclusion and the atomicity observation as PROV's contribution.

## OUT_OF_SCOPE

The Open Questions (transclusion at a shared position, concurrent insertion without a serializing authority, transclusion-provenance, post-edit fragmentation of the inserted run) are correctly deferred and make no claims; no out-of-scope topic is specified here. The re-insertion sub-case (b) references a state *produced by* a prior contraction but does not specify DELETE, so it remains in scope.

VERDICT: REVISE
