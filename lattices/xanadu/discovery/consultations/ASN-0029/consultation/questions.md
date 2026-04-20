# Sub-Questions — Document Lifecycle

**Inquiry:** What invariants govern document creation, ownership, and the relationship between documents in the docuverse? What does it mean to open, close, and create documents?

1. [nelson] When a new document is created, what properties must the system assign to it at the moment of creation that can never change afterward?
2. [nelson] What does ownership of a document guarantee to the owner — is it control over content, control over visibility, or something else entirely?
3. [nelson] Can ownership of a document ever transfer from one user to another, or is the creator-owner relationship permanent?
4. [nelson] What does it mean for a document to be "open" versus "closed" — is this a property of the document's editability, its visibility, or its relationship to the user?
5. [nelson] Must every document in the docuverse be unique, and what prevents two users from creating documents that the system treats as identical?
6. [nelson] Can a document ever be destroyed or removed from the docuverse, or does creation imply permanent existence?
7. [nelson] When one document includes content that originated in another document, what relationship must the system maintain between those two documents?
8. [nelson] Must the system preserve the order in which documents were created, and does a document's position in that ordering carry any meaning?
9. [nelson] If two documents share content through quotation or transclusion, does modifying one document's structure affect what the other document displays?
10. [nelson] What is the smallest thing that qualifies as a document — can a document be empty at creation, or must it contain at least some content?
11. [gregory] When a brand-new document is created (not via CREATENEWVERSION), how is its document-level tumbler address allocated — does `findisatoinsertnonmolecule` walk the granfilade under the user's account range (e.g., `1.1.0.2`) to find max+1, or is there a separate document counter?
12. [gregory] What state is initialized when a new document is created — is the POOM created empty (zero-height tree), or is there a sentinel entry, and are any granfilade or spanfilade entries written at creation time before any INSERT?
13. [gregory] When `OPENDOCUMENT` is called, does it do anything beyond inserting a BERT entry — for instance, does it load or pin the document's POOM in the cache, or is POOM loading deferred until the first operation on that document?
14. [gregory] When `CLOSEDOCUMENT` is called, does it flush dirty POOM nodes for that document to disk, or does it only remove the BERT entry and leave cache eviction to the grim reaper?
15. [gregory] The Node.0.User.0.Doc tumbler hierarchy implies a two-level ownership model — is the node address (`1.1`) assigned at server startup and fixed, and is the user account address (`1.1.0.N`) allocated at account creation time, or can these be assigned dynamically?
16. [gregory] Can a user create a document under another user's account range (e.g., user `1.1.0.2` creating doc `1.1.0.3.0.5`), or does the backend enforce that document allocation stays within the creating user's own account subtree?
17. [gregory] CREATENEWVERSION allocates the version under the source document if owned, or under the user's account if not — what exactly is the ownership test in `makehint`? Is it a tumbler prefix match between the session's account address and the source document's address?
18. [gregory] Is there a CREATEDOCUMENT operation distinct from the first INSERT into a new address, or does the document implicitly come into existence when content is first inserted — i.e., does the POOM get created lazily on first write?
19. [gregory] When multiple FEBE sessions have the same document open with READBERT, and one session upgrades to WRITEBERT, does `checkforopen` reject the upgrade while other readers hold the document, or is there no upgrade path (must close and reopen)?
20. [gregory] Is there any mechanism to enumerate all documents in the system — for example, can a session walk the granfilade's document-level address range to discover existing documents, or is document discovery limited to `FINDDOCSCONTAINING` via shared I-addresses?
