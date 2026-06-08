# Review of ASN-0100

This ASN is substantively complete: every conjunct of ExtendedReachableStateInvariants (per-state, composite-boundary, and the P3 composite obligation) is addressed, the boundary cases (empty document, prepend with forced full clearance, append, re-insertion into a cleared subspace, deep `m_C ≥ 3` subspace) are each worked concretely, and both wp computations are non-trivial. The findings below are accretion/duplication issues consistent with the `review-mode.anti-bloat` classifier, not correctness gaps.

## REVISE

### Issue 1: The "re-derive S3/S7 because I3-C is violated" rationale is stated three times
**ASN-0100, §Effect Three / §Referential integrity / claims table (INS.inv.refint)**:
- §Effect Three: "INSERT re-derives S3 (§Referential integrity) and S7 (§Post-state V-position well-formedness) independently rather than inheriting them, because growing `dom(C)` (INS.C) violates I3's content frame I3-C."
- §Referential integrity: "we re-derive referential integrity directly (re-derived, not inherited; see §Effect Three)."
- INS.inv.refint row: "not inherited from I3-S3, whose proof premise rests on the content frame I3-C that INSERT violates."

**Problem**: One load-bearing point — I3's content frame I3-C is violated, so S3 must be re-derived — is asserted in three places, with §Effect Three and §Referential integrity each forward/back-pointing to the other. This is the "multiple paragraphs defer to the same downstream location" / repeated-content pattern.
**Required**: State the rationale once at the site of the actual re-derivation (§Referential integrity); reduce the other two to bare cross-references without restating the I3-C justification.

### Issue 2: The INS.M-exhaustive composite argument is duplicated, with an inconsistent attribution
**ASN-0100, §Arrangement functionality (S2)** and **§Atomicity and Canonical Order ("Arrangement of `d`")**:
- §Arrangement functionality: "Steps 1 and 4 (the K.α and K.ρ firings) frame `M`... Step 2's K.μ⁻ (when fired) only *removes* positions. Step 3's K.μ⁺ adds *exactly* the Insertion positions ... and the Shifted-right positions ... Hence every `s_C` position in `dom(M'(d))` is either a surviving pre-state position... an Insertion position, or a Shifted-right position — no fourth region exists."
- §Atomicity: "No other elementary step can introduce an `s_C` position, since K.α and K.ρ frame `M` (`M' = M`, ASN-0047) and K.μ⁻ only removes."

**Problem**: The same litany (K.α/K.ρ frame M; K.μ⁻ removes; K.μ⁺ adds exactly Insertion + Shifted-right) is rehearsed in both sections. Worse, the §Atomicity paragraph attributes the establishment to the wrong section: "this is the exhaustiveness clause INS.M-exhaustive, established at the effect specification (§The Operation: Formal Contract) from the composite construction" — but §The Operation: Formal Contract only *states* INS.M-exhaustive; the *proof* is in §Arrangement functionality.
**Required**: Prove INS.M-exhaustive once and point the §Atomicity uniqueness argument at that proof by reference. Fix the mis-pointer to name §Arrangement functionality (where the composite construction is actually discharged), not §The Operation: Formal Contract.

### Issue 3: Claims-table rows carry justification/deferral prose instead of bare claim statements
**ASN-0100, §Claims Introduced**: e.g. INS.inv.refint's Statement column — "Left and Shifted-right regions re-derived from pre-state S3★ + the monotone step dom(C) ⊆ dom(C') (P0) — not inherited from I3-S3, whose proof premise rests on the content frame I3-C that INSERT violates — Insertion region from INS.C"; INS.proj — "π, N_{ℓ,i} defined and derived in §Coverage and link discoverability"; INS.atomicity — "(established in §Atomicity and Canonical Order)".

**Problem**: A claims table is a structural slot whose Statement column should state the claim. Several rows instead embed proof sketches ("re-derived from... not inherited from... whose proof premise rests on...") or section-pointers. This is essay content / deferral pointers in a structural slot — the noise the precise reader must skip past to read the actual claim.
**Required**: Reduce these rows to the claim itself. Move the "why re-derived rather than inherited" reasoning to the prose body (consolidated per Issue 1); drop the "(established/defined in §X)" parentheticals — the body sections are the authority and the table need not point at them.

## OUT_OF_SCOPE

(none — the "Bounding the Scope" section correctly excludes DELETE/COPY/REARRANGE/link-subspace insertion/version/replication without defining claims for them.)

VERDICT: REVISE
