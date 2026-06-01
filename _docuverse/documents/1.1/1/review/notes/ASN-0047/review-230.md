# Review of ASN-0047

I checked the elementary-transition definitions, the K.δ case split, the K.μ~ decomposition and its necessity/sufficiency argument, the D-SEQ★ derivation (both m=2 and m≥3 cases), the cross-layer derivations (P6/P7/P8/GlobalLineage), and the two verification matrices. The mathematical core is sound: case splits are exhaustive, FrontierEquivalence proves both directions, the D-SEQ★ inner-position argument is complete, and the K.μ~ link-subspace fixity chain (Steps 1–4) is genuinely worked rather than waved. I found no skipped correctness case in the in-scope material.

The findings below are anti-bloat / reviser-drift, which this note's `review-mode.anti-bloat` classifier directs me to surface at source.

## REVISE

### Issue 1: Reviser-drift — prose referencing a prior-version defect
**ASN-0047, P4a definition (Coupling and isolation)**: "The witnessing existential ranges over the finite set `{Σ₀, ..., Σ_n}` of trace states — **the previously-undefined 'transition history' reference** — so the property is well-typed as a trace property even though it is not well-typed as a per-state invariant."

**Problem**: The phrase "the previously-undefined 'transition history' reference" describes the document's own revision history, not the claim. A cold reader cannot interpret "previously-undefined" — it is a note-to-self that a prior cycle's dangling term has now been pinned. This is exactly the meta-prose the precise reader must skip past. The definition box already defines the transition history explicitly two sentences earlier; the parenthetical adds nothing object-level.

**Required**: Delete the clause. The sentence reads cleanly as "ranges over the finite set `{Σ₀, ..., Σ_n}` of trace states, so the property is well-typed as a trace property…"

### Issue 2: Exhaustiveness essay with use-site inventory in a structural slot
**ASN-0047, Elementary transitions (closing paragraph)**: "The seven elementary kinds … plus the named composite K.μ~ are *structurally sufficient* for the *catalogued* modification modes of this ASN, enumerated per component as follows. (i) … (ii) … (iii) *Replacement* … takes three forms by composite shape … the exhaustive case split and the per-form composite traces are given in *Worked example: prior-provenance and first-time-transcluded replacements* (Contrast paragraph) and *Worked example: interior content replacement* (fresh-content)."

**Problem**: Two anti-bloat patterns compound here. (a) "structurally sufficient for the catalogued modification modes" is an unproven exhaustiveness claim — no theorem establishes it, and nothing downstream consumes it as a premise, so it is editorial assertion in a structural slot. (b) The (iii) clause is a use-site inventory / forward pointer ("the exhaustive case split … are given in *Worked example…*") that defers the content rather than advancing it. The substantive taxonomy (extension / contraction / reordering / replacement) is already carried by the operation definitions and the temporal-decomposition table.

**Required**: Drop the sufficiency assertion and the forward-pointer inventory. If the three replacement forms are worth naming, name them in one sentence at the point of use (the replacement worked examples), not as an advance catalogue here.

## OUT_OF_SCOPE

### Topic 1: Link-withdrawal / tombstoning mechanism reconciling D-CTG★ with Nelson LM 4/9
**Why out of scope**: The ASN correctly confines K.μ⁻ to suffix truncations and notes (Orphan links section, and Open Questions) that interior link withdrawal would require a separate mechanism. This is acknowledged future territory, not a defect in the present transition model.

### Topic 2: Concurrent/serialized link allocation under a shared home document
**Why out of scope**: Concurrency and atomicity beyond the single-event SequentialTransitionAxiom are explicitly listed as out of scope, and the ASN flags this as an open question rather than claiming a guarantee.

VERDICT: REVISE
