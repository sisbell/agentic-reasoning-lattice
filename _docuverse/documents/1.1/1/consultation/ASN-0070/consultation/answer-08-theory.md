## Question 8 [theory]

> How does the design distinguish between content that is genuinely part of a document and content that is merely transcluded from elsewhere, when resolving link endpoints?

# Native and Non-Native Bytes

The framing of your question contains an assumption I should address: there is no "merely" about transclusion. As I wrote: "Non-native bytes are as much a logical part of a document as native bytes" [LM 4/11]. The transcluded passage in your document is not a second-class citizen.

But the distinction you point to IS real and fundamental. It is the distinction between **native bytes** and **non-native bytes** (also called inclusions or virtual copies).

## The Distinction Is Encoded in Identity

Every byte in Xanadu has a permanent Istream address. The I-address itself encodes the home document — the document where the byte was first created. From [LM 4/11]:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations."

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies."

The tumbler address has the structure Node.0.User.0.Document.0.Element [LM 4/26]. The Document field IS the home document — there is nothing more to "look up." Distinguishing native from non-native is simply asking: does this byte's I-address fall within this document's range?

## How Link Endpoints Resolve

Links connect SPANS of bytes — not positions in documents. The endpoints are sets of byte spans, addressed by their Istream addresses [LM 4/42]:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes."

When a link endpoint resolves, the system follows I-addresses. Because the I-address carries the home document with it, the system always knows:

1. Which document was the origin of the bytes (the I-address tells you)
2. Where else those bytes appear (via FINDDOCSCONTAINING, which "returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located")
3. Where the bytes currently sit in any particular document's arrangement (the document's V→I mapping)

The link does not point at "document A's copy of these bytes" versus "document B's copy." There is only one set of bytes. They have one home. They appear in possibly many places. The link points to the bytes.

## What the User Experiences

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

When you follow a link, you arrive at the bytes. You can view them in their home context, or in any document that includes them. The glass-pane metaphor from [LM 2/34] captures it:

> "Think of the present document as a sheet of glass. It may have writing painted on it by the present author; it may have clear glass, windowing to something else..."

The painted writing is native. The clear glass — the window — shows non-native content from elsewhere. Both are part of what you read; they differ in where they were born and who owns them.

## Why This Matters for the System

The distinction has consequences:

- **Storage** [LM 4/11]: The owner of a document may delete bytes from their version, "but those bytes remain in all other documents where they have been included."
- **Royalty** [LM 2/45]: When a modified document is read, "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically."
- **Ownership** [LM 2/29]: Only the home document's owner may change the bytes; transcluding documents cannot modify what they include.
- **Permanence**: Because links point at I-addresses, and I-addresses persist independently of any single document, links survive editing of the document they were "in" [LM 4/42].

## Summary

The system does not flag bytes as "native" or "non-native" — that information is intrinsic to the I-address. When resolving a link endpoint, the system follows the I-address; the home document falls out of the address structure itself. The bytes are equally "part of" every document that includes them, but they have exactly one home, and that home is always discoverable. This is what makes attribution structural rather than metadata — and what makes the web of literature traceable rather than merely asserted.
