## Question 4 [theory]

> Must creating a new document leave the identities and content of all existing documents wholly untouched?

# Yes — creating a new document must leave all existing documents wholly untouched.

This follows directly from how the tumbler addressing and "baptism" mechanism work. Creating a new document is the allocation of a fresh address under your own account, and that allocation is guaranteed never to disturb addresses that already exist.

## The addressing guarantee

The core property of tumbler-space is that insertion never invalidates what is already there:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

Creation happens by **baptism** — forking a new sub-number under a number you own — and this is purely additive:

> "The basic principle is that of owned numbers... Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

Because addresses are forked rather than reorganized, existing documents keep both their identity and their place. As the forking concept summary puts it, "Creation never exhausts the space; insertion never invalidates existing references," and "No reorganization ever happens — once an address is forked, its relationship to its parent is permanent."

## Ownership protects existing content

Even setting addressing aside, a new document cannot reach into existing ones, because only an owner may alter a document:

> "Every document has an owner... Only the owner has a right to withdraw a document or change it." (2/29)

Your new document is created under your own account, so it has no authority to modify anyone else's content.

## What about new documents built from old ones?

This holds even when the new document is *derived* from existing material:

- **CREATENEWVERSION** — "This creates a new document with the contents of document `<doc id>`... The new document's id will indicate its ancestry." (4/66) The new version transcludes the source; it does not alter it.
- **Transclusion / COPY** is inclusion by reference, not destructive copying: the COPY summary notes "the copy shares I-addresses with the source," and the principle is that "modifications never damage originals."

Nelson states this explicitly for derived publications:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links." (2/45)

And because content lives permanently in Istream, even a new document that references existing bytes leaves those bytes' identities fixed: "Content at an Istream address never changes."

## Conclusion

Creating a new document — whether empty (`CREATENEWDOCUMENT`) or derived (`CREATENEWVERSION`, transclusion) — is strictly additive. It baptizes a new permanent address under the creator's own account, leaves every existing address valid (4/19), and cannot modify content the creator does not own (2/29). The identities and content of all existing documents remain wholly untouched.
