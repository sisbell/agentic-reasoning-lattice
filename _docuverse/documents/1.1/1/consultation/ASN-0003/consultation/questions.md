# Sub-Questions — I-Space and V-Space

**Inquiry:** What is the relationship between permanent content storage (I-space) and mutable document arrangement (V-space)? What invariants connect them?

1. [nelson] When a user stores content permanently, does the system guarantee that this content can always be retrieved by its original identity, regardless of how documents are later rearranged?
2. [nelson] Can the same permanent content appear at multiple positions within a single document, or across different documents, without being duplicated in storage?
3. [nelson] When a user edits a document — inserting, deleting, or rearranging — does any permanently stored content ever change or disappear from the system?
4. [nelson] Must every character visible in a document correspond to exactly one piece of permanently stored content, with no gaps or phantom positions?
5. [nelson] If content is removed from a document's visible arrangement, does the system still retain that content so other documents or links referencing it remain valid?
6. [nelson] Does the design require a fixed mapping from each position in a document's visible arrangement to a specific piece of permanent content, and must that mapping update atomically during edits?
7. [nelson] Can a document's visible arrangement ever reference content that does not exist in permanent storage, or must the system prevent such dangling references?
8. [nelson] When a new version of a document is created, does it share the same permanent content as the original, or does the system create fresh copies of the stored material?
9. [nelson] Must the system guarantee that two users viewing the same document position always see the same permanent content, or can the arrangement-to-content mapping vary by viewer?
10. [nelson] If the system assigns a permanent identity to a piece of content at storage time, must that identity remain unique forever — never reassigned to different content, even after the content is removed from all documents?
11. [gregory] When `insertpm` creates a new POOM bottom crum mapping V-displacement to I-displacement, does it verify that the I-addresses actually exist in the granfilade, or does it trust the caller unconditionally?
12. [gregory] After `deletend` removes a V→I mapping and `subtreefree` reclaims the POOM nodes, is there any remaining structure in the POOM that records which I-addresses were once referenced — or is the association completely erased from the document's perspective?
13. [gregory] When `isanextensionnd` detects that a new POOM entry's I-address is contiguous with an existing entry (reach == origin), does it check that the V-addresses are also contiguous, or could it merge entries that are V-discontinuous but I-contiguous?
14. [gregory] Can a single I-address span appear at multiple V-positions within the same POOM (via self-transclusion), and if so, does `permute` in the I→V direction return all such V-positions or only the first one found?
15. [gregory] When `vspanset2sporglset` walks the POOM to convert V-spans to I-spans, does it handle the case where a single contiguous V-span maps to multiple non-contiguous I-address ranges — specifically, how many sporgl entries does it produce for a V-span that crosses an I-address discontinuity?
16. [gregory] Does the POOM enforce that every V-position maps to exactly one I-address (bijectivity in the V→I direction), or can the tree structure represent overlapping V-ranges that map to different I-addresses?
17. [gregory] When `makegappm` shifts V-positions during INSERT, does it modify the I-displacement or I-width fields of the shifted POOM entries in any way, or are those fields guaranteed untouched?
18. [gregory] If content at I-address range [X, X+5] is transcluded into two documents and then deleted from one, does `findlinksfromtothreesp` still find links through the surviving document's POOM — confirming that I-space permanence makes link discovery independent of any single document's V-space state?
19. [gregory] When `findisatoinsertmolecule` queries the granfilade for max+1 allocation, does it search only within the target document's I-address subtree, or could a concurrent session's allocation under a different document influence the result?
20. [gregory] Does the V-width stored in a POOM bottom crum always equal the I-width in logical magnitude, even though they use different tumbler exponents — and is there any operation that could cause them to diverge?
