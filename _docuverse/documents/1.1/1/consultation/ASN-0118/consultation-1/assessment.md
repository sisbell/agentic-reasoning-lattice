# Channel Assignment — ASN-0118 review-1

**Date:** 2026-06-08 17:07

## Issue 1: Cross-ASN reference to non-foundation ASN-0115
Reason: The fix restates the V-spec and `act` definition using foundation primitives already cited in the ASN (ASN-0034 span/T12, ASN-0053 level-uniform/ordinal-level, ASN-0036 V-position). Purely a self-containment refactor derivable from the ASN's own substrate section.

## Issue 2: No concrete worked example
Reason: A worked numerical scenario is constructed by instantiating CP0–CP11 with specific tumblers drawn from the address structure already defined (ASN-0036 S7). No design intent or implementation evidence is required to plug numbers into the existing formal definitions.

## Issue 3: CP4 multiplicity arithmetic is wrong
Reason: Pure arithmetic correction of a counting claim (per-address occurrence count vs. aggregate `W`); fully derivable from the resolution definition CP0 and placement CP2.

## Issue 4: CP7b cites a lemma whose precondition is not met
Reason: Re-grounding discoverability on LP12 at the post-state is internal formal reasoning; LP12, LP16, LP18 preconditions are all stated in ASN-0098 and checkable against the ASN's own CP2/CP7 facts.

## Issue 5: Contiguity/sequentiality preservation asserted, not derived
Reason: The tiling argument is ordinal arithmetic combining CP2, CP3a, and valid-insertion-position bounds — all present in the ASN and its cited foundations (ASN-0034 shift algebra). Derivable internally.

## Issue 6: Weakest-precondition analysis is trivial
Reason: Computing a non-trivial wp (e.g. link discoverability or a self-transclusion postcondition) is a formal derivation over the operation's already-specified effects and the LP12 coverage condition. No external channel needed.

## Issue 7: CP8 provenance justification incomplete for already-referenced addresses
Reason: The fix splits CP8's discharge between J1★ (range-new addresses) and P2 provenance permanence (already-referenced), both stated in ASN-0047. The range-newness condition and the self-transclusion case (CP9) are already in the ASN; purely internal formal restatement.
