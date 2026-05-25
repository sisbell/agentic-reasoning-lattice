## Question 3 [theory]

> Must the deleted content returned by this operation retain its original identity, or is it sufficient to return a copy of the missing material?

# Deleted Content Must Retain Original Identity

Deleted content MUST retain its original Istream identity. Returning a copy with new identity would violate Xanadu's foundational guarantees.

## The Architectural Reason

In Xanadu, content identity IS the Istream address. Content is not identified by its byte values but by its permanent I-address. As stated in the sporgl-provenance concept derived from 4/10-4/11:

> "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses."

DELETE is explicitly defined as a Vstream operation that does NOT affect Istream:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The content remains at its original I-address. Historical backtrack RECOVERS the existing content — it does not RECREATE it.

## Why a Copy Would Fail

If deleted content returned with new identity, four guarantees collapse:

**1. Link survivability breaks.** Links attach to Istream bytes by I-address. If recovered content has a new identity, links to the deleted content would still point to the original (still in Istream), not the returned copy.

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

**2. Transclusion integrity breaks.** Other documents may have transcluded this content. They reference the original I-address:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

A copy with new identity would be a different inclusion — disconnected from existing transclusions.

**3. Origin traceability breaks.** The I-address encodes the Document field of origin:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

A copy fabricates new provenance.

**4. Non-destruction breaks.** Nelson's append-only storage principle:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Recovery is reading from append-only storage. There is nothing to copy from — only the original to be read.

## The Operational Principle

Historical backtrack is not reconstruction; it is dereferencing addresses that were temporarily not addressable in Vstream. The bytes never moved. The I-address never changed. The "delete" only removed the V→I mapping in the current arrangement.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

A historical backtrack returns the *same* bytes at the *same* I-addresses they always had. Identity preservation is not optional — it is the entire point.
