Now I have the complete specification. Here is the full answer:

---

## REARRANGE: Transposition of Two Regions

### What It Does

REARRANGE is a **swap of exactly two regions** within a document's V-space. It is not a general permutation — it transposes precisely two designated regions, swapping their positions in the virtual byte stream.

From Nelson's specification [LM 4/66–4/67]:

> "The \<cut set\> consists of three or four v-addresses within the specified document. Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3, assuming cut 1 < cut 2 < cut 3. With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4, here assuming cut 1 < cut 2 and cut 3 < cut 4."

### Two Modes

**Three-cut mode** — the two regions are *contiguous* (they share cut 2 as boundary):

```
Before:  ...[ region A: cut1..cut2 ][ region B: cut2..cut3 ]...
After:   ...[ region B ][ region A ]...
```

**Four-cut mode** — the two regions may be *non-contiguous* (separated by intervening content):

```
Before:  ...[ region A: cut1..cut2 ]...gap...[ region B: cut3..cut4 ]...
After:   ...[ region B ]...gap...[ region A ]...
```

### What It Preserves

**Same length, same content, different order.** REARRANGE is a pure V-space operation. It changes the arrangement of content in the virtual byte stream but:

- **I-space is untouched** — no content is created or destroyed. The curated sources confirm REARRANGE is a "Pure V-space operation" (from the I-space/V-space concept mapping).
- **Document length is preserved** — since no bytes are added or removed, the V-stream has the same total length afterward.
- **All content survives** — the same bytes exist, just in a different V-space arrangement.
- **Links survive** — as Nelson states: "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them" [LM 4/30].

### What It Is NOT

It is **not a general permutation**. The command accepts exactly 3 or 4 cut points (`/* ncuts = 3 or 4 */`), which defines exactly two regions to swap. You cannot arbitrarily reorder three or more regions in a single REARRANGE call. To achieve a more complex permutation, you would issue multiple REARRANGE commands.

It is **not a move**. A move (take region A and place it at position X) would be a degenerate case — you'd express it as a swap of A with the content between A's current position and X. The three-cut form naturally captures this: swapping region A (cut1..cut2) with region B (cut2..cut3) effectively "moves" A past B (or vice versa).

### Summary

| Property | Value |
|----------|-------|
| **Operation** | Swap two regions |
| **Modes** | 3 cuts (contiguous regions) or 4 cuts (non-contiguous) |
| **Affects V-space?** | Yes — positions change |
| **Affects I-space?** | No — content unchanged |
| **Preserves length?** | Yes |
| **Preserves content?** | Yes — same bytes, different order |
| **Links survive?** | Yes — attached to I-space bytes, not V-positions |
| **General permutation?** | No — exactly two regions only |