# Sub-Questions — Two Space

**Inquiry:** What is the relationship between permanent content storage (I-space) and mutable document arrangement (V-space)? What invariants connect them?

1. [nelson] Must every piece of content that has ever been stored remain retrievable even after it no longer appears in any document's current arrangement?
2. [nelson] Can the same stored content appear at multiple positions within a single document or across different documents simultaneously?
3. [nelson] When a document's arrangement changes, does the underlying stored content remain byte-identical and at its original permanent address?
4. [nelson] Does every unit of content have a stable identity that is independent of which document currently includes it or where it appears?
5. [nelson] Must the system distinguish between "content as originally written" and "content as currently arranged for reading" as fundamentally separate concerns?
6. [nelson] If two documents share the same content by reference rather than by copying, must a reader be able to discover that the content is shared?
7. [nelson] Is the mapping from a document's visible arrangement to the underlying stored content always recoverable — can the system always trace displayed content back to its permanent origin?
8. [nelson] Must the permanent content layer be append-only, or can stored content ever be modified in place after initial storage?
9. [nelson] When content is included in a document by reference, does the document's arrangement record the precise extent of content referenced, or only a pointer to a larger stored unit?
10. [nelson] Must the system guarantee that the permanent content layer and the document arrangement layer are never merged — that no operation on arrangements can corrupt or alter stored content?
11. [gregory] When two documents both hold V→I mappings to the same I-address range (via transclusion), does the system record which document originally created that content, or are all V→I references to shared I-addresses indistinguishable at the storage level?
12. [gregory] I-addresses encode a document-level prefix (e.g., `1.1.0.1.0.1.0.1.x`) — does the system ever use this prefix to look up the originating document for a piece of content, or is the hierarchy purely a namespace partitioning convention with no runtime semantic role?
13. [gregory] Was permanent retention of all I-space content always the design intent, or was garbage collection of I-addresses unreferenced by any V-space mapping ever planned or prototyped?
14. [gregory] The storage layer is byte-opaque with one I-position per byte. Was there ever a design for variable-width content atoms (a character, a media element) that would each occupy a single I-position, or was byte-granularity always the intended resolution for the permascroll?
15. [gregory] Is the fan-out from I-space to V-space unbounded — can any number of documents map V-addresses to the same I-address range — or was there a practical or design limit on how many V→I references could share a single I-address span?
16. [gregory] When content becomes unreachable from all V-space mappings, it persists in I-space indefinitely — is there any mechanism or query to enumerate these orphaned I-address ranges, or are they invisible unless you already know their addresses?
17. [gregory] The V→I mapping within a single document can become arbitrarily fragmented (many small spans rather than a few large ones) through editing — does this fragmentation degrade any system behavior beyond requiring more mapping entries, or is it purely a representation cost?
18. [gregory] Was the two-space architecture (mutable V-positions over immutable I-identities) present from the earliest Xanadu designs, or did it emerge during green's implementation as a solution to a specific problem like transclusion tracking or content-addressed linking?
