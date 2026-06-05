# Sub-Questions — RETRIEVEDOCVSPANSET Operation (per-subspace document extent query)

**Inquiry:** What happens when a document is asked, by its identity alone, for the extent of each of its subspaces — the number of characters of text and the number of links it contains? What does the returned span-set describe, what relationship must each member span bear to its subspace, what does reporting them together reveal about the document that single-subspace extent queries would not, and what invariants must hold across the per-subspace spans the operation may return?

1. [theory] When a document is named by its identity alone, what must the system guarantee it returns about the size of each distinct kind of content it holds?
2. [theory] What does each member of the returned span-set describe about its corresponding part of the document?
3. [theory] What relationship must each reported span bear to the body of content it measures — must it account for every character or link present, and nothing outside it?
4. [theory] Why must the count of text and the count of links be reported as separate measures rather than as a single combined extent?
5. [theory] What does presenting the text-extent and the link-extent together reveal about a document that asking for either one alone could never show?
6. [theory] Must the returned set always describe the same kinds of content for every document, so that two documents' reports can be meaningfully compared?
7. [theory] What invariant must hold between a part's reported extent and the actual content a reader would find if they retrieved that part?
8. [theory] How must the design treat a part of the document that holds no content at all — must its extent still appear in the report, and as what?
9. [theory] What permanence guarantee, if any, attaches to these reported extents — may a later report of the same document identity ever contradict an earlier one without the document having changed?
10. [theory] Must the extents reported for the separate parts be consistent with one another and with the document as a whole, and what would a violation of that consistency mean?
11. [evidence] When RETRIEVEDOCVSPANSET walks a document's POOM via `retrievevspansetpm`, does it emit exactly one VSpec per occupied subspace, or can a single subspace yield multiple disjoint VSpecs if its POOM entries are non-contiguous in V-space?
12. [evidence] The KB states the text subspace VSpec reports width in characters while links live internally at `2.x` but are normalized to `0.x` in output — does the returned link VSpec's start tumbler use the `0.x` form, and is its width measured in number-of-links or in I-space byte extent?
13. [evidence] For each returned VSpec, must its start position be the subspace's minimum occupied V-address and its width exactly span to the maximum occupied V-address, or can the reported span overshoot into unoccupied positions within that subspace?
14. [evidence] Does `retrievevspansetpm` derive each subspace's extent from the POOM root displacement and width (`setwispnd`), or does it traverse to the bottom crums and accumulate per-entry widths?
15. [evidence] If a document has text in `1.x` but no links, does RETRIEVEDOCVSPANSET return a single-member span-set, or does it return a zero-width placeholder VSpec for the empty link subspace?
16. [evidence] After a link's POOM entry is removed via DELETEVSPAN on `2.x` (reverse-orphaned link [ST-LINK-REMOVE]), does the link subspace VSpec returned by RETRIEVEDOCVSPANSET reflect the now-absent V→I mapping, or does it still report the prior link count?
17. [evidence] The KB says RETRIEVEDOCVSPAN is "broken for documents with links — returns a bounding span covering both subspaces" — does RETRIEVEDOCVSPANSET's per-subspace separation come from a distinct traversal that classifies entries by `first_digit(v)`, or from post-processing the same bounding span?
18. [evidence] Must the text VSpec and link VSpec returned together be mutually disjoint in V-space (no overlap in tumbler ranges), and is this disjointness guaranteed by the subspace separator structure rather than checked at retrieval time?
19. [evidence] Does the type subspace (`3.x`, reserved per SS-ADDRESS-SPACE) ever appear as a third VSpec in the returned span-set, or does RETRIEVEDOCVSPANSET only ever report text and link subspaces?
20. [evidence] Since INSERT and DELETE preserve subspace isolation [FC-SUBSPACE], is it invariant that the text VSpec's width returned by RETRIEVEDOCVSPANSET is independent of how many links exist — i.e., editing in `2.x` never alters the reported `1.x` extent and vice versa?
