# Channel Assignment — ASN-0094 review-69

**Date:** 2026-05-24 19:35

## Issue 1: Foundation citation violation — ASN-0036 and ASN-0093 cited by number
Reason: The framework already maintains scaffolding clauses for substrate properties; the fix is to either surface the cited ASN-0036/ASN-0093 invariants as additional scaffolding clauses or defer to ASN-0086's SubstrateConformingLayer wholesale. Both routes are internal restructuring within the ASN's existing patterns.

## Issue 2: Sh5's central claim collapses to hand-curation
Reason: The choice between attempting a mechanical body-derivation proof and shrinking Sh5's scope to the organizational-convenience reading is a framework-internal architectural decision; the author already documents both readings, so the fix is to commit to one and remove the other's prose.

## Issue 3: Massive reviser-drift accretion
Reason: Pure prose-trimming exercise; the ASN's substantive content provides the canonical source for each restated point, so the consolidation work is identifying duplicates and removing them.

## Issue 4: Properties Introduced table entries are essays, not statements
Reason: Table-format editing; the body sections already contain the elaborated content, so the table entries can be reduced to one-line summaries by reference to the body.

## Issue 5: NullifyActiveSubsetCompatibility Corollary is over-elaborated
Reason: Editing exercise; the corollary's mathematical content (active-subset preservation under both branches via case-split) is already stated, and the surrounding meta-discussion can be cut without affecting the formal content.

## Issue 6: Walkthrough redundancy
Reason: Editing/consolidation; the Common rejection patterns enumeration provides the canonical reference for each pattern, so per-walkthrough re-derivations can be replaced with citations to that section.

## Issue 7: Three Peano-style axioms added in the appendix
Reason: Mathematical restructuring; the author can attempt to rebuild LinkAddressNotPrefixOfEmit Step II.0 using position-based reasoning over T0/T3/Prefix directly (avoiding the `#a − #b` length subtraction that drives the NAT-sub requirement), or alternatively defer the foundation-extension request to ASN-0034 — both routes are internal framework decisions.

## Issue 8: The "Reach of the framework's target-domain symbols" is a scope-boundary essay
Reason: Editing exercise; the scope boundary itself is already stated, and the udanax/Nelson commentary can be relocated to a design-notes file without changing the technical decision.

## Issue 9: The Sh-conf "Gate Ordering (consolidated)" duplicates per-contract ordering clauses
Reason: Deduplication; the consolidated table is the canonical source, and per-contract ordering paragraphs can be replaced with citations by gate number.

## Issue 10: AllocatedAddressAntichain's Case 3 worked example
Reason: Editing exercise; the choice between providing a contradiction-extraction trace at an almost-satisfying configuration or omitting the example entirely is internal, and both alternatives derive from the existing formal proof.

## Issue 11: The single-home/Sh4/FDD contracts each state mutual-exclusion and routing
Reason: Deduplication; the structural impossibility is established by the shape registry's idem-flag commitment, so one statement in the Canonical Shape Catalog section suffices.

## Issue 12: The "Catalog-wide citation audit" table is bloat
Reason: Editing exercise; the existing worked-check examples already demonstrate the per-row classification rule, and the audit table can be dropped without losing structural content.

## Issue 13: The proof of Sh0 Case A enumerates step classes
Reason: Proof-presentation editing; the case-equation closure argument is uniform across Sh0–Sh3, so the per-transition-class enumeration can be replaced with one statement plus a reference to the case-equation.

## Issue 14: Multiple "deferred to downstream" forward references
Reason: Structural reorganization; forward references can be resolved by inlining content at the citation site or by reordering material so cited content comes first, both of which are internal to the document.

## Issue 15: ShapeWellFormedness literal-vs-set arithmetic justifications
Reason: Editing exercise; the implication antecedents are formal equality tests against registry values, so the "literal" clarification adds no formal content and can be cut.
