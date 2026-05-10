# Revision Categorization — ASN-0036 review-1

**Date:** 2026-03-14 15:27

## Issue 1: S5 formal statement does not match its intent
Category: INTERNAL
Reason: The fix is a quantifier reformulation — the intended meaning (no architectural cap) and the correct quantifier structure (over reachable states, not within a single state) are both derivable from the ASN's own discussion of unbounded sharing.

## Issue 2: S7 derivation from T4 has two gaps
Category: NELSON
Reason: Part (b) is an internal type restriction, but part (a) — whether I-space allocation is architecturally required to scope addresses under the allocating document's tumbler prefix — is a design intent question. Gregory's evidence that the implementation does this is already in the ASN; what's missing is whether Nelson intended this as a structural guarantee or whether it's an implementation convention.
Nelson question: Is it a design requirement that every I-space address be allocated under (scoped beneath) the tumbler prefix of the document that created it, so that the document field of an I-address always identifies the originating document — or is this an implementation convention that a conforming system could organize differently?

## Issue 3: S8 correspondence run displacement is underspecified
Category: GREGORY
Reason: The formalization requires knowing how V-space positions are concretely structured — whether they are always element-level tumblers at a fixed depth, what "consecutive V-positions" means in the enfilade. This determines k's type and whether T12 spans can isolate individual positions for the degenerate decomposition.
Gregory question: In the V-enfilade implementation, are V-space positions always element-level tumblers at a fixed depth, and does "consecutive positions" mean incrementing only at the lowest-level ordinal — or can V-addresses appear at varying depths within a document's virtual address space?

## Issue 4: S8 run-count monotonicity claim is false
Category: INTERNAL
Reason: The reviewer identifies a straightforward logical error — deletion removes entire runs, so run count fluctuates. The fix (retract or restate as I-space allocation event count) follows from S0/S1 and the ASN's own distinction between I-space events and V-space arrangement.

## Issue 5: No concrete example
Category: INTERNAL
Reason: The ASN and ASN-0034 together provide sufficient definitions (tumbler structure, arithmetic, field parsing) to construct a synthetic worked example with specific tumblers demonstrating the state model across a transition. No external evidence is needed — the example is built from the axioms already stated.
