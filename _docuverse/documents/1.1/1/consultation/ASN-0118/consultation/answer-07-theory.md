## Question 7 [theory]

> When transcluded material is set into a destination's existing arrangement, what must the operation guarantee about the prior ordering and position of the content already there?

When you transclude material into a document at a given position, the operation is a content insertion in the Vstream, and it must guarantee that the existing content is preserved in both its relative ordering and its identity. Three things must hold:

## 1. Relative order of existing content is preserved

The content already in the document keeps its sequence. Insertion does not reshuffle or reorder anything that was there — it only opens a gap at the insertion point. Both `INSERT` and `COPY` place material at a specified V-stream address:

> "This inserts `<text set>` in document `<doc id>` at `<doc vsa>`. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66, `operations`)

> "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." (4/67, `operations`)

Content *before* the insertion point is untouched; content *after* it has its V-addresses uniformly increased by the length inserted. No existing item changes its position relative to any other existing item.

## 2. Positions shift uniformly, never arbitrarily

The displacement is a clean, uniform offset applied only to the tail following the insertion point. Vstream addresses are dense and contiguous, so the operation closes/opens gaps cleanly rather than scattering content (`v-space-addresses`: "INSERT shifts addresses after the insertion point").

## 3. Istream identity is untouched, so links survive

Critically, although the V-addresses of trailing content shift, the underlying Istream identity of every existing byte is unchanged. Because links attach to bytes (Istream), not to positions (Vstream), the reordering of V-addresses does not break anything attached to the existing content:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30, `v-space-addresses`)

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42, `link-survivability`)

## Summary

The transclusion operation must guarantee **non-destruction and order-preservation of the prior content**: nothing already present is deleted, divergent, or reordered relative to its neighbors; only the V-stream positions of content following the insertion point are shifted, uniformly, by the length of the inserted material; and because existing content retains its permanent Istream addresses, all links and references to it remain intact. This is the same guarantee Nelson frames generally as editing "without damaging the originals" (2/45, `versions`).

Note: The displacement rule is stated explicitly for `INSERT` (4/66). For `COPY`/transclusion the spec states only that material is placed "at the address determined by `<doc vsa>`" (4/67); the identical insertion-displacement behavior is the logical consequence of placing transcluded spans at a Vstream address, but is not separately spelled out for `COPY` in the curated sources. If you want Nelson's exact wording on COPY's effect on trailing content, NEED_RAW: 4/67.
