# Sub-Questions — RETRIEVEV Operation

**Inquiry:** What happens when a content fragment is read from the system by its address? What is returned, what guarantees of permanence and immutability does the returned fragment carry, what must the caller know to ask, and what invariants must hold for the read to be well-defined?

1. [theory] When a fragment is requested by its address, what exactly must the system return — the content itself, or a reference to it?
2. [theory] Once content has been assigned an address, must that address forever return the identical content, with no possibility of substitution or alteration?
3. [theory] Must the caller already possess the precise address of a fragment to read it, or can a fragment be reached without knowing its identity in advance?
4. [theory] Does reading a fragment by address ever change, consume, or affect that fragment in any way?
5. [theory] What guarantee does the design make that the same address, read at two different times, yields content that is bit-for-bit identical?
6. [theory] When content belongs to a particular version of a document, does its address bind it to that version permanently, or can the same address mean different things across versions?
7. [theory] Must every valid address correspond to content that genuinely exists, and what must happen when a caller asks for an address that names nothing?
8. [theory] Can two distinct fragments ever share a single address, or must each piece of content carry an identity that is uniquely its own?
9. [theory] What must remain true about the boundaries of a fragment — where it begins and ends — for a read by address to be well-defined?
10. [theory] Does sharing a fragment's address with another user grant them the ability to read precisely the same content the original holder would see?
11. [evidence] When RETRIEVECONTENTS resolves a V-address through the POOM to an I-address, does it return the raw bytes from the granfilade leaf, and are those bytes returned verbatim with no encoding interpretation per INV-BYTE-OPAQUE?
12. [evidence] Must the caller supply a V-address (requiring the document to be open and in their BERT list per PRE-DOCUMENT-OPEN), or can content be read directly by I-address without the document being open?
13. [evidence] If a read targets a V-position that has no POOM entry (a gap in V-space), does the operation return empty, error, or silently skip — and does it distinguish "no mapping" from "zero-width span"?
14. [evidence] Does a read against an I-address that still exists in the granfilade but is no longer referenced by any POOM (a deleted-but-permanent fragment per FC-GRANFILADE-PERMANENT) return its original bytes if addressed by I-address directly?
15. [evidence] For a multi-byte UTF-8 character spanning several I-positions, can a partial-width read return a fractured byte sequence that splits the character, and does the backend make any attempt to align reads to character boundaries?
16. [evidence] When reading transcluded content shared across documents (same I-address, different V-positions), does the read from each document's V-space return byte-identical content, and does the read path differ at all from reading natively-inserted content?
17. [evidence] Does the read path traverse the height-1 granfilade leaf as a 1:1 pass-through given MAXBCINLOAF=1, and does the read result depend in any way on the physical tree height after prior growth (EC-EMPTY-DELETE-TREE)?
18. [evidence] Does a read that triggers cache eviction via the grim reaper ever return stale or partially-flushed bytes, or is operation-level atomicity (INV-ATOMICITY) sufficient to guarantee the read reflects current committed granfilade state?
19. [evidence] Across the INV-ENFILADE-CONFLUENCE property, is a read by V-address guaranteed to return identical bytes regardless of the insertion order that produced the current tree shape, and does incontextlistnd participate in ordering the returned content?
