# Sub-Questions — Content Deletion

**Inquiry:** What must DELETE preserve? What happens to addresses, links, and other documents that reference deleted content? In what sense is deletion reversible?

1. [nelson] When content is deleted from a document, does the permanent identity of that content survive the deletion, or is the identity itself destroyed?
2. [nelson] If a link points to content that has been deleted, must the system preserve the link itself, and what must it report when someone follows that link?
3. [nelson] Does deletion remove the content from all documents that share it through transclusion, or only from the document where the deletion was performed?
4. [nelson] Must the system guarantee that a deleted passage can always be restored to its original position in the document, and if so, what information must be retained to make this possible?
5. [nelson] When content is deleted, does the address space of the document change — do the addresses of surrounding content shift, or do they remain stable?
6. [nelson] Can an author delete content that other documents have transcluded, and if so, what obligation does the system have to those other documents?
7. [nelson] Is deletion a new version of the document, preserving the pre-deletion state as a prior version that remains accessible?
8. [nelson] Must the system distinguish between content that was never present and content that was present but deleted — is there a visible trace of deletion?
9. [nelson] If deleted content carried royalty or compensation obligations, does deletion release those obligations or must they persist despite the content no longer being visible?
10. [nelson] Does the system permit permanent, irrevocable deletion of content, or must every deletion be reversible as a consequence of the permanence guarantee?
11. [gregory] When content at I-addresses [X,Y] is deleted from document A's POOM but document B still transcludes those same I-addresses, does `find_links` for a link whose endset spans [X,Y] return results when queried from document B but not from document A?
12. [gregory] If a link's source endset references I-addresses [X,Y] and only the middle portion [X+2,Y-2] is deleted from the home document's POOM, does `RETRIEVEENDSETS` still return the full I-span [X,Y], or does the I→V conversion via `span2spanset` produce two disjoint V-spans for the surviving portions?
13. [gregory] After DELETE removes all text content from a document, does `findisatoinsertmolecule` still return the next I-address after the original high-water mark, or does the allocation counter appear to reset because the granfilade query finds no entries under the document's I-range?
14. [gregory] When DELETE shifts surviving POOM entries left via `strongsub`, and two formerly non-contiguous entries become V-adjacent, does `isanextensionnd` merge them into a single crum on a subsequent INSERT, or does merging only happen at COPY/INSERT time for new entries?
15. [gregory] If document A creates a link to content X, then A deletes content X, then document B transcludes content X from the granfilade by its I-address — is there any mechanism in the system to transclude content by I-address directly, or must the content exist in some POOM somewhere to be copyable via `docopy`?
16. [gregory] Does `FINDDOCSCONTAINING` return document A after A has deleted the queried content, given that the spanfilade DOCISPAN entries for A are never removed — and if so, does the front-end or any layer filter out documents that no longer actually contain the content?
17. [gregory] When DELETEVSPAN targets the link subspace (V-position `0.2.x`), removing a link's POOM entry, does this operation shift other link POOM entries at higher V-positions leftward, or does the exponent guard in `strongsub` prevent shifting within the link subspace?
18. [gregory] After DELETE of a V-span that partially overlaps a POOM crum, does `slicecbcpm` produce a new crum whose I-displacement is offset from the original to reflect the surviving portion, or does it retain the original I-displacement and reduce only the I-width?
19. [gregory] If two versions share I-addresses via CREATENEWVERSION, and one version deletes some of that shared content, does `SHOWRELATIONOF2VERSIONS` (compare_versions) still correctly identify the overlap based on I-addresses that remain in both POOMs, or does it report reduced overlap?
20. [gregory] When DELETE produces a negative V-position tumbler for a surviving entry, does subsequent INSERT at a positive V-position interact correctly with the negative-positioned entry — specifically, does `makegappm` shift negative-V entries, or does the two-blade mechanism in `findaddressofsecondcutforinsert` classify them as beyond the second cut?
