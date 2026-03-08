## Question 3 [nelson]

> If two documents include the same passage, must the system guarantee that both arrangements point to identical underlying content, making the shared origin visible?

## Yes — but only when inclusion uses transclusion (the COPY operation)

The answer depends on *how* the two documents came to contain the same passage. Xanadu draws a sharp distinction.

### Transclusion: shared I-space origin is guaranteed

When document B includes a passage from document A via the COPY operation, both documents' V-space arrangements point to the **same I-space addresses**. The bytes are not duplicated — they exist once in I-space, and both V-streams reference them.

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents." [LM 2/36]

The COPY operation is explicitly described as transclusion — it "shares I-addresses with the source" [LM 4/67]. Both arrangements point to identical underlying content by construction.

### Shared origin is structurally visible and discoverable

The system provides FINDDOCSCONTAINING specifically for this:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

And origin traceability is a fundamental guarantee:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address itself encodes the originating document — `Node.0.User.0.Document.0.Element` — so shared origin is not metadata that can be stripped. It is structural.

### Independent creation: NO shared origin, even for identical text

This is the critical distinction. Content identity is based on **creation**, not **value**. If two users independently type the identical passage, each gets different I-space addresses. The system does not recognize them as sharing origin because they don't — they were created independently.

Only transclusion (COPY) produces shared I-space addresses. Only shared I-space addresses make the relationship visible to FINDDOCSCONTAINING and to the correspondence mechanism.

This is by design. Shared origin means "derived from the same act of creation," not "happens to contain the same bytes." The system preserves provenance, not textual coincidence.

### Summary

| Scenario | Same I-addresses? | Origin visible? | Discoverable via FINDDOCSCONTAINING? |
|----------|-------------------|-----------------|--------------------------------------|
| B transcludes from A (COPY) | Yes | Yes — structural | Yes |
| B independently types same text | No | No — different origins | No |
| B creates version of A (CREATENEWVERSION) | Yes | Yes — structural | Yes |

The guarantee is: **when two documents share content through the system's inclusion mechanism, they necessarily point to the same underlying I-space content, and that shared origin is always visible and discoverable.** The system does not merely *permit* this — it *cannot work any other way*, because transclusion is reference, not duplication.
