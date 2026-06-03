# Channel Assignment — ASN-0091 review-32

**Date:** 2026-06-03 11:15

## Issue 1: Phantom foundation invariant "S9 (TwoStreamSeparation)"
Reason: Pure citation-accuracy fix against sibling foundation ASN-0036. The property `Σ'.M(d) ≠ Σ.M(d) ⟹ Σ'.C = Σ.C` already follows from RE-C, so it can be restated as a local corollary without external input. Neither design intent nor implementation evidence is at issue.

## Issue 2: Phantom foundation invariant "S7c"
Reason: Internal — ASN-0036 and ASN-0047 enumerate S7a/S7b/S7d (and S7) with no S7c; dropping the nonexistent label is mechanical and derivable from the foundation text itself.

## Issue 3: Phantom foundation lemma "R-SP (RearrangeSufficientPrecondition)"
Reason: Internal — re-anchoring on the lemmas ASN-0084 actually contains (R-RI, R-PIV, R-SWP, R-BLK, R-CANON, etc.) or restating the per-invariant discharges self-contained is a corpus-internal exercise; the discharges' actual premises (RA-dom, RA-π, structural projections) are already spelled out in this ASN.

## Issue 4: Phantom foundation lemma "R-DISP"
Reason: Internal — the displacement `Δ(μ) = w_β − w_α` is computable directly from R-S2 (already cited and used in the same trace), so the fix is to swap the citation, requiring no design or implementation input.

## Issue 5: Renamed foundation invariants/operations
Reason: Internal — using the verbatim foundation names (`Document(e)`, P4a = TraceWitnessing, `T4-valid`, K.δ Document case) is a lookup against ASN-0047/0093; no design intent or implementation behavior is in question, only naming fidelity.
