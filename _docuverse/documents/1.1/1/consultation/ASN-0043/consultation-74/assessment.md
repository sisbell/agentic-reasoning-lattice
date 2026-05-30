# Channel Assignment — ASN-0043 review-74

**Date:** 2026-05-30 07:59

## Issue 1: L11a summary table contradicts the body derivation
Reason: Internal reconciliation — the table and body are two descriptions of the same proof within this ASN; the body's "instantiate GlobalUniqueness, no case split" account is already present, so the table row is rewritten to match it. No design intent or implementation evidence is at stake.

## Issue 2: Worked-example length leaks into the general L9 lemma
Reason: Internal — the fix replaces a concrete `#d' = 5` with the general bound `#g = #d' + 3 ≥ #d' + 1 ≥ 1`, derivable from the lemma's own quantification and T12's action-point condition already stated here.

## Issue 3: S7c cited but absent from the ASN-0036 foundation
Reason: Internal — the dependence can be weakened using facts already in this ASN: `subspace_I(b) = E(b)₁` needs only `#E ≥ 1`, which S7b's `zeros(b) = 3` plus T4's field-segment constraint deliver, so the `#E ≥ 2` appeals to S7c can be dropped where only `#E ≥ 1` is used. The cross-ASN confirmation is a foundation question, not a Nelson/Gregory one.

## Issue 4: Axiom-justification essay prose around L1c
Reason: Internal — the structural facts (third zero at `#s+1`, `s = h(a)`) are already captured by L1c's postcondition; collapsing the rationale paragraphs is pure prose discipline within the ASN.

## Issue 5: Repeated T4-validity derivation boilerplate
Reason: Internal — the derivation is established once at L1c via T10a.4; the duplicate parentheticals and the "Home and Ownership" re-walk are replaced with a bare cite. No external content needed.

## Issue 6: Scope-lift point repeated across five sections
Reason: Internal — the scope-lift caveat is consolidated to one location (Open Questions) and removed from the other four; this is deduplication of the ASN's own forward-looking note.

## Issue 7: Self-described bookkeeping inventory in the L9 proof
Reason: Internal — the inventory advances no reasoning beyond the state-local checks already listed; deleting or reducing it to one sentence is editorial cleanup within the proof.
