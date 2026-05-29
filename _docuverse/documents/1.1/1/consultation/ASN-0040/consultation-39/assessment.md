# Channel Assignment — ASN-0040 review-39

**Date:** 2026-05-28 19:49

## Issue 1: The T4-preservation (TA5a) case analysis is written out four times
Reason: Pure deduplication — extract one "new element satisfies T4" lemma and cite it. The mathematical content already exists in the ASN; no design intent or implementation evidence is at stake.

## Issue 2: B4 is stated twice in full
Reason: Editorial deduplication of a label already defined in §B4. Internal to the document.

## Issue 3: B_type proof opening is misplaced and forward-references B_fin
Reason: Reordering/citation placement, fully resolvable from the ASN's own dependency structure. No external channel needed.

## Issue 4: Downstream-consumer enumeration in B_type's introduction
Reason: Removing a sentence that names consumers; purely editorial and derivable from the ASN alone.

## Issue 5: Non-circularity / document-ordering justifications around B0a and Bridge1
Reason: Trimming defensive meta-prose to a one-line construction statement. The partition's basis is already in the text; internal fix.

## Issue 6: "Load-bearing parenthesization" notation gloss
Reason: Deleting a reading-instruction paragraph; the formula carries its own scoping. Fully internal.

## Issue 7: Comparative essay in B8
Reason: Cutting rationale prose to one sentence while keeping the proof. No design intent question — the comparison to ASN-0034 is already understood from the ASNs themselves.

## Issue 8: Repeated "B6(iii) is ASN-0040's bridging restatement of TA5a" rationale
Reason: Deduplication of a clarifying remark to a single home at B6. Internal.

## Issue 9: Re-lettering of foundation (ASN-0034) notation, with explanation
Reason: A notation-consistency decision between ASN-0040 and its foundation ASN-0034. Both documents are available in the spec; resolvable by reading them, but confirming ASN-0034's actual symbol usage avoids guessing.
Gregory question: In ASN-0034, what symbols are used for the transition vocabulary versus the state and state space (is it Σ for vocabulary and s/𝒮 for states)?

## Issue 10: Joint-induction framing repeatedly defers to "the proofs below"
Reason: Restructuring where each preservation argument lives; the arguments themselves are all present in the ASN. Internal organizational fix.
