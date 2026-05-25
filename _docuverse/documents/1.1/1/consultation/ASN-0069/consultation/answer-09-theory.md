## Question 9 [theory]

> What must happen to the shared content if the source document is later withdrawn — must the fork retain access?

# Withdrawal and Forks: What Must Persist

The short answer: **published content must remain accessible to forks; withdrawal is constrained precisely because others depend on it.** This is not a technical accident but a deliberate contractual commitment.

## The Core Commitment

For published documents, withdrawal is restricted *because* of the dependencies forks and inclusions create:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The "due process" requirement exists to protect the web of inclusions and links that forks represent.

## Supersession, Not Erasure

Even when an author publishes corrections, the prior version must persist:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

## The Architectural Guarantee

Even setting aside the contract, the transclusion architecture itself preserves fork access. Deletion from one document does not remove content from documents that included it:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is because transclusion is reference, not copy — forks point to permanent Istream addresses. The original document's Vstream arrangement can change, but the Istream content persists, and the fork's references continue to resolve.

## The Non-Damage Principle

The whole point of inclusion-based forking is that originals survive forking, and forks survive modifications to originals:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate-- without damaging the originals. This is done by inclusion links." [LM 2/45]

> "This means a whole new pluralistic publishing form. If anything which is already published can be included in anything newly published, any new viewpoint can be freely presented by an easily-made annotated collage. (The old viewpoint is still present too—you can always say, 'Show me what this originally was.')" [LM 2/45]

## The Exception: Privashing

I deliberately created an escape hatch for authors who want universal access but reserve the right to withdraw — but they pay a price: forks have no protection.

> "An author who wishes to render his work universally available, but wishes also to retain the right to withdraw it at any time, has a simple means for so doing. The author simply designates his or her document as a private document with unrestricted distribution."

For privashed content, anyone who linked or forked has no recourse if the owner withdraws. The privashing author also receives no royalty — which is the incentive to publish properly instead.

## What This Means in Practice

1. **For published content + fork**: The fork must retain access. The original cannot be withdrawn without lengthy due process precisely because the fork (and other inclusions/links) depend on it. The Istream content persists; the fork's references continue resolving.

2. **For privashed content + fork**: The fork has no guarantee. If the author withdraws, the fork loses access. This is the bargain — the author traded royalties for the right to withdraw.

3. **The principle**: Forking creates a dependency. The system honors that dependency through both architecture (Istream permanence, transclusion-by-reference) and contract (publication is a binding commitment to permanence).

Note: Nelson does not explicitly address what happens if "lengthy due process" succeeds and a published document IS withdrawn — whether forks would then lose access or whether the Istream content survives the legal withdrawal for the sake of dependent works. NEED_RAW: 2/43-2/45 might clarify whether withdrawal-via-due-process preserves Istream for dependents.
