# Revision Consultation — ASN-0063

**Review:** review-6.md
**Date:** 2026-03-21 19:43

## Summary

5 REVISE items analyzed: 4 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 3: Orphan links section claims K.μ⁻ achieves link withdrawal without noting D-CTG constraint

**Category:** NELSON
**Reason:** The formal constraint (D-CTG prevents arbitrary interior removal) is clear from existing definitions. But whether link withdrawal should be supported and what mechanism Nelson intended — complete removal, boundary-only removal, or a separate withdrawal operation — is a design intent question.

**Nelson question:** When a document owner withdraws a link, did you envision the link being removed from the document's arrangement (requiring a mechanism to maintain contiguous ordering), or did you intend a different withdrawal mechanism such as marking the link as inactive while preserving its arrangement position?

**Nelson's Answer:**

This is an important question, and the answer follows directly from how links are addressed in tumbler-space.

## Links Have Permanent Addresses

Links are fundamentally different from bytes in one crucial respect: **links keep their creation-order addresses permanently**.

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

Link `2.5` is always the fifth link created in that document. Link `2.755` is always the 755th. There is no rearrangement of links — they do not have the Vstream flexibility that bytes enjoy. Bytes can be rearranged, inserted, transposed; links cannot. Their addresses are fixed at creation.

## Deletion Means "Not Currently Addressable"

The diagram on page 4/9 shows "DELETED LINKS" as a valid system state, with the annotation:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This parallels the treatment of deleted bytes exactly. The link is not removed from tumbler-space. It is not renumbered. It transitions to a state where it is **not currently addressable** — meaning the system will not return it in ordinary queries — but it remains structurally present for historical backtrack and may persist in other versions of the document.

## Why This Must Be So

Consider what would happen if link deletion required renumbering. Link `2.5` is deleted, so links `2.6` through `2.N` shift down. But other documents may contain **links-to-links** pointing at `2.6` by its tumbler address. Renumbering would break those references — violating the permanence guarantee:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." [LM 4/19]

The entire tumbler system is designed so that addresses, once assigned, are never invalidated. Renumbering links on deletion would destroy this invariant.

## The Mechanism

Link withdrawal is therefore the second of your two options: **the link is marked as inactive while preserving its arrangement position**. More precisely:

1. The link's tumbler address (`N.0.U.0.D.V.0.2.K`) remains permanently assigned
2. The link transitions to "not currently addressable" — it will not appear in `FINDLINKSFROMTOTHREE` results or `RETRIEVEENDSETS` responses for the current version
3. Historical backtrack can reconstruct the version where the link was active
4. If someone created a version of the document before the deletion, that version still contains the link
5. The gap in the link sequence (e.g., `2.4`, *gap*, `2.6`) is simply a consequence — links were never contiguous by guarantee, only sequential by creation order

This is consistent with the overall philosophy: **nothing is truly destroyed in Xanadu**. "Deletion" is always a Vstream operation — a change to what is currently visible — never an Istream operation that destroys permanent content.

NEED_RAW: [4/9, 4/31] — I would want to verify the exact visual layout of the page 4/9 diagram showing DELETED LINKS state, and confirm whether page 4/31 says anything additional about link address permanence beyond what's captured in the curated sources.
