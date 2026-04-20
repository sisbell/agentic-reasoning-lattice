## Question 9 [nelson]

> How does address permanence relate to link integrity — if an address is permanent, does the system guarantee that any link pointing to that address will always connect to the intended content?

## Address Permanence and Link Integrity

The short answer: address permanence is **necessary but not sufficient** for link integrity. Nelson's architecture achieves link integrity through three distinct guarantees working in concert, not through address permanence alone.

---

### The Three Guarantees

**1. Address Permanence (Tumblers)**

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This guarantees that the *location* never changes. Once a tumbler is assigned, it is assigned forever. But a permanent address is just a stable name — it says nothing about what happens to the content at that name.

**2. Content Immutability (I-Space)**

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

I-space content never changes after creation. A byte stored at I-address X will always be that same byte. This is the deeper guarantee: not just that the address persists, but that what lives there is immutable.

**3. Span-Based Attachment (Link Survivability)**

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Links attach to **bytes** (I-space entities), not to **positions** (V-space coordinates). This is the mechanism that converts address permanence and content immutability into actual link integrity.

---

### Why Address Permanence Alone Is Insufficient

Consider what would happen if links pointed to V-space positions instead of I-space content:

- V-space addresses shift on every edit: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]
- A link to "V-position 47" would point to different content after any insertion before position 47
- The *address* might be permanent, but it would no longer designate the *intended content*

Nelson explicitly acknowledges this instability:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

V-space addresses are ephemeral by design. A permanent V-space address would be meaningless because the mapping V→I changes with every edit.

The architectural solution: links point to I-space spans. Since I-space addresses are both permanent (tumbler guarantee) and immutable (append-only guarantee), the link always resolves to the same bytes.

---

### The DELETE Question

This is where the design becomes subtle. "Deleting" content removes it from V-space but NOT from I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So if Alice links to paragraph P in Bob's document, and Bob "deletes" P:
- P disappears from Bob's current V-stream
- P's I-space content remains forever
- Alice's link still points to valid I-space bytes
- The link **survives** — the content exists, it's just no longer in Bob's current arrangement
- Previous versions of Bob's document still show P
- Any other document that transcludes P still shows it

The link connects to the **intended content** because I-space is immutable. Whether that content is currently *visible in the target document* is a separate question from whether the link is *intact*.

---

### Where the Guarantee Has Limits

Nelson's design guarantees that a link will always point to the same bytes. But there are three areas where "connecting to the intended content" has caveats:

**1. Accessibility depends on storage funding.**

Nelson specifies that "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5]. Storage requires ongoing rental. If the owner stops paying, the content may become inaccessible even though its address remains permanently assigned and the link remains structurally valid. The address is permanent; accessibility is not unconditionally guaranteed.

**2. Authenticity is not cryptographically verified.**

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

The system trusts the Storage Vendor franchise to preserve content faithfully. There is no technical mechanism to verify that bytes returned at an address are the original bytes. A compromised vendor could alter content while the address and link remain "valid." Trust is contractual, not mathematical.

**3. Ghost elements are valid link targets.**

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

A link can point to an address where nothing has ever been stored. The address is permanent, the link is structurally valid, but there is no "intended content" — only an intended location. This is by design (it enables forward references and hierarchical queries), but it means address permanence does not guarantee content existence.

---

### Version-Spanning: The Strongest Form of the Guarantee

The most powerful expression of the address-permanence-plus-link-integrity relationship is **version-spanning links**:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

Because links point to I-space content, and because correspondence between versions is computed from shared I-space origin, a link made against version 1 of a document automatically works in version 2, version 3, and any future version — as long as the corresponding bytes survive. The permanent address identifies the content; the I-space architecture makes that identification survive across all versions.

---

### Summary

| Guarantee | What It Ensures | What It Does NOT Ensure |
|-----------|----------------|------------------------|
| **Address permanence** | Location never changes | Content exists or is accessible |
| **I-space immutability** | Content at location never changes | Content is accessible or authentic |
| **Span-based linking** | Link attaches to content, not position | All linked bytes still exist |

The three work together: permanent addresses mean the name is stable; I-space immutability means the content at that name is stable; span-based linking means the connection tracks the content, not the arrangement. The result is that a link will always point to the same bytes it originally designated — provided those bytes remain in I-space (which they do, since I-space is append-only) and the storage vendor is trustworthy (which is contractual, not technical).

Nelson's architecture achieves link integrity not through any single mechanism, but through the **separation of identity from arrangement**. The permanent address lives in I-space where content is immutable. Editing happens in V-space where addresses are ephemeral. Links cross from V-space into I-space, anchoring themselves to permanent content. This is why Nelson insists on the I-space/V-space distinction — without it, address permanence would be meaningless for link integrity.
