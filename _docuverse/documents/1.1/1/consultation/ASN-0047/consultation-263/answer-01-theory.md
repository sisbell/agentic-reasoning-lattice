## Question 1 [theory]

> Did the design intend a document's links to form a dense, contiguous, arrival-ordered stream (so withdrawal can only truncate from the end), or did it intend tombstoning that leaves interior gaps when a link is withdrawn?

## Answer: Tombstoning with interior gaps — not end-truncation

The design intends link withdrawal to **tombstone**, leaving interior gaps in a permanently arrival-ordered stream. Withdrawal is **not** restricted to truncating from the end. The evidence rests on three architectural commitments that, taken together, force the tombstoning model.

### 1. Link addresses are permanent serial positions assigned at arrival

A document's links occupy the `0.2.N` subspace and are numbered by creation order:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

And critically:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

"Permanent order of arrival" means the address assigned to a link never changes. The Element-field design reinforces this: the link-address digit "designating the link's serial position" — and links "are currently not rearrangeable" (i-space-addresses, 4/30). Unlike bytes (which can be rearranged in Vstream), link serial positions are fixed for the life of the document.

### 2. Withdrawal is deletion-in-place, not removal-and-compaction

Nelson's own enumeration of a document's technical contents lists deleted links as a distinct, preserved state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

A withdrawn link becomes "not currently addressable" but is retained for historical backtrack and may persist in other versions. It is not erased and its slot is not freed for reuse — doing so would violate the permanence guarantee that "any address... remain[s] valid forever" (tumblers, 4/19).

### 3. The two commitments together force interior gaps

These two facts are jointly incompatible with an end-truncation-only model. For withdrawal to only shorten the stream from the end, the system would need either:

- **address reuse / renumbering** — but that contradicts "permanent order of arrival" (4/31) and tumbler permanence; or
- **a rule that only the last-arrived link may be withdrawn** — but no such restriction appears anywhere. The "DELETED LINKS" state (4/9) applies to links generally, and link ownership lets the owner withdraw any of their links (link-deletion).

Since any interior link (say `0.2.5`) can be withdrawn, and withdrawing it neither renumbers `0.2.6 … 0.2.N` nor frees position `5` for reuse, the withdrawal necessarily leaves a gap at position 5. That is tombstoning. The arrival-ordered stream is therefore **sparse-able** — dense at creation, but riddled with holes as withdrawals accumulate — rather than a dense run you can only shorten from the tail.

### Why the design wants it this way

Tombstoning is the same mechanism Nelson applies to deleted *bytes* — "DELETED BYTES (not currently addressable, awaiting historical backtrack functions...)" (delete-semantics, 4/9). Nothing is destroyed; it is made non-current while remaining recoverable and still valid in prior versions. Interior gaps are the price of two higher-priority guarantees: permanent addressing (a citation to link `0.2.5` must never silently resolve to a different link) and historical backtrack (the withdrawn link must remain reconstructible).

---

**One caveat on sourcing:** the verified Nelson quotes above establish (a) permanent arrival-order addressing and (b) deletion-as-tombstone. The specific claim that "deleting link `0.2.5` does not renumber `0.2.6`…`0.2.N`" is a *logical consequence* of those two quotes rather than a verbatim Nelson statement. If you want Nelson stating the non-renumbering of interior link deletions explicitly (rather than by inference), that would be: NEED_RAW: 4/31, 4/9 (pages 198, 176) — to check the surrounding prose for any explicit treatment of interior withdrawal and slot reuse.
