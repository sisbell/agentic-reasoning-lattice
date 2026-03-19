# Sub-Questions — Address Permanence

**Inquiry:** What guarantees must the system provide about address stability? Once content is assigned an address, what operations may and may not affect that assignment?

1. [nelson] Once content is assigned a permanent address, must that address remain valid and resolvable for the entire lifetime of the system?
2. [nelson] When a user edits a document by inserting or deleting content, must the addresses of all other existing content remain unchanged?
3. [nelson] If the same content appears in multiple documents through inclusion, must it be reachable through a single stable address regardless of how many documents reference it?
4. [nelson] Must the address of content be determined solely by when it was created, or may the system reassign addresses to optimize retrieval?
5. [nelson] When a new version of a document is created, must content retained from the prior version keep its original address, or may versioning introduce new addresses for the same material?
6. [nelson] Must links that reference content by address continue to resolve correctly after any sequence of editing operations performed on the linked document?
7. [nelson] If a user deletes content from a document, must the system preserve the address assignment so that historical references and links remain valid?
8. [nelson] Must every unit of content ever added to the system receive a unique address that is never reused for different content?
9. [nelson] When content is quoted or transcluded into a new document, must the address visible to the reader be the original author's address, preserving the connection to source?
10. [nelson] Must the system guarantee that no operation — creation, editing, deletion, sharing, or reorganization — can cause two distinct pieces of content to share the same address?
11. [gregory] When `findisatoinsertmolecule` allocates a new I-address as max+1, is there any scenario — concurrent sessions, CREATELINK interleaving, or version creation — where two distinct content insertions could receive the same I-address?
12. [gregory] After DELETE shifts a POOM entry's V-position leftward via `tumblersub`, can any subsequent operation (INSERT, COPY, REARRANGE) restore the original V-position, or is the pre-delete V-address layout permanently lost?
13. [gregory] The `strongsub` exponent guard in DELETE returns the link position unchanged when width.exp < pos.exp — was this intentional isolation design or an accident that happens to work, and are there tumbler configurations where the guard fails to protect link subspace positions?
14. [gregory] When COPY creates a new V→I mapping in the target document, does the target's POOM entry store an independent copy of the I-displacement, or does it share a pointer with the source — i.e., could any mutation of the source POOM corrupt the target's I-address reference?
15. [gregory] If a document's entire text content is deleted and then new text is inserted, the new text gets fresh I-addresses — but does the POOM's V-address numbering restart from 1.1, or does it continue from the shifted position left by the delete?
16. [gregory] CREATENEWVERSION copies text-subspace POOM entries — are the I-displacements in the version's POOM byte-identical copies of the original's, or are they recomputed, and could recomputation ever produce different tumbler representations for the same logical I-address?
17. [gregory] When `isanextensionnd` coalesces a new insertion into an existing POOM crum by extending its width, does this change the I-displacement of the existing crum, or only the width — and can coalescing ever cause an adjacent crum's displacement to shift?
18. [gregory] The spanfilade DOCISPAN entries persist after DELETE with no cleanup — if document D1 once contained I-span X and D1 is later queried via `find_documents_containing(X)`, does the system return D1 even though D1's current POOM no longer maps to X, or is there a POOM cross-check?
19. [gregory] REARRANGE preserves I-addresses while changing V-addresses — when a pivot moves content from V:1.2 to V:1.4, does the POOM entry's I-displacement field remain bit-identical, or is it rewritten during the rearrangement even though the logical value is unchanged?
20. [gregory] After CREATELINK advances the I-address allocation counter past the text range, subsequent text inserts receive non-contiguous I-addresses — does this gap in the I-address space have any effect on `findpreviousisagr` performance or correctness, and can the gap ever be reclaimed?
