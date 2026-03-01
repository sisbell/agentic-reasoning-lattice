# Documents

Source: Literary Machines, 2/11-2/20, 2/29-2/35, 4/6-4/12

## Semantic Intent

### What It Means

A document in Xanadu is fundamentally different from a file. It is an owned unit of evolving content—not a static container but an "ongoing braid" that grows through time. Every document has an owner who controls it, and the document preserves its complete history of changes.

The key insight is that a document is not just its current state, but the entire trajectory of its evolution. You can ask for any part of a document at any point in its history, and the system will reconstruct that state. This is not backup or versioning as an afterthought—it's the fundamental nature of what a document is.

A document consists of its contents (including history and alternatives) and its out-links—the connections it makes to other documents. The in-links (what points to this document) are owned by whoever created them and stored elsewhere. This separation matters: you own what you create, including the links you make.

### User Guarantee

- **Ownership is absolute**: Only the owner may change a document or withdraw it
- **History is permanent**: Every previous state remains accessible
- **Identity is stable**: A document that exists can always be found at its address
- **Composition is transparent**: When your document includes material from others through windows, that relationship is visible and the source owner is credited

### Principle Served

Documents serve the principle that **literature is debugged**—that we can finally have a proper system for interconnected, evolving written works. The existing system of publishing treats documents as frozen artifacts, but real intellectual work involves constant revision, commentary, response, and cross-reference. Xanadu's documents embrace this reality.

The document model also solves the **historical backtrack** problem: the need to recover previous states, compare versions, and understand how ideas evolved. Rather than making complete copies (conventional backup), the system stores changes incrementally and can reconstruct any historical state on demand.

### How Users Experience It

- Create a document and it belongs to you—no one else can modify or delete it
- Edit freely, knowing every previous version remains accessible
- Ask for "a certain part of a certain version at a certain point in time"
- See what changed between versions side by side
- Quote material from other documents through windows—the connection to the original is maintained
- Receive royalties when others window your content
- Find all documents that reference yours through their out-links

### Nelson's Words

> "A document is really an evolving ONGOING BRAID." (2/14)

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted... and think then of successive versions of the document, at successive instants of time, as alive in this space-time vortex." (2/15)

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." (2/16)

> "Every document has an owner, the person who created and stored it (or someone who arranged it to be created and stored, such as a publishing company). The rightful copyright holder, or someone who has bought the document rights... Only the owner has a right to withdraw a document or change it." (2/29)

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." (2/31)

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist. Thus the 'Jabberwocky' is a document; and a set of links between them, were someone to create it, would yet be a separate document." (2/29)

---

## Additional Semantic Points (Chapter 4)

### Universal Container

A document may have any structure (sequential or not) and hold any type of information: text, graphics, 3D data, sound, DNA sequences, or references to external objects. The system imposes no constraints on what a document can be.

### Distributed Composition

A document is not a physical unit. Its contents may be scattered throughout the docuverse, assembled from other documents. This is invisible to users—they experience one coherent document regardless of where pieces originate.

### Interconnection Tracking

At its heart, Xanadu is a system for keeping track of interconnections. The things being interconnected can exist entirely outside the system. You can use Xanadu purely to organize and link external materials without storing any content at all.

### Link Ownership Principle

A link's home document indicates who owns it—not what it points to. Links connecting parts of a document need not reside in that document. Conversely, a link need not point anywhere in its home document. Ownership and application are independent.

### Nelson's Words (Chapter 4)

> "The Xanadu document is the unit of the system. There is almost nothing in the Xanadu system but Xanadu documents." (4/6)

> "The Xanadu document may have any structure (sequential or not) and may hold any type of information." (4/6)

> "Properly understood, then, this is a system for keeping track of interconnections. The things which are interconnected can be somewhere else entirely; keeping them on our system is merely an additional convenience for the user." (4/10)

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

---

## Related Concepts

| Concept | Relationship |
|---------|--------------|
| [i-space-v-space](i-space-v-space.md) | Documents own I-space content and have V-space arrangements |
| [versions](versions.md) | Documents evolve through versions (the "ongoing braid") |
| [tumblers](tumblers.md) | Documents have permanent tumbler addresses |
| [links](links.md) | Documents contain out-links; in-links point to them from elsewhere |
| [transclusion](transclusion.md) | Documents can window content from other documents |
| [publishing](publishing.md) | Published documents cannot be withdrawn |
| [copyright](copyright.md) | Ownership determines who can modify |

## FEBE Operations

| Operation | How documents apply |
|-----------|-------------------|
| **CREATENEWDOCUMENT** | Creates owned document with permanent address |
| **CREATENEWVERSION** | Creates new version of existing document |
| **INSERT, DELETE, REARRANGE, APPEND** | Modify document (require ownership) |
| **MAKELINK** | Link home document determines ownership |
| **RETRIEVEDOCVSPAN** | Gets document's V-stream extent |
| **RETRIEVEDOCVSPANSET** | Gets document's text and link spans |

See [Concept-Operation Map](../concept-operation-map.md) for full mapping.
