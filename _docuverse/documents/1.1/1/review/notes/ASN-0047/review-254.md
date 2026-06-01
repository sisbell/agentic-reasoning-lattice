# Review of ASN-0047

I read the full ASN. The mathematical core is sound: I checked the K.δ structural identities (zeros/parent under k=0/1/2), the D-SEQ★ derivation (both m=2 and m≥3 cases), the K.μ~ admissibility/realisability coincidence, the FrontierEquivalence biconditional, and all five worked examples against the elementary effects — no correctness defect surfaced. The findings below are confined to the `review-mode.anti-bloat` patterns the classifier flags.

## REVISE

### Issue 1: The K.δ case-(ii) freshness mechanism is stated three times
**ASN-0047, K.δ definition (case ii), "K.δ case (ii) discharge and parent-allocator activation", and Worked example Step 4**

The freshness-discharge mechanism for each k-regime is restated verbatim across three locations:
- K.δ definition, k=0: "`inc(t, 0) ∉ E` (the operational frontier check, discharged by FrontierEquivalence)."
- Discharge section, k=0: "Freshness `inc(t, 0) ∉ E` is discharged by FrontierEquivalence."
- Worked example Step 4: "freshness `inc(t, 0) ∉ E` is discharged via the *derived* form of T10a's chain-advancement uniqueness at `(t, 0)` (FrontierEquivalence)."

The k=1/k=2 "per-`(t,k')` direct uniqueness axiom" discharge is likewise stated in both the definition and the discharge section.

**Problem**: This is the flagged pattern "two paragraphs in different sections say the same thing in different words." The definition and the discharge section have genuinely distinct jobs (the definition states requirements + structural identities; the discharge section performs the parent-allocator *activation* analysis with the spawnPt-premise table), but the freshness-mechanism sentence is pure restatement carried in both, then a third time in the worked example. A reader following the freshness obligation re-encounters the identical FrontierEquivalence pointer three times.

**Required**: State the per-k freshness mechanism once — in the K.δ definition — and have the discharge section reference it for activation context only, without re-asserting the FrontierEquivalence / per-`(t,k')` discharge. The worked example should cite, not re-derive, it.

### Issue 2: P4 is introduced as a named property only to be declared unsatisfiable
**ASN-0047, "P4 (ProvenanceBounds — introduced and immediately superseded)"**: "`Contains(Σ) ⊆ R` ... P4 is unsatisfiable for the unscoped relation once any link-subspace mapping exists. The provenance bound must therefore be stated against the content-subspace restriction of containment, which P4★ below supplies."

**Problem**: P4 never holds in the extended state by the ASN's own argument, yet it is given a property label, a Properties-Introduced-table row ("superseded by P4★"), and a cross-reference target ("the same reason the unscoped P4 fails against P7 (*P4 box* above)"). Naming and tabulating a property that the ASN immediately proves cannot hold is meta-prose machinery around motivation rather than a load-bearing claim — it advances reasoning only as a strawman for P4★.

**Required**: Fold the "unscoped bound fails against P7 once link mappings exist" observation directly into P4★'s motivating sentence and drop the named P4, its box, and its table row. The motivation survives without a phantom property.

## OUT_OF_SCOPE

### Topic 1: Forked-arrangement / source-arrangement invariants
The first open question ("must a forked document's initial arrangement be identical, or a proper subset of its source's?") is correctly deferred — it is a constraint on a future operation-level ASN, not a gap in the transition taxonomy.

### Topic 2: Concurrent allocation and link-withdrawal mechanisms
The open questions on serialization under concurrent same-document allocation and on a separate link-withdrawal/tombstone mechanism are genuinely new territory (concurrency and a presentational mechanism outside K.μ⁻'s contract), not errors in this ASN.

VERDICT: REVISE
