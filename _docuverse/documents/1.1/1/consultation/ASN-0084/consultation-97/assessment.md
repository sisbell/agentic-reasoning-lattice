# Channel Assignment — ASN-0084 review-97

**Date:** 2026-05-30 19:46

## Issue 1: "S8-uniq" reuses a foundation property name for a strictly weaker statement, then claims a non-maximal partition satisfies it
Reason: This is a purely internal naming/exposition fix — rename the per-position notion and restate R-BLK's claim as "a run partition (disjoint + covering), not maximal." Both the foundation's S8 uniqueness meaning and R-BLK's actual content are already present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: EXT-VAC over-derives an exhaustiveness characterization beyond the single fact any proof consumes
Reason: This is an internal pruning fix — the only consumer (R-BLK Phase 1) and the one fact it needs are both stated in the ASN, and D-SEQ already supplies the immediate implication. Trimming the surplus bound derivation requires nothing from Nelson or Gregory.
