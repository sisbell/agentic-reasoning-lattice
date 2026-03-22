## Question 5 [nelson]

> If a link references content belonging to a document the link creator does not own, what sharing or permission guarantees must the system maintain for that link?

## Link Permission Guarantees for Cross-Owner References

The answer depends entirely on whether the referenced content is **published** or **private**.

---

### Published Content: No Permission Required

When a link's endsets reference published content owned by someone else, the system requires **zero permission** from the content owner. This is not a gap — it is the explicit design:

> "Accessibility and free linking make a two-sided coin. On the one hand, each user is free to link to anything privately or publicly. By the same token, each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract." [LM 2/43]

The publication contract pre-grants all linking rights:

> "Since the copyright holder gets an automatic royalty, anything may be quoted without further permission. That is, permission has already been granted: for part of the publication contract is the provision, 'I agree that anyone may link and window to my document.'" [LM 2/45]

The content owner **cannot prevent, remove, or interfere with** incoming links. The link lives at the creator's address, not the target's:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

---

### The System's Obligation: Keep the Target Accessible

The critical guarantee the system must maintain is that **published content remains available** — precisely because others' links depend on it:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This creates a binding chain:
1. Alice publishes document D
2. Bob creates a link from his document to spans in D
3. Bob's link is Bob's property (at Bob's address)
4. Alice cannot withdraw D because Bob's link depends on it
5. Alice cannot delete Bob's link because it lives in Bob's document

If Alice publishes a superseding version, the old version must remain:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

---

### Link Survivability: The Structural Guarantee

The system must maintain that links survive editing of the target content:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

Because links point to Istream addresses (permanent content identity) rather than Vstream positions (current arrangement), the content owner's edits cannot break the link. The link survives "deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43].

---

### Private Content: Restricted Access

For private documents, the situation inverts. A private document "may be read and linked-to only by the owner and his or her associates" [LM 2/42]. Linking to private content requires being an owner or designee — no pre-granted permission exists.

---

### Compensation in Lieu of Control

Nelson explicitly separates **compensation** from **control**. The content owner gives up control over who links to their work but never gives up compensation:

> "In our planned service, there is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." [LM 2/43]

This is the core bargain: the publication contract trades control for guaranteed automatic payment. Permission friction disappears because compensation is structural.

---

### Summary of Guarantees

| Guarantee | Who bears it | Source |
|-----------|-------------|--------|
| **Anyone may link to published content** | System + publication contract | 2/43 |
| **Content owner cannot prevent incoming links** | Publication contract | 2/43 |
| **Published content must remain accessible** | Content owner (contractual) | 2/43 |
| **Links survive target editing** | System (structural, via I-addresses) | 4/42 |
| **Link creator owns the link** | System (home document = ownership) | 4/12 |
| **Content owner receives automatic royalty** | System (per-byte, automatic) | 2/43 |
| **Old versions persist after supersession** | Content owner (contractual) | 2/43 |

The design philosophy is that **no sharing or permission negotiation is needed** — the act of publication is itself the grant of permission, and the royalty mechanism is itself the compensation. The system's obligation is to keep the content accessible and the links attached.
