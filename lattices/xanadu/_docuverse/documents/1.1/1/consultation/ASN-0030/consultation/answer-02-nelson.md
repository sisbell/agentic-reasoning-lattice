## Question 2 [nelson]

> If a user removes content from their document, does the content's original address continue to exist, and must the system still be able to locate that content through it?

## Yes — absolutely and unconditionally.

When a user removes content from their document, the content's original I-space address continues to exist permanently, and the system must still be able to locate that content through it. This is not a special case or edge behavior — it is the foundational design principle of Xanadu storage.

### What DELETE actually does

DELETE operates exclusively on V-space (the document's current arrangement). It does not touch I-space (permanent storage). Nelson's diagram on page 4/9 shows "DELETED BYTES" as an explicit system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The phrase "not currently addressable" applies only to that document's current V-stream. The I-space address remains valid.

Nelson makes this explicit:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

### Why the address must persist

Three guarantees depend on this:

**1. Historical backtrack.** Previous versions of the document still reference this content through their V-space mappings to the same I-space addresses. If the I-space content were destroyed, historical backtrack would be impossible.

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

**2. Transclusion integrity.** Other documents may transclude (window) the same content. Their references point to I-space, not to the originating document's V-space. Deletion from one document cannot affect another's view.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

**3. Link survivability.** Links attach to I-space content, not V-space positions. If I-space content were destroyed on deletion, links would break — violating the survivability guarantee.

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

### The architectural basis

Xanadu's storage is append-only by design:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Every byte ever created has a permanent I-space address of the form `Node.0.User.0.Document.0.Element`. That address encodes origin and never changes. The entire system — tumblers, enfilades, the permanence guarantee — rests on this:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

### Summary

| What happens on DELETE | Affected? |
|---|---|
| V-space arrangement (current view) | **Yes** — content removed from current version |
| I-space content (permanent storage) | **No** — bytes remain forever |
| I-space address (permanent identity) | **No** — address remains valid |
| Previous versions | **No** — still contain the content |
| Transclusions in other documents | **No** — still resolve to I-space |
| Links pointing to the content | **No** — still attached to I-space bytes |

The content's original address does not merely "continue to exist" — it *cannot cease to exist*. The system is designed so that destruction of stored content is architecturally impossible. This is the meaning of Nelson's rejection of "destructive replacement" as the storage paradigm. Xanadu's answer to "what happens when you delete?" is: you change the view, never the thing viewed.
