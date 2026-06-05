# Sub-Questions — READLINK Operation (read a link's structure by its address)

**Inquiry:** What happens when a link's endsets and type are read directly by the link's own address? What is returned, what does the reader learn about the relationship the link records, what does this reveal that following the link or searching for it by endpoint would not, and what invariants govern the structure the read may return?

1. [theory] When a link is read by its own identity, what must the system return about the relationship that link records?
2. [theory] What guarantee governs the completeness of a link's endsets when the link is read directly rather than traversed?
3. [theory] Must the type a link carries be permanent, or may a link's recorded type change across versions?
4. [theory] What does reading a link directly reveal about its relationship that following the link to its endpoints would not?
5. [theory] When a link names multiple endsets, what ordering or grouping among them must the read preserve?
6. [theory] Must a link's identity remain stable even as the documents it connects are edited or re-versioned?
7. [theory] What invariant ensures that the endsets a link reports actually correspond to existing content regions?
8. [theory] Can a link's endsets reference other links, and must a direct read disclose that nesting faithfully?
9. [theory] What must the design guarantee about a reader's ability to interpret a link's type without consulting its endpoints?
10. [theory] Is a link a first-class document in its own right, such that reading it shares the same permanence guarantees as reading content?
11. [evidence] When a link orgl is read by its own I-address (docISA.0.2.N), are all three endsets returned as raw I-address spans, or are they converted to V-addresses during the read?
12. [evidence] Does direct read of the link orgl preserve the positional ordering of the three endsets (source, target, type), and is that ordering structurally fixed within the orgl?
13. [evidence] How are the three endsets encoded inside the link orgl's enfilade — as separate subspaces within the orgl, or as a flat sporglset, and does the read return them as distinct spans?
14. [evidence] When the type endset references the global type namespace at 1.0.2.x, does a direct read return that type address as a raw I-address span identical in structure to the source and target endsets?
15. [evidence] Does direct read by link ID succeed for an orphaned link whose endpoint content has been deleted from all V-streams, returning the original endset I-addresses unchanged?
16. [evidence] For an endset that spans non-contiguous I-addresses (e.g., after a pivot fragmented the linked content), does a direct read return multiple sporgl entries per endset, and does it preserve their I-address ordering?
17. [evidence] Unlike FOLLOWLINK's silent filtering of unreferenced (DEL5) I-addresses during I→V conversion, does a direct read of the link orgl return the full endset I-spans without filtering against current POOM state?
18. [evidence] Does the link orgl as read reveal the link's home document identity (the docISA prefix of its ISA), and is that derivable from the link's own address structure?
19. [evidence] Is there an invariant that a link orgl always contains exactly three endsets, and does a direct read fail or return a partial structure if any endset's I-span is empty?
20. [evidence] Does direct read of the link orgl require the home document to be open under BERT (PRE-DOCUMENT-OPEN), or is the granfilade-resident orgl readable by ISA without a document-open precondition?
