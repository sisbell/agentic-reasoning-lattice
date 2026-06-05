## Question 10 [theory]

> Must requesting one end of a link leave the link itself, its other ends, and all referenced documents entirely unchanged?

## Short answer

Yes — at the level of link structure and document content, requesting one end of a link is a pure read. It leaves the link, its other endsets, and the documents those endsets point into entirely unchanged. The only things that move are *accounting* counters (cash register / royalty), and even those touch a document's bookkeeping area, not the link or the referenced content.

## Why the link and the referenced documents are untouched

**1. Retrieval operations "return"; they do not modify.** Nelson's command set splits cleanly into editing operations (INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND — all requiring ownership and all mutating Vstream) and retrieval operations, which are phrased purely as returning data. The operation that requests link endsets is RETRIEVEENDSETS:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

Likewise FINDLINKSFROMTOTHREE "returns a list of all links..." (4/69) and RETRIEVEV "returns the material..." (4/67). None of these alter what they read.

**2. The endsets are symmetric and independent.** A link's three endsets each map independently onto the tumbler line:

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

Requesting one endset addresses one side of the Tumbler Square; it neither consults nor disturbs the others. If you only ask for one end, the documents on the *other* ends need not even be contacted.

**3. Content is immutable.** Whatever a referenced endset points at lives in Istream, and Istream content never changes — reading it cannot alter it. "Deleted" content is preserved; arrangement edits are Vstream-only (see `i-space-v-space.md`, `delete-semantics.md`). So a read against any end cannot perturb the bytes there.

**4. Links survive *editing*, and only the owner edits.** The only thing that mutates a link's attachment is editing the bytes it straps to — and that is an ownership action, not a read:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

A request is not an edit, so it triggers none of this.

**5. The privacy principle assumes reads don't write.** Nelson treats reading as something the system must be able to do *without recording*:

> "The network will not, may not monitor what is read or what is written in private documents." (2/59)

This only makes sense if requesting/reading is non-mutating by nature.

## The one real caveat: accounting side effects

"Entirely unchanged" is true for the link and the referenced documents' *content and structure*, but not for their *accounting state* when content is actually delivered. Each published document carries a cash register:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document." (5/13, per `enforcement-model.md`)

And royalty accrues on delivery:

> "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned." (2/43)

So if requesting an end causes bytes/links to be *delivered* out of a document, that document's counter increments and a nib accrues. This is bookkeeping in the document's system area, not a change to the link, its endsets, or the referenced text. And a request that merely returns endset *addresses* (RETRIEVEENDSETS) need not deliver content from the far documents at all.

## Bottom line

Requesting one end of a link is referentially transparent with respect to everything the question names: the link object, its other endsets, and all referenced documents remain structurally and content-wise unchanged. The sole exception is monotonic accounting state (cash register / royalty) on any document whose bytes are actually delivered — which alters bookkeeping, never the link or the documents themselves.

I'm confident in the structural/content claim from the verified sources. If you want the exact wording of RETRIEVEENDSETS and the surrounding retrieval-command semantics confirmed against the page, NEED_RAW: 4/70.
