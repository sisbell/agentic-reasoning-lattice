# Channel Assignment — ASN-0043 review-143

**Date:** 2026-05-30 22:21

## Issue 1: L1a previews L2's endset-independence claim — duplicated reasoning across two sections
Reason: This is an internal editorial fix — removing the endset-independence preview from L1a and letting L2 carry it. The decision is fully derivable from the ASN's own structure (L1a's invariant is `home(a) ∈ dom(Σ.M)`; L2 already states endset-independence). No design intent or implementation evidence is needed.

## Issue 2: Worked-example verification is misordered — a check invokes a result established below it
Reason: This is a pure reordering of existing verification checks — moving D-MIN before D-SEQ and grouping L- and S-checks. All content already exists in the ASN; no external channel is required.
