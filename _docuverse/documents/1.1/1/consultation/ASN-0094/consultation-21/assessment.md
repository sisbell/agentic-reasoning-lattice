# Channel Assignment — ASN-0094 review-21

**Date:** 2026-05-20 03:16

## Issue 1: Departure from ASN-0086's Nullify-as-sole-R-producer discipline is undocumented
Reason: The conflict is about whether retraction was intended to carry attribution (F≠∅) or be a bare nullify alias. Nelson's design intent settles whether attributed retraction is part of the model; Gregory confirms whether the implementation records retraction attribution.
Nelson question: Was retraction intended to carry an attribution endset (who retracted), or is retraction in the design strictly a bare "this tuple is nullified" operation with no actor recorded?
Gregory question: Does the udanax-green retraction operation accept or record any attribution metadata about the retracting party, or does it only carry the address of the tuple being nullified?

## Issue 2: "Or, equivalently" baseline relaxation doesn't cover Sh4
Reason: The defect is internal — Sh4/FDD/SHCD's quantifier structure (over pairs/homes) is already stated in the ASN, and the gap between per-tuple conformance and pair-wise/homed-set invariants is derivable from the ASN's own preservation proofs.

## Issue 3: Case I of RetractionTargetNotOnChain conflates first- and subsequent-emission branches
Reason: The defect is internal — FreshEmissionAddress (cited in the ASN) defines exactly when each branch fires, and Case I's hypothesis `home(b) = d` makes the first-emission predicate non-empty by direct inspection.

## Issue 4: T_cat / ~ finiteness is asserted but per-class accessibility for the framework's catalog operations is not derived
Reason: The defect is internal — the choice between coverage-class membership and literal endset membership is a framework-design decision driven by what the Sh-conf gate consumes; the ASN already commits to per-class constancy and `~`-closure, so the decidability reading is derivable from the ASN's existing scaffolding.

## Issue 5: The Sh5(b) discipline's "literal name-citation" rule has no formal verification mechanism in the framework
Reason: The defect is internal — the ASN already enumerates its catalog rows and template bodies; verifying each template against the four data-symbol categories is a mechanical pass over content already in the ASN, with one row (latest_K_for_addr) demonstrating the pattern.
