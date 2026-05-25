## Question 4 [theory]

> Must origin information for a span remain accurate forever, even after the original document is edited or withdrawn?

# Origin Information Must Remain Accurate Forever

**Yes—origin information for a span must remain accurate forever.** This is not a feature of the system; it is structural. Origin is encoded in the I-address itself, and the I-address is permanent by design.

## Why Origin Is Structural, Not Metadata

Every byte in Xanadu has a permanent Istream address whose Document field encodes which document originally created it. Origin information cannot be stripped because there is no separate "origin field" to strip—the address *is* the origin claim.

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

## Editing Does Not Affect Origin

Editing operates on Vstream (arrangement), never on Istream (identity). The I-address—and therefore the origin information—is invariant under all editing operations.

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

Even DELETE does not erase origin information. Deleted bytes remain in Istream and may still be referenced by other documents:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

## Withdrawal Cannot Sever Origin

Published documents cannot simply be withdrawn—precisely because others depend on their continued accessibility (links and transclusions point at them). Permanence of access is a *requirement*, not a courtesy:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." (2/43)

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

When supersession occurs, the *origin* doesn't change—a newer version exists, but the original's I-addresses still resolve to the original bytes, and a transclusion made against the original still points to the original.

## Why This Must Be So

Origin permanence is load-bearing for several other guarantees:

- **Attribution** — every transclusion fetches from its home location; severing origin would break the fetch
- **Royalties** — payment flows to the I-address owner; ambiguous origin means broken payment
- **Link survivability** — links attach to I-addresses; if origin became inaccurate, the link's meaning would shift
- **Historical backtrack** — reconstructing past states requires that the bytes' identities have not been rewritten

The whole architecture rests on the principle that **identity does not change**. A document edit changes what is currently visible in that document's Vstream; it does not retroactively edit the origin of any byte. A withdrawal removes nothing from Istream—at most it suppresses current readability, while leaving the I-addresses intact for the links and transclusions that depend on them.

## Summary

Origin information remains accurate forever, by construction:
1. The Document field of every I-address is the origin claim
2. I-addresses are permanent and immutable
3. Editing changes Vstream, never Istream
4. Deletion makes content "not currently addressable" but leaves Istream untouched
5. Withdrawal is contractually constrained precisely to preserve origin chains for dependent links and transclusions

If origin information could become inaccurate, the entire web of transclusion, attribution, royalty, and citation would collapse. The system exists to make that impossible.
