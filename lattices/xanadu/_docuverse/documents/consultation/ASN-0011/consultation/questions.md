# Sub-Questions — Document Lifecycle

**Inquiry:** What invariants govern document creation, ownership, and the relationship between documents in the docuverse? What does it mean to open, close, and create documents?

1. [nelson] When a new document is created, what permanent identity does the system assign, and can that identity ever be reused or reassigned to a different document?
2. [nelson] What does ownership of a document mean — does the owner have exclusive control over its content, or only over who may modify it?
3. [nelson] When a new version of a document is created, what is the relationship between the original and the new version — are they the same document or distinct documents with a shared history?
4. [nelson] Must the system guarantee that creating a new document leaves every existing document completely unchanged — its content, its links, its versions?
5. [nelson] What does it mean to "open" a document — does opening grant the user a private working copy, or does it expose the shared permanent original?
6. [nelson] Can a document exist with no content at all, or must document creation always establish some initial content?
7. [nelson] When multiple users share a document, what guarantees govern simultaneous modification — must one user's changes be invisible to another until explicitly published?
8. [nelson] Once a document has been created and published, can it ever be destroyed or made permanently inaccessible, or does permanence forbid this?
9. [nelson] If document A includes content from document B through transclusion, and someone creates a new version of document B, must document A still show the original content it referenced?
10. [nelson] What is the relationship between a user's account and the documents they create — does the system permanently record who created each document, and can this attribution ever be severed?
11. [gregory] When CREATENEWDOCUMENT allocates a document address under a user's account (e.g., `1.1.0.2.0.N`), does it use `findisatoinsertnonmolecule` with the same query-and-increment pattern as link allocation, and what is the upper bound tumbler it searches against?
12. [gregory] What is the initial state of a freshly created document's POOM — is it an empty enfilade tree with a root node already allocated, or is the orgl created lazily on first INSERT?
13. [gregory] When a document is opened via OPENDOCUMENT, what exactly is stored in the BERT entry — just the (document-address, connection-id, access-level) triple, or does it also cache a pointer to the document's orgl root?
14. [gregory] When CLOSEDOCUMENT is called, does the backend remove the BERT entry and release any cached orgl pointer, or does the orgl remain in the node cache until the grim reaper evicts it?
15. [gregory] Does the ownership check in `makehint` (do2.c:78-84) compare the user's account tumbler against the document's parent address using tumbler prefix matching, or does it use a separate ownership table?
16. [gregory] When CREATENEWVERSION allocates a version address as a child of the source document (e.g., `doc.0.1`), does the `.0.1` suffix occupy the same tumbler field level as the document's own `.0.N` element field, creating a deeper nesting level in the address hierarchy?
17. [gregory] Can a session open the same document multiple times with different access levels (e.g., READBERT then WRITEBERT), or does `checkforopen` reject the second open if the document already has a BERT entry for that connection?
18. [gregory] When CREATENEWDOCUMENT is called, does it create any spanfilade entries or granfilade entries for the new empty document, or is the document's existence recorded solely through its orgl allocation and address-space reservation?
19. [gregory] If two sessions have the same document open with READBERT, and one session upgrades to WRITEBERT, does the BERT mechanism detect the conflict and reject the upgrade, or is there a separate OPENDOCUMENTFORWRITING request that performs the exclusivity check?
20. [gregory] Does `findorgl` traverse a global document registry to locate a document's orgl root by address, or does it walk the granfilade B-tree using the document's I-address as a key — and what happens when `findorgl` is called for a document address that was never created?
