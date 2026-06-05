# Sub-Questions — FOLLOWLINK Operation (read one endset of a link by selector)

**Inquiry:** What happens when one endset of a link is requested by giving the link's address together with a selector for which end? What is returned, what relationship must the returned spec-set bear to the endset the link records at that position, what does the result expose about the link without naming or returning the other endsets, and what invariants govern the spec-set the operation may return?

1. [theory] When a link's address is presented together with a selector naming one of its ends, what must the design guarantee the result represents about that single end?
2. [theory] What relationship must the returned specification bear to the end the link actually records at the selected position — must it denote exactly the same content region, no more and no less?
3. [theory] If the content at the selected end has been edited or rearranged since the link was made, must the returned specification still describe the same identified material the link committed to?
4. [theory] Must the operation reveal which document or documents the selected end points into, or only the abstract region the link records?
5. [theory] What must the design promise about not exposing, naming, or hinting at the link's other ends when only one end is requested?
6. [theory] If the selected end is empty — the link records no content at that position — what must be returned, and how must that differ from the case of an invalid selector?
7. [theory] Must two requests for the same end of the same link, with no intervening change to the link, always return specifications that denote identical content?
8. [theory] What identity must the returned end-specification carry — is it permanently tied to the same link and the same position, regardless of when it is requested?
9. [theory] May the returned specification ever describe content that the link does not actually connect at that end, and what guarantee forbids such over- or under-coverage?
10. [theory] Must requesting one end of a link leave the link itself, its other ends, and all referenced documents entirely unchanged?
11. [evidence] When the link's ISA (`docISA.0.2.N`) and an end selector are supplied, does the operation return the endset's raw I-address spans from the granfilade link orgl, or are they first converted to V-positions before being returned?
12. [evidence] How is the end selector encoded — as a fixed index into the three stored endsets (source/from, target/to, type), and what happens if a selector value outside that range is supplied?
13. [evidence] Must the returned spec-set be a value-exact copy of the I-address spans the link orgl records at that endset position, or can it differ in tumbler exponent representation between the stored I-width and the returned width?
14. [evidence] If the requested endset references content across multiple non-contiguous I-address ranges (a split endset from CREATELINK's automatic sporgl splitting), does the returned spec-set preserve all those spans as separate VSpecs?
15. [evidence] Are unreferenced I-addresses (DEL5 — those in no current POOM) silently filtered from the returned spec-set the way FOLLOWLINK filters them during I→V conversion, or is the raw stored endset returned regardless of current reachability?
16. [evidence] In what order are the spans returned within the spec-set — sorted by I-address via `incontextlistnd`, or in the stored order the endset was recorded at link creation?
17. [evidence] If the requested endset is empty or its content has been deleted such that nothing is currently referenced, does the operation return an empty spec-set without error rather than failing?
18. [evidence] Does requesting one endset by selector read or expose any I-addresses belonging to the other two endsets (the non-selected source/target/type), or is access strictly confined to the selected position?
19. [evidence] Does this operation require the link's home document to be open under BERT (PRE-DOCUMENT-OPEN / `findorgl`), and does it succeed for an orphaned link whose endpoint content is undiscoverable via `find_links`?
20. [evidence] Does the returned spec-set carry the endset's content-identity (I-address) addressing directly, or does it embed the source document identity (sporgl) so the caller knows which document's V-space the spans originate from?
