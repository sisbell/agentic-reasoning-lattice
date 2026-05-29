# Channel Assignment — ASN-0036 review-130

**Date:** 2026-05-28 23:24

## Issue 1: ShiftPreservation is fully proved but has no proof-level consumer in this ASN
Reason: This is a purely internal structural question — whether any claim in the ASN depends on the lemma — answerable by inspecting the ASN's own Depends clauses and proofs. The worked example already spells out the TumblerAdd prefix rule inline, so removal is derivable without external evidence or design intent.

## Issue 2: Abstract restatement duplicates the concrete "Violation" example
Reason: Pure redundancy cut — the concrete example and Open Question already carry the point. Deciding which copy to remove requires only reading the ASN's own text.

## Issue 3: Motivational meta-prose in a structural slot (OrdAddHom lead-in)
Reason: Trimming essay framing to the lemma statement is an internal prose edit; the lemma and proof already establish the homomorphism with no need for external input.

## Issue 4: Derivation prose and contracts state the same postconditions twice (self-flagged)
Reason: The duplication is between the ASN's own prose and its own contract postconditions; keeping the distinctness step and dropping the rest is fully derivable from the ASN's existing content.
