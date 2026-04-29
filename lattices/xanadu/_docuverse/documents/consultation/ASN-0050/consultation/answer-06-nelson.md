## Question 6 [nelson]

> Does removing content from a document's arrangement cause the remaining content to close the gap and form a new contiguous sequence, or must the system preserve the position where content once appeared?

## The Gap Closes: V-Space Is Always Contiguous

The remaining content closes the gap. This is fundamental to how V-space works.

### Direct Evidence

The V-space design intent states explicitly that V-addresses are **dense** — they "always form a contiguous sequence starting at 1." There are no holes in a virtual byte stream.

Nelson's description of INSERT confirms the mechanism:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

INSERT shifts subsequent addresses **up** by the insertion length. By the same logic, DELETEVSPAN shifts subsequent addresses **down**, closing the gap. The virtual byte stream remains contiguous after both operations.

### Why This Must Be So

V-space is defined as a **virtual byte stream** — a logical sequence:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

A "sequence of bytes" with holes in it is not a sequence. The V-stream is the document as the user sees it right now — position 1 is the first byte, position N is the last, and everything in between is occupied.

### V-Addresses Are Ephemeral by Design

Nelson is explicit that V-addresses change constantly and nobody should care:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

And:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

This is the key architectural insight: **links point to I-space, not V-space**. V-addresses can shift freely because nothing depends on their stability. Links attach to bytes (I-addresses), not positions (V-addresses). So when DELETE closes the gap and shifts every subsequent V-address, no links break — they were never pointing at V-addresses in the first place.

### The Two-Space Separation Makes This Work

The whole point of the I-space/V-space separation is that:

- **I-space is permanent**: content lives there forever, addresses never change
- **V-space is ephemeral**: the current arrangement, freely rearrangeable

DELETE removes bytes from V-space (the current view) while leaving them intact in I-space (permanent storage). The V-stream contracts; the I-stream is untouched. Previous versions still have their own V-arrangements that include the "deleted" content. Other documents that transclude the content still show it.

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

"Not currently addressable" means not in the current V-stream — but still present in I-space, recoverable through historical backtrack, and visible in other documents.

### Summary

DELETE causes the V-stream to close the gap. Position preservation would contradict the definition of V-space as a contiguous byte stream. The system can afford this because nothing of value depends on V-address stability — links, transclusions, and version correspondence all operate through I-space addresses, which are permanent and unaffected by V-space rearrangement.
