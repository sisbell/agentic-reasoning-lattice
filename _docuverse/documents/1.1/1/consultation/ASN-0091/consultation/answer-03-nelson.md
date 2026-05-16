## Question 3 [nelson]

> After rearrangement, does the document's content stream contain exactly the same set of content as before — no additions, no losses — or may rearrangement discard or duplicate material?

## REARRANGE Is Content-Preserving

After rearrangement, the document's content stream contains **exactly the same set of content** — no additions, no losses, no duplications. Nelson's specification is unambiguous on this point.

### The Specification

From LM 4/67 (page 234):

> "Rearrange **transposes** two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3. With four cuts, the regions are from cut 1 to cut 2, and from cut 3 to cut 4."

The word **transposes** is precise. A transposition swaps two things — it is a permutation, not a transformation that can add, remove, or duplicate content. The two identified regions exchange positions; everything else stays where it is.

### Three-Cut vs Four-Cut

- **Three cuts** (A, B, C): Swaps the adjacent regions [A..B] and [B..C]
- **Four cuts** (A, B, C, D): Swaps the non-adjacent regions [A..B] and [C..D]

In both cases the operation is a swap. The document afterward contains the same bytes in a different Vstream order.

### Architectural Confirmation

REARRANGE is a **pure Vstream operation**. It changes the arrangement of content in the virtual byte stream without touching Istream (permanent storage). Nelson's FEBE command set separates concerns cleanly:

| Operation | Effect on content |
|-----------|-------------------|
| INSERT | Adds new bytes (extends Istream) |
| DELETE | Removes from Vstream (Istream unchanged) |
| COPY | Maps existing Istream content into Vstream (transclusion) |
| APPEND | Adds new bytes at end |
| **REARRANGE** | **Reorders Vstream — no Istream change** |

From LM 4/30 (page 197), confirming the Vstream-only nature:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them."

Links survive rearrangement precisely *because* the bytes themselves are unchanged — only their Vstream positions shift.

### Summary

REARRANGE is a content-preserving transposition. The Vstream before and after contains the identical multiset of I-address references. No bytes are created, destroyed, or duplicated. This follows necessarily from the Istream/Vstream separation: REARRANGE modifies the mapping (which Istream content appears at which Vstream position), not the content itself.
