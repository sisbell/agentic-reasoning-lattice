## Question 9 [theory]

> What does the design require about the boundary between newly inserted content and the content on either side of it — must the new region join the surrounding material seamlessly while remaining distinguishable as separately introduced?

## The boundary: seamless in Vstream, distinguishable in Istream

The design requires **both** properties simultaneously, and it achieves them by assigning the two requirements to its two different address spaces.

### Seamless join (Vstream)

Insertion makes the new region a continuous part of the document's virtual byte stream. INSERT renumbers everything after it:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

There is no gap, marker, or seam at the V-level — V-addresses are dense and contiguous, and included material reads "just as if" it belonged there:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." (4/11)

So reading flows across the boundary without interruption. That is the "seamless join."

### Remaining distinguishable (Istream)

At the same time, every byte keeps a permanent Istream identity encoding where it came from, so the introduced region never loses its separate provenance:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

> "Native bytes of a document are those actually stored under its control... all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Non-native byte-spans are called inclusions or virtual copies." (4/11)

If the inserted content is brought in by COPY (transclusion), it carries the *source's* I-addresses, so it is intrinsically marked as separately introduced. If it is freshly typed, it receives new native I-addresses appended chronologically — Nelson's storage is append-only, "filed, as it were, chronologically" (2/14) — and version comparison exposes it as the part with no counterpart in the prior arrangement:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70, SHOWRELATIONOF2VERSIONS)

### Why the boundary holds under further editing

Because links and spans attach to *bytes* (I-identity), not positions, the surrounding material on either side keeps its identity when the new region is spliced in:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

### Answer

Yes to both halves of your question. The design requires the inserted region to **merge seamlessly** into the reading sequence (Vstream contiguity, following addresses shifted, no visible seam) while requiring it to **remain distinguishable as separately introduced** (permanent Istream addresses, traceable home document, and version correspondence that isolates exactly the added span). The seam is erased in the *arrangement* but preserved in the *identity* — that is precisely the I/V separation Nelson's model depends on.

(One nuance worth flagging: the curated sources strongly establish seamless-Vstream + traceable-Istream, but they do not contain a single passage that *explicitly states as a requirement* "an insertion must be both seamless and separately distinguishable." That conclusion is synthesized from the INSERT semantics (4/66), the native/non-native distinction (4/11), and origin traceability (2/40). If you want Nelson's own words tying insertion directly to this boundary property, NEED_RAW: 4/8-4/12, 2/35-2/40.)
