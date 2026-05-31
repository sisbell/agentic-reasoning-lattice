# Channel Assignment — ASN-0047 review-144

**Date:** 2026-05-31 14:30

## Issue 1: Document revision-history narration in normative prose
Reason: Purely editorial — deleting sentences that narrate the ASN's own drafting history. No design intent or implementation evidence is involved; the current precondition/derivation is already stated in the ASN.

## Issue 2: "Consumes / Produces / Does not consume" dependency-chain block is essay content in a structural slot
Reason: A presentation-restructuring task. The Steps (A)–(E) proofs already exist in the ASN; collapsing the annotation ledger and stating each proof once is internal to the document.

## Issue 3: Self-referential "single normative discharge gloss" notes
Reason: Editorial removal of meta-prose framing while retaining the substantive "frame"/"full-clearance" definitions, all of which are present in the ASN.

## Issue 4: Use-site inventories attached to definitions and lemmas
Reason: Removing downstream-consumer enumerations is internal bookkeeping cleanup; the named lemmas and identities remain citable by name without the inventories.

## Issue 5: `m_L ≥ 2` lower-bound justification is a non-sequitur and redundant with inherited S8a
Reason: The fix is derivable from the ASN's own carried invariants — S8a (ASN-0036, a Class (a) per-state invariant here) gives `#v ≥ 2` directly, so `m_L ≥ 2` follows without the TA7a appeal. No external channel is needed to substitute the correct derivation.

## Issue 6: Multiple paragraphs defer to the same downstream location
Reason: Consolidating scattered forward-references into a single placement is an internal reorganization of already-present material.

## Issue 7: K.δ k = 0 rationale re-derives an already-excluded conjunct
Reason: The precondition structure and structural identities settling `¬IsNode(t)` are already in the ASN; removing the state-then-justify-restatement is internal editing.
