# Channel Assignment — ASN-0134 review-13

**Date:** 2026-06-13 23:27

## Issue 1: idem=⊤ "no duplicate" is not a consequence of the per-home contract
Reason: Derivable from the ASN alone — the reviewer reconstructs the entire gap from the note's own text (§4 instance (i)'s "free-running … the wrong axis entirely," the MIC clauses, and the already-cited ASN-0128 I1/I1a/I4), and the choice between adding a global per-coverage-class clause (a) or weakening M1(b)(ii) (b) is an internal reconciliation of MIC against the model's existing idem semantics, not a question of new design intent or implementation evidence. Nelson's per-home locality is already cited and is precisely what creates the tension, so the resolution needs no further intent; Gregory's single-threaded loop is already established as globally over-satisfying, so it cannot inform what the *minimal* contract must add for idem=⊤ dedup.
