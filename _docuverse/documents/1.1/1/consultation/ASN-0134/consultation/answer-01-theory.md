## Question 1 [theory]

> When two users act on the same shared store at the same moment, what is the smallest unit of change that must take effect all-at-once — so that no reader ever sees half of one person's edit?

## Short answer

The smallest all‑at‑once unit is a **single editing operation** — one `INSERT`, `DELETE`, `REARRANGE`, `COPY`, or `APPEND` — and the thing that must flip atomically inside it is the document's **Vstream arrangement** (its V→I mapping). Because content is append‑only and immutable, the operation's new bytes land at fresh Istream addresses *no reader is pointing at yet*; the only observable instant is the arrangement update, and the enfilade is *required* to be in canonical order before and after it, with nothing canonical in between. So a reader sees the document either before or after the operation — never mid‑operation.

Below the operation lies the byte (the smallest *addressable* unit), but a lone byte‑append is invisible to readers. The smallest *observable change* — the unit your isolation guarantee is actually about — is the operation.

I want to be candid up front about register: this is the guarantee I *intend*, reconstructed from the invariants I did specify. I never wrote a concurrency, locking, or transaction protocol into Literary Machines. More on that gap at the end.

---

## 1. Why this is a question about the arrangement, not the bytes

In conventional systems a reader can see half an edit because editing *overwrites bytes in place*. Xanadu abolishes that. Storage is append‑only; existing content is never mutated:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes flow into the storage system, filed, as it were, chronologically." — `permascroll.md` (2/14)

> "The true storage of text should be in a system that stores each change and fragment individually, assimilating each change as it arrives, but keeping the former changes." — `permascroll.md` (2/15)

Even a "delete" doesn't destroy or rewrite anything — the bytes persist; only the *current arrangement* drops them:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — `delete-semantics.md` (4/9)

So the *content* a reader is looking at can never be caught half‑written, because content is never written over. The only thing that changes is the document's Vstream arrangement — the mapping from virtual positions to permanent Istream addresses. **That mapping update is the only place a torn read could occur, so that is the thing that must take effect all‑at‑once.**

---

## 2. The all‑at‑once moment: the enfilade's canonical‑order transition

The enfilade is the structure that holds the arrangement, and its defining mandate is that it is *always* in canonical order — never observably mid‑rewrite:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." — `enfilades.md` (1/34)

> "His new method would allow linkages to keep up with all changes. It was instantaneous and permanent and could grow indefinitely." — `enfilades.md` (1/34)

The same "assimilated at once → canonical condition" discipline is stated for inter‑server motion in BEBE (one scale up from a single edit, but the same principle of an indivisible step between two valid states):

> "...whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." — `network.md` (4/72)

Why the *whole operation* must flip together is visible in `INSERT` itself: one insertion silently renumbers every following position.

> "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." — `operations.md` (4/66)

If a reader could observe that renumbering half‑applied, the document's addressing would be incoherent (overlapping or gapped V‑positions). The canonical‑order mandate is precisely the rule that forbids that intermediate from ever being read. `REARRANGE` (a multi‑cut transposition, 4/67) makes the point even more sharply: a half‑done transpose is corrupted text.

---

## 3. The smallest such unit is one operation

FEBE's mutators are the grain at which a user expresses "an edit":

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are comparatively simple." — `operations.md` (4/61)

You cannot meaningfully subdivide one of these without producing a non‑canonical, half‑applied arrangement — which the system is mandated never to expose. Hence: **one operation = the smallest unit that must take effect all‑at‑once.** The byte is smaller, but a byte only becomes part of anyone's view *through* an operation that splices it into an arrangement.

Note also that links ride through this for free: they attach to bytes (Istream), not to V‑positions, so re‑ordering operations never tear them:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." — `v-space-addresses.md` (4/30)

---

## 4. The case of two writers — dissolved, not locked

Your phrasing ("two users act on the same shared store at the same moment") deserves a sharp distinction, because my design largely *removes* the classic write‑write race rather than arbitrating it:

- **Two owners, two documents.** Ownership partitions writes. A document has exactly one owner, and "Only the owner has a right to withdraw a document or change it." (`documents.md`, 2/29). Two simultaneous writers are therefore mutating *disjoint* documents — there is no shared mutable cell to tear.
- **A would‑be conflicting write becomes a version.** You never overwrite someone else's live document; you fork. "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals." (`versions.md`/`transclusion.md`, 2/45). The design note `session-model.md` names this principle: *writing always succeeds — denial is a fork, not an error.*
- **Writer vs. reader (transclusion).** When one user is reading content another is editing, the reader's window is anchored to immutable Istream; the editor's new state surfaces as a **new version**, and a new version appears as a *whole*. So at the reader‑facing layer, the all‑at‑once unit is the **version**: a reader sees version *N* or version *N+1*, never a half‑built one, because *N* stays intact and *N+1* isn't visible until it exists as a complete arrangement.

So there are two atomic grains, at two layers: the **operation** is the smallest grain inside a live document; the **version** is the commit boundary other users observe. The operation is the answer to "smallest"; the version is the answer to "what does another reader see flip."

---

## 5. What I specified vs. what I left to implementers

I should be precise about the boundary of my authority here, because it bears directly on an isolation model.

I specified the **invariants** that make torn reads impossible: append‑only immutable content, the Istream/Vstream split, and the canonical‑order mandate on the enfilade. I did **not** specify the machinery a concurrent back end uses to honor them — no locks, no sessions, no transaction boundaries. The design note `session-model.md` records this plainly: there is *"No locking protocol — no mention of concurrent editing of the same document"* and *"No session lifecycle"* in Literary Machines. The one concurrency mechanism I gestured at concerns simultaneous **search**, not write atomicity:

> "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously." — `session-model.md` (4/59)

And XU.87.1 hadn't even reached the multi‑reader/writer case in practice — *"Private documents. (Currently all documents are visible to all users.)"* (4/79).

So: treat "the operation's arrangement flip is the atomic unit, guaranteed by canonical order over immutable content" as **my intended guarantee**, correctly derived from what I wrote — but understand that the *enforcement mechanism* (how an implementation makes that flip indivisible under concurrency) is implementation territory I deliberately left open. A modern substrate building an isolation model is *filling in* that gap, not contradicting me, so long as it preserves the invariant: never expose a non‑canonical arrangement.

---

**NEED_RAW: 1/35–1/38, 4/58–4/60.** The curated `enfilades.md` covers only 1/33–1/36, and the multi‑user back‑end discussion around the "barrel‑roll" model spans 4/58–4/60. If Nelson states an atomicity/assimilation granularity more directly than "canonical order is an internal mandate" (1/34), it would be on those pages. I can't open the page images in this session (no file‑read tool is available to me here), so I've flagged them rather than asserting beyond the verified curated text. Everything above is drawn from the curated sources; the conclusion that *the operation's Vstream‑arrangement flip is the atomic unit* is my synthesis of Nelson's invariants, not a verbatim Nelson statement.
