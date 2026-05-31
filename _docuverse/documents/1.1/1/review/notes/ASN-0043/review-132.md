# Review of ASN-0043

## REVISE

### Issue 1: L11a's case analysis over-derives a single-step precondition

**ASN-0043, L11a — LinkUniqueness**: "GlobalUniqueness's single-system precondition reduces to showing both events lie in the one tree 𝒯 — which the two cases establish via T10a's at-most-once-per-`(t, k')` constraint." (followed by the *Distinct homes* and *Shared home* paragraphs).

**Problem**: L11a's own premise already states "distinct allocation events producing link addresses `a₁` and `a₂` **in the system**" — that is precisely GlobalUniqueness's precondition (distinct events within one T10a system), so GlobalUniqueness yields `a₁ ≠ a₂` directly. The single-tree membership the author worries about follows in one step: by S7d every document is a node of the single tree 𝒯, and by L1c each link's chain is seeded at its document node and proceeds by T10a steps, hence never leaves 𝒯. The *Distinct homes* / *Shared home* split, and in particular the *Shared home* paragraph's reconstruction of T10a's at-most-once edge-sharing (`inc(d, 2)` is "one shared edge", the `s_L−1` advances "must precede any descent", `inc(d.0.s_L, 1)` is "a second shared edge"), establishes nothing beyond "both events lie in 𝒯" and re-derives foundation (GlobalUniqueness/T10a) internals inline. This is the accretion pattern flagged for this note: prose that reconstructs a foundation proof rather than citing it.

**Required**: Replace both case paragraphs with the one-step argument — S7d places each home in 𝒯, L1c keeps each link chain within 𝒯, so both events are distinct allocation events of the single T10a system and GlobalUniqueness applies. Drop the shared-edge / at-most-once reconstruction.

### Issue 2: L13's validity claim restates L4(c)

**ASN-0043, L13 — ReflexiveAddressing**: "Link addresses are valid targets for endset spans."
**ASN-0043, L4(c)**: "Cross-subspace endsets. Endset spans may reference addresses in the link subspace — that is, addresses of other links."

**Problem**: L13's opening assertion is the same claim L4(c) already makes, phrased differently. L13's genuine content — the canonical link-to-link span and its coverage via PrefixSpanCoverage, plus the CONS-cell composition — is not redundant, but the leading "valid target" sentence duplicates L4(c).

**Required**: Drop the redundant validity sentence; have L13 cite L4(c) for admissibility and confine itself to the canonical-span/compound-link content that is its own.

### Issue 3: The "L0a discharge" is named for L0a but defined inside L0b

**ASN-0043, L0b proof ("*The L0a discharge*") and its call sites**: the disjointness argument is labeled "the L0a discharge" yet resides in L0b's proof; L9, FSP, L11b, and the worked example all invoke "the L0a discharge."

**Problem**: A reader following "By the L0a discharge" will look under L0a, where no such argument appears — it is in L0b. The cross-references defer to a location that does not match the name.

**Required**: Either move the discharge argument under L0a, or rename it (e.g., "the subspace-disjointness discharge") so the label points to where it is defined.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
