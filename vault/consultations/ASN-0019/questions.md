# Sub-Questions — Operation Journaling

**Inquiry:** What must the system guarantee about recording and replaying the history of operations performed on content? What properties must an operation log satisfy for faithful state reconstruction?

1. [nelson] Must the system preserve a complete, ordered record of every operation performed on a document, such that any prior state can be faithfully reconstructed?
2. [nelson] What must the system guarantee about the identity of each recorded operation — must every operation be uniquely and permanently identifiable?
3. [nelson] Must the operation history itself be permanent and append-only, or may entries be revised or removed after recording?
4. [nelson] What must the system guarantee about attributing each operation to the user who performed it, and must that attribution be tamper-proof?
5. [nelson] Must replaying the history of operations on a document produce exactly the same content and link structure as existed at the original moment, with no deviation?
6. [nelson] What must the system guarantee about the ordering of operations when multiple users edit shared content concurrently — must a single canonical sequence be established?
7. [nelson] Must the operation history preserve the relationship between editing operations and the specific version of a document they produced, so that every version is reachable by replay?
8. [nelson] What must the system guarantee about links that reference a historical state of content — must following such a link reconstruct the document as it appeared at that point in its history?
9. [nelson] Must the operation log record not only changes to content but also changes to sharing permissions, link creation, and other non-content operations with equal fidelity?
10. [nelson] What must the system guarantee if an operation depends on content originating in another document — must the log capture that cross-document provenance so replay remains faithful even across document boundaries?
11. [gregory] Can the monotonic I-address ordering within the granfilade reconstruct a total temporal ordering of content creation events across documents, or do per-document allocation ranges (via `findisatoinsertmolecule`) only guarantee ordering within a single document's I-address subrange?
12. [gregory] Since the spanfilade is write-only and DOCISPAN entries persist after DELETE removes V→I mappings from the POOM, do the accumulated DOCISPAN entries contain enough information (document ID, I-address span) to distinguish an INSERT from a COPY — or do both operations produce structurally identical spanfilade entries pointing to the same I-addresses?
13. [gregory] After DELETE mutates a POOM and the pre-delete V→I mapping is lost, is there any path — using the granfilade's permanent content, the spanfilade's DOCISPAN history, and CREATENEWVERSION snapshots — to reconstruct what V-address a given I-address occupied before the deletion, or is the V-position information irrecoverably destroyed?
14. [gregory] Was there ever a design intent for an operation journal or event log in udanax-green — something beyond the implicit history encoded in the granfilade's append-only structure and the spanfilade's monotonic growth — or was faithful state reconstruction explicitly delegated to the client via CREATENEWVERSION snapshots?
15. [gregory] If a replay mechanism were to reconstruct a document's current POOM state from a sequence of recorded operations, does the `makegappm` shift logic in `insertnd` depend on any transient state (like current tree shape or crum boundaries) that would differ between original execution and replay, or are the V-address shifts purely a function of the insertion point and width regardless of enfilade structure?
