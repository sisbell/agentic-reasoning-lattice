## Question 10 [theory]

> When the rearranged content is shared with another document, what isolates that other document's arrangement from being altered by this transposition?

## What isolates the other document

The isolation comes from the **Istream/Vstream separation**: REARRANGE is a pure Vstream operation that changes only the *rearranging* document's arrangement, while the shared content's permanent identity (its Istream addresses) is untouched — and the other document holds its *own independent Vstream mapping* over that same shared Istream content.

### The mechanism

When content is shared between documents, it is shared by **reference to Istream**, not by copy. Each document is a separate Vstream arrangement (a V→I mapping) over the same immutable Istream bytes. Transposing content in document A rewrites A's V→I mapping; it does not change the bytes themselves, and document B's V→I mapping is a wholly separate structure.

Per the `i-space-v-space` FEBE table:
- **REARRANGE** — "Pure Vstream operation"
- **COPY** — "Creates Vstream mapping to existing Istream (transclusion)"

Because rearrangement acts only on Vstream, and Istream is immutable, the shared content's identity never moves. Nelson:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

The other document obtains the shared bytes from their home location and gives them their own ordinal positions — so A's reordering of its own Vstream cannot reach into B's arrangement:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

### Why this holds for arrangement specifically

Each version/document is "a different Vstream arrangement over [the] same Istream content" (`i-space-v-space`), and editing changes the *arrangement, not the content*. This is the same principle that makes modifications non-destructive:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." (2/45)

A rearrangement is one such change: it re-twists one document's braid (its Vstream order) without altering the shared Istream content or any other document's separate mapping to it.

### Summary

The other document is isolated because (1) shared content lives once in immutable **Istream**, (2) each document expresses its order through its *own* **Vstream** mapping, and (3) **REARRANGE is a pure Vstream operation** confined to the document issuing it. The transposition reshuffles one document's references; it cannot touch the underlying content or the independent arrangement of any document that includes it.
