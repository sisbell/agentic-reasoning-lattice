## Question 5 [theory]

> Must the system guarantee that deleted content remains permanently discoverable from other documents that still arrange it?

# Yes — this is a core guarantee, and it falls directly out of the Vstream/Istream separation.

Deletion in Xanadu is a **Vstream** operation, not an **Istream** operation. When the owner of a document deletes content, they remove it from *their* current arrangement only. The bytes persist in Istream, and any *other* document that arranges those same bytes is wholly unaffected.

## Nelson states this explicitly

The most direct statement appears in the technical specification, where Nelson distinguishes the owner's deletion from the content's continued life elsewhere:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The state diagram on 4/9 labels the "DELETED BYTES" condition with the same point:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

"May remain included in other versions" is the answer to your question: the home document's deletion does **not** propagate to documents that transclude the content.

## Why the guarantee holds structurally

This is not a courtesy — it is a consequence of how transclusion works. A windowing document does not hold a copy; it references the permanent Istream address. The referencing document's Vstream mapping is independent of the home document's arrangement:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

Because the connection is by reference (shared I-address), the home owner *cannot* sever it by editing their own Vstream. This is the **non-destruction guarantee**: "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." (2/45)

## Discoverability specifically

The discovery operation is built to ignore the home document's current state entirely. `FINDDOCSCONTAINING` finds every document arranging the material "regardless of where the native copies are located":

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

So the deleted content remains both **accessible** (through the transcluding document's arrangement) and **discoverable** (through find-by-content search across the docuverse), independent of whether the home document still shows it.

## One boundary worth flagging

Nelson's *permanence* of content rests on the storage layer, which is governed separately by economics — "ALL SERVICES MUST BE SELF-SUPPORTING... archival storage must be economically self-sustaining" (4/5). The semantic guarantee is unconditional: deletion never removes content that another document arranges. The *physical* persistence of the underlying Istream bytes ultimately depends on storage continuing to be funded. But within the system's model, the deletion of content in one document can never make it undiscoverable from another document that still arranges it.
