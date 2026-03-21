## Question 6 [nelson]

> After placement, if someone examines the document, must the system be able to reveal that the content originated from a specific prior location rather than being freshly authored?

# Yes — Origin Revelation Is a Fundamental Guarantee

After COPY places content into a document, the system **must** be able to reveal that the content originated from a specific prior location. This is not an optional feature — it is an architectural invariant that follows directly from how COPY works.

## COPY Creates Transclusion, Not Duplication

The COPY operation is defined as:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

Critically, **COPY shares I-addresses with the source**. The copied content retains the permanent Istream addresses of the original document where those bytes were created. It does not receive new I-addresses. The destination document's Vstream now maps to I-addresses that belong to another document.

## The System Distinguishes Native from Non-Native Bytes

Nelson explicitly defines two categories of content within any document:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

After COPY, the placed content consists of **non-native bytes** — inclusions whose I-addresses encode their home document. The system knows these bytes were not authored here because their I-address tumbler encodes a different `Node.0.User.0.Document` origin.

## The User-Facing Guarantee

Nelson states this as an absolute:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

This is not a "can if you look hard enough" capability. It is a design invariant. For any character in any document, the system reveals its origin.

## Content Identity Is Based on Creation, Not Value

Two documents containing identical text created independently have **different** I-addresses. Transcluded content **shares** the same I-address as the original. This is how the system distinguishes "wrote the same words independently" from "quoted from the original":

> "The virtual byte stream of a document may include bytes from any other document." [LM 4/10]

The I-address IS the provenance. There is no separate provenance metadata that could be stripped or lost.

## FINDDOCSCONTAINING Operationalizes This

The system provides a dedicated operation for tracing content origin:

> "This returns a list of all documents containing any portion of the material included by \<vspec set\>." [LM 4/70]

This works precisely because COPY preserves I-addresses. The system can find every document that contains bytes from a given source — because those bytes share I-addresses with the source.

## Why This Must Be So

The entire economic and attribution model depends on it. Royalties flow to the original author when their bytes are delivered — which requires the system to know whose bytes they are:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

"Determined automatically" means structurally — from the I-addresses, not from user-supplied metadata. If the system could not reveal that content originated elsewhere, it could not compute royalty splits, could not maintain attribution, and could not support the "step through the window" navigation that lets readers reach the original context.

## Summary

After COPY, examining a document **must** reveal non-native content and its origin. This is not an optional inspection capability but an architectural consequence of how Xanadu works: COPY shares I-addresses, I-addresses encode home documents, and the system always distinguishes native from non-native bytes. The guarantee is structural and unseverable.
