## Question 2 [theory]

> For a link with more than three endsets (the n-set case at 4/79), is FINDLINKSFROMTOTHREE meant to constrain only the from/to/type slots and leave any further endsets unmatched, or was a different treatment of the extra endsets intended?

I apologize — that tool call was a mistake; it's not relevant here. Let me address your question directly.

## Summary

I cannot fully answer this from the verified curated sources, because they do not cover the **n-set case at 4/79**. My curated extractions consistently describe the Xanadu link as having exactly **three** endsets (from-set, to-set, type/three-set), and they do not mention links with additional endsets. So the specific question — how `FINDLINKSFROMTOTHREE` is meant to treat endsets beyond the third — is not resolved by the material I can verify.

What the verified sources *do* establish:

**1. The command, as specified, constrains exactly three slots.** From the operations extraction (4/69):

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

By name and signature, `FINDLINKSFROMTOTHREE` exposes only three constrainable endset slots (from, to, three). There is no slot in this signature for a fourth-or-higher endset.

**2. The satisfaction model is phrased generally over "each endset."** From the links and operations extractions (4/58):

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

This wording — "each endset" rather than "each of the three endsets" — is notable. Read strictly, it could imply that *every* endset must be matched, which would have direct consequences for n-set links (the request would need a corresponding part for each). Read in the context of the three-endset model that pervades 4/42–4/47, it likely just means the three endsets.

**3. The dominant model throughout is strictly three-way.** The endsets and three-endset-links extractions (4/42–4/47) describe from-set, to-set, and type as *the* three endsets, with no mention of a generalized n-set form. So whatever 4/79 says about n-sets is not reconciled in the curated material.

## What I cannot verify

Your question presupposes an n-set generalization introduced at 4/79. My curated coverage of 4/79 only concerns unimplemented features (private documents, accounting, multi-server methods) and does not mention n-set links. I therefore cannot confirm either (a) that the extra endsets are intentionally left unmatched, or (b) that a different treatment was intended. Resolving this requires the original text.

NEED_RAW: 4/79 (the n-set statement and its surrounding context), and the link-search specification pages 4/58–4/60 and 4/69 (to check whether the "each endset" satisfaction rule and the `FINDLINKSFROMTOTHREE` signature were written with n-set links in mind).
