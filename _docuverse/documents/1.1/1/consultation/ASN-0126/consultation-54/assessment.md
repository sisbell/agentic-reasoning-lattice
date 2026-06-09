# Channel Assignment — ASN-0126 review-54

**Date:** 2026-06-09 14:06

## Issue 1: "Properties established" re-derives P1–P4 that already have a narrative home
Reason: Purely structural — deciding one home per property and converting the P1–P3/P5 entries to pointers is editing the ASN's own organization, with no appeal to design intent or implementation behavior.

## Issue 2: the wp equation drops the L3 conjunct it names in the gate, without discharging it
Reason: The fix is derivable from content already present — the review supplies L3's three clauses and their discharge (arity-3 from precondition (0), slots from the `F, G ∈ Endset` input typing, slot-3 non-emptiness from the RegisteredAdmissible lemma already proved in-note), so the reviser only assembles the existing one-liner.

## Issue 3: "load-bearing vs convenience" and cross-substrate name prose is meta-commentary
Reason: A pure deletion of editorializing prose while keeping the two structural facts stated alongside it; removing commentary needs no verification of design intent or implementation, only the ASN's own text.
