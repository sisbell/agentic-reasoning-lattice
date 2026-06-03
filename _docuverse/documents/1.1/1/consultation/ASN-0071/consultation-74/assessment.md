# Channel Assignment — ASN-0071 review-74

**Date:** 2026-06-03 16:16

## Issue 1: vspec definition contradicts its own precondition list and the empty-source resolution case
Reason: Derivable from the ASN alone. The precondition list, *Resolution*, and F-DEEP all already commit consistently to admitting the empty-source case (`V_{s_C}(d_s) = ∅`); only the "minus two clauses" prose conflicts. The reviewer's preferred resolution (a) — relabel as "minus three clauses," explicitly drop clause (i), keep the empty-source treatment — restores internal consistency with the already-authoritative precondition list and needs no external evidence or design intent.
