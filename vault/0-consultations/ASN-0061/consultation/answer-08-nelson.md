## Question 8 [nelson]

> If permissions were granted on a region of a document that overlaps with the removed content, what must happen to those permissions after the removal?

## Nelson Does Not Specify Per-Region Permissions

This question presupposes a mechanism that does not exist in Literary Machines. My access model operates at the **document level**, not the region level:

> "A document may be private or published. [...] A private document may be read and linked-to only by the owner and his or her associates. A published document is available to anyone, and may be read and linked-to by anyone." [LM 2/42]

There are no permissions granted on regions of documents. A document is either private (owner and designees) or published (everyone). That is the entire access model.

## What DOES Happen to Structures on Removed Content

DELETE removes content from the **Vstream** (current arrangement) but not from **Istream** (permanent storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So after deletion:

- **Links** to the removed region **survive** — they point to Istream addresses, not Vstream positions: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]
- **Transclusions** in other documents are **unaffected** — they reference Istream content directly
- **Previous versions** still contain the content
- The content's **permanent I-address** and origin traceability are unchanged

The document-level access status (private or published) does not change because of a Vstream deletion. A published document remains published. Content removed from the current view remains accessible through historical backtrack and through any other documents that transclude it.

If your question arises from an implementation that introduces sub-document permissions (which would go beyond what I specified), that is an implementation design decision, not something Literary Machines addresses. NEED_RAW: [4/9, 2/42-2/43] if you want to verify against the original pages.
