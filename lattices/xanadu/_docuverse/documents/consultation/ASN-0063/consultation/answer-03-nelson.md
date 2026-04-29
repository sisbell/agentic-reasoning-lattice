## Question 3 [nelson]

> Does creating a link allocate new content storage for the link's own structure, or does the link exist purely as an index entry over existing content?

## Links Are Stored Entities, Not Mere Index Entries

Creating a link **allocates new storage** in tumbler-space. A link is a concrete, addressable object — not a derived index over existing content.

### The Direct Evidence

Nelson is explicit that links and content bytes are the **only two kinds of stored entities**:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

Links have their own addresses in a document's element subspace. From the link address structure:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

And from the link-to-link discussion, the storage status is stated directly:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link." [LM 4/49]

### What Gets Stored

A link is described as:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user. It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

The stored structure contains the three endsets (from-set, to-set, type) — each an arbitrary span-set referencing addresses elsewhere in the docuverse. The endsets are **pointers** to existing content; they don't copy the content. But the link itself — the "package" holding those three pointers together — is a newly allocated stored object.

MAKELINK confirms this: it creates a new entity and returns its identity:

> "This creates a link in document \<doc id\> from \<from set\> to \<to set\> connected to \<three set\>. It returns the id of the link made." [LM 4/68]

### Links Parallel Bytes in Every Way

The document's technical contents (page 4/9) list two parallel categories:

| Category | Stored? | Has addresses? | Can be "deleted"? |
|----------|---------|-----------------|-------------------|
| **Bytes** | Yes | Yes (byte subspace) | Yes — enters historical backtrack state |
| **Links** | Yes | Yes (link subspace) | Yes — enters historical backtrack state |

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This is the same language used for deleted bytes. Both are permanent entries that can be made "not currently addressable" but never truly removed — consistent with append-only storage.

RETRIEVEDOCVSPANSET counts both categories as part of a document's contents:

> "This returns a span-set indicating both the number of characters of text and the number of links in document \<doc id\>." [LM 4/68]

### Separate Storage Infrastructure

The enfilade architecture reinforces this. Nelson describes a dedicated **linking enfilade** (Barus's contribution) separate from the content enfilade:

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely." [LM 1/34]

> "Barus's work, which we refer to jocundly as 'the eye in the pyramid,' made possible an efficiently ever-linkable enfilade." [LM 1/34]

This is a separate data structure designed specifically for storing and indexing links — not a secondary index derived from content.

### Summary

A link is a **first-class stored entity** in the Istream alongside content bytes. Creating a link:

1. **Allocates storage** for the link structure (the three endsets)
2. **Assigns a permanent tumbler address** in the document's link subspace
3. **Enters the append-only record** — subject to the same non-destruction guarantees as bytes
4. **Is maintained by dedicated data structures** (the linking enfilade)

The endsets within the link are references (spans pointing to existing content), but the link itself is new stored matter. It is not an index entry derived from content — it is content of a different kind.
