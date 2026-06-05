## Question 2 [theory]

> What does the origin of a document's content stream signify, and must it remain fixed for the entire life of the document?

## What the origin of a document's content stream signifies

A document's content stream has a permanent home position in tumbler-space — its **origin** — which the FEBE operation `RETRIEVEDOCVSPAN` returns explicitly:

> "This returns a span determining the origin and extent of the V-stream of document <doc id>." (4/68)

That origin is the document's tumbler address, and it carries three layers of meaning encoded in the address fields:

> "There are four major fields, each expandable indefinitely, with three major dividers between them. These fields are Server, User, Document and Contents." (4/26)

So the origin signifies **provenance** (which Node/server the content lives on), **ownership** (which User/account controls it), and **identity** (which Document the bytes were born into). This is what makes attribution structural rather than metadata:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

## Must it remain fixed for the life of the document?

**Yes — the origin is permanent, and this permanence is the whole point.** Once a document's address is "baptized" in tumbler-space, it stays valid forever:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

This is the crucial distinction between Istream (permanent identity) and Vstream (mutable arrangement). The *origin* belongs to the permanent layer; the *extent* and internal ordering can shift through editing, but the home position cannot:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

That moving address is the byte's V-position within the arrangement — not the document's origin. The origin (the home location to which all native bytes belong) never moves:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

## A nuance for included content

Note that a document's *V-stream* may weave in bytes whose origin is **another** document (transclusions). Those included bytes retain *their own* permanent origin — the home document where they were created — regardless of how many documents window them:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

So every span in a document's content stream traces back to a fixed origin — either the document's own home position or the home position of the source it transcludes — and none of those origins ever change for the life of the content. The arrangement (Vstream) is fluid; the origins (Istream home locations) are eternal.
