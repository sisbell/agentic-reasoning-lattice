# Channel Assignment — ASN-0094 review-61

**Date:** 2026-05-24 08:26

## Issue 1: Sh4 contract is described as "registered" but is actually automatic for idem=⊤
Reason: The fix is a clarification of the ASN's own framework — Sh4's automatic-from-shape status vs FDD/SHCD opt-in status is documented within the ASN (shape registry, Sh4 contract definition, FDD subsumption paragraph), so the four-case Π_K reduction can be derived from existing content.

## Issue 2: SubstrateConsumerActiveSubsetCompatibility Lemma is heavy for its substantive content
Reason: This is a structural/stylistic design choice about whether to elevate the (α)/(β) split to a numbered Lemma or condense it. The choice between condensing and strengthening (with an exhaustiveness claim) is internal to the ASN's own framing decisions.

## Issue 3: LinkAddressNotPrefixOfEmit's general additivity argument is preserved but trivial under current scaffolding
Reason: The reviewer flags that the general NAT-card additivity at Step II.1 is structurally trivial under current substrate scaffolding (zeros(d) = 2 forces #w ≤ 1, never exercising zeros(w) ≥ 1). Determining whether to retain or inline the general argument depends on whether the implementation actually produces (or admits) deeper document configurations.
Gregory question: In udanax-green, do document-level tumblers ever carry `zeros(d) > 2`, or does the implementation strictly maintain the four-field (N, U, D, E) hierarchy with two field-separator zeros at the document level — making the Step II.1 general additivity argument trivial at every substrate-reachable input?

## Issue 4: The Π_K conjunct's necessity argument needs tightening
Reason: The postcondition `(a, F, G) ∈ A_K^{Σ'}` is ambiguous between "any witness" and "new tuple deposited" readings; choosing which reading is intended and stating it clearly is an internal authoring decision derivable from the ASN's existing Sh4 contract semantics.

## Issue 5: Resolution row's "standalone admissibility" verification could be tighter
Reason: Adding an explicit Sh5(b) audit walk for the standalone Resolution registration is a mechanical application of the audit checklist (steps 0–3) already defined in Sh5(b), with the templates already exhibited in the walkthrough.

## Issue 6: Catalog audit table density limits extension feasibility
Reason: Adding worked Sh5(b) audit checks for Retraction's `pair_K(F̂, b)` and Provenance's `to_K(b)` is a mechanical application of the existing audit procedure (categories i–vi, literal name-citation rule) to template bodies already specified in their respective walkthroughs.
