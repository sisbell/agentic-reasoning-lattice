## Question 3 [theory]

> What determines whether a document "contains" content — direct authorship, inclusion from elsewhere, or both?

# What Determines Whether a Document "Contains" Content

**Both.** A document contains content through direct authorship AND inclusion from elsewhere. The determining factor is the document's **Vstream arrangement** — not where the bytes physically live in Istream.

## The Native/Non-Native Distinction

Nelson explicitly addresses this with two complementary terms:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

The critical claim: containment is symmetric across origin.

> "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

## The Vstream Is the Document

A document's identity is its arrangement, not its storage:

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

So when you ask "what does document D contain?", the answer is its Vstream — which may pull from many Istream sources across the docuverse.

## Compound Documents Are Mostly Inclusions

> "A compound document consists of parts of old documents together with new material. Or we may say it really consists of quote-links and new material." [LM 2/32]

A compound document may contain *very little* native content yet still be a full document with an owner who receives royalties.

## The Operational Confirmation: FINDDOCSCONTAINING

The semantics are confirmed by how the system searches. FINDDOCSCONTAINING:

> "...returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." [LM 4/63]

The phrase "regardless of where the native copies are located" is decisive — containment is determined by Vstream membership, not Istream ownership.

## Documents Also Contain Their Out-Links

Beyond bytes, documents contain the links whose home they are:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links, the links it contains that point to other documents. By contrast, a document's in-links are those stored elsewhere which point to it." [LM 2/31]

Link containment follows the same ownership-by-home rule:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

## Summary

A document "contains" content along three dimensions:

| Containment type | What it includes | Where it lives |
|---|---|---|
| **Native bytes** | Content authored directly | Document's own Istream |
| **Inclusions** | Transcluded virtual copies | Other documents' Istream |
| **Out-links** | Links whose home is this document | Document's link subspace |

All three are equally "part of" the document from the user's perspective. The Vstream — the document's arrangement — is what the document IS. Native vs. non-native is an implementation distinction the front end is unaware of: "the address of a byte in its native document is of no concern to the user or to the front end" [LM 4/11].
