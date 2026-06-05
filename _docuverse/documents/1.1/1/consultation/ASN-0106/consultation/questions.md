# Sub-Questions — RETRIEVEDOCVSPANSET Operation

**Inquiry:** What happens when several spans of a document are read together? What is returned, what relationship do the returned fragments bear to one another and to the document's arrangement, what does the system reveal that would not be visible by reading each span separately, and what invariants must the operation maintain across the combined result?

1. [theory] When several spans of one document are read together, what must the system return as a single result rather than a loose collection of separate pieces?
2. [theory] What relationship must the returned fragments bear to one another — are they ordered, and if so, by what authority does that ordering arise?
3. [theory] Must the combined result preserve the document's own arrangement, so that fragments appear in the sequence the document defines rather than the sequence requested?
4. [theory] What does reading spans together reveal about the gaps between them that would remain invisible if each span were read on its own?
5. [theory] When two requested spans overlap, what must the system guarantee about the shared content — is it returned once, twice, or marked as common?
6. [theory] Must the identity of each returned fragment remain traceable to its exact place in the document, so the reader knows where within the whole each piece belongs?
7. [theory] What does the combined reading reveal about adjacency — whether two fragments sit directly together in the document or are separated by unrequested content?
8. [theory] What permanence guarantee must hold across the combined result, so that every fragment refers to the same version of the document?
9. [theory] If the same content appears in more than one requested region, what must the result reveal about that content being shared within the single document?
10. [theory] What invariant must the operation maintain so that reading spans together never alters, reorders, or loses any content compared to the document as it stands?
11. [evidence] When RETRIEVEDOCVSPANSET reads a multi-span specset, does it return the text subspace (1.x) and link subspace (internal 2.x, normalized 0.x) as separate VSpecs, or interleaved within one ordered result?
12. [evidence] If the request specset contains overlapping V-spans, does the combined result return duplicated fragments, or does the system coalesce them into a single covering VSpec?
13. [evidence] Does the order of VSpecs in the returned result follow the request specset's order, or is it re-sorted by V-address through incontextlistnd during tree traversal?
14. [evidence] When two requested spans map to I-addresses that are contiguous in I-space, does retrieval merge them into one returned fragment, or preserve the V-span partition from the request?
15. [evidence] Does reading several spans together expose self-transclusion — i.e., reveal that distinct V-positions in the result share the same I-address — in a way single-span reads would not?
16. [evidence] If a requested span crosses a POOM crum boundary, does whereoncrum classification split it into multiple returned sub-fragments, and are those sub-fragments tagged with their I-addresses?
17. [evidence] When the combined read walks the POOM via vspanset2sporglset, does it emit one sporgl per contiguous I-span, automatically splitting a single requested V-span at non-contiguous I-address boundaries?
18. [evidence] Does a zero-width span included in a multi-span request contribute an empty fragment to the result, or is it silently dropped from the combined output?
19. [evidence] Across the combined result, does the operation guarantee that the union of returned V-widths equals the sum of requested span widths (no overlap, no gap), preserving a V-space bijection?
20. [evidence] If the document's POOM contains a negative V-position from a prior DELETE shift, how does that fragment sort and appear within the ordered multi-span result relative to positive-V fragments?
