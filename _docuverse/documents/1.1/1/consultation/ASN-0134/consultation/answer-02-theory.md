## Question 2 [theory]

> If one user is reading content while another is writing it, must the reader see only changes that have fully landed, or may the reader witness a change still in progress?

## Direct answer

Literary Machines does not impose either requirement. Nelson never specifies read‑isolation or atomicity semantics for simultaneous reading and writing — there is no commit barrier, no locking protocol, and no statement about whether a read may observe an edit mid‑flight. The curated extraction is explicit on this point: "Nelson does not specify a session model... **No locking protocol** -- no mention of concurrent editing of the same document" (`session-model.md`). So the honest answer is that the book *neither requires* the reader to see only fully‑landed changes *nor forbids* witnessing one in progress. This is an undesigned layer.

But the architecture is not neutral about it. It settles the question at two levels and leaves a real gap at a third. The levels have to be separated, because "a change" means different things at each.

## 1. At the byte/content level, a torn read is impossible

Content lives in Istream and is immutable once written. Storage is append‑only — "the changes... into the storage system, filed, as it were, chronologically" (2/14, `storage.md`) — and content is fetched from its permanent home: "Native bytes of a document are those actually stored under its control and found directly in storage under its control" (4/11, `i-space-v-space.md`). A byte either exists at its I‑address or it does not; it is never rewritten in place.

Consequence: a reader can never witness a *half‑formed byte*. A change‑in‑progress cannot manifest as corrupted or partial content. Whatever "witnessing a change in progress" could mean, it cannot mean a torn value.

## 2. In the normal editing path, reader and writer are not touching the same object

The document is the V→I mapping; **edits change the mapping, not the Istream content** (`v-space-addresses.md`, grounded in 4/30, 4/11). And editing is structurally a forking act, not destruction: "A document is really an evolving ONGOING BRAID" (2/14, `versions.md`), where superseding leaves the prior arrangement intact — "the author may readily publish a superseding document, but the former version must remain on the network" (2/43, `links.md`).

So in the common concurrent case the writer does not mutate what the reader is reading; the writer produces a *new arrangement* over the same immutable Istream while the reader's version persists. Two further facts reinforce this:

- The writer is the **owner**, and a not‑yet‑published document is private — "accessible only to you and your designees" (`session-model.md`, 2/42). The reader can only be reading concurrently if the document is published, i.e. a stable version.
- "Writing always succeeds": "denial is a fork. The user gets a version" (`session-model.md`), grounded in "users may create new published documents out of old ones indefinitely... without damaging the originals" (2/45).

Across version boundaries, then, the model behaves like snapshot isolation: reader on version N, writer forks N+1, N is unaffected. The reader sees only landed state because the writer's work‑in‑progress is, by construction, a *different* arrangement.

## 3. The genuine gap: a multi‑step edit on one shared, live arrangement

The unanswered case is editing *within a single version* — INSERT/DELETE/REARRANGE mutate "current version" in place (the mapping changes). Whether a reader pouncing during a REARRANGE can observe the state after the cut but before the paste, or an INSERT's text before its paired DELETE, is **undefined** in Literary Machines. Nelson gives no isolation level for operations on one shared mutable Vstream.

What he does give is adjacent but not on point:
- **Part‑pounce** describes reads as assembled on demand — "THE PART YOU WANT COMES WHEN YOU ASK FOR IT" (2/16, `storage.md`) — which says the read reflects *whatever the mapping is at the instant of the pounce*, but says nothing about whether that instant can fall inside another user's operation.
- The **barrel‑roll shared search model** is the only place he addresses many users at once — "the back end [will] combine the search models of different users to create a barrel‑roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously" (4/59, `session-model.md`) — but this is about *search* throughput, not edit isolation.
- The implementation he describes had not reached this problem at all: "Private documents. (Currently all documents are visible to all users.)" (4/79, `session-model.md`).

Note the asymmetry: the append‑only chronological substrate makes a clean snapshot read *trivially implementable* (pin the read to a chronological point and the operation either lands before or after it). The substrate **enables** "see only landed changes." Nelson simply never **mandates** it.

## Bottom line

- Must the reader see only fully‑landed changes? **Not as a stated guarantee.** Nelson never wrote that rule.
- May the reader witness a change in progress? **At the content level, no** (Istream immutability forbids torn bytes). **At the operation level on a single live arrangement, undefined** — the spec is silent.
- The architecture's center of gravity is toward isolation‑by‑forking: the canonical edit produces a new version while the old one persists, so the reader of a published version is structurally insulated from the writer's in‑progress work. The dirty‑read window survives only for fine‑grained simultaneous mutation of one shared arrangement, which Nelson left to the implementor (this is the same undesigned session/locking layer that Gregory's BERT mechanism, *not* in Literary Machines, was built to fill).

For specification purposes this is best recorded as a **real, correctly‑open gap**: read‑isolation level is an implementation choice the substrate constrains (no torn content) but does not fix (no operation atomicity guarantee). It is not derivable from Nelson's text either way.

---

NEED_RAW: 4/74–4/79 (connection/network mechanics) and 5/14–5/18 (Storage Vendor duties) — only if you want primary‑source confirmation that *no* atomicity/isolation statement exists anywhere in the connection or vendor‑contract material. The curated `session-model.md` already extracts and concludes "no locking protocol / no concurrent‑editing semantics," so I'm treating the gap as established; the raw check would be belt‑and‑suspenders, not a correction.
