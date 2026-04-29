# Revision Consultation — ASN-0026

**Review:** review-2.md
**Date:** 2026-03-08 00:25

## Summary

7 REVISE items analyzed: 6 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 2: Σ.D has no structural properties

**Category:** NELSON
**Reason:** Part (a) — stating Σ.V(d) defined iff d ∈ Σ.D — is an internal formalization fix. But part (b) — whether Σ.D is monotonic or can shrink — is a design intent question. I-space is monotonic (P1); whether the document set shares this permanence property requires Nelson's architectural intent.

**Nelson question:** Is the set of documents permanent (monotonically growing, like I-space), or can documents be destroyed — and if so, what happens to their tumbler addresses and version history?

**Nelson's Answer:**

## Documents: Permanent or Destructible?

**Short answer:** Published documents are effectively permanent — the set is monotonically growing. Private documents can be withdrawn by their owner. In neither case are tumbler addresses ever reused or I-space content destroyed.

---

### Published Documents: Permanent by Design

Nelson is explicit that publication creates a permanence obligation:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Even when an author publishes a corrected version, the old version must survive:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

The reason is structural: other users' links depend on the document's continued existence. Those links are *their property* (at their addresses, under their control). Withdrawing a published document would destroy other people's property.

### Private Documents: Withdrawable

The owner has full authority over private documents:

> "Every document has an owner, the person who created and stored it... Only the owner has a right to withdraw a document or change it." [LM 2/29]

Nelson also describes "privashing" — publishing with a withdrawal escape hatch:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution."

The tradeoff: privashed documents earn no royalties, and anyone who linked to them has no recourse if the author withdraws.

### Peremptory Challenge: Forced Removal

One exception to permanence: anonymous defamatory content can be removed by the affected individual:

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

This applies only to anonymous ("John Doe") publications where the author won't defend. For identified publishers, peremptory challenge "no longer holds water" — removal requires negotiation or court order.

---

### What Happens to Tumbler Addresses?

Tumbler addresses are permanent regardless of document state:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Crucially, documents are *ghost elements* — they are not stored objects but conceptual positions in tumbler-space:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents--bytes and links." [LM 4/23]

A document IS its contents (bytes and links at I-space addresses). The tumbler address is a permanent coordinate in the docuverse. Even if a document is withdrawn, its address is never reassigned — the position remains occupied (or conceptually reserved) on the tumbler line forever.

### What Happens to I-Space Content?

I-space is append-only. Content is never destroyed:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

DELETE operates only on V-space (the current arrangement), not I-space (permanent storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This means "withdrawal" most likely means making the document inaccessible through normal retrieval — not destroying its I-space content. The bytes remain; the V-space view is removed.

### What Happens to Version History?

Version history is inherently permanent because:
1. Each version is a V-space arrangement over I-space content
2. I-space content is append-only
3. Previous versions "may remain included in other versions" [LM 4/9]

Nelson guarantees historical backtrack:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." [LM 2/15]

---

### Gaps in the Specification

Nelson does not specify:

1. **What "lengthy due process" entails** for withdrawing a published document — he establishes that it's hard but doesn't detail the mechanism
2. **What happens when storage rental lapses** — the funding model requires ongoing payment, but the consequences of non-payment are unspecified
3. **Whether "removal" via peremptory challenge destroys I-space content** or merely removes V-space accessibility — given the append-only model, V-space removal is the more consistent reading
4. **Whether withdrawn documents' I-space content remains accessible** to other documents that transclude it — the structural answer should be yes (those transclusions point to I-space, not to the withdrawn document's V-space)

### Summary

| Document State | Can Be Destroyed? | Tumbler Address | I-Space Content | Version History |
|---------------|-------------------|-----------------|-----------------|-----------------|
| **Published** | No (except "lengthy due process") | Permanent | Permanent | Permanent |
| **Private** | Yes (owner can withdraw) | Permanent (never reused) | Likely permanent (append-only) | Likely preserved |
| **Privashed** | Yes (owner can withdraw at will) | Permanent (never reused) | Likely permanent | Likely preserved |
| **Anonymous + challenged** | Yes (peremptory challenge) | Permanent (never reused) | Unspecified | Unspecified |

The docuverse is designed to grow forever. The set of published documents is monotonically increasing by intention and by structural necessity — because the links others have made to them are *their* property, and permanence of content is the foundation that makes permanent addresses meaningful.
