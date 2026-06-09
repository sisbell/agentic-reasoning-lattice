## Question 7 [theory]

> What must remain true about the document's total extent of content after the rearrangement, compared with before?

## Answer

After a REARRANGE, the document's **total extent of content must be exactly preserved** — the same bytes are present, in the same quantity, merely permuted into a different order. REARRANGE neither adds nor removes content; it transposes two regions.

Nelson defines the operation purely as a transposition:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

This makes REARRANGE a **pure Vstream operation** (see `i-space-v-space.md`) — it changes only the arrangement (the V→I mapping), not the underlying content. Contrast this with the operations that *do* change extent:

- **INSERT** — "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66) → extent grows.
- **DELETEVSPAN** — "This removes the given span from the given document." (4/66) → extent shrinks (in Vstream).

REARRANGE has no such length effect. Concretely, what must hold:

1. **V-stream length invariant** — the document's total character/byte count is identical before and after.
2. **Content set invariant** — the multiset of bytes (and their I-addresses) is unchanged; nothing is created or destroyed, only reordered.
3. **Extent span unchanged** — `RETRIEVEDOCVSPAN`, which "returns a span determining the origin and extent of the V-stream of document" (4/68), must report the same extent.

Because the same bytes survive (just relocated), this is also why links are unaffected: links "attach to bytes, not positions," so survivability holds across "deletions, insertions and rearrangements, if anything is left at each end." (4/43)

In short: REARRANGE is a permutation of existing content. The total extent is a **conserved quantity** — exactly equal before and after.

NEED_RAW: 4/67 — to confirm whether Nelson states an explicit conservation/length-equality invariant for REARRANGE on the page itself, beyond the transposition definition quoted above.
