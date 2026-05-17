## Question 3 [theory]

> Was link emission designed so that every link is sited as a sibling within its home document's link allocator, with no link ever placed as a child of another link?

Yes — by default. In the address scheme, every link a document is home to gets a flat, sequentially-allocated slot in the document's `0.2` subspace, with no link sited beneath another link.

From `_docuverse/.../links.md` (which extracts the addressing structure from LM 4/31):

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.2    → second link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

Nelson's words, cited there from 4/31:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Two important nuances, both from the curated sources:

1. **"Link-to-link" is not nesting.** A link can *point at* another link's address via its endsets (covered in `link-to-link.md`, 4/49–4/51). That's a target relationship, not an allocation relationship. The pointing link still lives at its own flat sibling slot in some home document's `0.2` space.

2. **Nelson left the door open to subdivision.** From 4/31, quoted in `links.md`:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

So the *implemented* design (XU.87.1) is flat sibling emission per home document. Subdivision under a link address was floated as a future possibility, not specified.

If you want me to verify the exact wording around subdivision (whether Nelson commits to "no link is a child of another link" or merely defers the question), NEED_RAW: 4/31, 4/49–4/51.
