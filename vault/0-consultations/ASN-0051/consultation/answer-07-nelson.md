## Question 7 [nelson]

> What can a link holder rely on about the identity of the endpoints — must the system guarantee that the content at each end is exactly what was there when the link was created, or only that the addresses remain valid?

## What a Link Holder Can Rely On: Content Identity at Endpoints

The short answer: **both**. The system guarantees that addresses remain valid AND that the content at those addresses is exactly what was there when the link was created. But there are important nuances about partial survival and the absence of cryptographic proof.

---

### The Core Guarantee: Istream Immutability

Links point to **Istream addresses** — the permanent identity space where content lives forever. Istream is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content at an Istream address **never changes**. This is not a policy — it is the architectural foundation. There is no operation in the FEBE protocol that overwrites Istream content. INSERT appends new bytes to Istream. DELETE removes content from Vstream (the current arrangement) but leaves Istream untouched:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Therefore, the bytes referenced by a link's endsets at creation time are **guaranteed to be the same bytes** at any future time. The content is immutable at the address level.

---

### Links Attach to Bytes, Not Positions

Nelson is emphatic that links are "straps between bytes," not pointers to positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

Because the link is attached to the bytes themselves (via their permanent I-addresses), and those bytes never change, the link holder can rely on the content identity at each endpoint being exactly what it was at creation.

---

### The Partial Survival Nuance

While the **bytes** never change, the **span** a link covers may shrink. If some bytes in an endset are removed from the current Vstream arrangement, the link survives on whatever bytes remain:

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." [LM 4/42]

The visual annotation on page 4/43 makes the condition explicit:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**"

So a link holder can rely on this: every byte the link still touches is **identical** to what was there at creation. But the link may now touch **fewer** bytes than it originally did. The surviving content is exact; the coverage may have narrowed.

---

### What About Complete Deletion?

If ALL bytes at one end are removed from the current Vstream, the link loses practical navigability in that version. However, the I-addresses remain valid — those bytes still exist in Istream. The delete-semantics design intent confirms:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The link's endset addresses don't become invalid. The content is still there in Istream. But the link may not be discoverable through normal Vstream navigation in the current version. Previous versions and other documents that transclude the same content still provide paths to those bytes.

---

### No Cryptographic Verification

The guarantee is **architectural and contractual**, not cryptographic. Nelson explicitly acknowledges the absence of technical verification:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." [LM 5/18]

The system relies on the Storage Vendor franchise to faithfully preserve content. If a vendor is compromised or dishonest, there is no cryptographic backstop to prove content has been tampered with. The architectural design (append-only Istream) makes tampering structurally unnecessary, but does not make it technically detectable.

---

### Summary

| Aspect | Guarantee |
|--------|-----------|
| **Address validity** | Permanent. Tumbler addresses never expire or get reassigned. |
| **Content identity** | Exact. Istream is immutable; bytes at an I-address never change. |
| **Span coverage** | May shrink. If some bytes leave the Vstream, the link survives on the remainder. |
| **Vstream context** | Not guaranteed. The document arrangement around the linked bytes may change. |
| **Cryptographic proof** | None. Trust is contractual (Storage Vendor franchise), not mathematical. |

The link holder can rely on the strongest possible content guarantee short of cryptographic verification: the system's fundamental architecture makes it impossible to change content at an I-address through any defined operation. The bytes the link was created against are the bytes it will always find. What may change is how many of those bytes remain visible in the current version of the document — but those that remain are exact.
