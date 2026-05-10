## Question 10 [nelson]

> Must a single endpoint be confined to content within one document, or may one endpoint of a link span content across multiple documents?

## A single endset MAY span content across multiple documents.

Nelson is explicit and unambiguous on this point. Each endset is an **arbitrary collection of spans** that can reference bytes scattered across the entire docuverse — including bytes in different documents.

### Direct evidence

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. **These may be anywhere in the docuverse.**"
> — [LM 4/42]

> "The from-set may be an arbitrary collection of spans, **pointing anywhere in the docuverse**. Similarly, the to-set may be an arbitrary collection of spans **pointing anywhere in the docuverse**. We adopt the same convention for link types."
> — [LM 4/43]

> "**ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE**"
> — [LM 4/45], diagram caption

### Why this works

Endsets are span-sets, and spans are pairs of tumbler addresses. Since tumbler addresses form a single universal address space covering all servers, accounts, and documents, a span-set can naturally include spans from document A, document B, and document C — all in a single endset.

From the spans concept: a span-set is "a series of spans" used to "designate a separated series of items exactly, including nothing else" [LM 4/25]. There is no constraint limiting those spans to one document.

### The design intent

This generality is deliberate. Nelson designed endsets to be maximally flexible — a link's from-set might touch three separate passages in three different works because the idea being connected genuinely spans those locations. Restricting an endset to a single document would undermine the vision of links as connections across the entire web of literature.

The MAKELINK operation accepts `<from set>` and `<to set>` as sets, not as single document-local positions [LM 4/68]. The link's home document determines **ownership**, not the scope of what it can connect:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to."
> — [LM 4/12]
