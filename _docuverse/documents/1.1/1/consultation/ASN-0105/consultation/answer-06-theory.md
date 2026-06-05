## Question 6 [theory]

> If the document's arrangement changes after a span is read, what must remain true about the faithfulness of the already-returned result to the arrangement at read time?

## Answer

The already-returned result must remain a **faithful, immutable snapshot of the arrangement as it existed at read time** — subsequent edits to the live document cannot retroactively falsify it. This guarantee holds because of two underlying invariants in Nelson's design: content immutability (Istream) and the preservation of every prior arrangement (historical backtrack / versions).

### Why a later rearrangement cannot make the result a lie

When you read a V-span, you receive bytes via the document's *current* arrangement (Vstream). That arrangement is explicitly ephemeral — it shifts whenever the document is edited:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

So the *mapping* from V-address to content changes after editing. But two things protect the faithfulness of what was already returned:

**1. The content it referenced is permanent (Istream).** A read result is composed of bytes whose identity never changes:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

The Vstream position may move, but the bytes themselves (and their permanent I-addresses) are invariant. The returned result therefore continues to denote exactly the same content it denoted at read time.

**2. The arrangement at read time is itself permanently reconstructable (historical backtrack).** Editing never destroys a prior arrangement; it adds a new one:

> "The file management system we are talking about automatically keeps track of the changes and the pieces, so that when you ask for a given part of a given version at a given time, it comes to your screen." (2/15)

> "This users may also republish documents out of old ones indefinitely, making whatever changes seem appropriate--without damaging the originals." (2/45)

Because the read-time arrangement is never overwritten, the snapshot you hold can always be checked against the version it came from — it never becomes orphaned or unverifiable.

### What "must remain true," stated precisely

The result must continue to correspond *to the arrangement that was current at the instant of the read* — not to the now-mutated live document. The system never silently rewrites an already-delivered result to match later edits; doing so would violate the non-destruction guarantee. The snapshot stays true to read-time reality because:

- the bytes it returned are immutable (Istream), and
- the version/arrangement it was drawn from is preserved (historical backtrack).

If the caller instead wants to know what those positions became *after* the change, that is a separate, explicit request — Nelson frames this for transclusion windows as the user asking, *"What has this passage become?"* (transclusion, time-fixed vs. location-fixed windows, 2/37) — not something that retroactively alters the prior result.

---

**Note on scope:** Nelson does not state a single sentence reading "a RETRIEVEV result must remain faithful to read-time arrangement." The answer above is a synthesis of three explicitly documented invariants — Istream immutability (4/11), historical backtrack (2/15), and non-destruction (2/45). If you want me to confirm whether Chapter 4's protocol section attaches any explicit consistency/snapshot wording to RETRIEVEV itself, that would be: NEED_RAW: 4/61-4/67.
