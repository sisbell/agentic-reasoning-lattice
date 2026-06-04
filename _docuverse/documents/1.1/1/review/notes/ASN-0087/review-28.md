# Review of ASN-0087

## REVISE

### Issue 1: Self-labeled non-load-bearing prose in the L1c verification
**ASN-0087, Per-State Invariants at Σ' (L1c)**: "*Supplementary observation — chain uniqueness (not load-bearing; L1c needs only existence).* Given the downstream invariants ... the chain ... is the *unique* structural inc-derivation meeting L1c's constraints."
**Problem**: The reviser explicitly marks this observation as not load-bearing for the invariant being discharged. L1c requires existence; uniqueness advances no claim in this ASN. This is meta-prose the precise reader must skip past.
**Required**: Delete the supplementary observation, or move uniqueness to a downstream ASN that actually consumes it.

### Issue 2: M-DepthConv over-justification and triple-deferred "retained downstream"
**ASN-0087, Inputs (M-DepthConv)**: "This is not an arbitrary tie-break: it is the canonical link-subspace depth of the standard creation path. Nelson fixes ... Gregory's `findnextlinkvsa` (do2.c:151–167) realizes ... Nelson does *not*, however, declare depth 2 a closed invariant..."
**Problem**: The convention's content is "MAKELINK fixes first-link depth at m=2." The surrounding sentences justify *why* the convention is reasonable (defensive "not an arbitrary tie-break," dual Nelson/Gregory citations, anticipation of deeper links) rather than advancing the operation's meaning. Separately, the clause "the general `m_L(d)` reading is retained downstream" appears three times (Inputs, Effect, claim table M-DepthConv) — the same downstream deferral restated.
**Required**: State the convention once with its minimal warrant (Σ leaves m free; MAKELINK commits to minimal m=2). Drop the duplicated "retained downstream" deferrals to a single statement.

### Issue 3: Reflexive case re-derived in four locations
**ASN-0087**: the forced-discoverability-via-`v_ℓ` result appears in (a) the worked-example "Reflexive variant," (b) "Weakest Precondition" Case 2, (c) the "Reflexive Endsets" section, and (d) "Atomicity" ("The reflexive case is treated in the 'Reflexive Endsets' section").
**Problem**: The same analytical point — `ℓ ∈ coverage(eᵢ) ⟹ v_ℓ ∈ project(ℓ,i,d,Σ')` forced regardless of `Σ.M(d)` — is stated and partially re-derived in four places, with cross-section deferrals between them. The concrete worked-example variant is acceptable as an example, but it re-explains M-Reflexive verbally rather than just exhibiting it.
**Required**: Consolidate the derivation in "Reflexive Endsets" (carrier of M-Reflexive); reduce the WP Case 2 and Atomicity mentions to a citation; keep the worked-example variant as numbers-only without re-deriving the lemma.

### Issue 4: "Permanence" section opening duplicates "Permanence of the Recording"
**ASN-0087, Permanence**: "By LP13 (ASN-0098), the link persists unconditionally: ... The link is permanent in the strongest sense: its identity, its value, and its home are all immutable."
**Problem**: This restates "Permanence of the Recording" (L12 + LP13 + LP3★) already established earlier. The genuinely new content here is the `v_ℓ ↦ ℓ` binding / K.μ~ link-subspace-fixing analysis; the opening paragraph repeats prior material.
**Required**: Open the section directly with the new V-position-binding analysis and cite the earlier permanence result rather than restating it.

### Issue 5: Essayistic design-intent prose in structural slots
**ASN-0087, Discoverability Is Symmetric / What Does Not Change / What Is Indexed**: e.g. "This matches Nelson's design intent: when a link's endsets reach into different documents..."; "The phenomenology Nelson describes ... falls out of the architecture"; "This is the abstract content of what Nelson calls the system's 'inter-indexing mechanisms'."
**Problem**: These are framing essays explaining motivation, sitting in slots that carry derivations (the LP12 symmetry claim, the frame guarantees). They restate the formal result in motivational prose without advancing it.
**Required**: Retain the formal claims (LP12 symmetry, `Σ'.C = Σ.C` totality, M-NoIndexState) and trim the Nelson-intent restatements to at most a single grounding sentence each.

## OUT_OF_SCOPE

### Topic 1: V-position movement within the link subspace by later operations
**Why out of scope**: The Open Question on whether a link's `v_ℓ` may move under subsequent operations concerns K.μ~/K.μ⁻ mechanics (reordering/contraction), which are version/arrangement-operation territory for a future ASN, not MAKELINK.

### Topic 2: Endset well-formedness for forward-reaching (not-yet-allocated) addresses
**Why out of scope**: The Open Question on constraints beyond `e₃ ≠ ∅` for spans referencing unallocated I-addresses is genuine future territory; L4 (ASN-0043) already permits such spans, and tightening them is not a MAKELINK obligation.

VERDICT: REVISE
