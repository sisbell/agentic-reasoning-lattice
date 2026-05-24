# Channel Assignment — ASN-0094 review-39

**Date:** 2026-05-23 20:54

## Issue 1: "Strictly increasing under →-steps by R3" wording in Sh0–Sh3 induction framings
Reason: Fix is internal — correctly characterizing R3 (non-strict monotonicity) vs R0 (freshness gives strictness only at K.λ-steps at K or `K' ~ K`) is derivable from ASN-0086 citations already in the ASN.

## Issue 2: Sub-case II.B counterfactual example for `#w ≥ 2`
Reason: Fix is internal — the choice between simplifying the proof to exploit the structural `#w ≤ 1` bound or justifying the general additivity argument's robustness is a presentation decision derivable from the ASN's own L1 + T4(iv) reasoning already on the page.

## Issue 3: Resolution row standalone admissibility lacks an exhibited example at a distinct K
Reason: Fix is internal — adding a standalone walkthrough at a fresh Resolution-shape K (e.g., `approved_by`) follows the existing template-evaluation pattern; Sh5(b)'s mechanical-generation rule and the framework's preservation theorems supply everything needed.

## Issue 4: NullifyActiveSubsetCompatibility Case A proof says "in symmetry with Case B's explicit derivation" — but Case A is presented first
Reason: Pure editorial restructuring — either swap case order or rewrite Case A's preamble to lead with its direct argument. No external input needed.

## Issue 5: ShapeWellFormedness behavior at unregistered `(c_F = 0|1, t_F = -)` is unstated
Reason: Fix is internal — the semantic motivation (non-empty branch of `0|1` at `t_F = -` would force `slot_addrs(F) ⊆ ∅`, making the `|slot_addrs(F)| = 1` branch uninstantiable) is derivable directly from Sh-conf clause (d)'s reading already in the ASN.
