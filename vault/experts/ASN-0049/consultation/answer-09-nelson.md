## Question 9 [nelson]

> Does the permanence guarantee apply equally to shared content and to content that exists in only one document, or can shared content ever become unavailable?

## Permanence and Shared Content

The short answer: the permanence guarantee applies to **all published content equally**, but shared content actually has **stronger practical protection** because others' property depends on it.

### The Blanket Rule

Nelson states the permanence guarantee as a universal principle applying to all published content:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

This applies regardless of whether anyone has linked to or transcluded the content. Publication itself is the trigger.

### Shared Content Has Stronger Protection

While the rule covers all published content, Nelson's **justification** for it is precisely that sharing creates dependency. When others link to or transclude your content, their property depends on yours:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Transclusion makes this dependency structural. Non-native bytes are "obtained by front-end or back-end requests to their home locations" [LM 4/11]. If document A transcludes from document B, A's content literally requires B's I-space to be accessible. Withdrawing B would not merely break a navigational convenience — it would destroy part of A's content.

### The Economic Tension

There is one area where Nelson's design creates an unresolved vulnerability for all content, shared or not. Storage requires **ongoing payment**:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Nelson specifies ongoing storage rental paid by the owner. He does **not** specify what happens when that payment lapses. This creates a gap: the permanence guarantee says you cannot *voluntarily withdraw* published content, but what if you simply stop paying?

For shared content, this gap is arguably more dangerous than for unshared content, because a lapse in one owner's payment could cascade — breaking transclusions in many other documents simultaneously.

### The Hierarchy of Protection

Reading across the curated sources, there is an implicit hierarchy:

| Content State | Permanence | Basis |
|---|---|---|
| Published + actively shared (linked/transcluded) | Strongest | Contractual + others' property depends on it |
| Published + not yet shared | Strong | Publication contract prevents withdrawal |
| "Privashed" (private with unrestricted access) | Weak | Owner can withdraw at any time; "no recourse" for linkers |
| Private | None (to others) | Owner has full control |

Nelson explicitly designed "privashing" as an escape valve for those unwilling to accept the permanence obligation:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." [LM 2/48]

The tradeoff is explicit: no royalties, and anyone who linked to privashed content has no recourse.

### I-Space vs. Accessibility

It is worth distinguishing two senses of "available":

1. **I-space existence**: Content in I-space is permanent by architecture. DELETE removes from V-space only — "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9]. Even "deleted" content remains in I-space and can be reached through other versions or historical backtrack. This applies equally to all content.

2. **Network accessibility**: Whether content can actually be retrieved across the network depends on the storage vendor remaining operational and the owner maintaining storage rental. Nelson provides some protection through vendor contracts — "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16] — and through distributed backup. But the economic sustainability question remains unresolved.

### Conclusion

Nelson designed the system so that **shared content can never become unavailable through the owner's voluntary action** — the publication contract forbids it, precisely because others depend on it. The permanence guarantee applies to all published content, but sharing creates the moral and practical foundation for that guarantee.

The one scenario Nelson does not fully address is **involuntary unavailability** — what happens when an owner cannot or does not pay storage costs. In this scenario, shared content is more vulnerable than unshared content in one sense (more downstream damage) but also more likely to be preserved in another (greater incentive for the network to maintain it, and its bytes may exist in backup copies across multiple vendors).
