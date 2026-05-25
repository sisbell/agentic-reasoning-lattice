## Question 5 [theory]

> When a user forks a document, what rights or claims over the shared content does the new version's owner acquire?

# Rights Acquired by the New Version's Owner

When a user forks a document (via `CREATENEWVERSION` or windowing/inclusion), they acquire ownership over a **new derivative document**, but acquire **no ownership claim over the shared/original content**. The fork is a new Vstream arrangement over Istream content that remains owned by its original creators.

## Rights ACQUIRED by the Forker

**1. Ownership of the new version itself.** The new document has its own tumbler address with ancestry encoded in its ID. From CREATENEWVERSION: *"This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry."* (4/66)

As owner of the new version: *"Only the owner has a right to withdraw a document or change it."* (2/29)

**2. Right to arrange, modify, and add new material.** Nelson explicitly establishes this as a "pluralistic publishing form":

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links." (2/45)

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." (windowing extract)

**3. Right to publish without seeking permission.** The publication contract pre-grants this:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" (2/45)

**4. Proportional royalty for the forker's own contributions:**

> "If a modified document is read, the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically." (2/45)

**5. Inclusion of others' content "as if it were native":** From the i-space-v-space concept: *"Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies."* (4/11)

## Rights NOT Acquired

**1. No ownership over the shared/original Istream content.** The original bytes retain their I-addresses and remain owned by the original creator. *"Document A can include Document B, even though Document B is owned by someone else."* (2/35, windowing)

**2. Cannot modify or withdraw the original:**

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The forker cannot delete content from the original — only from their own Vstream arrangement.

**3. Original author retains their royalty share** on their own bytes (the automatic proportional split applies).

**4. Original remains accessible.** Nelson stresses non-destruction: *"The old viewpoint is still present too — you can always say, 'Show me what this originally was.'"* (2/45)

## The Underlying Architecture

The forker acquires what the system structurally permits:
- A new **Vstream arrangement** (theirs to control)
- New **native bytes** they add (theirs at new I-addresses)
- A **transclusion relationship** to the original (live or time-fixed)
- **Royalty proportional to authorship**, computed automatically

The Istream content of the original is untouched and unowned by the forker. Attribution is structural (encoded in I-addresses), so the original author's authorship cannot be severed by forking — *"You always know where you are, and can at once ascertain the home document of any specific word or character."* (2/40)

## Summary

Forking gives you ownership of a **new view** that contains and modifies someone else's content, but the underlying content remains theirs. You own the arrangement, the additions, and the resulting compound document; the original author retains ownership of their bytes, their royalties on those bytes, and the inviolability of their original work.
