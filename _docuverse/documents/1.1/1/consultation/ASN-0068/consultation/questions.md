# Sub-Questions — COMPAREVERSIONS Operation

**Inquiry:** Given two documents, how does the system identify which Istream content they share? What determines the correspondence and what form does the result take?

1. [theory] What must the system guarantee about the identity of a piece of content shared between two documents?
2. [theory] When two documents contain the same content, must the design treat that content as one shared entity rather than two copies?
3. [theory] What is the smallest unit of content at which sharing between documents can be recognized?
4. [theory] Must the determination of shared content be exact, or may it tolerate approximate or near-matching content?
5. [theory] What form must the result of comparing two documents take — a list, an overlay, a derived document, or something else?
6. [theory] Must the system be able to identify shared content between any two documents, regardless of when each was created?
7. [theory] What must the design guarantee about the symmetry of the comparison — does the order of the two documents affect the result?
8. [theory] Must the comparison reflect the full version history of each document, or only their current states?
9. [theory] What must remain true about the original documents after a comparison is performed — are they altered, annotated, or untouched?
10. [theory] Must the shared-content result itself be a permanent, addressable, and linkable entity within the system?
11. [evidence] When `compare_versions` (SHOWRELATIONOF2VERSIONS) runs on two documents, does it traverse both POOMs to compute I-address intersection, or does it query the spanfilade DOCISPAN entries for both documents and intersect there?
12. [evidence] Does the correspondence result returned by `compare_versions` take the form of a SpecSet pairing — i.e., a list of `(VSpec_in_doc1, VSpec_in_doc2)` tuples where each pair shares the same I-address span — or does it return I-address spans directly without V-mapping?
13. [evidence] When a single I-address span is mapped to multiple V-positions in one document (self-transclusion), does `compare_versions` emit a separate correspondence pair for each V-position, producing an N×M cross-product against the other document's mappings?
14. [evidence] Does `find_documents_containing` use the spanfilade DOCISPAN entries as its sole source of truth, meaning two documents identified as sharing content may in fact no longer share it after DELETE operations [EC-STALE-SPANFILADE]?
15. [evidence] When correspondence is computed, are I-address spans matched by exact equality, by overlap, or by containment — and what does the result look like when doc1 contains I:[.0.1.1,.0.1.10] and doc2 contains I:[.0.1.3,.0.1.7] (a strict subset)?
16. [evidence] Does the correspondence computation in `correspond.c` operate on the granfilade I-address dimension, or does it consult the spanfilade's 2D index keyed by (I-span, document)?
17. [evidence] When two documents share I-addresses originating from a third document (transitive transclusion via COPY chains), is the correspondence result identical to the case where doc1 directly transcluded from doc2 — i.e., is provenance forgotten in favor of pure identity intersection?
18. [evidence] For the `correspond.c` link-subspace crash [EC-COMPARE-CRASH], does the crash occur during I-address extraction from link orgls, or during the V-position back-mapping phase when link I-addresses fail the permascroll lookup?
19. [evidence] Is the correspondence computation symmetric — does `compare_versions(A, B)` produce the same VSpec pairings as `compare_versions(B, A)` with arguments swapped, or is one document treated as the reference?
20. [evidence] When correspondence pairs are reported, are they constrained by the caller-supplied specset bounds on BOTH documents (intersection filtered to both windows), or only on the first document with the second reported in full?
