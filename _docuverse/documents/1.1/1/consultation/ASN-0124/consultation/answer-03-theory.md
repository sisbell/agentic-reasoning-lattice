## Question 3 [theory]

> What relationship must a returned document bear to the queried material — is partial overlap with even one fragment sufficient for inclusion, or must the document contain the queried regions in full?

## Answer

**Partial overlap with even a single fragment is sufficient.** A document is returned by `FINDDOCSCONTAINING` if it contains *any portion* of the queried material — it need not contain the queried regions in full, and it need not contain all of them.

Nelson's own descriptions of the operation are explicit on this point. The criterion is stated twice, both times with the broad "any" quantifier:

> "This returns a list of all documents containing **any portion** of the material included by <vspec set>." (4/70)

> "This returns a list of all documents containing **any** of the material specified by the span addresses, regardless of where the native copies are located." (4/63)

So the inclusion test is an existential one: *does this document contain even one byte of the queried set?* If yes, it is returned. There is no requirement of full coverage, no requirement that the document contain the spans contiguously, and no requirement that it contain every span in the request set — overlap with one fragment qualifies.

## Why the semantics must be this permissive

This is not an incidental looseness; it is what the operation is *for*. `FINDDOCSCONTAINING` is the discovery mechanism behind transclusion-tracking and royalty accounting — finding every document that quotes, windows, or otherwise includes your content. A full-containment rule would defeat that purpose: you could never discover the document that quotes a single sentence of a long work, which is precisely the common case.

The "regardless of where the native copies are located" clause (4/63) reinforces this. The search runs against shared Istream origin — it finds documents whose Vstream arrangements reference the queried I-addresses, however small the fragment. This is consistent with the per-byte royalty model, where the cash register "increments whenever bytes or links are delivered out of the document" (5/13): if compensation is owed for any byte used, then discovery must surface any document using any byte.

## Consistency with the link-search model

The same "any match suffices" design pattern governs link search, which uses an explicit satisfaction model:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (per the curated `links` source, 4/58)

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

For links, the rule is OR-within-an-endset (one span matching is enough) and AND-across-endsets. `FINDDOCSCONTAINING` is the simpler, purely existential case: a single dimension (content), where any overlapping fragment makes the document a match. In both, the system errs toward inclusiveness — surfacing a candidate on the strength of one matching fragment rather than demanding complete coverage.

---

*Note: the two governing quotes (4/70, 4/63) come directly from the verified curated extraction of the FEBE operation definitions; I have not needed raw pages beyond them, as both state the inclusion criterion verbatim.*
