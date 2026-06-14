## Question 4 [theory]

> Must edits to two unrelated documents be free to take effect independently, or does the design require even unrelated changes to fall into one shared sequence?

# Edits to Unrelated Documents: Independent, Not Serialized

**Verdict: independent.** Edits to two unrelated documents must be free to take effect independently. The design does not require unrelated changes to fall into one shared sequence — and several of its load-bearing decisions exist precisely so that they *cannot* be forced into one.

Here is why that is the intent, working from the mechanisms up.

## 1. Editing operations are document-scoped; their effects never cross a document boundary

The renumbering caused by an edit is confined to the document being edited:

> "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

> "This removes the given span from the given document." (4/66)

An INSERT into document A shifts the V-addresses *in A*. It has no reach into document B. There is no operation whose effect is "renumber the docuverse." If unrelated edits had to share one sequence, an edit anywhere would have to be reconciled against edits everywhere — and nothing in the operation set works that way.

## 2. Addressing is decentralized by design — there is no central sequencer to share

The whole point of tumbler allocation is to let independent actors create without coordinating:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

A single shared sequence over all changes would reintroduce exactly the central authority that forking was invented to abolish. Two owners editing two documents each fork addresses under their own subtree; neither has to wait for, or even know about, the other.

## 3. Time is deliberately kept out of the address

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

Addresses order content by *structural position in the tree*, not by a global temporal order of edits. The system does not stamp unrelated changes onto a common timeline as a condition of their taking effect; ordering-in-time is metadata you may filter on, not a serialization gate.

## 4. The only global ordering is structural — and it is insertion-stable

There *is* one total ordering in Xanadu: the tumbler line (a depth-first walk of the docuverse tree). But it orders **positions, not events**, and inserting into one subtree does not renumber any sibling subtree — that is the same invariant as (1) and (2) above: "the other addresses remain valid" (4/19). So even the system's single shared ordering is undisturbed by edits made elsewhere. It is a map of where things are, not a log of when things happened.

## 5. The distributed layer makes independence mandatory, not merely permitted

Servers assimilate change autonomously and asynchronously:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." (4/72)

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." (4/71)

And the design assumes the network is never whole:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)

This is the decisive point. If unrelated changes had to enter one shared sequence, a partitioned or offline node could never make progress — it could not claim its slot in a global order. Because the docuverse is designed *for* a perpetually-broken network, independent progress on unrelated documents is a requirement of the architecture, not a convenience. Ownership reinforces this at the document level: "Only the owner has a right to withdraw a document or change it." (2/29)

## 6. Where sequences *do* exist, they are strictly *within* a single document

To be precise about the boundary of the claim, Xanadu does impose local ordering disciplines — but they are per-document, not cross-document:

- **Per-document history.** The append-only store files one document's changes "as it were, chronologically" so that "when you ask for a given part of a given version at a given time, it comes to your screen" (2/14, 2/15). This is a single document's braid, reconstructable on demand — not a global log.
- **Per-document link order.** "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31) Order-of-arrival is scoped to the home document's own link space.

Neither of these reaches across to an unrelated document. They are exactly the kind of local sequence the question contrasts against a shared one.

---

## Bottom line on intent

The unit of control, of ownership, of addressing, and of edit-effect is the **document**. Unrelated documents share no edit sequence; their changes take effect independently, and the decentralized addressing plus the always-broken-network assumption mean the system is built so that no global serialization is ever required for an edit to land. A shared sequence over unrelated changes would contradict the coordination-free allocation (forking/baptism) and the partition-tolerant network model at the heart of the design.

**A note on sourcing:** Nelson does not state "unrelated documents need not be serialized" in those words anywhere in the curated material; there is no section explicitly framed as concurrency semantics. The verdict above is a synthesis of his verified statements about document-scoped operations (4/66), decentralized forking (4/17–4/20), time-free addressing (4/18), and the autonomous, broken-tolerant network (4/72, 4/75). Each supporting quotation is verbatim and verified, but the conclusion that ties them together is inference from design principles rather than a single quoted ruling. If you want me to look for a more direct statement, the pages most likely to contain one are the BEBE/network discussion and the back-end concurrency notes — flagging: NEED_RAW: 4/72–4/79 (and 4/58–4/59 for the back end's shared "barrel-roll" search model, the one place Nelson discusses combining multiple users' activity).
