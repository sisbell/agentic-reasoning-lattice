## Question 9 [theory]

> What must remain true about the original documents after a comparison is performed — are they altered, annotated, or untouched?

# Originals Are Untouched

Comparison must leave both documents completely unchanged. This is not a courtesy — it is a structural impossibility for comparison to do otherwise in my system.

## The Comparison Operation

The protocol command `SHOWRELATIONOF2VERSIONS` is purely a read operation:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

It returns *information about correspondence* — ordered pairs of spans. It does not write, mark, annotate, or modify either document. The output goes to the caller; the documents themselves are unaffected.

## Why This Must Be So

**Storage is append-only.** I built the entire storage paradigm around non-destruction:

> "Virtually all of computerdom is built around the inadequate convention of making whole copies of each current version ... A document is really not just a block of text ... it is an ongoing changing file ... an evolving braid." [LM 2/14]

A comparison cannot reach back and alter Istream content — Istream content is immutable by design.

**Only owners can modify.** Even if some operation wished to alter a document, it cannot:

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

A reader comparing two documents has no ownership authority over either, and the comparison operation itself confers none.

**Modifications never damage originals.** This is one of the fundamental guarantees of the system:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." [LM 2/45]

If even the act of *publishing a new derivative version* leaves the original intact, then certainly the act of merely *comparing* two existing documents leaves both intact.

## Highlighting Is Display, Not Modification

When I say:

> "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." [LM 3/13]

— this happens in the viewer, on the user's screen. The highlighting is a visual rendering of the correspondence relation returned by the comparison. It is not stored back into either document. The documents themselves remain bytes at their permanent Istream addresses.

## If a User Wants to Annotate

A user who wishes to record observations from a comparison creates *their own document* containing links (likely counterpart links or comment links) pointing into the compared documents. Those links live at *the user's* address, in *the user's* document — owned by them, not attached to the originals:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

The originals receive new *in-links* (which they cannot refuse, having been published), but their contents — their bytes, their arrangements, their identities — remain exactly as they were.

## Summary

After comparison:
- Istream content of both documents: **unchanged** (it is immutable)
- Vstream arrangements of both documents: **unchanged** (no edit operation occurred)
- No annotations are added to either document
- Any commentary the comparing user wishes to record lives in *their* document, not in the compared ones
- The comparison produces *information about* the documents, leaving the documents themselves wholly untouched

Comparison is observation. The observer does not mark the observed.
