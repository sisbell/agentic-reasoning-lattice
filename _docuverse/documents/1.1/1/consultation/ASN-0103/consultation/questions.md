# Sub-Questions — CREATENEWDOCUMENT Operation

**Inquiry:** What happens when a user creates a new document under an account? What is allocated, what is preserved about existing documents and the content store, what distinguishes the new document from one made by forking, and what invariants must the completed operation maintain?

1. [theory] What must a user be able to count on about a newly created document's identity remaining permanently distinct from every other document, including ones created later?
2. [theory] When a document is created empty, what does the design guarantee about its content — does it hold nothing, or some inherent starting state the user can rely on?
3. [theory] What distinguishes a freshly authored document from one born by versioning, from the standpoint of what each shares with prior documents?
4. [theory] Must creating a new document leave the identities and content of all existing documents wholly untouched?
5. [theory] What does the design promise about a new document's relationship to the shared content store — does its creation add any content, or only a place to hold content?
6. [theory] What ownership or authorship guarantee binds a new document to the account under which it was created?
7. [theory] Once creation completes, what must remain permanently true about the document's identity for as long as the system endures?
8. [theory] What must the system guarantee about a new document being immediately and unambiguously referable by links the moment it exists?
9. [theory] Should a newly created document share no content history with any other document, unlike one produced through versioning?
10. [theory] What invariant about the total population of documents must hold after creation — that exactly one new addressable document now exists and nothing else changed?
11. [evidence] When CREATEDOCUMENT allocates a new document address under an account, does `findisatoinsertnonmolecule` query the granfilade for the current maximum document tumbler under that account's `Node.0.User` parent and return max+1?
12. [evidence] What bounded upper limit does the document-address allocation use to distinguish document tumblers from element-level tumblers within the account's I-address range?
13. [evidence] Does creating a new document invoke `createenf` to build an initial empty POOM (2D orgl) tree, and what is the structural height of that freshly created empty enfilade?
14. [evidence] Does CREATEDOCUMENT allocate or pre-create any of the three subspaces (text `1.x`, link `2.x`, type `3.x`), or are they materialized lazily on first INSERT/CREATELINK?
15. [evidence] Does creating an empty document produce any DOCISPAN entries in the spanfilade, or does the spanfilade remain unchanged until content is inserted?
16. [evidence] Does CREATEDOCUMENT touch the granfilade at all, or does the granfilade's monotonic I-address high-water mark remain unchanged since no content molecules are stored?
17. [evidence] After creation, is the new document automatically registered in BERT as open with WRITEBERT access for the creating connection, or must the caller issue a separate open?
18. [evidence] Compared to a freshly created empty POOM, does a CREATENEWVERSION document differ by having text-subspace V→I entries copied in, while CREATEDOCUMENT's POOM has zero bottom crums?
19. [evidence] Does CREATEDOCUMENT preserve every existing document's POOM, granfilade, and spanfilade state untouched, satisfying the F0 cross-document frame axiom?
20. [evidence] Does the new document address satisfy INV-IADDR-MONOTONIC under its account parent — strictly exceeding all previously allocated document tumblers even if intervening documents were never populated?
