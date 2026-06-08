## Question 8 [theory]

> If two documents share the same underlying content, what guarantee isolates one document so that inserting into it leaves the other's arrangement and its experience of that shared content completely unchanged?

## The guarantee: Istream/Vstream separation (non‑destruction)

The isolation you're describing comes from Xanadu's separation of **content** (Istream, permanent and immutable) from **arrangement** (Vstream, per‑document and editable). When two documents share underlying content, they share *Istream* bytes — but each holds its **own independent Vstream arrangement** over those bytes. An INSERT touches only the target document's Vstream; it never writes to Istream, so it cannot reach the other document's arrangement.

### Why insertion stays local

INSERT is defined to shift positions **within the one document it operates on**, nothing else:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

The renumbering is confined to "the document" — the document named in the command. The other document has a separate Vstream, so its addresses are untouched.

### Why the shared content itself is safe

Insertion adds new bytes to the target's arrangement; it does not alter, move, or destroy the shared Istream bytes. Nelson states the converse case (deletion) explicitly, and the principle is the same — operations on one document's current version don't propagate to other documents holding that content:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

This is the **non‑destruction guarantee**: "modifications never damage originals" — derivative/sharing documents "are permanently defined (and stored) in terms of the originals and the changes" (2/37, 2/45).

### Why the other document's *experience* is unchanged

The second document references the shared content by its permanent Istream address, and that address keeps returning the same content regardless of edits elsewhere:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

Because transclusion/sharing is **inclusion by reference, not copy**, "no copying operations are required among the documents" and the original "stays where it is" (transclusion, 2/36). The sharing document resolves the same Istream bytes in the same order it always did, so its arrangement and its reader's experience are completely unaffected.

### In short

- **Istream** holds the shared bytes, immutable.
- **Vstream** is each document's *own* mapping over Istream; INSERT edits only the target document's mapping (4/66).
- Shared content "remain[s] in all other documents where [it has] been included" (4/11), and is reached by stable address (4/11).

The net effect is the guarantee Nelson names elsewhere as editing "without damaging the originals" (2/45) — the second document's arrangement and experience of the shared content are guaranteed unchanged.

(One caveat for completeness: this assumes the sharing document references the content by a fixed/location arrangement. Nelson notes a window can be fixed "at a relatively fixed location… in which case updates are seen automatically" (2/37) — but an *insertion into a separate document* is not an update to the shared bytes, so even an auto‑updating window sees no change.)
