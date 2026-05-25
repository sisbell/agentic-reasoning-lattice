## Question 6 [theory]

> What must the system guarantee about distinguishing original content from content that was incorporated from elsewhere?

# Distinguishing Original from Incorporated Content

The system MUST maintain this distinction structurally, not as removable metadata. Here is what I require:

## 1. Every Byte Knows Its Home

The address itself encodes origin. Each byte has a permanent Istream address whose Document field identifies the document that *created* it. "Native bytes" live under their home document's control; everything else is fetched from its home:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

This is not metadata that can be stripped. To deliver a non-native byte at all, the system must request it from its origin.

## 2. Identity by Creation, Not Value

Two documents containing identical text but written independently have *different* I-addresses. Identity tracks *where the content was born*, not what it says. This means "the same passage" can only be recognized as the same when it shares Istream origin — through transclusion, not coincidental retyping.

## 3. Inclusions Are First-Class Citizens of the Document

Non-native bytes occupy positions in the Vstream "just as if they were native to the document":

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

But their Istream addresses still point home. The Vstream-to-Istream mapping is the distinction.

## 4. Always Traceable to Home

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is the user-facing guarantee. The mechanism (I-addresses) makes it impossible for the system to *lose* the distinction — it can only choose whether to *display* it.

## 5. Automatic Royalty Division Depends On It

The whole economic model requires this guarantee. When a compound or modified document is read:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

"As determined automatically" means the system must, at delivery time, count which bytes came from where. Without the native/non-native distinction, micropayment collapses.

## 6. The Original Is Always Recoverable

Even within a compound document that re-presents another author's work:

> "If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage. (The old viewpoint is still present too — you can always say, 'Show me what this originally was.')" [LM 2/45]

## What Is NOT Guaranteed

The system guarantees the *capability* to distinguish; it does not mandate that every front end *display* every inclusion. Quote-links explicitly acknowledge authorship; ordinary inclusions need not be flagged in the reader's view:

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated" [LM 4/53]

The guarantee is structural availability. How a particular front end presents this — with visible windows, with margin marks, with hover-reveal — is a design choice. But the *underlying knowledge* must always be retrievable from the address itself.

## The Underlying Principle

Reference, not copy. A copy severs the connection to origin and becomes "frozen and dead" [LM 2/48]. Transclusion preserves the live connection. The distinction between "wrote it here" and "included it from there" is the difference between literature as a web of acknowledged influences and literature as an unattributable mush. The system exists to preserve that web.
