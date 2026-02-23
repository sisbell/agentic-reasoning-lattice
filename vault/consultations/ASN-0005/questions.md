# Sub-Questions — Content Deletion

**Inquiry:** What must DELETE preserve? What happens to addresses, links, and other documents that reference deleted content? In what sense is deletion reversible?

1. [nelson] When a user deletes content from their document, does the content's permanent address continue to exist, and can other documents still retrieve what was at that address?
2. [nelson] If document A includes shared content originally from document B, and document B's owner deletes that passage, does document A lose its copy or does the shared content survive independently?
3. [nelson] What happens to a link whose endpoint falls within a region that has been deleted — does the link itself survive, and can it still be followed?
4. [nelson] Is deletion an act of removing content from existence, or an act of removing content from a particular document's visible arrangement while the content remains permanently stored?
5. [nelson] If deletion is reversible, what must the system remember so that an undelete restores not just the content but also its original position and its relationships to links and shared references?
6. [gregory] After DELETE removes a V-span from document A, and document B holds a transclusion of the same I-addresses, does `find_links` called on document B still discover links whose endsets overlap those I-addresses — confirming that DELETE in A has zero effect on link discovery through B?
7. [gregory] When FOLLOWLINK resolves a link whose source endset I-addresses have been deleted from every document's POOM, does `span2spanset` return an empty specset for that endset, or does it return the raw I-addresses without V-position mapping?
8. [gregory] If content at I-addresses [.0.1.3, .0.1.5] is deleted from document A, then later someone COPYs that same I-address range from document B (which still has it via transclusion) back into document A, does document A's POOM now contain entries pointing to the original I-addresses — effectively restoring the content identity that links and version comparisons depend on?
9. [gregory] After DELETE shifts surviving POOM entries left via `tumblersub`, do the I-widths stored in those surviving bottom crums remain exactly unchanged — confirming that DELETE's V-space compaction never modifies any I-displacement or I-width field in a surviving crum?
10. [gregory] When `FINDDOCSCONTAINING` is called with a specset whose I-addresses were deleted from document A but still exist in the spanfilade as stale DOCISPAN entries, does the query return document A as a result — and if so, is there any mechanism the caller can use to distinguish stale from current containment?
