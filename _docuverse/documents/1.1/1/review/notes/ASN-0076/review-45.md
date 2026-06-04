# Review of ASN-0076

## REVISE

### Issue 1: Triple statement of the orphan/resurrection reading across E7 and E11

**ASN-0076, E7 closing remark and E11 (intro + "The collapse")**: E7 ends with "We make this precise in E11 below ... absent independent arrangement of the referents in some document, `ℓ_sup` is orphaned (LP17) and becomes discoverable only once a later transition arranges an I-address in its coverage (LP18)." E11's intro then restates the same framing ("governed instead by `d`'s arrangement, and is one EDITLINK is, by E10, powerless to settle on its own"), and E11's collapse paragraph restates it a third time ("`ℓ_sup` is orphaned in `Σ'` (LP17), and only a later transition arranging an I-address in its coverage can resurrect it (LP18)").

**Problem**: The LP17/LP18 orphan-then-resurrect reading is asserted three times in adjacent claims, two of them informally before E11 derives it. This is the "multiple paragraphs defer to the same downstream location" / "two paragraphs say the same thing" accretion pattern flagged for anti-bloat mode. E7's job is to establish the structural witness (`coverage` memberships); the discoverability deferral belongs to E11 alone.

**Required**: Reduce E7's closing remark to a single pointer ("discoverability is arrangement-governed; see E11") without the LP17/LP18 informal reading, and drop the recap sentence from E11's intro. Let E11's collapse paragraph carry the orphan/resurrection statement once.

### Issue 2: Intro restates the "edit ≠ in-place mutation" thesis twice

**ASN-0076, opening section**: "We will resolve the tension by observing that 'editing' need not — and, we will argue, *must* not — mean 'in-place mutation.' A document ... is not edited by overwriting; the original persists ... a new version is created alongside it ..." followed two paragraphs later by "What there *is*, however, is the means to express edit semantics as a composite of two link-allocation events."

**Problem**: The version-pattern thesis and the "express as composite" claim are stated, then the consultation-evidence paragraph re-establishes the same "no mutation primitive" commitment, then the thesis is restated. The motivational scaffolding repeats the same point before E0 proves it.

**Required**: Collapse to a single statement of the thesis plus the evidence; the proof is E0's job, not the intro's.

### Issue 3: E6 conflates "admissible" with "no constraint on the (ℓ_old, d_new) pair"

**ASN-0076, E6**: "for any state `Σ` satisfying all invariants, any `ℓ_old ∈ dom(Σ.L)`, and any `d_new ∈ Σ.E_doc` (not required to equal `home(ℓ_old)`), the composite EDITLINK is admissible at `Σ`."

**Problem**: EDITLINK's admissibility also requires valid endset inputs (L3) and `τ_sup ∈ T`. As stated, E6 asserts unconditional admissibility from `ℓ_old ∈ dom(Σ.L) ∧ d_new ∈ E_doc` alone, but those two conjuncts are not the entire precondition. The intended claim — that nothing couples `d_new` to `home(ℓ_old)` — is narrower than "admissible."

**Required**: State E6 as "EDITLINK places no constraint coupling `d_new` to `home(ℓ_old)`; given otherwise-valid inputs, every pair `(ℓ_old, d_new)` with `ℓ_old ∈ dom(Σ.L)` and `d_new ∈ E_doc` is admitted," matching what the proof actually shows.

## OUT_OF_SCOPE

### Topic 1: Supersession-chain invariants, cycles, and "current successor" computation
**Why out of scope**: The note correctly defers chain semantics, cycle conditions, retraction meaning, and reader-side authority resolution to future ASNs (Open Questions). These are new territory built on EDITLINK, not defects in it.

### Topic 2: Authorization of who may publish a supersession against another owner's link
**Why out of scope**: E6's application-layer note defers executor/capability semantics to a future authorization ASN. The link model has no executor field; this is genuinely absent state, not a gap in EDITLINK.

VERDICT: REVISE
