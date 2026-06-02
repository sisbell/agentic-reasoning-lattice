## Question 1 [theory]

> Is CREATENEWVERSION intended to produce a complete copy of the source document's current contents, or may a new version deliberately include only a portion of the source's content?

## Answer

**CREATENEWVERSION produces a complete copy of the source document's current contents.** It is not a mechanism for selective/partial inclusion. Partial inclusion is achieved through different operations (COPY/transclusion, or "versioning by inclusion").

### The operation itself copies the whole document

The FEBE specification is explicit that CREATENEWVERSION duplicates the entire contents of the source:

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

The phrase "*the* contents of document <doc id>" (not "part of" or "a span of") indicates the full current arrangement. Mechanically this is transclusion of the entire source — the new version shares the source's I-addresses, so no bytes are physically duplicated, but logically the new version begins as a complete view of the source. After creation, you then edit it with INSERT, DELETE, and REARRANGE; those edits change the new version's Vstream while leaving the source untouched (see `versions.md`, `delete-semantics.md`).

### Partial inclusion is a separate mechanism

When you want a new document that includes only *part* of a source, Nelson provides other tools:

- **COPY (transclusion of spans):** "The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." (4/67) — this lets you bring in arbitrary spans rather than the whole document.
- **Versioning by inclusion (windowing):** "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." (from `windowing.md`, 2/46)

The Hamlet example illustrates partial assembly via quote-links rather than CREATENEWVERSION: a modified "version" is built from "a quote-link to the first part of the original... then the word 'luge'; then a quote-link to the rest of the play" (from `transclusion.md`).

### Summary

| Goal | Operation |
|------|-----------|
| New version starting from the **complete** source | CREATENEWVERSION (then edit) |
| New document including only **portions** of a source | COPY / quote-links / versioning by inclusion |

So CREATENEWVERSION is intended to start from the full current contents. A "version" that deliberately contains only a portion of another document is constructed through transclusion/windowing, not through CREATENEWVERSION itself.

---

One caveat on scope: the curated sources fully specify CREATENEWVERSION's "creates a new document with the contents of" behavior, but they don't show Nelson explicitly *prohibiting* a partial variant of the command. If you want confirmation that no partial-version form of CREATENEWVERSION is described in the protocol section — NEED_RAW: 4/65-4/67.
