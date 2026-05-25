## Question 4 [theory]

> What guarantees about content permanence must hold across both the source and the fork after the fork occurs?

# Permanence Guarantees Across Source and Fork

After a fork occurs (CREATENEWVERSION or any inclusion-based derivative), the following guarantees must hold for **both** the source document and the forked document:

## 1. Istream Content Is Immutable

The bytes themselves never change. Both source and fork reference the same underlying Istream content; only their Vstream arrangements differ.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control" [LM 4/11]

The fork shares Istream addresses with the source. Edits to either side change only the Vstream mapping — the original bytes remain at their permanent I-addresses.

## 2. The Source Is Not Damaged by the Fork

Forking is non-destructive. The original document remains exactly as published.

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals. This is done by inclusion links." [LM 2/45]

## 3. Addresses Remain Permanent on Both Sides

Both the source's tumbler address and the fork's tumbler address are valid forever. The fork receives a new address indicating ancestry; neither address is ever reassigned.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

## 4. Deleted Content Persists Where Included

If the source owner later deletes bytes from their Vstream, those bytes remain accessible through the fork (and vice versa).

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## 5. Published Source Cannot Be Withdrawn

If the source was published before the fork, others (including the fork's owner) may have linked to it. The source must remain accessible.

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

## 6. Links Survive Across Both Versions

Links made to content that exists in both source and fork remain valid on both sides. Links can refractively follow from one version to corresponding places in the other.

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

## 7. Historical Backtrack Remains Available

Every prior state of both source and fork remains reconstructible.

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

## 8. Attribution Is Preserved Structurally

The fork's Vstream points back to Istream addresses owned by the source. Origin cannot be severed.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

## 9. Ownership Boundaries Hold

Source owner retains exclusive control over the source's Vstream; fork's creator owns the fork's Vstream. Neither can modify the other.

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

## 10. Royalty Flow Continues for Both

When the fork is read, royalties split automatically — the source owner is paid for bytes originating in the source, the fork's creator for bytes they added.

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." [LM 2/45]

---

## Summary

The fork operation is **structurally non-destructive**: it creates a new Vstream arrangement over (potentially shared) Istream content. After forking, all permanence guarantees that held for the source individually now hold for the pair — Istream immutability, address validity, link survival, historical reconstructability, attribution, ownership integrity, and (if published) the perpetual-availability obligation. The source's permanence is not diminished by the fork's existence; the fork inherits the source's permanence for any content it transcludes.
