## Question 2 [theory]

> What relationship must the content remaining after a deletion bear to the positions it occupied in the document before the span was removed?

The shell environment isn't returning output, so I'll answer from the verified curated sources.

## Answer

The content remaining after a deletion must keep its **relative order** and re-close into a **contiguous, gap-free Vstream** — the bytes that followed the deleted span slide down to occupy the vacated positions, so the document stays in canonical order. Crucially, this renumbering happens only in **Vstream** (the document's current arrangement); the deleted content's **Istream identity is untouched**.

### What shifts: Vstream positions

Nelson states the renumbering rule explicitly for INSERT, and deletion is its symmetric inverse:

> "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." — 4/66

For DELETEVSPAN the curated text only says:

> "This removes the given span from the given document." — 4/66

By the same Vstream-arithmetic principle, the V-addresses of the characters following a deleted span are *decreased* by the span's length, so the remaining content collapses to fill the gap. The Vstream stays dense (a contiguous sequence with no holes).

### The governing invariant: canonical order

This gap-closing is mandated by the enfilade requirement that every edit leave the file in canonical order:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." — 1/34 (on Barus's contribution)

### What does NOT change: Istream identity

The remaining content's relationship to its *original* positions is therefore one of **arrangement, not identity**. The Vstream positions change, but the permanent Istream addresses of the surviving bytes do not — which is why links stay attached:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." — 4/30

And the deleted bytes themselves persist (they leave the current arrangement but not storage):

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

### Summary

| Aspect | Relationship to pre-deletion positions |
|--------|----------------------------------------|
| Relative order of survivors | Preserved (unchanged) |
| Vstream addresses of survivors after the cut | Shifted down to close the gap (contiguous, canonical order) |
| Istream identity of survivors | Identical — never changes |
| Links on survivors | Remain attached (point to Istream) |

**One caveat to flag:** Nelson gives the V-address renumbering rule verbatim only for INSERT (4/66); the symmetric *decrease* on deletion is the logical inverse plus the canonical-order mandate (1/34), not a direct verbatim DELETE quote. If you want Nelson's exact wording on deletion renumbering specifically: NEED_RAW: 4/66.
