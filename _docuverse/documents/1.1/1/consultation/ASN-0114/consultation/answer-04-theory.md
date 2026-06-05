## Question 4 [theory]

> Must the operation reveal which document or documents the selected end points into, or only the abstract region the link records?

## Short answer

The operation returns **the abstract region the link records** — a span-set on the tumbler line — and nothing more. But in Xanadu that distinction collapses: the "abstract region" is expressed in tumbler addresses, and a tumbler address structurally *contains* the document field. So naming the span already names the document(s). The operation never has to "reveal" document identity as a separate act, because document identity is inseparable from the address.

## Why

An endset is "a link may be to or from an arbitrary set of bytes... anywhere in the docuverse" (endsets, 4/42), and those bytes are located by address: "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (endsets, 4/45). What the retrieval operation hands back is exactly that mapping:

> "RETRIEVEENDSETS... This returns a list of all link end-sets that are in <spec set>." (operations, 4/70)

The returned endsets are spans of tumbler addresses. And a tumbler address is not document-agnostic — its third major field *is* the document:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (i-space-addresses, 4/26)

So the span `Node.0.User.0.Document.0.Element` carries the document on its face. There is no representation of an endpoint that points "into the abstract" while concealing which document it lands in. This is the origin-traceability guarantee restated at the link level:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (origin-traceability / transclusion, 2/40)

## The distinction the question implies isn't a real fork

You could imagine two designs: (a) the operation returns opaque region IDs and you must separately resolve which document, or (b) it returns document-bearing addresses directly. Nelson chose (b) by construction — the address space *is* the document space. The only sense in which the result is "abstract" is that it gives you the *positions* (spans), not the *bytes*. Fetching the actual content is a different operation:

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." (operations, 4/61)

If you instead want the *set of documents* as the primary result rather than reading it off the spans, that is the dedicated operation:

> "FINDDOCSCONTAINING... This returns a list of all documents containing any portion of the material included by <vspec set>." (operations, 4/70)

## One caveat on the type endset

The above holds cleanly for the from-set and to-set, which point at content. The *type* endset is different: it may point to a "ghost element" — an address where nothing is stored.

> "What the 'type' designation points to is completely arbitrary... The search mechanism does not actually look at what is stored under the 'type'... it merely considers the type's address." (endsets, 4/44–4/45)
> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (endsets, 4/45)

Even there, the address still has a document field — it just may name a position that no document has populated. So the operation still hands you a document-bearing address; whether a document *exists* there is a separate matter.

## Bottom line

The operation reveals the abstract region — and because that region is a tumbler span, revealing it inherently reveals the document(s) the end points into. The two are the same disclosure, not a choice between them.
