## Question 10 [theory]

> Must the system distinguish, in its answer, between documents that contain the content as original authorship versus those that contain it through reuse?

# Must the System Distinguish Native vs Transcluding Documents in FINDDOCSCONTAINING?

**No, the operation is not required to tag its results — but the distinction is always recoverable from the structure itself.**

## The Operation Returns Both, Without Differentiation

FINDDOCSCONTAINING explicitly returns both kinds of documents together, without distinguishing them in the result:

> "This returns a list of all documents containing any portion of the material included by <vspec set>." [LM 4/70]

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

The phrase "regardless of where the native copies are located" is the key. The operation deliberately conflates native and non-native containment — both qualify as "containing."

## Why the Distinction Is Always Recoverable

Even though the operation returns an undifferentiated list, the native vs. transcluded distinction is preserved structurally. Each byte carries a permanent I-address encoding its home document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

This is what I mean by the attribution guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

So from any document in the returned list, the front end can compare the content's I-address against that document's own address space. One match is the home document (native authorship); the rest are inclusions (reuse).

## What This Means for the User-Facing Guarantee

I designed it this way because both relationships are legitimate forms of containment. A document that windows my prose genuinely contains it — non-native bytes are "as much a logical part of a document as native bytes" [LM 4/11]. Asking "who contains this material?" should surface the full web of relationships, not just the originator.

But the *kind* of containment matters for some purposes (royalty attribution, finding the canonical version, deciding whom to credit). The system must always make the distinction *available* to the front end through I-address inspection. It need not bake the distinction into FINDDOCSCONTAINING's wire format.

## Summary

| Requirement | Status |
|-------------|--------|
| Operation must tag results as native vs. transcluded | **No** — returns undifferentiated list [LM 4/63, 4/70] |
| System must preserve the distinction structurally | **Yes** — encoded in I-addresses [LM 4/11] |
| User must always be able to determine origin | **Yes** — attribution guarantee [LM 2/40] |

The structural information is sufficient; explicit tagging is a front-end convenience, not a back-end obligation.
