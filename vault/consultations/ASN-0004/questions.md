# Sub-Questions — Content Insertion

**Inquiry:** What must INSERT preserve and establish? What are its preconditions, postconditions, and frame conditions with respect to the address space, existing content, and links?

1. [nelson] When new content is inserted into a document, must every piece of content that existed before the insertion remain retrievable at its original identity?
2. [nelson] Does insertion require that the target document already exist and that the inserting user hold appropriate permission over it?
3. [nelson] Must the position chosen for insertion fall exactly within the document's current content boundaries, or may it extend beyond the last position?
4. [nelson] After insertion, must the new content receive a permanent identity that has never been used before and will never be reused?
5. [nelson] Must all links whose endpoints referenced content in the document before insertion continue to resolve to exactly the same content afterward?
6. [nelson] Does insertion into one version of a document leave every other version's content and structure completely unchanged?
7. [nelson] Must the system guarantee that the inserted content becomes immediately and permanently retrievable — that no future operation can make it vanish?
8. [nelson] After insertion shifts existing content to later positions, must the correspondence between each piece of content and its permanent identity be preserved exactly?
9. [nelson] Must insertion be all-or-nothing — either the new content appears and all bookkeeping updates succeed together, or the document remains as if nothing happened?
10. [nelson] Does insertion into a shared passage affect every document that includes that passage, or only the document where the insertion was requested?
11. [gregory] When makegappm shifts existing POOM entries right by the insertion width, does it shift every entry with V-position ≥ the insertion point, or only those entries whose V-position falls between the insertion point and the second blade computed by findaddressofsecondcutforinsert?
12. [gregory] If a document contains text at V:1.1-1.5 and a link at V:0.2.1, and INSERT places new text at V:1.3, does the link entry at V:0.2.1 remain byte-identical in the POOM — same V-displacement, same I-displacement, same widths — with zero modification to any field?
13. [gregory] When two successive INSERTs target the same V-position (e.g., INSERT "A" at V:1.1 then INSERT "B" at V:1.1), does isanextensionnd ever coalesce these into a single POOM crum, or does same-position insertion always create a separate crum because the new I-address is not adjacent to the shifted entry?
14. [gregory] Does INSERT guarantee that the DOCISPAN entry written to the spanfilade records exactly the contiguous I-address range allocated for this insertion, and never a wider or narrower span — even when isanextensionnd coalesces the new content with an adjacent existing POOM entry?
15. [gregory] When INSERT allocates fresh I-addresses via findisatoinsertmolecule, and the document previously had a CREATELINK that advanced the allocation counter past the text range, does the new text I-address start immediately after the link orgl's I-address, or does it resume within the text subspace (.0.1.x) specifically?
16. [gregory] If INSERT is called with a V-position beyond the current document extent (e.g., the document spans V:1.1-1.5 and INSERT targets V:1.100), does the backend create the POOM entry at V:1.100 with a gap, or does it clamp or reject the position?
17. [gregory] After INSERT completes, are ALL pre-existing granfilade entries — both text molecules and link orgls belonging to any document — guaranteed byte-identical to their state before the INSERT?
18. [gregory] When INSERT shifts a POOM entry right via tumbleradd in makegappm, and the entry's V-displacement plus the insertion width would cross the subspace boundary (e.g., V:1.14 + width 0.2 reaching into 2.x), does findaddressofsecondcutforinsert prevent this shift, or could a text entry be pushed into the link subspace?
19. [gregory] Does INSERT write anything to the spanfilade beyond the single DOCISPAN entry for the newly allocated I-span — for instance, does it update or duplicate DOCISPAN entries for the shifted POOM entries whose V-positions changed?
20. [gregory] When INSERT is dispatched through the FEBE protocol, does putinsert send the success response to the client before doinsert executes the POOM mutation, and if doinsert fails (e.g., findorgl BERT check), does the client receive a success response for a mutation that never occurred?
