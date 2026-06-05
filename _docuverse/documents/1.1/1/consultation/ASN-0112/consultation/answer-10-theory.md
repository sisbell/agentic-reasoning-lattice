## Question 10 [theory]

> If two documents share content, must each still report its own distinct origin and extent, independent of the other's answer?

# Yes — each document reports its own origin and extent, independent of the other

Sharing content does not merge two documents into one. In Xanadu the shared bytes live once in **Istream**, but each document is its own **Vstream** arrangement with its own identity, its own address, and its own extent. The query that answers "where does this document begin and how far does it run" — `RETRIEVEDOCVSPAN` — operates on a single named document:

> "This returns a span determining the origin and extent of the V-stream of document <doc id>." (4/68, see `operations` memory)

The argument is a `<doc id>`. The answer is derived from *that document's* Vstream, not from any document it happens to share content with.

## Why the two answers are necessarily distinct

**1. Identity is structural and per-document.** Every document has its own permanent tumbler address (Node.0.User.0.Document). Two documents that share content are still two different positions in tumbler-space. There is no shared "extent" to report because extent is a property of a Vstream, and each document has its own.

**2. Transcluded bytes count as part of the borrowing document's own stream.** Nelson is explicit that included (non-native) content occupies an ordinal position in the borrowing document exactly as native content would:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "Non-native bytes are as much a logical part of a document as native bytes." (4/11)

So Document B's extent includes its transcluded span as B's own V-positions — it does not defer to or inherit Document A's extent.

**3. Origin (home) is traced per byte, not per document pair.** Even though content is shared, each byte's home document remains independently ascertainable:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

A document's *origin* in the `RETRIEVEDOCVSPAN` sense is the start of its own V-stream; the *home* of any individual transcluded byte is separately recoverable via its I-address. Neither is computed by consulting the other document's answer.

**4. Arrangements are independent even over identical content.** Two versions/documents can arrange the same Istream content differently:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." (2/19, see `versions` memory)

Because no arrangement is privileged, each document must answer for its own extent on its own terms.

## The correspondence point

The system *can* relate the two — that two documents share content is discoverable (`FINDDOCSCONTAINING` returns "all documents containing any portion of the material," 4/70). But correspondence is a *relation computed across* the documents; it does not collapse their separate extents. Each document still reports its own span.

**Summary:** Shared content is referenced once in Istream but belongs fully to each referencing document's own Vstream. `RETRIEVEDOCVSPAN` is per-document, so each document independently reports its own origin and extent — neither answer depends on, defers to, or is altered by the other.
