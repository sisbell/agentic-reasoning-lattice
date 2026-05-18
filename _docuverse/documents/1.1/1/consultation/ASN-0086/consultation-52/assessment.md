# Channel Assignment — ASN-0086 review-52

**Date:** 2026-05-18 04:50

## Issue 1: Implementation hypotheses placed inside Setup
Reason: Structural/organizational fix internal to the ASN — relocating three named hypotheses to a separate section requires only restructuring existing prose, no external evidence needed.

## Issue 2: R0a-Cor2's narrowing acknowledged narrower than design intent
Reason: The fix requires deciding whether depth-2 is the correct spec or merely implementation-observed; this needs both design intent (does Nelson admit deeper sub-links as foundational?) and implementation evidence (does udanax-green actually constrain to depth-2?).
Nelson question: Does the foundational link-model design intend depth-N recursive sub-link allocation as a core principle, or is depth-2 the intended specification with deeper structure handled by other mechanisms?
Gregory question: Does `findisatoinsertmolecule` (or any udanax-green link allocation path) ever produce link addresses with element-field length > 2, and if so under what conditions?

## Issue 3: R5's proof lacks substantive derivation
Reason: The fix is to expand the proof with a concrete self-targeting tuple construction that exercises R0's invariant-preservation argument; this is derivable from existing ASN-0043 and ASN-0086 content (R0, L4(c), L13).

## Issue 4: Single-tuple scope of Nullify ambiguously specified
Reason: Committing Nullify to one regime is a design choice that should align with what the design requires and what the implementation actually delivers; both channels inform whether the disciplined regime should be the contract.
Nelson question: Was Nullify intended to be a substrate-absolute operation (single-tuple scope unconditional) or a layer-conditional operation whose guarantees rest on caller discipline?
Gregory question: Does udanax-green's retraction path enforce the sibling-frontier discipline on the emitter address and rely on it for single-tuple-scope behavior, or does it admit retractions whose fresh emitters could land at prefix-extensions of the target?

## Issue 5: wp Case 3 (nullifying the retractor) is contrived
Reason: Replacing a trivial wp example with a substantive one (e.g., composed Emit_K + Nullify, or Observe over a coverage-class claim) is constructible from the ASN's existing operation definitions.

## Issue 6: R0a Stage 1 reverse-direction argument is redundant
Reason: Pure prose trimming — the antichain conclusion's symmetry is a standard observation, internal to the proof.

## Issue 7: Forward-reference accretion in R0a-Cor2's prose
Reason: Editorial trimming — removing meta-commentary from the lemma statement is purely internal.

## Issue 8: R6c Corollary cites unnamed ASN-0036 frame
Reason: The fix requires grounding the "arrangement-modification frame" in specific ASN-0036 clauses (P3 ArrangementMutability, combined with L12/L12a from ASN-0043); this is recoverable from the existing spec corpus without external consultation.
