## Question 6 [nelson]

> If two documents share the same content by reference rather than by copying, must a reader be able to discover that the content is shared?

## Yes — discovery of shared content is a structural guarantee

Nelson makes this clear at multiple levels: structural, operational, and as an explicit user-facing promise.

### The structural basis: I-space identity

When content is shared by reference (transclusion), both documents' V-space arrangements point to the **same I-space addresses**. This is not metadata — it is the mechanism itself. The system knows content is shared because the addresses are identical.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

Content identity is based on creation, not value. Independently created identical text gets different I-addresses; transcluded content shares the same I-address. The sharing relationship is therefore always computable from the addresses alone.

### The explicit user promise

Nelson states this as a guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

And for windowed (transcluded) content specifically, he requires **two-way** discoverability:

> "As already stated, it is possible for the reader to ask to see the materials which are windowed to by a given document. However, it must also be possible for the reader to ask to see whatever documents window to the current document. Both are available at any time." [LM 2/37]

### The operational mechanism

The FEBE protocol includes a dedicated operation for exactly this:

> **FINDDOCSCONTAINING**: "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This means: given any content, you can ask the system "what other documents contain this same material?" and get a complete answer.

### A nuance: automatic display vs. queryable discovery

There is one important distinction Nelson draws. A **quote-link** (explicit quotation) is visually indicated to the reader. But a plain **inclusion** may not be automatically shown:

> "Note that a quote-link is not the same as an inclusion, which is not ordinarily indicated." [LM 4/53]

So the system distinguishes between:

| Mechanism | Automatically visible? | Discoverable on request? |
|-----------|----------------------|--------------------------|
| **Quote-link** (explicit quotation) | Yes | Yes |
| **Inclusion** (plain transclusion) | Not necessarily | Yes — always |

Even for plain inclusions, the reader **can always discover** the sharing. The front end may not highlight it by default, but the structural information is always present and the FINDDOCSCONTAINING operation always works.

### Summary

The answer is unambiguous: **yes, a reader must be able to discover that content is shared.** This is:

1. **Structural** — shared I-space addresses make the relationship computable
2. **Operational** — FINDDOCSCONTAINING is a core protocol command
3. **Guaranteed** — "you can at once ascertain the home document of any specific word or character"

The only question is whether the front end *automatically shows* the sharing or requires the reader to ask. For quote-links, it is shown. For plain inclusions, the reader may need to query — but the system must always answer truthfully.
