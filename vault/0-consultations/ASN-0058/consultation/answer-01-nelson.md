## Question 1 [nelson]

> When a document presents content in a different order than it was originally created, must each contiguous run of consecutively-created content be represented as a single indivisible mapping unit?

## No. Nelson does not require contiguous I-runs to be indivisible mapping units.

The V→I mapping is conceptually **byte-level**, and operations can freely split any contiguous run of consecutively-created content.

### What Nelson specifies

The document IS the mapping from V-addresses to I-addresses. Each version defines a different mapping:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

V-addresses are always dense and contiguous (1 through N). I-addresses are permanent and immutable. The mapping between them is what changes during editing.

### REARRANGE proves splits are permitted

The REARRANGE operation explicitly breaks contiguous I-runs:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3... With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4." [LM 4/67]

If bytes I:100–109 form a contiguous run appearing at V:50–59, and you REARRANGE with cuts at V:53 and V:57, the result is two non-adjacent groups of the original I-run (V:50–53 gets the second region, V:54–59 gets the first). The contiguous I-run has been split across non-contiguous V-positions. No constraint prevents this.

INSERT has the same effect — inserting new content in the middle of a contiguous I-run splits it into two V-regions separated by the inserted material:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

### Spans are the natural unit, not a mandated atom

Spans are how the FEBE protocol refers to content — they are the operational currency. SHOWRELATIONOF2VERSIONS returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. The COPY operation takes a "spec set" (set of spans) as input [LM 4/67].

But Nelson never states that the mapping representation MUST keep maximal I-contiguous runs as indivisible units. He specifies:

1. The **conceptual model** — bytes have I-addresses and V-addresses
2. The **operations** — INSERT, DELETE, REARRANGE, COPY freely alter V-order
3. The **enfilades** — data structures that "manage huge agglomerates of text and their arrangement" [LM 1/33]

The internal representation of the V→I mapping is left to the enfilade implementation. Nelson describes the POOM enfilade as mapping V→I addresses but does not detail its atom of representation in Literary Machines.

### Summary

A contiguous run of consecutively-created I-addresses is a **span** — the natural and efficient unit for referring to content. But it is not an **indivisible** mapping unit. The editing operations demonstrate that any such run can be split, reordered, or interleaved with other content. The mapping granularity is conceptually per-byte; spans are an optimization for how the system *refers to* and *stores* mappings, not a constraint on what mappings are expressible.

NEED_RAW: [4/10, 4/11] — the curated sources cover these pages well, but the original pages may contain diagrams showing the V→I mapping structure that could add precision to this answer.
