# Sub-Questions — Address Permanence

**Inquiry:** What guarantees must the system provide about address stability? Once content is assigned an address, what operations may and may not affect that assignment?

1. [nelson] Once content is assigned an address in the system, may any operation — editing, deletion, or versioning — ever change that assignment?
2. [nelson] If a user inserts new content into the middle of an existing document, must the addresses of all previously stored content remain exactly as they were?
3. [nelson] May the system ever assign a previously used address to different content, or must every address be permanently bound to exactly one piece of content?
4. [nelson] When a new version of a document is created, do the shared passages retain their original addresses, or does versioning produce new addresses for the same content?
5. [nelson] If content is deleted from a document, does its address cease to exist, or must the address remain valid and the content remain retrievable through other means?
6. [nelson] When the same content appears in multiple documents through transclusion, must it be identified by one single address everywhere, or may different documents use different addresses for the same content?
7. [nelson] Must links continue to function correctly after editing operations precisely because the addresses they reference are guaranteed never to change?
8. [nelson] Must every act of storing new content produce a fresh address that has never been used before and will never be used again?
9. [nelson] If a user rearranges passages within a document — moving a paragraph from one position to another — must the content's permanent address remain unchanged despite its new position?
10. [nelson] Must the system be able to answer, for any valid address, what content was originally stored there, regardless of how many edits or versions have occurred since?
11. [gregory] After INSERT stores text at a given I-address in the granfilade, is there any operation or sequence of operations that can modify the bytes stored at that I-address, or is the granfilade strictly append-only with no in-place mutation?
12. [gregory] When DELETE removes a V-span and the corresponding I-addresses become unreferenced by any POOM, can those same I-addresses ever be reassigned to new content by a subsequent INSERT or CREATELINK allocation?
13. [gregory] Does REARRANGE (both 3-cut pivot and 4-cut swap) preserve the I-address component of every affected POOM entry exactly, changing only V-displacements while leaving I-displacements and I-widths untouched?
14. [gregory] When COPY transcludes content from document A to document B, does document B's POOM receive exactly the same I-addresses as document A's POOM for the copied span, or does any intermediate conversion alter or re-allocate the I-address values?
15. [gregory] After CREATELINK allocates a link orgl I-address that advances the per-document allocation counter past the text range, can a subsequent text INSERT ever receive an I-address that falls within or before the link orgl's I-address range, or is the gap permanent?
16. [gregory] When INSERT shifts V-positions of existing POOM entries rightward via makegappm, does the shift apply uniformly to all entries at or beyond the insertion point within the same subspace, or can any entry be skipped or receive a different shift magnitude?
17. [gregory] Does CREATENEWVERSION produce a new document whose POOM entries contain exactly the same I-addresses as the source document's text subspace, with no re-allocation, re-mapping, or transformation of those I-address values?
18. [gregory] Once insertspanf creates a DOCISPAN entry in the spanfilade recording that document D contains I-address range R, is there any operation that removes or modifies that entry, or does it persist unconditionally even after DELETE removes that content from D's POOM?
19. [gregory] If a link is created with endsets referencing specific I-address spans, and those spans are later deleted from every document's POOM, do the link's stored endset I-addresses in the granfilade remain unchanged such that re-transcluding the same I-addresses makes the link discoverable again?
20. [gregory] When DELETE shifts surviving POOM entries leftward via strongsub and the exponent guard fires for cross-subspace entries, is the entry returned completely unchanged — same V-displacement, same V-width, same I-displacement, same I-width — or does any component get modified even when the V-displacement is preserved?
