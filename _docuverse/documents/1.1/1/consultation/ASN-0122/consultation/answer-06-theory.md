## Question 6 [theory]

> When the comparison is restricted to portions of documents rather than their full extents, what must the system guarantee about correspondences that cross or only partially overlap the requested boundaries?

## Short answer

The correspondence operation — **SHOWRELATIONOF2VERSIONS** — takes **spec-sets** as its two operands, so the comparison can be restricted to arbitrary portions rather than whole documents. When it is, the system must report each correspondence **clipped to the requested boundaries**: a correspondence that crosses or only partially overlaps a boundary is neither dropped nor returned wholesale — the system returns the **intersection**, exactly the overlapping sub-span that lies inside *both* requested portions.

The one verified textual anchor is the operation's own specification:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." (4/70)

The load-bearing phrase is "the spans **of the two spec-sets**." The returned spans are bounded by — reported relative to — the requested spec-sets, not the full documents. A correspondence that runs past a requested boundary therefore surfaces only as the portion that is "of" the requested spec-set.

## Why clip rather than drop, and why clip rather than overflow

Two obligations combine, cutting in opposite directions:

1. **No silent dropping (completeness within bounds).** Correspondence exists precisely to show "what parts of two versions are the same":
   > "...not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." (2/20)
   > "Moreover, highlighting the corresponding parts is a vital aspect of intercomparison." (3/13)

   If a partially-overlapping correspondence were discarded just because part of it fell outside the window, the user would get a *false* same/different picture for the very region they asked about. So the overlapping portion must be reported.

2. **No overflow past the request.** Equally, the result may not include content outside the requested spec-sets — the returned pairs are spans "of the two spec-sets," not of the whole documents. The part of the correspondence beyond the boundary is excluded.

The net guarantee is **intersection/clipping**: return exactly the sub-span shared with both requested portions.

## Why this falls out of the model (not a special case)

Correspondence in Xanadu is **structural**, not stored metadata — two positions correspond when they map to the same Istream (I-address) origin. Restricting the query to portions doesn't alter the correspondence relation; it just intersects that relation with the requested V-ranges on each side. And spans are built to be clipped this way — a span is defined purely by its endpoints, with everything between implicit:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

Because the clip on side A and the clip on side B must designate the *same* shared content, the two clips are tied together through their common I-addresses: the reported pair is the I-address overlap visible in **both** spec-sets at once. (This is the same "satisfy a corresponding part of the request on each side" shape Nelson uses for link search — "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58) — though he states that rule for links, not explicitly for correspondence.)

## Grounded vs. inferred

- **Grounded:** the operation runs on spec-sets and returns corresponding span-pairs "of the two spec-sets" (4/70); correspondence is structural / shared-origin; spans clip by endpoints (4/25); intercomparison must show what is the same (2/20, 3/13).
- **Inferred** (consistent with, but not verbatim in, the curated sources): the explicit rule that a boundary-crossing or partially-overlapping correspondence is **clipped to the intersection** — reported for its in-bounds portion, excluded for its out-of-bounds portion, and never silently dropped.

**NEED_RAW: 4/70 (raw page 237), surrounding protocol/operation text 4/68–4/71, and the spans pages 4/24–4/25** — to confirm whether Nelson states the partial-overlap / boundary-crossing behavior of SHOWRELATIONOF2VERSIONS explicitly, rather than leaving it to be derived from "the spans of the two spec-sets that correspond." (Note: this environment exposes no file/Read tool, so I could not open the page images directly to verify beyond the curated extracts.)
