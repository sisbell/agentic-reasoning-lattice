## Question 2 [nelson]

> After content is removed, do the positions of all content following the removal point shift to close the gap, or does the document retain a placeholder at the vacated positions?

## Positions Shift to Close the Gap

The Vstream always forms a **dense, contiguous sequence**. When content is removed, all subsequent positions shift down to maintain this invariant. There are no placeholders or holes.

### Direct Evidence

Nelson states explicitly for INSERT:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

DELETE is the symmetric operation. The Vstream is defined as a dense virtual byte stream:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

If you have 100 bytes and delete bytes 20–30, you now have 89 bytes addressed 1 through 89. The former byte 31 is now at V-address 20. The Vstream has no concept of "empty positions."

### Why This Works

The key is the two-address-space separation:

- **Vstream** (arrangement): positions shift freely during editing. "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing." [LM 4/11]

- **Istream** (identity): content remains forever at its permanent address. "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The deleted bytes are described as: "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" means they have no V-address in the current version — not that they occupy a placeholder V-address. They still exist in Istream and in previous versions.

### The Braid Metaphor

Nelson's "ongoing braid" metaphor captures this perfectly:

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." [LM 2/15]

When you subtract strands, the braid closes around the gap. It doesn't leave empty space where strands used to be.

### Summary

| Space | Effect of DELETE |
|-------|-----------------|
| **Vstream** | Gap closes; subsequent positions shift down; sequence remains dense 1..N |
| **Istream** | Nothing changes; bytes remain at permanent addresses forever |
| **Other versions** | Unaffected; each version has its own V-arrangement |
| **Links** | Survive, because they point to I-addresses, not V-positions |

NEED_RAW: [4/66] — to confirm whether Nelson's DELETEVSPAN description explicitly mentions position shifting, or whether the gap-closing property is only implicit from the dense-sequence invariant and the INSERT symmetry.
