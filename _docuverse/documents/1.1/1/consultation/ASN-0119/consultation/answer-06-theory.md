## Question 6 [theory]

> What does transposing two regions in a single operation — rather than moving one and later the other — reveal about the ordering guarantees the document must uphold?

Transposing two regions atomically — rather than as "move A, then move B" — exposes three ordering guarantees the document model must uphold.

## 1. The V-stream is a total order with no valid "in-between" state

Nelson defines the operation as a single transposition specified by cut points, not as a sequence of moves:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." (4/67)

All cuts are interpreted against **one** arrangement simultaneously. This matters because the document's Vstream is required to be a canonical total order at all times — the internal mandate inherited from the enfilade design:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34)

A move-one-then-other approach would manufacture an intermediate arrangement that is itself a real, addressable document state — not a neutral scratch step. The atomic transposition guarantees the document goes from one canonical ordering directly to another, never passing through an arrangement the author didn't intend.

## 2. Cut coordinates must resolve against a single, unshifted coordinate frame

V-addresses are dense and shift under editing:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

If you moved the first region and *later* the second, the second move's cut points would have to be recomputed in a coordinate frame that the first move already perturbed. Doing it in one operation reveals the real guarantee: all cut points are valid simultaneously against the *original* arrangement. The ordering invariant is frame-relative, and the operation fixes that frame so the two regions' boundaries can't drift out from under each other.

## 3. Ordering is relational and content-invariant

The "move A, leave B fixed" framing imposes a false asymmetry — one region privileged as moving, the other as stationary background. Transposition treats both as moving relative to each other. This reflects that position in Xanadu is defined by neighbors, not by an absolute index — exactly Nelson's "braid" image:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." (2/15)

And because REARRANGE is a pure Vstream operation, the reordering touches only the arrangement, never Istream content. The guarantee that survives the swap is connectivity: links attach to bytes, not positions, so a transposition cannot break them:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

## Summary

Atomic transposition reveals that the document must uphold a **single canonical total ordering**, evaluated against **one consistent coordinate frame**, while preserving **content identity and link attachment** underneath the reordering. Splitting it into two sequential moves would violate the first (creating an unintended intermediate version), strain the second (shifting the coordinates the second move depends on), and gain nothing for the third (survivability holds either way). The one-operation form is how the spec keeps "from cut 1 to cut 2" and "from cut 3 to cut 4" meaningful as the *same* arrangement.

One caveat: the interpretation that the intermediate state is semantically a distinct version is my reading of the canonical-order mandate, not a verbatim Nelson claim. If you want his exact words on REARRANGE's atomicity and the three-cut/four-cut geometry confirmed against the page image — NEED_RAW: 4/67.
