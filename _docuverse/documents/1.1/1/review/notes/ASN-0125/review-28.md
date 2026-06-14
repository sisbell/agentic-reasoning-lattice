# Review of ASN-0125

I checked the operation contracts (EL6, EL7), the supersession-class machinery (Df-CLS through EL5), the discipline-maintenance induction (EL-DM), the discovery and currency results (EL11–EL16), and the worked example against the foundation contracts of ASN-0034/0036/0043/0047/0086/0093/0098. The substantive proofs hold up: the antichain (R0a) and content-exclusion arguments in EL11(a), the unit-depth/wp-Case-2 reasoning in EL6(iv)/EL7(iv), the activity-agnostic standoff in EL14(e), the address-vs-position discipline in EL10, and the five-step worked trace all check out, including the unconditional-vs-disciplined splits and the de-listing construction in EL9(2). The necessity derivation (EL2+EL3) is exhaustive over the state components once read as the two-step argument it is. The single finding is prose accretion at a forward reference, which the anti-bloat pass targets.

## REVISE

### Issue 1: EL13 and EL14(d) restate the same temporal-selector result

**ASN-0125, EL13 (TemporalErasure)**: "no temporal selector — any 'most-recent-wins' rule — is definable from state, the order it would read having no state witness; a global tie-break (say, T1-least claim address) remains definable but ranks namespaces, not times. What this forecloses for selecting a single latest edit, and what the reader is owed instead, is EL14(d)."

**ASN-0125, EL14(d)**: "No state-definable selector canonically identifies the latest edit ... so no temporal, recency-respecting selector is a function of Σ. This does not contradict EL13's definable tie-break: an arbitrary order such as T1-least claim address is state-definable, but it ranks namespaces, not times, returning a representative without identifying the latest edit — definable, yet not canonical."

**Problem**: Both passages assert the identical two-part claim — (1) no temporal/recency selector is a function of Σ, and (2) the T1-least tie-break is definable but ranks namespaces, not times. EL13 explicitly defers the latest-edit-selection discussion downstream ("What this forecloses ... is EL14(d)") and then EL14(d) re-derives the very point rather than building on it. This is the forward-reference-plus-restatement pattern the anti-bloat classifier flags: two paragraphs in different sections saying the same thing in different words, joined by a deferral that the destination then ignores.

**Required**: Consolidate the analysis into one location. EL13 should carry the formal commutation result and stop at the bare consequence (cross-home assertion order has no state witness); EL14(d) should own the latest-edit application, including the T1-least-ranks-namespaces observation, citing EL13 rather than restating it — or invert the ownership. The "ranks namespaces, not times" sentence should appear once.

## OUT_OF_SCOPE

The future topics the note touches (retraction-authority invariants, meta-claim stratification, span-level correspondence under endset reshaping, principal-level rather than home-level attribution, and edit/registry coupling) are confined to the Open Questions and correctly deferred — EL8(b)/EL13/EL14(d) route principal resolution to the ASN-0042 overlay without claiming authority invariants here, and the bare `K.λ` is used as a foundation primitive rather than re-specifying out-of-scope original-link creation. Nothing in the body drifts into these areas; no separate OUT_OF_SCOPE finding is needed.

VERDICT: REVISE
