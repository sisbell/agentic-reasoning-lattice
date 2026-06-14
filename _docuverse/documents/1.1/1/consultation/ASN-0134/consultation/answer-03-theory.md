## Question 3 [theory]

> When many independent edits are proposed at once, what does the design guarantee about the single order in which they ultimately count — does every observer agree on that one order?

Short answer: **No.** The design does not promise that every observer converges on one globally-agreed total order over concurrent independent edits — and that silence is deliberate, not a gap I forgot to fill. Xanadu *dissolves* the "single commit order" problem rather than solving it with consensus. Where a definite, canonical order does exist, it is always **local** — fixed at one home, by order of arrival — never a synchronous agreement reached among all observers across the docuverse.

Let me be precise about what I intended, because the question carries a presupposition the system rejects.

## The presupposition: that concurrent edits must be merged into one line

The phrase "the single order in which they ultimately count" assumes a model where many writers contend for slots in one serialized history. That is the database/Ministry-of-Truth model, and it is exactly what Xanadu is built *against*. Two architectural choices remove the contention:

**1. Writing is single-owner, so the contention rarely arises.** Within any one document there is exactly one writer:

> "Only the owner has a right to withdraw a document or change it." (2/29)

So "many independent edits proposed at once" to the *same* document is not a state the model admits. The owner's own changes are simply filed as they arrive:

> "...suppose we create an append-only storage system. User makes changes, the changes [flow] into the storage system, filed, as it were, chronologically." (2/14)

That chronology *is* the order. It is definite and the same for every reader — but only because there is one writer and one home stamping it.

**2. When different people want to change the same material, they fork — they do not compete for a slot.** Divergence is the blessed outcome, not a conflict to be resolved into one line:

> "Another user, however, is free to create his or her own alternative version of the document he or she does not own. This, then, becomes a windowing document using the shared materials by including them. We may call this versioning by inclusion." (windowing, 2/45)

And there is no canonical line they are all trying to land on:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." (2/19)

Parallel versions, kept forever, intercomparable by correspondence — *not* one order that some edits win and others lose.

## Where order *is* canonical, it is per-home arrival order

The clearest case is links:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

That order is permanent and identical for everyone — but notice *why*: the links share one home, and that one node stamps arrival order. It is not a global agreement negotiated among observers; it is a single node's local sequencing, which everyone then reads back. Agreement here is a consequence of single-home authorship, not of a consensus protocol.

## You cannot even read a global order off the addresses — by design

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

Tumblers encode *provenance* — position in the forking tree — not *when* something happened. So the permanent address space deliberately carries no global temporal ordering for observers to agree on. Time is a separate, filterable attribute, not a coordinate everyone shares.

## The distributed reality forecloses synchronous global consensus

I never claimed all servers hold one identical global ordering at any instant. The opposite:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse..." (4/72)

> "...whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." (4/72)

The guarantee is that **each server is always internally canonical** and improves its map of elsewhere — *not* that all servers agree on one total order of all edits everywhere. Even where I contemplated many simultaneous users, it was about combining *reads*, not serializing *writes*:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." (4/59)

## Scope note — what I intended vs. what I left to the implementor

The semantic guarantees I made are: (a) per-document, single-owner, append-only chronology; (b) per-home permanent order-of-arrival for links; (c) forking/versioning so divergent edits coexist without merge; (d) nothing is ever lost. A mechanism that takes *truly simultaneous submissions from multiple parties* and serializes them into one agreed global order is **not part of the conceptual specification** — there is no global lock, no total-order broadcast, no notion of "the order in which they count" across the docuverse. That belongs to the back end and its per-server arrival ordering, which is implementation, not intent.

So, to your direct question: the design guarantees a definite, everyone-agrees order only *locally* (one home, by arrival). It guarantees **no** single global order over concurrent independent edits, and every observer is *not* promised to agree on one such order — because the system keeps the branches rather than collapsing them into one.

---

NEED_RAW: 4/59–4/60 and 4/61–4/79 (FEBE/BEBE protocol and concurrent-user handling) — to fully confirm the *absence* of any back-end serialization/total-order mechanism for simultaneous multi-party edits. My answer rests on a synthesis of verified curated passages (single-owner modification, forking, "no basic version," time-not-in-tumbler, "networks are always broken," per-server "continuously valid model"); the protocol pages are where any such mechanism would live if I had specified one, so a reader wanting certainty about the negative claim should check them directly.
