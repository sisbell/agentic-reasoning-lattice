# Channel Assignment — ASN-0112 review-19

**Date:** 2026-06-08 09:07

## Issue 1: V18 overstates origin-moving transitions
Reason: The second origin-moving transition (first-content insertion into a link-only document) is fully derivable from claims already in the ASN — V5 establishes link-only as a reachable non-empty state with `origin_d = [s_L,1,…,1]`, and `s_C < s_L` (SubspaceConventionAxiom, T1) forces the drop to `[s_C,1,…,1]`. No design intent or implementation evidence is needed; the correction is internal arithmetic.

## Issue 2: V10 duplicates V16
Reason: This is a structural/anti-bloat editorial judgment about whether V10 carries content distinct from V16 — purely a matter of the ASN's own claim algebra. The reach-arithmetic deferral to INSERT/DELETE is already a settled scope statement; no external channel can add an invariant the query itself doesn't bear.

## Issue 3: Removable forward-reference deferral
Reason: Pure prose deletion of a redundant pointer sentence; nothing about design intent or implementation is at stake.

## Issue 4: Motivational essay inside a proof / repeated rhetorical frame
Reason: All Nelson quotations cited (4/25, 4/68, etc.) are already present in the ASN from Literary Machines; the fix is relocating and pruning existing prose, not sourcing new design intent or evidence.
