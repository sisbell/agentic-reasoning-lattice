## Question 5 [nelson]

> When a segment is moved to a new position in the content stream, do the positions of all other segments shift to accommodate it, and must the system guarantee that no two segments occupy the same position?

## Yes — on Both Counts

The answer requires distinguishing Xanadu's two address spaces, because they behave very differently.

### Vstream: Positions Always Shift

The Vstream (virtual byte stream) is the document's current arrangement. It is always **dense and contiguous** — positions run from 1 to N with no gaps. Every editing operation preserves this property:

**INSERT** explicitly shifts all subsequent positions:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

**DELETE** closes the gap:

> "This removes the given span from the given document." [LM 4/66]

**REARRANGE** transposes two regions, which necessarily reassigns V-addresses for everything between and including the transposed regions:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

Nelson confirms that V-addresses are ephemeral by design:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

And:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

So yes: when a segment moves, **all other V-positions shift** to maintain the contiguous sequence. And yes: **no two segments can occupy the same V-position** — the virtual byte stream is a linear sequence where each position maps to exactly one byte.

### Istream: Nothing Ever Moves

The Istream is permanent, append-only storage. Content at an I-address **never changes and never moves**:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

I-addresses are unique by construction — each new byte gets the next sequential address in the document's content space. There is no mechanism to reassign or overlap I-addresses.

### The Architecture That Makes This Work

The document IS the mapping from V-addresses to I-addresses. The POOM enfilade maintains this mapping efficiently:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely. All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The "canonical order" mandate is exactly the guarantee you're asking about — after every operation, the mapping is in a valid, consistent state with no overlaps or gaps in Vstream.

### Summary

| Property | Vstream | Istream |
|----------|---------|---------|
| Positions shift on edit? | **Yes** — always dense, always contiguous | **No** — permanent, append-only |
| Unique positions guaranteed? | **Yes** — each V-position maps to exactly one byte | **Yes** — each I-address holds exactly one byte |
| Content "moves"? | Yes — content is rearranged in the virtual view | Never — content stays at its creation address forever |

The system separates **arrangement** (Vstream, mutable) from **identity** (Istream, permanent). Rearranging content changes the arrangement; the identity remains fixed. Links point to I-addresses and thus survive all rearrangements.
