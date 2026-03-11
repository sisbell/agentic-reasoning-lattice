## Question 6 [nelson]

> Can a document ever be destroyed or removed from the docuverse, or does creation imply permanent existence?

# Can a Document Be Destroyed or Removed from the Docuverse?

The short answer: **creation does not guarantee absolutely permanent existence, but the system is designed with an overwhelming bias toward permanence.** Nelson distinguishes several cases with different rules.

---

## Published Documents: Near-Permanent

Published documents are the strongest case for permanence. Nelson is explicit that publication creates obligations:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural — other users will have linked to your document, and those links are *their* property:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

So withdrawal is not absolutely impossible — "lengthy due process" implies a mechanism exists — but the default is permanence. Even superseded documents remain, because links depend on them.

The publication contract reinforces this. From the enforcement model, publishers may withdraw "only with one year's notice and fee" [LM 5/20].

---

## Private Documents: Owner Controls

Private documents are a different matter entirely. The owner has absolute control:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Since private documents are accessible "only by the owner and his or her associates" [LM 2/42], no one else has linked to them or depends on their existence. The owner can withdraw them freely.

---

## Privashed Documents: Withdrawable by Design

Nelson explicitly provides a middle path called "privashing":

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/48]

Privashed content is publicly accessible but can be withdrawn at any time. The tradeoff: no royalties, and anyone who linked to it has no recourse.

---

## Anonymous Content: Removable by Challenge

Anonymous ("John Doe") publications are explicitly vulnerable to removal:

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

This is the one case where content can be removed by someone other than its owner — precisely because the anonymous owner "won't hang around to defend their acts."

---

## I-Space Content: Append-Only, Never Overwritten

At the storage level, the architecture is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even "deletion" in Xanadu does not destroy I-space content:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

So at the I-space level, content is designed to be physically permanent. "Withdrawal" means removing accessibility, not destroying bytes.

---

## The Storage Funding Question

There is an unresolved tension. Nelson requires that "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5], and storage requires ongoing rental fees. He does not specify what happens when payment lapses — whether content becomes inaccessible, enters a grace period, or is preserved by the Author's Fund. This is a gap in the specification.

Vendor failure is handled: "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16]. But individual payment lapse is unaddressed.

---

## Summary

| Document State | Can Be Removed? | By Whom? | Mechanism |
|---|---|---|---|
| **Published** | With great difficulty | Owner only | "Lengthy due process," one year notice + fee |
| **Private** | Yes, freely | Owner | Owner's right to withdraw |
| **Privashed** | Yes, freely | Owner | By design — private with open access |
| **Anonymous (John Doe)** | Yes, if defamatory | Affected party | Peremptory challenge |
| **I-space bytes** | Never destroyed | No one | Append-only by architecture |

Creation implies **strong permanence by default**, especially for published content. But Nelson does not treat permanence as absolute — he provides withdrawal mechanisms for every case, just with varying friction. The key insight is that permanence is a *social obligation* enforced by the link structure (others depend on your content), not a physical impossibility of removal.
