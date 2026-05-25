# Channel Assignment — ASN-0068 review-6

**Date:** 2026-05-25 01:04

## Issue 1: CV-EMPTY motivation conflicts with CV-IN admissibility
Reason: The fix is internal — the ASN already contains the materials. Choosing between the two stated alternatives (explicit "empty subspace requires R = ⟨⟩" vs. relaxing CV-IN) is a spec-clarification choice derivable from CV-IN, S8-depth (ASN-0036), and the K.δ effect on M (ASN-0047), all of which are cited.

## Issue 2: "Valid V-predecessor" notation introduced inline rather than as a labeled claim
Reason: Promoting inline notation to a labeled CV-PRED definition with explicit existence/uniqueness/inverse clauses is structural cleanup. The proof obligations cite TS2 (ASN-0034), D-SEQ★ (ASN-0047), S8a (ASN-0036), and M-aux (ASN-0058) — all already referenced in the ASN.

## Issue 3: CV-MAX existence proof leans on S8-fin for left-walk termination when D-SEQ★ + S8a give a direct bound
Reason: The replacement bound (last-component decrement from D-SEQ★ bounded below by 1 from S8a) uses only claims already cited in the ASN. This is a proof refinement, not a content change.

## Issue 4: CV-ATOM's derivation is structurally a proof-by-absence
Reason: Restating the derivation as positive consequences of the run definition + CV-MAX is a proof restructure. The content of CV-ATOM is unchanged; the materials are all internal (run definition admits n ≥ 1; CV-MAX uniqueness handles aggregation and atomic isolation).

## Issue 5: Result type's bijection with `P(Span × Span)` is unlabeled but referenced
Reason: Promoting the projection to a labeled CV-SPAN-VIEW corollary uses the verification already given after CV-MAX (T12 from ASN-0034, level-uniformity from ASN-0053, OrdinalDisplacement from ASN-0034). The fix is consolidating existing material under a label.

## Issue 6: Concrete examples do not exercise differing depths
Reason: Constructing an example with m_a ≠ m_b is mechanical from the run definition and OrdinalShift's last-component formula (ASN-0034). The spec already commits to admitting differing depths; the example construction follows from definitions without needing implementation grounding or design intent.

## Issue 7: Self-comparison discussion lacks a labeled claim
Reason: The structural characterization of `corr_{a,a}` (diagonal + self-transclusion off-diagonal pairs) is already derived in the self-comparison discussion. Promoting it to a labeled CV-SELF claim uses only the relation definition and S7 (ASN-0036), both cited.
