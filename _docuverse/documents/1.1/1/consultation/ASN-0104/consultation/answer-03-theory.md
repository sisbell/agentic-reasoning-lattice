## Question 3 [theory]

> Must the caller already possess the precise address of a fragment to read it, or can a fragment be reached without knowing its identity in advance?

## Answer

**You do not need to possess a fragment's precise address in advance.** Xanadu's design explicitly separates *content delivery* (which consumes addresses) from *discovery* (which produces them). A caller can reach a fragment through relationship, containment, or hierarchy — and obtain its precise address as a *result*, not a prerequisite.

### Direct delivery does take an address

Only one FEBE operation actually ships content bytes, and it takes a spec-set:

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." (4/61)

> "RETRIEVEV ... This returns the material (text and links) determined by `<spec set>`." (4/67)

So at the moment of delivery, *some* address is named. The real question is whether the caller must have known it beforehand — and the answer is no.

### You can address by *container*, not identity

Tumbler-space is hierarchical, and the "1-positions" let you name a whole region without naming any fragment inside it:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." (4/38, from `spans.md`)

Because of **ghost elements**, you can target an account or node even though nothing is stored there, and the system resolves what lies beneath:

> "A link to or search of an account or node will find any of the documents under it." (4/23, from `ghost-elements.md`)

This means a caller who knows only "this author" or "this server" can reach fragments whose individual identities were never known to them.

### Discovery operations *produce* identities you didn't have

Several operations exist precisely to find content you cannot yet name:

- **FINDDOCSCONTAINING** — "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." (4/63, from `operations.md`)
- **Link search** — given any endset, find connected material: "This returns a list of all links which are (1) in `<home set>`, (2) from all or any part of `<from set>`, and (3) to all or any part of `<to set>` and `<three set>`." (4/69, from `operations.md`)

The link mechanism is bidirectional in discovery, so you can arrive at a fragment by asking what points *to* something else:

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside connections without appreciable delay." (2/46, from `document-discovery.md`)

And there is no central catalog you must consult — discovery is woven into the link/address structure itself:

> "For instance, there is no system directory; rather, we encourage the on-line publishing of directory documents by users." (4/41, from `document-discovery.md`)

### Summary

A fragment can be reached **without knowing its identity in advance**. You can navigate by containment (account/node/version ranges, ghost elements), by relationship (link search, "what connects here?"), or by content (FINDDOCSCONTAINING), and these operations hand you the precise addresses that RETRIEVEV then uses for delivery. The precise address is the *output* of reaching a fragment, not a required *input*.
