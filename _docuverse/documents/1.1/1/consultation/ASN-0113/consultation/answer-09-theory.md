## Question 9 [theory]

> What permanence guarantee, if any, attaches to these reported extents — may a later report of the same document identity ever contradict an earlier one without the document having changed?

## Short answer

There is **no primitive permanence guarantee attached to the reported extents themselves**. The extents are a *derived view* of a document's current V-stream, and V-stream is explicitly ephemeral. However, permanence is *inherited indirectly*: because each version's arrangement is fixed once it exists, a report keyed to a fixed document/version identity is deterministic and cannot contradict an earlier report unless the document has changed.

## What the "reported extents" are

Two FEBE operations report extent:

- **RETRIEVEDOCVSPAN** — "This returns a span determining the origin and extent of the V-stream of document `<doc id>`." (4/68)
- **RETRIEVEDOCVSPANSET** — "This returns a span-set indicating both the number of characters of text and the number of links in document `<doc id>`." (4/68)

Both describe the document's *current* V-stream arrangement — character count and home-link count.

## Why no permanence attaches to the report directly

Nelson's stated permanence guarantees attach to **addresses**, to **Istream content identity**, and to **version persistence** — not to V-stream positions or counts. The V-stream is explicitly mutable:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

So the extent is a property of the *current arrangement*, which editing reshuffles. INSERT/DELETE/REARRANGE change the character count and shift positions — but these are document changes, modifying the current version while "old versions [are] unaffected."

## Why a contradiction cannot arise "without the document having changed"

The stabilizing fact is **version permanence**. Each version's V→I mapping is frozen once created; editing forks a new arrangement rather than mutating an existing one. If "document identity" is pinned to a specific version (FEBE doc ids encode ancestry — CREATENEWVERSION returns a new id whose "id will indicate its ancestry"), then that version's content is fixed, so:

- character count is a deterministic function of fixed content
- the home-link count is stable, since links "are in their permanent order of arrival" (4/31) and adding/removing a home link is itself a document change

Therefore, for a fixed version identity, **a later report cannot contradict an earlier one unless the document changed** — which the question stipulates it has not.

Note the link count covers only home links: RETRIEVEDOCVSPANSET counts "the number of links in document `<doc id>`," i.e. links the document *owns*. In-links from elsewhere are owned at other addresses and are not part of this extent, so third parties linking *into* the document cannot perturb its reported extent.

## One genuine edge case

A document's V-stream "may include bytes from any other document" (transclusion). A **location-fixed (floating-in-time) window** is one where "updates are seen automatically" (2/37). Whether the byte-extent of a *windowing* document tracks a source that grows or shrinks — and whether that would count as "the document having changed" — is not settled in the curated material.

NEED_RAW: 2/36-2/40, 4/67 (COPY/window semantics and whether RETRIEVEDOCVSPANSET resolves through floating transclusions or fixes the span at COPY time).

## Bottom line

The permanence is *inherited, not primitive*. Nelson guarantees permanent addresses, immutable Istream content, and persistent versions; he does **not** state an independent permanence guarantee for RETRIEVEDOCVSPAN/RETRIEVEDOCVSPANSET. Given those underlying guarantees, a report bound to a fixed version identity is stable and non-contradicting — except possibly through floating transclusion windows, which the sources leave unresolved.
