## Question 2 [theory]

> When a link is withdrawn (made "not currently addressable"), does its V-position in the home document's link subspace remain occupied as a tombstone, or is the position freed and the surrounding range compacted?

The position remains occupied as a tombstone; it is not freed or compacted.

This follows from Nelson's explicit principle of **permanent order of arrival** for links. From `concepts/links.md` quoting 4/31:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Unlike bytes (which shift in Vstream as content is inserted/deleted), link addresses in the `version.0.2.N` subspace are permanent ordinals tied to creation order. Link #755 is always #755.

The page 4/9 diagram, cited in `design-intent/link-deletion.md`, describes the deleted-link state explicitly:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Three things follow from this:

1. **"Not currently addressable"** — the link is removed from the current Vstream view, not destroyed. This is tombstone semantics: the address exists, the link is just not exposed.

2. **"Awaiting historical backtrack functions"** — recovery is possible. If positions were compacted, the deleted link's identity would be overwritten by whatever shifted into its slot, breaking backtrack.

3. **"May remain included in other versions"** — other versions of the document may still reference the link at its original position. Compaction would invalidate those references.

This parallels Nelson's treatment of deleted bytes (4/9), which are similarly preserved in Istream while being removed from current Vstream addressability. The asymmetry is that bytes can be rearranged in Vstream while links cannot — links retain their creation-order positions permanently, which is precisely what makes tombstones the structural requirement rather than a design choice.

NEED_RAW: 4/31, 4/9 — The curated sources support the tombstone conclusion via inference from "permanent order of arrival" + the deleted-state description, but Nelson does not appear to state explicitly "the position remains occupied" or "no compaction occurs" in the extracted material. Confirming directly on the raw pages would strengthen this from strong inference to verified statement.
