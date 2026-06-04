# Review of ASN-0076

## REVISE

### Issue 1: The τ_sup supersession-type-convention deferral is repeated across five sections
**ASN-0076, §The Composite / The Supersession Relationship / E4 / Appendix / Open Questions**: the same deferral appears at:
- §The Composite (τ_sup bullet): "Whether `τ_sup` lies in `dom(C)`, `dom(L)`, or neither ... is not constrained by the link model."
- The Supersession Relationship: "a convention this ASN cannot fix and defers to a future ASN on type-endset conventions (see Open Questions)."
- E4 note: "identifying `ℓ_sup` as *the* supersession requires the external `τ_sup` convention deferred in The Supersession Relationship."
- Appendix Step 2 gap; Open Questions Q2.

**Problem**: This is the forward-reference-accretion pattern — multiple paragraphs in different sections deferring to the same downstream location. The repetition does not advance the argument; the reader re-encounters the identical caveat four times after first meeting it.
**Required**: State the τ_sup-convention deferral once (at its definition in §The Composite), and let E4/Appendix/Open Questions reference the structural witness without re-litigating the deferral.

### Issue 2: Defensive proof-strategy meta-prose in E0
**ASN-0076, E0**: 
- "We derive freshness *at `Σ`* — the state at which the successor step fires — rather than appealing to first-emission freshness at the earlier entity-allocation event."
- "this is an observation about what the ordering achieves, not a justification of why the ordering must be as it is."
- "If the user wishes to allocate further links under `d_new` between the successor and supersession steps, those allocations belong to a different composite, not to this one."

**Problem**: The first two explain *why the proof is structured a certain way* rather than advancing it — reviser-drift defending against prior findings. The third imagines a case the composite's atomicity (ValidComposite★ adjacency, already established two sentences earlier) excludes.
**Required**: Delete the strategy-defense sentences; the freshness derivation stands on its own without announcing which alternative it declines. Drop the "if the user wishes" sentence — adjacency is already fixed.

### Issue 3: "Why Editing Cannot Be Otherwise" and "On Identity" restate established results
**ASN-0076, §Why Editing Cannot Be Otherwise / §On Identity**: the former re-proves that L12 forbids in-place mutation (the ASN's opening premise, already used in E1/E8/E9); the latter restates E2 (`ℓ_old ≠ ℓ_new`) and L12 (counter-claim cannot mutate `ℓ_sup`).
**Problem**: Essay content occupying structural slots, adding no claim or derivation beyond what E1, E2, E8, E9 already establish.
**Required**: Fold any non-redundant remark into the relevant claim's interpretation and remove the standalone sections.

### Issue 4: E7's reconciliation paragraph re-derives foundation lemmas
**ASN-0076, E7, "Reconciliation with ASN-0098's discoverability"**: "Unless the referents ... are independently arranged ... `ℓ_sup` is *orphaned* in the exact sense of LP17 ... LP18 (Resurrection) guarantees that once any subsequent transition arranges an I-address in its coverage, `ℓ_sup` becomes `discoverable_from` that document."
**Problem**: The load-bearing point — `covers` is an inverse `Σ.L` lookup, not arrangement-conditional `discoverable_from` — is one sentence. The remainder re-states LP17/LP18 (foundation, ASN-0098) and re-explains orphan/resurrection, which the foundation already owns.
**Required**: Keep the direction-and-state-component distinction; cite LP17/LP18 for the orphan consequence without reproducing their content.

### Issue 5: Appendix "Illustrative Reader Procedure" is a section of deferral prose
**ASN-0076, Appendix**: explicitly "illustrative, not a verified property," it lists four gaps each deferred to a future ASN, then a four-step sketch each step re-caveated against the same gaps.
**Problem**: The section establishes no property and consists almost entirely of meta-prose about what cannot yet be done, with four more forward references. The motivating intent ("the structural witnesses are intended to support a future reader") is one sentence buried under hedging.
**Required**: Reduce to a single short paragraph stating that E7's `covers` witness is the intended substrate for a future link-search ASN, and move the gap enumeration into Open Questions where the deferrals already live.

## OUT_OF_SCOPE

### Topic 1: Acyclicity / termination of supersession chains
**Why out of scope**: Open Questions correctly defers the invariants governing supersession-chain cycles to a future ASN; EDITLINK's per-composite guarantees (E0–E10) do not require it.

### Topic 2: Authorization of who may select `d_new`
**Why out of scope**: E6's application-layer note correctly defers executor/capability constraints to a future authorization ASN.

META: not applicable — the ASN defines a composite operation over link state and its invariants abstractly; it has not drifted into implementation mechanics, it has accreted meta-prose around its forward references.

VERDICT: REVISE
