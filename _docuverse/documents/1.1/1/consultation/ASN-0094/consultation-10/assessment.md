# Channel Assignment — ASN-0094 review-10

**Date:** 2026-05-19 22:52

```
## Issue 1: Cross-ASN references to ASN-0093 and ASN-0036 without foundation inclusion
Reason: Framework-architecture decision about which ASN-0086 abstractions to consume vs. enumerate; derivable from existing ASN-0086 SubstrateConformingLayer machinery already in the foundation.
```

```
## Issue 2: Worked examples implicitly assume `dom(Σ₀.L) = ∅` without stating it
Reason: Pure initial-state precondition fix — make the assumption explicit at each walkthrough's setup. Internal.
```

```
## Issue 3: R registration in T_cat assumed but not stated as a baseline requirement
Reason: Framework-internal baseline requirement; add R ∈ T_cat with the Retraction shape as a precondition. Derivable from ASN-0086's Nullify reduction already cited in the document.
```

```
## Issue 4: Sh4 Case D textual error — "below" should be "above"
Reason: Pure textual fix locating the scope clarification subsection relative to the proof. Internal.
```

```
## Issue 5: Catalog rows for Resolution and Retraction omit base templates, tension with Sh5 META discipline (b)
Reason: Sh5(b) mechanically determines base templates from shape components; the fix is to either enumerate them by analogy with DirectedPair or qualify the catalog presentation. Internal consistency repair.
```

```
## Issue 6: Variable name "home_K" reused across walkthroughs without disambiguation
Reason: Naming-convention fix at the example-prose level; no semantic content at stake. Internal.
```

```
## Issue 7: Definition — RetractionType is restated but not used; relationship to ASN-0086's machinery is unclear
Reason: Question is whether ASN-0094 restates or extends ASN-0086 definitions; ASN-0086 is already in the foundation, so the relationship is determinable by inspection. Internal.
```

```
## Issue 8: AllocatedAddressAntichain Case 3 Step 3.2 — implicit dependence on `#E(·) ≥ 1`
Reason: Proof-refinement question about which strength of the E-field non-emptiness assumption the conclusion actually consumes. Derivable by re-reading the proof's own use sites.
```

```
## Issue 9: Sh-conf's "effective wp" under non-relational-layer regimes is under-specified
Reason: Citation addition tying Retraction's shape to the unit-depth discipline at the wp_eff derivation site; both pieces are already present in the ASN and in ASN-0086. Internal.
```
