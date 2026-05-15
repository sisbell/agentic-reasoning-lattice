## Question 2 [theory]

> Does Nelson use "bundle" as a defined term in Literary Machines (or the concept notes) with a meaning distinct from an I-span / mapping block — and if so, what does it denote?

Based on the curated sources above, **"bundle" does not appear as a defined term in Literary Machines**. The curated concept notes and design-intent docs cover Nelson's vocabulary (braid, span, endset, span-set, compound document, compound link, faceted link, inclusion, window) and none of them introduce "bundle" with a distinct technical meaning.

The closest Nelson-defined concepts in the curated material:

- **"Braid"** — for the evolving document itself: *"A document is really an evolving ONGOING BRAID."* (2/14). This is the metaphor for a document's history, not a structural unit like an I-span.
- **"Compound document"** — *"A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material."* (2/32-ish, via `transclusion.md` / `windowing.md`).
- **"Compound link" / "faceted link"** — *"Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links."* (4/51).
- **"Span-set"** — a discontiguous set of spans (one endset can be a span-set). This is the structural aggregate Nelson does define.

For context: the project's `ASN naming scheme` memory notes that "strand/bundle/span" vocabulary was *derived from* Nelson's braid metaphor — i.e., "bundle" is **project coinage inspired by** Nelson, not Nelson's own defined term, as far as the curated sources show.

NEED_RAW: I cannot verify absence from the full book purely from the curated extracts. To definitively confirm Nelson never uses "bundle" as a defined term, a grep across `resources/literary-machines/raw/*.txt` would be needed (particularly likely loci: 2/13-2/22 storage/braid discussion, 4/41-4/60 link structure, 4/15-4/40 tumblers/spans).
