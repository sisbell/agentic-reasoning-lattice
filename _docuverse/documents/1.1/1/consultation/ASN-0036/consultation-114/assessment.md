# Channel Assignment — ASN-0036 review-114

**Date:** 2026-05-28 20:27

## Issue 1: Verbatim T10a.4 gloss repeated across five contracts
Reason: Pure deduplication of identical prose — state the T10a.4 → T4-validity dependency once at S7b and cite it from S7a/S7c/S7/S7d. No design intent or implementation evidence needed; the dependency facts already exist in the ASN.

## Issue 2: S7c Consequences (b) and (c) are forward-reference / use-site inventory
Reason: Relocating already-present content — Consequence (b) is proved in ShiftPreservation, Consequence (c) belongs at the TA7a use-site. Both fixes are internal reorganization derivable from existing material.

## Issue 3: Definition contracts carry forward references and downstream-parallel notes
Reason: Removing meta-prose (forward pointers, reciprocal "parallels X" notes) from the `subspace`/`subspace_I` contracts. Purely editorial; the projections and their derivations are already present.

## Issue 4: S2 postcondition restates its own axiom
Reason: Either delete the redundant single-valuedness restatement or replace it with the well-definedness of `ran(M(d))` — both options are derivable from S2's own axiom and definitions already in the ASN.

## Issue 5: S8-fin justified by operations-layer appeal, not stated at strand level
Reason: The issue itself confirms S8-fin is legitimately a design requirement; the fix is to drop the operational-derivation prose. This is an internal presentation choice — keep the bare axiom — needing no external channel.

## Issue 6: Self-labeled non-dependency essay under S8-depth
Reason: The paragraph already declares itself non-load-bearing motivation; removing or compressing it is purely editorial and derivable from the ASN's own structure.
