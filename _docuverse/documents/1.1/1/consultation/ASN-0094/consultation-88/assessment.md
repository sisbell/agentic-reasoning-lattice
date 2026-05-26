# Channel Assignment — ASN-0094 review-88

**Date:** 2026-05-25 20:45

## Issue 1: Cross-ASN references to non-foundation ASNs in SubstrateConformingLayer Definition
Reason: The fix is internal — reconcile the ASN's self-containment claim against its actual usage by inlining needed invariants into local scaffolding or dropping the catalog. The author can audit which clauses load-bear by inspecting the proofs already in this ASN.

## Issue 2: Redundant restatement at end of Retraction walkthrough
Reason: Pure editorial removal — the cross-reference adds no derivation beyond what EffectiveWpSimplification already establishes locally.

## Issue 3: "Failure mode" paragraph is near-tautological
Reason: Editorial cleanup — the precondition is already covered by the "Singleton-returning template under FunctionalDependencyDiscipline" paragraph immediately above.

## Issue 4: Sh4 Case D "structurally restricted" justification is overdetermined
Reason: Editorial tightening — the routing into Case D belongs in CaseAClosureForAK's statement (already defined in this ASN), so the justification can be moved or compressed to a single citation.

## Issue 5: Empty-G + idem = ⊤ admits an unobserved boundary
Reason: Framework design choice — BundledDirectedPair is introduced in this ASN, and the author can either document the semantic implication using the existing Sh4 contract content or move to Open Questions. The Nullify Compatibility section already establishes the active-vs-audit framing that would inform the note.

## Issue 6: "Lifetime semantics for `T_cat^rep`" repeats the configuration-parameter claim three times
Reason: Editorial consolidation of three paragraphs that say the same thing.

## Issue 7: AllocatedAddressAntichain — Case 3 element-level case-split is undermotivated
Reason: Citation cleanup against foundation references (T4 family in ASN-0034) — author can split T4 vs T4a/b/c citations based on what each foundation theorem supplies; this is derivable from the foundation refs already named.

## Issue 8: Worked Example "verifies postconditions" but doesn't verify wp_eff explicitly
Reason: The EffectiveWpSimplification formula is already stated in the ASN; adding a concrete computation at Emission 1 of the worked example is mechanical instantiation of the existing formula.

## Issue 9: Open Questions tag "[scope boundary]" for initial state baseline conflicts with framework reach
Reason: Structural reorganization within the ASN — the empty-baseline precondition is already documented in the Initial-State Baseline section; the choice between elevating to a top-level commitment vs. generalizing proofs is a framework-internal design decision.
