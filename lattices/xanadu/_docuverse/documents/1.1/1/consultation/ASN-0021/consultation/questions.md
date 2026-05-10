# Sub-Questions — Frame Condition Completeness

**Inquiry:** What must each operation explicitly guarantee about state it does not intend to modify? What frame conditions must hold across all operations to ensure unaffected properties — ownership, links, addresses — are preserved?

1. [nelson] When content is appended to a document, must the ownership of every other document in the system remain exactly as it was before the operation?
2. [nelson] If a link is created between two passages, must all existing links — including those touching the same documents — remain unchanged in their endpoints and meaning?
3. [nelson] When a document is shared with a new user, must the permanent addresses of all content within that document remain identical to what they were before sharing?
4. [nelson] Must an editing operation on one version of a document guarantee that all prior versions remain retrievable with identical content?
5. [nelson] When a user transfers ownership of a document, must every link pointing into or out of that document continue to resolve to the same content as before the transfer?
6. [nelson] If content is inserted at a position within a document, must all content that was not part of the insertion retain its original identity and permanent address?
7. [nelson] When a new document is created, must the system guarantee that no existing document's structure — its sequence of content, its boundaries, its permissions — is altered in any way?
8. [nelson] Must a deletion or rearrangement within one document guarantee that any other document quoting or including the same content still resolves correctly?
9. [nelson] When permissions on a document are narrowed or revoked for one user, must the visibility and access for all other authorized users remain completely unchanged?
10. [nelson] If a version is marked or labeled, must the system guarantee that the content, links, and ownership associated with every other version of that document remain unmodified?
11. [gregory] When `docopy` reads the source document's POOM to extract I-addresses, is the source POOM guaranteed to be completely unmodified afterward — no rebalancing, no displacement updates, no cache-dirty flags set on source nodes?
12. [gregory] During `deletend`, after POOM entries are disowned via `subtreefree`, does the code make any attempt to touch granfilade nodes for the orphaned I-addresses, or is the granfilade entirely out of scope for the delete path?
13. [gregory] When `makegappm` shifts V-positions rightward during INSERT, does it walk only the POOM entries within the current subspace (between the two blades), or does it visit entries in all subspaces and rely on the blade classification to skip them?
14. [gregory] If REARRANGE moves content from V-position `1.x` to a position that numerically falls in `0.2.x` (the link subspace), does the POOM accept this new mapping without error, and does `retrievevspansetpm` subsequently return it as a link-subspace entry?
15. [gregory] When `insertendsetsinspanf` indexes a new link's endsets, does it read or modify any existing spanfilade entries for those same I-address ranges, or does it strictly append new entries alongside whatever already exists?
16. [gregory] During CREATENEWVERSION, `docopyinternal` copies text-subspace POOM entries — does this copying process create any new entries in the granfilade or spanfilade for the version document, or are those layers touched only by the DOCISPAN registration?
17. [gregory] When multiple FEBE sessions have the same document open for read access, and one session performs a `find_links` that triggers heavy spanfilade traversal and cache eviction via `grimlyreap`, can this eviction corrupt or modify the in-memory POOM state that another session's concurrent read operation depends on?
18. [gregory] After `deletevspanpm` removes a link's V→I mapping from the POOM, does the link's orgl structure in the granfilade remain byte-identical — same endset I-spans, same type reference — or could the deletion path touch the orgl's internal structure?
19. [gregory] When `strongsub` fires its exponent guard during DELETE shifting (returning the link position unchanged), does this guarantee extend to ALL entries with higher exponents than the deletion width, or only to entries in the specific `0.2.x` link subspace range?
20. [gregory] If two documents each transclude the same I-address range and one document performs INSERT at a V-position before the transcluded content, does the shifting in that document's POOM leave the other document's POOM V-addresses completely unchanged, including the displacement values stored at intermediate tree nodes?
