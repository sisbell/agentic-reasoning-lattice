# Channel Assignment — ASN-0099 review-22

**Date:** 2026-05-26 23:55

## Issue 1: Conformance contract for `findlinks_V` is implicit, not explicit
Reason: The fix mirrors the existing F2/F3, F2-filt/F3-filt, F2-sco/F3-sco pattern using F12 (TwoPhaseFactoring) to derive V-side conformance from I-side conformance plus correct `image` computation. Fully derivable from the ASN's own content.

## Issue 2: F10's general "version chains nested" claim is verified only for one case
Reason: The structural argument for the general version-nesting case uses the same machinery already deployed for the specific instance (anchor non-nesting via CrossDocDisjointness, T1 case (i) at the divergence position, PrefixOrderingExtension). The fix is either to lift the argument from instance to lemma or soften prose — both derivable from existing content.

## Issue 3: F4's realizability discharge implicitly assumes reachability from Σ₀
Reason: The reachability of a base state with `dom(Σ.M) ≠ ∅` from Σ₀ follows from the standard K.δ initialization chain in ASN-0047 (node → account → document). The fix is a one-sentence citation to existing substrate axioms, requiring no external consultation.

## Issue 4: A1's transitional status
Reason: Nelson's design-intent position on A1 ("the substrate spec should harden this convention into an axiom — that is the design intent") is already captured in A1's grounding, and Gregory's implementation evidence is already recorded. The fix is an authorial framing decision about A1's permanence based on existing consultations — derivable from the ASN's own content.
