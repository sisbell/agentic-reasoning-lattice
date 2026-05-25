## Question 3 [theory]

> When content appears in multiple documents through sharing, which document does the design consider its origin?

The **home document** is the origin. This is the document where the bytes were natively created -- the document "under whose control" the bytes are actually stored. When the same content appears elsewhere through transclusion, those appearances are references back to the home document, not new origins.

The connection is **structural**, not metadata. Every byte has a permanent Istream address with the form `Node.0.User.0.Document.0.Element`, and the Document field directly encodes which document originally created that byte. Transcluded content shares the same I-address as the original; it does not get a new address in the including document.

## Nelson's Words

On native vs. non-native bytes:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

On the user's ability to trace any content back to its origin:

> "This world nevertheless remains simple in design. The virtuality is simple in structure and repeats in layers. You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

On ownership and persistence:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

## Key Distinction: Identity, Not Equivalence

The design is careful here: two documents containing **identical text** that were **independently created** have *different* I-addresses -- they are two origins of similar-looking content. But transcluded content -- content windowed from another document -- retains the I-address of its source. This is how the system distinguishes "wrote the same words" from "quoted from the original."

The home document is also the entity that receives royalties for that content's delivery, even when the bytes are being served as part of a compound document elsewhere:

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." (2/45)

## Why This Matters

Origin is not an attribute attached to content (a citation, an author field) -- it is the address itself. To fetch transcluded content, the system must request it from its home location. The connection cannot be severed because the fetching mechanism *requires* it. This is what makes attribution unstrippable within the docuverse.
