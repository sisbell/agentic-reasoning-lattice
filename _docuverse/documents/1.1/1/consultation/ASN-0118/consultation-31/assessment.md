# Channel Assignment — ASN-0118 review-31

**Date:** 2026-06-10 19:50

## Issue 1: S8a well-formedness of the span start is asserted but no longer derivable
Reason: The minimal fix (delete or condition the sentence) is internal, but choosing between deletion and an explicit boundary-well-formedness precondition depends on whether the implementation actually validates span starts; the ASN's existing Nelson quotes already settle the design-intent side (boundaries are permissive designators).
Gregory question: Does udanax-green validate or normalize the start tumbler of a V-span in a spec-set (e.g., reject starts with zero components or non-position tumblers) before resolving it, or does it accept any boundary tumbler and resolve purely by intersection with bound positions?

## Issue 2: I3-VP / I3-VD invoked outside their hypotheses
Reason: Internal fix — the ASN already deploys the correct derivation route (OrdShiftHom(b) and the shift length identity) for the gap-fill positions; the same one-liners apply to the shifted positions, and the review spells this out.

## Issue 3: The exhibited composite's K.ρ inventory is indeterminate
Reason: Either variant is internally consistent, so fixing the canonical witness is a choice — but it should match what the implementation does when re-copying content whose reference was already recorded, which is implementation evidence.
Gregory question: When COPY places content into a document that already has a recorded reference to that I-address (e.g., re-copying previously deleted transcluded material), does udanax-green skip the provenance/reference recording step or emit it redundantly?

## Issue 4: Repeated deferral to the composite section, with a near-verbatim duplicated sentence
Reason: Internal fix — purely an organizational/redundancy edit; the obligation and its discharge are both already present in the ASN, and the review specifies exactly which pointer to compress.
