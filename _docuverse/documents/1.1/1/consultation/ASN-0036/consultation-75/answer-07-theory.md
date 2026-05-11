## Question 7 [theory]

> Did the two-stream design require a fixed V-position depth (specifically m = 2 for the text subspace) as an architectural commitment, or was the depth choice deliberately left open to be fixed by allocation/insertion operations?

Looking at the curated sources, I can identify the relevant material on V-position depth and the byte-subspace structure.

## What Nelson Specifies

The standard byte address structure within a document, as described in the V-space and link material, appears to use a **basic depth of m=2** (subspace identifier + single position digit):

From v-space-addresses.md (4/30):
> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."

The phrasing "the digit" (singular) implies a single digit follows the subspace identifier "1". Similarly for links, links.md cites (4/31):
> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)"
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)"

INSERT operates on this single-digit position, per operations.md (4/66):
> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text."

This describes linear shifting of positions, not depth manipulation.

## Where Nelson Leaves Depth Open

Crucially, links.md contains this quote from 4/31:
> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed."

This explicitly identifies the **basic depth as 2** ("'2' and the position") while flagging that **further depth was deliberately contemplated** as a "distinct possibility" — not committed but anticipated.

This is consistent with the general tumbler philosophy, per tumblers.md (4/19):
> "A tumbler consists of a series of integers. Each integer has no upper limit... New items may be continually inserted in tumbler-space while the other addresses remain valid."

And per i-space-addresses.md (4/29):
> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions."

## Answer

From the curated sources, the picture is **both/and rather than either/or**:

- The text subspace has a **default operational depth of m=2** (subspace identifier "1" + single position digit), and this is what standard FEBE operations like INSERT manipulate.
- This depth was **not an architectural commitment** sealing off deeper structure. Nelson explicitly notes that "subdivision by further digits" beyond the subspace identifier and position is "a distinct possibility" with "several possible uses... discussed" (4/31, referring to links, but the same forking principle governs the whole tumbler).
- The forking principle of tumblers — that any digit can be subdivided indefinitely without invalidating existing addresses — means depth is **inherently open-ended at the addressing level**, even when day-to-day allocation uses a flat m=2 pattern.

So m=2 reflects an **allocation convention used by the basic INSERT/DELETE operations**, not a depth ceiling baked into the design. The curated material directly supports that the architecture leaves further subdivision available.

NEED_RAW: 4/30-4/31 — for the full surrounding discussion of byte vs. link subspace structure and the specific "further uses" Nelson alludes to for deeper subdivision, the raw pages would confirm whether Nelson explicitly extends the "further digits" remark beyond links to bytes, or treats the byte position as more strictly single-digit.
