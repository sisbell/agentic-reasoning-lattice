# Review of ASN-0087

## REVISE

### Issue 1: Problem statement overstates the discoverability guarantee
**ASN-0087, The Problem / What Is Indexed?**: "link creation must produce four things: an *identity* ..., a *value* ..., a *home* ..., and *discoverability* (the property that a query of the content reached by the link's endsets surfaces the link). The MAKELINK operation is the event by which all four come into being."
**Problem**: A link can be born *orphaned*. If every endset's coverage misses every document's arrangement range (content that exists in `dom(C)` but is currently unarranged, or forward-reaching spans into unallocated addresses), then by the body's own M-WP and LP17 the link is discoverable from no document at the post-state. So MAKELINK does not "bring discoverability into being" — it establishes only the LP12 *mechanism*, and actual discoverability is conditional on arrangement-reach (M-WP) or reflexivity (M-Reflexive). The intro presents as an unconditional product what the body correctly proves to be conditional. The framing "what is rendered discoverable" repeats the overclaim.
**Required**: Reconcile the intro with M-WP/LP17 — state that MAKELINK establishes the discoverability *property* (LP12), which yields actual discoverability only when some endset coverage meets some arrangement range; note explicitly that a link may be born orphaned.

### Issue 2: Reflexive authoring contradicts "cannot specify the address"
**ASN-0087, Inputs**: "The caller does *not* — and cannot — specify the link's address."
**ASN-0087, A Worked Example (Reflexive variant)**: "the caller computes `ℓ = [d, 0, 2, 1]` from `Σ` via `A_L(d)`'s deterministic first-emission rule."
**Problem**: M-Reflexive and the wp Case 2 reflexive disjunct (`ℓ ∈ coverage(eᵢ)`) require the caller to commit the link's own address into an endset span *before* MAKELINK runs. This is only possible if the caller predicts `ℓ`, which directly conflicts with the flat assertion that the caller "cannot specify the link's address." Moreover, the predicted value is state-dependent (`ℓ = inc(ℓ_prev, 0)` for subsequent emissions); the ASN never addresses what happens if an intervening allocation invalidates the prediction between authoring and execution, so M-Reflexive's realizability is asserted but not established.
**Required**: Clarify that "cannot specify" means the address is not an operation *parameter* (it is derived), while a reflexive author must *predict* the deterministic emission; and state the precondition under which the prediction is sound (e.g., no intervening `A_L(d)` emission), or scope reflexive authoring to the protocol layer explicitly.

### Issue 3: Reflexive case derived twice
**ASN-0087, A Worked Example (Reflexive variant) and Weakest Precondition Case 2**: Both passages independently establish `v_ℓ ∈ project(ℓ, i, d, Σ')` and forced discoverability from `ℓ ∈ coverage(eᵢ)`.
**Problem**: The worked-example reflexive variant re-derives exactly the content of M-Reflexive that wp Case 2 already proves (same `Σ'.L(ℓ).eᵢ = eᵢ`, same `Σ'.M(d)(v_ℓ) = ℓ`, same conclusion). Two passages in different sections say the same thing in different words.
**Required**: Keep the derivation in one location and have the other cite it.

### Issue 4: Essayistic rationale in structural slots
**ASN-0087, What Is Indexed? / Atomicity / No Permission Check**: e.g. "This is the abstract content of what Nelson calls the system's 'inter-indexing mechanisms' ..."; "Nelson's 'canonical operating condition' language suggests external atomicity is expected ... The strand model does not, by itself, supply it."; the "No Permission Check" closing rationale "Per Nelson's publication contract ... the design intent rules it out."
**Problem**: These paragraphs are rationale/essay content that does not advance the formal argument — the load-bearing statements ("no separate index state," "the composite is not atomic," "MAKELINK performs no permission check") are already carried by M-NoIndexState, M-CompAtomicity, and the operation-level statement. The Nelson-attribution and design-intent prose are meta-justification a precise reader must skip past.
**Required**: Reduce to the operational statement (what the operation does/does not do) and drop the appended design-intent justifications, or move them to a non-normative note.

## OUT_OF_SCOPE

### Topic 1: Protocol-level atomicity enforcement
The ASN correctly defers composite-level atomicity to the protocol layer (M-CompAtomicity). The mechanism by which a protocol layer enforces single-event visibility is new territory, not an error here.

VERDICT: REVISE
