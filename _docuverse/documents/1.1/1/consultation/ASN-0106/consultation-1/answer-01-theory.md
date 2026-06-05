## Question 1 [theory]

> Was RETRIEVEDOCVSPANSET intended to report a document's extent as two summary counts (text-width and link-width), or as a full structural decomposition of its arrangement?

RETRIEVEDOCVSPANSET was intended to report **two summary counts**, not a full structural decomposition.

Nelson's own definition is explicit:

> "This returns a span-set indicating both the number of characters of text and the number of links in document <doc id>." (4/68)

So the operation yields a span-set with exactly two quantities: a text-width (count of characters) and a link-width (count of links). It does not enumerate where bytes live, how spans map to Istream, the arrangement of content, or which specific links exist — it is a size report on two dimensions.

This is clarified by contrast with its sibling operation. RETRIEVEDOCVSPAN returns the *extent* of the document as a single span:

> "This returns a span determining the origin and extent of the V-stream of document <doc id>." (4/68)

The pairing makes the design intent clear:
- **RETRIEVEDOCVSPAN** — one span giving origin + extent of the V-stream (where/how long).
- **RETRIEVEDOCVSPANSET** — a span-set giving the two counts (how much text, how many links).

Neither returns a structural decomposition of the arrangement. Full structural / content retrieval is the job of other operations — RETRIEVEV returns the actual material ("the material (text and links) determined by <spec set>", 4/68), and RETRIEVEENDSETS / the FINDLINKS family enumerate link structure.

This also fits the broader FEBE philosophy that storage internals (the V→I mapping, the actual arrangement) are hidden from the user; the front end gets semantic summaries and content on request, not the internal decomposition.

**Answer:** Two summary counts — a text-width (number of characters) and a link-width (number of links) — reported as a span-set. It was not intended as a structural decomposition of the document's arrangement.
