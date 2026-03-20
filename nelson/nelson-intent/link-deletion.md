# Link Deletion

Source: Literary Machines, 4/9 (page 176), 4/12 (page 179), 2/29 (page 109)

## What It Means

Links CAN be deleted by their owners. This is distinct from "link survivability" which addresses what happens when the *content a link points to* is edited.

Nelson's architecture explicitly includes "DELETED LINKS" as a valid state in a document's technical contents, parallel to "DELETED BYTES." Both represent content that is "not currently addressable, awaiting historical backtrack functions, may remain included in other versions."

## Key Distinctions

**Link Survivability (what the invariant protects):**
- Links survive when you edit the *content they point to*
- As long as any referenced bytes remain at each end, the link remains valid
- This is automatic - the system doesn't need to "fix" links after editing

**Link Deletion (owner's administrative right):**
- The link's owner can explicitly remove a link from their document
- This is an ownership action, not a content editing side effect
- Deleted links enter the "not currently addressable" state

## Who Can Delete a Link

**The owner of the link's home document** - and only that person.

Nelson establishes:
1. "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)
2. "Only the owner has a right to withdraw a document or change it." (2/29)

A link pointing FROM your document TO another document is YOUR link. The author of the target document cannot delete your link - they can only delete content that might break it.

## User Guarantee

- **You control your links:** Links you create (in your documents) are yours to keep or delete
- **Others cannot delete your links:** Even if someone doesn't like your link pointing to their content, they cannot delete it (though they can delete the content it points to)
- **Deleted links are historically recoverable:** Like deleted bytes, deleted links await "historical backtrack functions"
- **Links may persist in other versions:** If someone versioned your document before you deleted the link, that version still contains it

## Principle Served

**Ownership integrity:** Your annotations, comments, and connections are YOUR property. The link freedom principle ("each user is free to link to anything") includes the freedom to un-link.

**Non-destruction:** Even deletion doesn't destroy - it makes "not currently addressable" pending historical backtrack. The link still exists in Istream.

## Nelson's Words

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

> "Only the owner has a right to withdraw a document or change it." (2/29)

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)
