## Question 9 [theory]

> Should a newly created document share no content history with any other document, unlike one produced through versioning?

Yes. This distinction is fundamental to Nelson's design, and it follows directly from the difference between the two creation operations.

## CREATENEWDOCUMENT produces an empty document

A newly created document starts empty—it has no content at all, and therefore shares no Istream history with anything:

> "CREATENEWDOCUMENT: This creates an empty document. It returns the id of the new document." (4/65)

Because it is empty, there are no I-addresses in common with any other document. Any content you subsequently write into it gets fresh I-addresses native to that document. It shares content history only if you later transclude (COPY) material in.

## CREATENEWVERSION explicitly shares content and records ancestry

A version is the opposite case—it transcludes the entire content of its source and carries an address marking its lineage:

> "CREATENEWVERSION: This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

The shared content is the whole point: each version is a different Vstream arrangement over the *same* Istream content. This shared Istream origin is what makes correspondence and refractive link-following work:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

## The semantic intent

The shared origin is precisely what distinguishes a version from a fresh document. With versions, the system can intercompare them—"show you, word for word, what parts of two versions are the same" (2/20)—because they refract from common Istream content. A brand-new document has no such common origin, so nothing corresponds.

One nuance worth flagging: Nelson notes that the *address* relationship of a version is structural, not a claim about derivation per se—"In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation" (4/29). But the operative difference for your question is content: a version is *born holding* the source's content (shared Istream), while CREATENEWDOCUMENT is born empty (no shared content history).

**So the answer is yes**: a newly created document shares no content history with any other document, whereas a version is defined by sharing content history with its source.
