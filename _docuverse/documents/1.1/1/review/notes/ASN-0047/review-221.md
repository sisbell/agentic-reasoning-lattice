# Review of ASN-0047

## REVISE

### Issue 1: `shift(t, 0) := t` reinvented from ASN-0034 instead of citing the foundation that already establishes it
**ASN-0047, S8★ (link-subspace discharge)**: "We adopt the convention `shift(t, 0) := t` for any tumbler `t` (extending ASN-0034's OrdShift, which is stated for `n ≥ 1`, to the boundary case `n = 0` as the identity)."

**Problem**: ASN-0036's S8 — the very foundation result that S8★ extends and that the content-subspace discharge applies "directly" — already states this exact convention ("Under the convention `shift(t, 0) := t`, a correspondence run is a triple..."). Re-deriving it from ASN-0034's OrdShift reinvents notation a foundation already defines (Standard 7). The risk is small here, but the citation should point to the result it is extending.

**Required**: Replace the parenthetical with a citation to ASN-0036's S8 convention. The convention is inherited, not introduced.

### Issue 2: Implementation-anomaly essay sentence embedded mid-derivation in J1'★
**ASN-0047, Scoped coupling constraints, J1'★ derivation**: "...Gregory confirms the implementation accumulates entries 'from every content addition.' Gregory further identifies one implementation anomaly where provenance recording is skipped for a particular command, 'making content invisible to find_documents' — the abstract specification treats this as a defect, since the coupling is required."

**Problem**: The first half (design-choice justification for imposing J1'★) advances the argument. The "Gregory further identifies one implementation anomaly..." sentence does not — it bears on no part of J1'★'s statement, its wp computation, or its preservation, and sits in the middle of a formal derivation. This is essay content in a structural slot; per the forward-reference-accretion guidance, flag its placement.

**Required**: Remove the anomaly sentence from the derivation, or relocate it to commentary outside the wp argument.

### Issue 3: The allocated-empty vs. default-empty `M(d) = ∅` distinction is explained in three separate slots
**ASN-0047**: the same distinction is restated in (a) *The state model* — "Notational convention (default value)" ("`M(d) = ∅` does not signal allocation status — a freshly registered document also has `M(d) = ∅`"); (b) *Elementary transitions*, "Subsumption of ASN-0093's K.σ"; and (c) the K.δ `IsDocument(e)` frame ("The registered `M'(e) = ∅` is the *allocated-empty* arrangement... distinct from the unallocated default `M(e) = ∅`...").

**Problem**: (c) re-explains in full the distinction (a) already establishes. Two paragraphs say the same thing in different words — the pattern the anti-bloat classifier flags as compounding across cycles.

**Required**: State the allocated-empty/default-empty distinction once (the Notational convention is the natural home) and have the K.δ frame and K.σ-subsumption text reference it rather than restate it.

## OUT_OF_SCOPE

None. The ASN correctly defers named operations (INSERT/DELETE/COPY/REARRANGE/MAKELINK/CREATENEWVERSION), link-inheritance-under-fork, concurrency, and tombstoning to its Open Questions rather than specifying them, consistent with the declared scope.

VERDICT: REVISE
