# Channel Assignment — ASN-0099 review-32

**Date:** 2026-05-27 05:03

```
## Issue 1: F4's uniqueness framing is heavy machinery for what is largely a tautology
Reason: This is a presentational reorganization decision — whether to lead F4 with realizability or with the formal uniqueness framing. The substantive content (realizability discharge, F1's match-formula choice, the F2/F3 conformance contract) is already fully present in the ASN; the fix involves restructuring what is there, not new design intent or implementation evidence.
```

```
## Issue 2: Worked example claims "F2/F3 verification against the instance" but the verification is necessarily tautological at the abstract level
Reason: Pure section-heading and framing fix — the prose already gestures at the abstract-spec-vs-implementation distinction; the fix is to make the headers match the prose's intent. Derivable from the ASN's own content.
```

```
## Issue 3: A1b's "closed-world reading" embeds an interpretive commitment that propagates to most downstream claims without flagging at point of use
Reason: This is a dependency-tagging consistency decision. The dependency graph from A1b to its consumers (F9, F9★, F9-cor, F9★-cor, F17, F18, F19-filt, F19-sco) is fully traceable within the ASN; the question is whether to tag uniformly or accept inheritance-by-chain. Internal to the ASN's own structure.
```

```
## Issue 4: F12's "definition" status conflicts with downstream treatment
Reason: Notation choice — distinguishing "by F12 (def)" from "by F12" at citation sites, or restating F12 as an abbreviation. The epistemic status of F12 is already settled in the ASN as definitional; the fix is purely about how to signal that at downstream citations.
```

```
## Issue 5: Worked example Query 11 verifies F9★ but the verification reduces to F9★-cor via a different state name
Reason: Worked-example composition choice — either reorganize Query 11's two-step sequence or add an explicit note about the cross-step precondition transfer. Internal to the worked example's construction; no design intent or implementation evidence is at stake.
```

```
## Issue 6: F2-V's dual conformance models (factored-through-result vs direct-V-side) is presented as a disjunction but is really a presentation choice for implementations
Reason: Presentation simplification — the two models produce identical outputs, so the fix is to either compress to a brief note or clarify what implementation flexibility actually exists. Derivable from F2-V/F3-V's own structure as already stated.
```

```
## Issue 7: The substrate-level fix for A1b is acknowledged but not pursued
Reason: To justify deferring the substrate revision rather than pursuing it, the methodological commitment to the closed-world reading should rest on something — either design intent (was the convention Nelson's, or is it a later interpretation?) or implementation evidence (does the udanax-green codebase actually preserve L across these operations?). Both inputs strengthen the deferral justification without requiring the substrate revision itself.
Nelson question: Is the closed-world reading of operation effect clauses — that state components absent from both effect and frame are preserved across the transition — part of the intended convention for the substrate operation vocabulary, or is it a downstream interpretive choice?
Gregory question: Does the udanax-green implementation of the operations corresponding to K.μ⁺ (content arrangement extension), K.μ⁻ (arrangement contraction), and K.ρ (provenance recording) leave the link store unmodified across each operation's execution?
```
