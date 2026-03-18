## Question 2 [nelson]

> If a span of content is removed from one document but that same content is shared by other documents through transclusion, must those other documents remain completely unaffected by the removal?

## Yes — absolutely and by explicit design.

Nelson states this directly at **4/11**:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included."

This is a necessary consequence of the I-space / V-space separation.

### Why architecturally

DELETE operates **only on V-space** — it removes content from a document's current arrangement. It does **not** touch I-space, where the bytes permanently reside.

When document B transcludes content from document A, document B's V-space maps directly to the **I-space addresses** of those bytes — not to document A's V-space positions. So when document A's owner deletes those bytes from A's current version:

- A's V-space mapping is removed (the bytes disappear from A's current view)
- The I-space content is untouched
- B's V-space mapping still points to those same I-space addresses
- B is completely unaffected

Nelson's diagram annotation at **4/9** confirms the state of deleted content:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

"May remain included in other versions" — and by extension, in other documents that transclude the same I-space content.

### The deeper principle

This follows from Nelson's rejection of destructive storage:

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals." [LM 2/45]

The non-destruction guarantee means that no editing operation in one document can damage content visible through another document. DELETE changes **your view**, not the underlying reality.

### One nuance: window modes

Nelson describes two transclusion modes [LM 2/37]:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically."

A **location-fixed window** that tracks the current V-space of the source document could reflect the deletion — the window would show the source document's updated arrangement. But this is about what the *window shows of the source's view*, not about destruction of the underlying content. The I-space bytes still exist, previous versions still contain them, and any direct transclusion (COPY operation) remains intact.

### Summary

| What happens when A deletes content | Effect on document B (which transcludes it) |
|--------------------------------------|---------------------------------------------|
| A's V-space mapping removed | B's V-space mapping unchanged |
| I-space bytes untouched | B still resolves to same I-space content |
| A's previous versions still show it | B shows it as before |
| Links to those I-space bytes survive | B's attribution to source intact |

The answer is unambiguous from Nelson's text: transclusion in other documents **must** remain completely unaffected by removal from the source document's current version.
