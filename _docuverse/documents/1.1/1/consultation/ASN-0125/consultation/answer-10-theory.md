## Question 10 [theory]

> If editing a link never mutates anything but only adds, what guarantee distinguishes a system that preserves permanence under editing from one that merely simulates editing by deletion and recreation?

# The guarantee is correspondence, not "append-only"

Your question contains a trap, and it is the right trap to set. **"Only adds" does not separate the two systems, because deletion-and-recreation also only adds.** When you "edit by deletion and recreation," you append a tombstone for the old link and append a fresh link — nothing is overwritten in place. In my own design, deletion is *logical*: a deleted link enters the state

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

That is an addition, not a mutation. So by the letter of *never mutates, only adds*, both systems qualify. Append-only storage is **necessary but not sufficient** for permanence. The distinguishing guarantee must be something the simulation cannot counterfeit.

That guarantee is **identity continuity, made visible as correspondence — operationally, reach-through.** A system preserves permanence under editing when everything attached to the old state continues to resolve *to the edited object*: every prior link, transclusion, and metalink reaches through to the new state. A delete-and-recreate retains the old state too (as a tombstone) but never *binds* it to its successor — so the old references are orphaned, and the successor is born disconnected.

## Why the two look identical on disk but are not

Both operations leave `{old object, new object}` in storage. The difference is **relational, not material** — and that is exactly why you cannot detect it by inspecting bytes.

Links are addressed by creation order:

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)

So a recreated link does not inherit the old link's address — it gets the *next* serial. The old address becomes a deleted-link tombstone (4/9); the new link sits at a different address entirely. Now recall that a link is itself an addressable object, so other links can point at it:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

A metalink that pointed at the old link's address — a commentary, a dispute, an "the author is really someone else" claim (4/52) — now points at dead matter. The recreation reproduced the link's *content* while severing everything that pointed at it.

## What permanence preserves that simulation cannot

Genuine permanence rests on **shared Istream identity**, from which correspondence is *computed* rather than recorded — it cannot be forged by a recreation, because a freshly made link has fresh I-addresses with no shared origin. Three of my guarantees all reduce to this one fact:

- **Survivability.** Links bind to bytes, not positions: *"it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived."* (4/42)
- **Reach-through on supersession.** *"the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version."* (2/43)
- **Refractive following.** *"Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions."* (2/26)

Each presupposes that the successor and the predecessor *share identity*. Delete-and-recreate breaks that share, so none of these three can fire.

## The operational test

You cannot tell the two systems apart by examining content. You tell them apart by asking one question: **does an incoming reference survive the edit?**

Point a metalink at the link. Perform the edit. Follow the metalink.
- **Permanence:** it resolves to the new state.
- **Simulation:** it dangles at the tombstone.

That is the falsifiable signature. The thing being tested is *identity*, and identity is precisely what deletion-and-recreation cannot carry across — even though it copies everything else.

## Why this is the right place to draw the line

Permanence is a property of **identity, not of storage**. Append-only storage conserves *bytes*; the permanence guarantee conserves *connections*. A recreated link is a "frozen and dead" copy in miniature:

> "Any detached copy someone keeps is frozen and dead, lacking access to the new linkage." (2/48)

It has the text and lacks the living web. And the web is the whole point — the system exists to preserve the interconnections that *are* literature, not merely the content. Delete-and-recreate is the exact failure mode Xanadu was built to prevent: it conserves text while destroying literature.

## Intent versus implementation — one caveat

Note that I deliberately gave Xanadu *no* edit-link mutation primitive. You `MAKELINK` — you add. So Xanadu literally "edits by adding," which means Xanadu itself can be driven into the simulation failure if a front end deletes-then-makes. The intended path for change is **supersession** (keep the old, bind it to the new so references reach through), not deletion. So the guarantee is *not* "we only add" — that is merely the mechanism, and it is the mechanism both honest editing and simulated editing share. The guarantee is the promise on top of it: **succession preserves correspondence, so every reference reaches through to the edited object.** Retention without that binding is a tombstone; retention *with* it is permanence.

---

*All quotations above appear verbatim in the verified curated sources; no raw-page consultation was required for this answer.*
