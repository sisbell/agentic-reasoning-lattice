## Question 2 [theory]

> Does the design require batch or range operations over the link subspace (e.g., "all links of document d in arrangement order") that would need correspondence-run structure analogous to the content subspace, or are link-subspace operations always per-individual-link?

# Link-Subspace Batch Operations

**Yes**, FEBE includes batch/range operations over the link subspace, but **no**, they do not require correspondence-run structure analogous to the content subspace. Here is why.

## Batch operations DO exist over links

Three FEBE operations explicitly operate over ranges or sets of links:

- **RETRIEVEENDSETS**: "This returns a list of all link end-sets that are in <spec set>." (4/70)
- **FINDLINKSFROMTOTHREE**: "This returns a list of all links which are (1) in <home set>..." (4/69)
- **FINDNEXTNLINKSFROMTOTHREE**: Paginated retrieval to handle "avalanches of material" — "no more than <nlinks> items past that link on that list." (4/69)

And spans explicitly cover links: "Thus we may have spans of characters, **spans of links**, spans of documents, spans of versions, and spans covering large combinations of them" (4/24).

So "all links of document d" is naturally expressible as a span: `N.0.U.0.D.V.0.2.1` through `N.0.U.0.D.V.0.2.M`.

## But the link subspace has only ONE ordering

The crucial asymmetry with content:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

This means:
- Links have **no V/I distinction**. Their address *is* their identity *is* their position.
- Links are addressed `N.0.U.0.D.V.0.2.N` where the final `N` is the serial creation number — and that's the only order they have.
- "All links of document d in arrangement order" collapses to "all links of document d in creation order" — there is no separate arrangement.

By contrast, bytes have V-addresses that "may be continually altered by editorial operations" (4/30), which is exactly what forces correspondence-run structure for the content subspace.

## Where correspondence still matters for links

Correspondence concerns don't vanish entirely — they shift from the link to its **endset targets**:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

The refractive following uses **content** correspondence (shared Istream origin) to resolve where an old link's targets land in a new version. The link itself doesn't need correspondence-runs; its endsets reach into content that does.

## What Nelson leaves open

Nelson explicitly flags potential future structure inside the link subspace without specifying it:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

If link subdivision were later defined to include arrangement-like reordering, *then* correspondence-run structure might be needed. As specified, it is not.

## Summary

| Aspect | Content subspace | Link subspace |
|---|---|---|
| Distinct V- and I-addresses | Yes | No (single creation-order address) |
| Rearrangeable across versions | Yes | No — "permanent order of arrival" (4/31) |
| Needs correspondence-runs? | Yes | No (for the links themselves) |
| Batch/range operations exist? | Yes | Yes (RETRIEVEENDSETS, FINDLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE) |
| Where correspondence applies | Within the subspace | Externally, via link endsets pointing at content |

Link-subspace batch operations are real and important (especially for pagination of large result sets), but they are *enumerations over a single permanent order*, not joins across rearranged orderings. The structural complexity that correspondence-runs solve for content does not arise for links as Nelson specifies them.
