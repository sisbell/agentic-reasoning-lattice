## Question 5 [theory]

> When the query names multiple non-contiguous regions of content, what does the result reveal about the pattern of sharing across documents that a query about a single contiguous span could not?

## Direct answer

A query over a single contiguous span can only reveal the *dispersal* of one intact block — "who else holds this passage." A query that names multiple non-contiguous regions reveals the *recombination* pattern: which documents draw together pieces that are **separate in the source**. That co-occurrence structure — the signature of collages, compound, and derivative documents that reassemble scattered fragments — is something a single span can never expose, because one region has nothing to co-occur with.

## How the two queries differ at the naming level

Nelson draws a sharp line. A contiguous span is "from here to there," and "There is no choice as to what lies between; this is implicit in the choice of first and last point" (4/25). To name scattered material you must use a span-set: "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans" (4/25). A query naming several non-contiguous regions is therefore a request-set — "a set of spans, or spanset, presented to the back end in the FEBE protocol" (4/37).

## What the operation returns

`FINDDOCSCONTAINING` over such a set "returns a list of all documents containing any portion of the material included by <vspec set>" (4/70) — "regardless of where the native copies are located" (4/63). The result is the union of every document sharing *any* of the named pieces.

## What multiple regions reveal that one span cannot

- **Convergence / collage.** The documents that surface for several of the named regions are the ones that have *recombined* your separated material — the compound and derivative works that, in Nelson's terms, present "an easily-made annotated collage" (2/45). A single-span query cannot distinguish a document that quotes only region A from one that stitches A, B, and C together, because it never names B or C.
- **Grain of reuse.** It shows whether your material is taken as a block or cherry-picked fragment-by-fragment and reassembled elsewhere — the fine-grained pattern of sharing rather than the fate of one chunk.
- **Material split by editing.** Editing rearranges content, so a once-contiguous passage can become discontiguous. The span-set is the natural way to follow those scattered remains and learn which documents still hold them — a trace a single contiguous span can no longer express once the block is broken apart.
- **Precision against noise.** A contiguous span covering A-through-C necessarily drags in all the connecting material (4/25) and returns every document overlapping the bulky middle. A span-set names only A and C, so the sharing pattern it reveals is about *exactly* those passages.

## Why the architecture supports this

This is the retrieval-side mirror of how Xanadu links are built. A link end "may be on a broken, discontiguous set of bytes... a link may be to or from an arbitrary set of bytes" anywhere in the docuverse (4/42) — precisely so one connection can relate several separate passages. Link search uses the rule that "a link satisfies a search request if one span of each endset satisfies a corresponding part of the request" (4/58) — the "AND of the ORs" that makes a scattered set of regions a first-class query target. `FINDDOCSCONTAINING` applies the same logic to shared content: by accepting a set of regions rather than one span, it can report co-occurrence, not just dispersal.

## Caveat (interpretation)

Nelson specifies that `FINDDOCSCONTAINING` returns the *list* of containing documents (4/70, 4/63); reading off which documents share *several* of the regions (the full co-occurrence map) means cross-referencing that result — something the architecture supports but that Nelson does not spell out as a single return value. The comparative claim above — that the non-contiguous query reveals a recombination/co-occurrence pattern a single span cannot — is my synthesis from the cited operation, span-set, and endset semantics, not a verbatim Nelson statement.

NEED_RAW: 4/61–4/70 (the FEBE command discussion, especially the `FINDDOCSCONTAINING` passages on 4/63 and 4/70) — to confirm whether Nelson addresses this comparison between contiguous and non-contiguous queries explicitly.
