# Review of ASN-0047

The transition model is mathematically thorough: the elementary-transition frames, the K.δ case split, the D-SEQ★ derivation (both `m = 2` and `m ≥ 3`), and the per-elementary verification matrix are sound, and the inductive base (Σ₀) is enumerated rather than asserted. My findings below are confined to placement and forward-reference accretion, consistent with this note's `review-mode.anti-bloat` classifier. I did not find a correctness gap in the discharge of any invariant conjunct.

## REVISE

### Issue 1: "Link V-position permanence" paragraph is misfiled under K.μ~
**ASN-0047, *Decomposition of K.μ~***: The closing paragraph "Link V-position permanence. A withdraw-and-re-add composite re-seats a link..." describes a **K.μ⁻ + K.μ⁺_L** composite (full link-subspace clearance followed by two re-appends in opposite order), explicitly noting "clause (v)'s single-K.μ~ fixity does not extend to a lifetime guarantee."

**Problem**: The content is correct (the suffix-removal/full-clearance reasoning and the `ℓ ∉ ran(M(d))` guard analysis both hold), but it concerns a *different composite* than the section it sits in. A reader tracing the K.μ~ decomposition (Steps A, B, FIX, RANGE, necessity/sufficiency) must skip past a paragraph about K.μ⁻ + K.μ⁺_L re-seating that plays no role in the K.μ~ argument. The instructions direct flagging placement of correctly-stated "what an operation does/does not do" content that sits in the wrong slot.

**Required**: Relocate to the link-subspace contraction discussion (near K.μ⁺_L / the orphan-link material) or to a short standalone note on link re-positioning, so the K.μ~ decomposition reads contiguously.

### Issue 2: ValidComposite★ / Scoped-coupling material is forward-referenced from three separate earlier paragraphs
**ASN-0047, *Coupling and isolation*, *Cross-layer*, P4★, P4a**: The coupling machinery (ValidComposite★, J1★/J1'★ wp derivations) lives in *Scoped coupling constraints*, but is deferred to from at least three prior locations: the K.ρ/K.μ⁺ trigger note ("...full statement and wp derivation in *Scoped coupling constraints* below"); the P4★ paragraph ("Validity of a composite transition... is defined as ValidComposite★ in *Scoped coupling constraints* below"); and the P4a definition's trace clause ("each Σ_j →* Σ_{j+1} is a valid composite transition (ValidComposite★)").

**Problem**: This is the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern. P4★ in particular is *defined* before the notion of validity it depends on, forcing a forward pointer that the reader must hold open across several thousand words.

**Required**: Either state the ValidComposite★ clause-(1)/(2) skeleton once at first need (the *Coupling and isolation* preamble) and reference it locally thereafter, or move the P4★ definition adjacent to ValidComposite★ so the dependency is resolved in place rather than deferred from three sites.

## OUT_OF_SCOPE

### Topic 1: Interior link renumbering (compact-and-renumber DELETEVSPAN)
**Why out of scope**: K.μ⁻ models link-subspace contraction by suffix removal only; the implementation's interior `DELETEVSPAN` compacts surviving V-positions. The ASN correctly defers this to an Open Question rather than claiming coverage — it belongs in a future renumbering-aware contraction ASN, not this one. The named-operation `DELETEVSPAN` is itself in the excluded list.

VERDICT: REVISE
