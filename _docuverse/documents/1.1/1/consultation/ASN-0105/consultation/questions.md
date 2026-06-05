# Sub-Questions — RETRIEVEDOCVSPAN Operation

**Inquiry:** What happens when a span of a document is read at once? What is returned, what relationship does the returned content bear to the document's arrangement at the moment of reading, what does the system do about positions within the span that hold no content, and what invariants must the operation maintain about the result's faithfulness to the arrangement?

1. [theory] When a continuous span of a document is read at once, what must the returned content faithfully preserve about the order in which those contents appear in the document?
2. [theory] What relationship must the returned content bear to the document's arrangement at the precise moment the read occurs, and must it reflect that arrangement exactly?
3. [theory] When some positions within the requested span hold no content, what must the system return for those empty positions, and how must their absence be represented?
4. [theory] Must the returned content show the document's content as it is currently arranged, or as it was originally composed before any rearrangement?
5. [theory] What identity guarantee must the returned content carry, so that a reader can know which underlying content each returned piece corresponds to?
6. [theory] If the document's arrangement changes after a span is read, what must remain true about the faithfulness of the already-returned result to the arrangement at read time?
7. [theory] When a requested span extends beyond where the document's content ends, what must the system guarantee about the portion of the span that has no corresponding content?
8. [theory] Must reading the same span twice, with no intervening edits, return content identical in both substance and order, and what guarantees this stability?
9. [theory] What must the result preserve about the boundaries between distinct pieces of content within the span, or must the span appear as a single undifferentiated whole?
10. [theory] What invariant must hold between the length of the span requested and the structure of the result, so a reader can map each returned position back to its place in the document?
11. [evidence] When a contiguous V-span is read via `retrieverestricted`, does the returned content reflect the POOM's V→I mapping as it exists at that instant, or can cached enfilade nodes return a stale arrangement after a prior INSERT/DELETE in the same session?
12. [evidence] If the requested V-span includes positions that have no POOM entry (a gap between two crums), does the read skip those positions silently, return a placeholder, or truncate the result at the first gap?
13. [evidence] When the read span straddles two non-contiguous I-spans (e.g., text split by the CREATELINK allocation gap), does the result preserve V-order via `incontextlistnd`'s insertion-sort, or does it reflect I-address ordering?
14. [evidence] Does reading a span whose endpoints fall in the interior of existing crums invoke `slicecbcpm`, or does the read operate on whole crums and clip the returned bytes afterward without mutating the POOM?
15. [evidence] For a read span that extends beyond the document's current root width, does the operation clamp to the existing content boundary, or does it return content up to the requested width including empty trailing positions?
16. [evidence] Since the granfilade is byte-opaque [INV-BYTE-OPAQUE], if a read span boundary falls mid-way through a multi-byte UTF-8 character, does the operation return the partial byte sequence as-is?
17. [evidence] When the same I-address appears at multiple V-positions within the read span due to self-transclusion, does the read return the content once per V-position, faithfully reproducing each occurrence in the arrangement?
18. [evidence] Does a read of a span containing a negative V-position tumbler [EC-NEGATIVE-VPOSITION] — produced by a prior DELETE shift — return that content, and does `intervalcmp` order it before the positive positions?
19. [evidence] If the read span crosses from the text subspace (`1.x`) into the link subspace (`2.x`), does `retrieverestricted` return link orgl I-addresses intermixed with text, or is there a boundary that halts the read at the subspace transition?
20. [evidence] Across the different physical tree shapes a POOM can take (taller after DELETE, varied split history), does a read of the same logical V-span always produce byte-identical results, confirming [INV-ENFILADE-CONFLUENCE] holds for contiguous span reads?
