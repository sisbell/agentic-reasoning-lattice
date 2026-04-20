## Question 7 [nelson]

> If a user deletes content from a document, must the system preserve the address assignment so that historical references and links remain valid?

## Yes — absolutely and by multiple reinforcing principles.

Deletion in Xanadu removes content from the document's **V-space** (current arrangement) but does **not** remove it from **I-space** (permanent storage). The address assignment is permanent. This is not a design preference — it is load-bearing architecture upon which links, versions, transclusion, and attribution all depend.

---

### 1. DELETE is a V-space operation, not an I-space operation

The diagram on page 4/9 explicitly shows "DELETED BYTES" as a valid system state:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

And Nelson clarifies:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The bytes are removed from the current view. They are not destroyed, and their I-space addresses remain occupied.

---

### 2. Tumbler addresses are permanent by design

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

An address, once assigned, is never invalidated and never reused. This applies to all content — including content that has been "deleted" from a document's current version.

---

### 3. Links depend on I-space permanence

Links attach to spans of bytes in I-space, not to positions in V-space:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

If deletion destroyed I-space addresses, every link to the deleted content would break — violating the survivability guarantee. The entire link architecture assumes that I-space content is permanent.

---

### 4. Historical backtrack requires reconstructability

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

If deleted content lost its address, previous versions could not be reconstructed. The historical backtrack guarantee — that you can always return to any previous state — requires that all I-space content remain at its permanent address.

---

### 5. The storage paradigm is append-only

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." [LM 2/14]

Nelson designed Xanadu specifically to reject destructive replacement. The append-only model means content is added but never overwritten or removed. Deletion is a change to the arrangement (V-space), not the archive (I-space).

---

### 6. Transclusion depends on permanent addresses

Other documents may transclude the "deleted" content:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

If Alice's document transcludes a paragraph from Bob's document, and Bob "deletes" that paragraph from his current version, Alice's document still shows it — because Alice's V-space mapping points to Bob's I-space address, which is permanent. Destroying the address would break Alice's document.

---

### Summary

The answer follows from the fundamental separation of I-space and V-space. Deletion is a V-space operation — it changes what the document currently shows. The I-space address, the content at that address, and all references to it (links, transclusions, version history) remain intact. This is not optional; it is the architectural invariant upon which permanence, link survivability, historical backtrack, and transclusion all rest.
