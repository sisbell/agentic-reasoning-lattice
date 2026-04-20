## Question 2 [nelson]

> What is the minimal set of distinct ways the system's collection of documents can grow — can documents only be created, or can they also be split or merged?

## Document Growth: Two Primitives, No Split, No Merge

The FEBE protocol defines exactly **two** operations that add documents to the docuverse:

### 1. CREATENEWDOCUMENT — Creation ex nihilo

> "This creates an empty document. It returns the id of the new document." (4/65)

A fresh, empty document with a new tumbler address under the creator's account.

### 2. CREATENEWVERSION — Forking from an existing document

> "This creates a new document with the contents of document \<doc id\>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

A new document that shares all I-space content with the source. The address encodes derivation. From a structural standpoint this is the document-level instance of forking:

> "So the docuverse is all really one big forking document." (4/18)

### No Split, No Merge

Neither operation exists as a primitive. Of the 17 XU.87.1 commands, only the two above create documents. The remaining editing operations (INSERT, COPY, APPEND, REARRANGE, DELETEVSPAN) modify documents that already exist.

**Why split is unnecessary:** You can achieve the effect by creating two new documents and using COPY (transclusion) to reference different portions of the original into each. The original remains intact. The "split" documents are just new V-space arrangements over existing I-space content.

**Why merge is unnecessary:** You create a new document and COPY content from multiple sources into it. This is exactly what compound documents are:

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." (2/32)

The sources remain independent; the new document references them through transclusion.

### Why This Is Sufficient

The I-space/V-space separation makes split and merge redundant as primitives. Documents are V-space arrangements over permanent I-space content. "Splitting" and "merging" are just creating new arrangements — which is exactly what CREATENEWDOCUMENT + COPY already provides. Adding dedicated split/merge operations would be redundant machinery atop the same underlying mechanism.

The collection grows monotonically: documents are created (empty or as forks), content is added through INSERT/COPY/APPEND, and published documents cannot be withdrawn:

> "It is in the common interest that a thing once published stay published, as in the world of paper." (2/43)

### Summary

| Growth mode | Operation | What happens |
|---|---|---|
| **Ex nihilo** | CREATENEWDOCUMENT | Empty document, fresh address |
| **Fork** | CREATENEWVERSION | New document sharing source's I-space, ancestry in address |

Two primitives. Everything else — compound documents, derivative documents, annotated collages — is composition of these two creation modes with the editing operations that populate them.
