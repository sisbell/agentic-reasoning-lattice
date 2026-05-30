# Channel Assignment — ASN-0043 review-73

**Date:** 2026-05-30 07:46

## Issue 1: T10a.8 is cited as a foundation claim but is not in the foundation
Reason: Pure citation/derivation question against the ASN-0034 foundation. The fix is to derive zero-count preservation inline from TA5(c) + TA5-SigValid (both present in foundation) or confirm T10a.8's existence — both resolvable from the ASN's own cited authorities, no design intent or implementation evidence needed.

## Issue 2: L9 reasons at length about a case its own precondition excludes
Reason: Reviser-drift cleanup. The precondition `dom(Σ.M) ≠ ∅` already excludes the analyzed case; trimming the carrier-root excursion is a purely editorial fix derivable from the ASN's own logic.

## Issue 3: L1c narrates the draft's own revision history
Reason: Editorial removal of meta-prose. The `k₁ = 2` structural argument already stands in its own terms; deleting the "earlier draft" framing requires no external input.

## Issue 4: Use-site inventories instead of meaning-advancing prose
Reason: Editorial deletion of redundant forward consumer-lists. Downstream claims already cite their premises; removal is internal cleanup.

## Issue 5: PrefixSpanCoverage relocation note repeated across three locations
Reason: De-duplication of a relocation note across three sections. Choosing the single home (Open Questions) is purely internal editorial.

## Issue 6: L-fin prose explains why the axiom is needed rather than what it says
Reason: Trim the necessity essay down to the S8-fin parallel. Internal editorial fix, no design or implementation question.

## Issue 7: A proof sketch sits under a clause declared an axiom
Reason: Internal consistency decision — axiom-vs-lemma classification. The sketch claims derivability from ASN-0034 primitives already cited; choosing to fully derive (LEMMA) or assert (AXIOM, dropping the sketch) is resolvable from the ASN's own foundation references.
