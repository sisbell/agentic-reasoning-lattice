## Question 1 [nelson]

> When a new link is created, does the link itself become permanent content with its own identity, or is it a mutable annotation that can be withdrawn?

## Links Are Permanent Content — But Owners Can "Delete" Them

A link, once created, is **permanent content with its own identity**. It is also **withdrawable by its owner** — but "withdrawal" in Xanadu means the same thing as "deletion" of bytes: removal from the current view, not destruction from existence.

### Links Are First-Class Stored Entities

Links are one of only two things actually stored in tumbler-space:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

Each link has its own permanent tumbler address in the `2.x` subspace of its home document, and these addresses are permanently ordered by creation:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Unlike bytes, which can be rearranged in Vstream, **links keep their creation-order addresses permanently**. Link `2.1` is always the first link created in that document; link `2.755` is always the 755th. Deleting link `2.5` does not renumber `2.6` onward.

Because links have addresses, they can be targets of other links:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link." [LM 4/49]

This confirms links have the same ontological status as content — addressable, referenceable, linkable.

### Owners Can Delete Links — But Deletion Is Not Destruction

Nelson explicitly includes "DELETED LINKS" as a valid document state on page 4/9, with language identical to deleted bytes:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This follows the same non-destructive semantics as byte deletion. Only the owner of the link's home document can delete it:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

So if Alice creates a comment link pointing to Bob's document, **Bob cannot delete Alice's link** — it lives at Alice's address. Alice can delete it, but even then it remains in Istream, recoverable through historical backtrack, and may persist in other versions of Alice's document.

### The Parallel with Bytes

| Property | Bytes | Links |
|----------|-------|-------|
| Stored in tumbler-space | Yes | Yes |
| Has permanent I-address | Yes | Yes |
| Owner can "delete" | Yes | Yes |
| Deletion removes from Istream | No | No |
| Recoverable via historical backtrack | Yes | Yes |
| May persist in other versions | Yes | Yes |
| Rearrangeable in Vstream | Yes | **No** — permanent order of arrival |

Links are actually **more permanent** than bytes in one respect: bytes can be rearranged within a document's Vstream, but links maintain their creation-order addresses forever.

### Summary

A link is permanent content with its own identity. Its creator can withdraw it from the current version of their document, but this is Vstream deletion — the link remains in Istream, is recoverable through historical backtrack, and may survive in other versions. The link's tumbler address is never reused or reassigned. In this sense, a link is not a "mutable annotation" — it is an immutable record that can be hidden from view but never truly destroyed.
