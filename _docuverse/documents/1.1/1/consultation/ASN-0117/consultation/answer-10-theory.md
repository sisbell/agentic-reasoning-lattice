## Question 10 [theory]

> When a span is deleted, what guarantee isolates that document's arrangement change from the arrangements of all documents that share the affected content?

## Answer

The guarantee is the **separation of Istream (content) from Vstream (arrangement)**. A DELETE is a pure Vstream operation — it removes content from *one document's* current arrangement without touching the underlying Istream bytes. Because every other document that shares that content references the same permanent Istream addresses through its *own* independent Vstream mapping, the deleting document's arrangement change is structurally isolated from theirs.

### Why deletion is local to one Vstream

DELETE does not destroy content; it only edits the deleter's V→I mapping. Nelson's architecture explicitly marks deleted bytes as still present in storage and still live in other documents:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, **may remain included in other versions**.)" — 4/9

The decisive statement is on the next page:

> "Note that the owner of a document may delete bytes from the owner's current version, **but those bytes remain in all other documents where they have been included**." — 4/11

This is possible because the deletion changes only the document's *arrangement*, not the content's identity. The Vstream is "the document's arrangement of content," while the Istream is where "content permanently lives" with addresses that are "absolute and immutable" (see `_docuverse/.../i-space-v-space.md`). The DELETE FEBE operation "removes from Vstream only; Istream unchanged" (i-space-v-space FEBE table).

### Why other documents are unaffected

Documents that share the deleted content do so by **transclusion** — inclusion by reference, not copy. Each holds its own Vstream that points at the shared Istream addresses:

> "Non-native byte-spans are called inclusions or virtual copies." — 4/11

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." — 4/11

Since the Istream bytes are never removed and each document's arrangement is an independent mapping, one owner's edit cannot reach into another's view. This is the same principle stated for publishing as the **non-destruction guarantee**:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — **without damaging the originals**." — 2/45

### Summary

When a span is deleted, the isolating guarantee is that **content lives permanently in the immutable Istream while each document arranges it through its own Vstream**. DELETE edits only the deleting document's Vstream mapping; the Istream content persists, and every sharing document's separate arrangement continues to resolve to the same untouched Istream bytes. (Drawn from `_docuverse/.../i-space-v-space.md`, `delete-semantics.md`, and `transclusion.md`.)
