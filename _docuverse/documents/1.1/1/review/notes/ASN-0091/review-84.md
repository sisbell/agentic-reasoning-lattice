# Review of ASN-0091

The mathematical content is sound: the abstract Vstream-only class is cleanly separated from the REARRANGE_K realisation, the RE-* derivations chain correctly from RA-dom/RA-π/RA-frame, the L-chain disjoint-adjacency lemma is correctly applied in every witness, and the five worked examples check out arithmetically (I verified the fragmentation, coalescence, equality, non-uniqueness, and collapse traces). No cross-ASN references outside the foundation set; no drift into implementation mechanics. The remaining issues are the meta-prose accretion this note's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: Inline provenance editorializing duplicates the Provenance column
**ASN-0091, "Projection Transports Along π" and "Composite-Boundary Properties"**: "The derivation rests only on RA-π and coverage state-independence, so it holds for every Vstream-only realiser." and "These three derivations use only RE-C, RE-R, and RE-ran, all of which hold for every Vstream-only realiser; the composite-boundary preservation is therefore abstract, not specific to REARRANGE_K."
**Problem**: The "Claims Introduced" table exists precisely to record the abstract/REARRANGE_K/structural provenance of each claim in a dedicated column. Restating "holds for every Vstream-only realiser" / "abstract, not specific to REARRANGE_K" inline at each derivation duplicates that column. This is the recurring classification remark the anti-bloat pass is meant to remove at source — it does not advance the derivation, it labels it.
**Required**: Drop the inline abstractness remarks; let the Provenance column carry the classification. If a derivation's premises genuinely need stating (RA-π + coverage state-independence), state them without the editorial "so it holds for every realiser" coda.

### Issue 2: Per-example RA-adm bullets restate the same abstract discharge
**ASN-0091, Worked Example admissibility bullets**: e.g. "RA-adm is discharged once, abstractly... Σ' here is reachable, so the per-state foundation invariants hold at Σ' without per-invariant re-verification" (Worked Example 1) and "RA-adm holds for the reachable Σ' by the abstract discharge" (bijection example).
**Problem**: RA-adm is discharged once for every reachable Σ in "REARRANGE_K Realises the Abstract Class." The per-example bullets that merely re-assert "discharged abstractly, Σ' reachable" add no concrete verification — unlike the adjacent P4★/P7a bullets, which exhibit actual sets. Multiple sections deferring to the same upstream discharge is the repeated-deferral pattern. (The collapse example's bullet is the exception — `Σ' = Σ` is a genuinely distinct argument and should stay.)
**Required**: Remove the redundant RA-adm bullets from worked examples whose discharge is the unmodified abstract one; keep only where the discharge differs (the collapse case).

### Issue 3: Anticipatory meta-framing of the reachability scope
**ASN-0091, "Reachability scope of the realisation"**: "The discharge of RA-adm for the REARRANGE_K realiser below routes through reachability: it shows Σ' reachable and reads off the per-state foundation invariants from ASN-0047's ExtendedReachableStateInvariants."
**Problem**: This sentence describes what the following paragraph does before doing it — forward-reference meta-prose. The load-bearing content is the scoping conclusion ("we scope the realisation theorem accordingly"); the preamble narrating the proof strategy is not.
**Required**: Cut the anticipatory first sentence; open directly with the scoping statement and let the subsequent paragraph perform the discharge.

## OUT_OF_SCOPE

### Topic 1: Reconstitution of a split transcluded span
The note's own Open Questions ask whether two fragments jointly reconstitute the original source span (RE-trans only establishes per-fragment origin). This is correctly deferred — it is new territory, not a defect here.

### Topic 2: Link-subspace rearrangement semantics
RE-sub fixes the link subspace pointwise; what an operation *reordering* the link subspace would have to preserve is properly left as an Open Question.

VERDICT: REVISE
