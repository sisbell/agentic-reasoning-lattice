# Channel Assignment — ASN-0094 review-57

**Date:** 2026-05-24 03:08

## Issue 1: Lemma — RetractionSelfFreshness stated mid-proof
Reason: Pure structural reorganization — the lemma is fully established in the current draft; the fix is moving it before Sh4's induction. Derivable from the ASN alone.

## Issue 2: Sub-case 3b worked example uses substrate-impossible configurations
Reason: R0a-Cor2 (strict `#E(·) = 2`) is already settled in ASN-0086, so the example's vacuity-on-substrate is internally determinable. Fix is either to scope the example explicitly or remove it.

## Issue 3: Sh5(b) per-shape uniformity admitted to be aspirational
Reason: The question of whether the typed predicate vocabulary was intended to mechanically derive templates from shapes or to be a hand-curated catalog is a design-intent question Nelson can settle.
Nelson question: Did the typed predicate framework envision a mechanical derivation of predicate forms from a relation's structural type, or an open-ended catalog of predicate roles attached to types by layer convention?

## Issue 4: Preservation theorems are "theorems under layer-discipline contracts"
Reason: The framework already justifies the layer-level placement (Sh4 Status paragraph); the review's complaint is presentational tagging. Derivable from the ASN alone.

## Issue 5: ASN-0086's Nullify postcondition is changed; audit-slice multiplicity is lost
Reason: Whether Nullify was designed as set-semantic or multiset-semantic is a Nelson question; what udanax-green actually does on duplicate Nullify of the same target is a Gregory question. Both channels needed before deciding whether to revise ASN-0086 or change ASN-0094's approach.
Nelson question: Was Nullify designed to record one retraction event per call (multiset/audit semantics), or to assert the target's nullified status once regardless of call multiplicity (set semantics)?
Gregory question: When udanax-green's allocator processes two consecutive bare retractions targeting the same address, does it produce one link-store entry or two?

## Issue 6: Length and scope sprawl
Reason: ASN scoping/decomposition decision; no design or implementation question. The framework's contents are internally enumerable for split. Derivable from the ASN alone.

## Issue 7: Three Peano supplements introduced in the appendix
Reason: Foundation extension decision — the question is whether (Peano-rec), (Peano-zero-least), (Peano-pred) belong in the foundation or a derived ASN. No Xanadu-specific design intent and no implementation evidence at issue. Derivable from the ASN alone.

## Issue 8: Coverage walkthrough's Rejection case C4 is structurally orthogonal
Reason: The substrate's chain-index machinery is fully axiomatized in ASN-0086 (R0a-Cor1, FreshEmissionAddress) and ASN-0034 (T10a.7); the fix is applying those axiomatized properties concretely to C1-C3. Derivable from the ASN alone.
