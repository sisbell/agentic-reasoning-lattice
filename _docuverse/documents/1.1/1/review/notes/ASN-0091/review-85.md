# Review of ASN-0091

## REVISE

### Issue 1: Target document named inconsistently (`d` vs `d_tgt`)

**ASN-0091, "Projection Transports Along π" / RE-proj / claims table**: "at the rearrangement target `d_tgt` ... and at any non-target document `d ≠ d_tgt`" and "π̂_d := π at the rearrangement target `d_tgt`".

**Problem**: Every other section — RE-other, RE-trans, RE-sub, RE-ext, the abstract definition, all worked examples — names the rearrangement target `d` and uses `d_view`/`d'` for the other role. RE-proj alone flips this: `d` becomes the *running quantifier* and `d_tgt` the target. A reader carrying "`d` = target" from the preceding ten sections hits RE-proj where `d` now ranges over all documents. The section is internally consistent, but the global double-use of `d` for two distinct roles is a genuine clarity defect in an otherwise carefully-typed document.

**Required**: Use one name for the target across the whole note. Either keep `d` as the target in RE-proj and introduce a fresh running variable, or adopt `d_tgt` everywhere; do not let `d` denote the target in twelve sections and the running variable in one.

### Issue 2: Scope-gloss paragraph in the REARRANGE_K realisation

**ASN-0091, "REARRANGE_K Realises the Abstract Class"**: "*Reachability scope of the realisation.* The discharge of RA-adm below establishes it only for a *reachable* pre-state Σ, so we scope the realisation theorem accordingly — REARRANGE_K realises the abstract Vstream-only class on every Σ reachable from Σ₀..."

**Problem**: This is a standalone paragraph whose only object-level content is the qualifier "the realisation theorem holds for reachable Σ." The rest ("the discharge ... below establishes it only for...", "we scope the realisation theorem accordingly") is forward-pointing meta-prose justifying a scoping decision rather than advancing the argument — the same scope-gloss class trimmed in a prior cycle. The reachable-Σ condition is a theorem qualifier; it belongs in the theorem statement, where the subsequent discharge already derives the reachability obligation naturally.

**Required**: Fold the reachable-Σ qualifier into the realisation claim itself and delete the self-referential framing and the forward pointer to "the discharge ... below."

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics and span-reconstitution after a cut splits a same-source transclusion

**Why out of scope**: The ASN already routes both to its Open Questions and explicitly does not establish whether two fragments jointly reconstitute the original source span (RE-trans note). These are future-ASN territory, not defects here.

VERDICT: REVISE
