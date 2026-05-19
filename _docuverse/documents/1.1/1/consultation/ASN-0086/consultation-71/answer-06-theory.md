## Question 6 [theory]

> In Nelson's design, is retraction conceived as a withdrawal operation that applies specifically to *link claims* (excluding content and documents), or was retraction intended to operate uniformly over any addressable entity?

# Retraction in Nelson's Design

Retraction was intended to operate **uniformly over any owned addressable entity** — not as something specific to link claims. The same architectural state and the same ownership-based authority apply to bytes, links, and documents alike.

## Architectural Evidence: Uniform "Deleted" State

The strongest evidence is Nelson's own architectural diagram on page 4/9, which lists both as parallel states with **identical descriptions**:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The wording is word-for-word the same. Nelson treats deletion of content and deletion of links as one architectural concept.

## Authority is Ownership-Based, Not Entity-Type-Based

> "Only the owner has a right to withdraw a document or change it." [LM 2/29]

The principle is **ownership**, applied uniformly. Whoever owns the entity may withdraw it. Link ownership is determined by the link's home document (LM 4/12), so the same owner-authority rule governs link retraction as governs byte/document retraction.

## The Asymmetry is Not the Operation but the Constraint

Nelson does distinguish *published* documents — but the distinction is about **constraints on the act**, not about a different operation:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Compare with **privashing**, where withdrawal remains freely available:

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution." (curated source: publishing.md)

So the operation (withdrawal) is uniform; only the *cost* differs depending on what the entity is and who depends on it.

## Peremptory Challenge: A Separate Mechanism, Also Uniform

For anonymous content, removal is effected by third parties:

> "If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

This is "removal of the materials" — undifferentiated by entity type.

## Why the Question Even Arises

The framing in the question — that retraction might apply *specifically to link claims* — likely reflects modern intuition that links are "claims" (an Author link from outside the document is a *claim* about authorship; a supersession link is a *claim* about replacement). Nelson does acknowledge that links can be claims (LM 4/52, footnote: "the Author link can also be used from outside a document to claim that the author is really someone else"), but he never builds a separate retraction mechanism for that case. A claim-link is retracted the same way any other link is: its owner deletes it, and it enters the "not currently addressable, awaiting historical backtrack" state.

## Summary

| Entity | Retraction operation | Constraint |
|---|---|---|
| Bytes (content) | DELETE → "not currently addressable" | Owner authority; persists in Istream and other versions |
| Links (any type, incl. claims) | DELETE → "not currently addressable" | Owner of home document; persists in Istream and other versions |
| Private documents | Withdrawal | Owner authority, no external constraint |
| Published documents | Withdrawal | Owner authority, but "lengthy due process" required |
| Anonymous content | Peremptory challenge | Third-party initiated when owner unavailable |

The operation is uniform. The constraints scale with the social and contractual dependencies others have built upon the entity. Nelson did not carve out link claims as a special case — he treated every addressable entity as subject to the same ownership-based withdrawal, governed by the same historical-backtrack semantics.
