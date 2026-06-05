## Question 7 [theory]

> If the same region is asked about twice with the content unchanged, must the system return identical endsets each time?

## Short answer

Nelson never states an explicit idempotence or determinism guarantee in the curated material — but the architecture implies a qualified "yes," with one important distinction between *content unchanged* and *links unchanged*.

## What the architecture implies

Endsets are not computed fresh from semantic analysis; they are *stored structure*. A link's three endsets are concrete addresses on the tumbler line:

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (4/45)

Because both the content and the links have permanent addresses, retrieving the endsets of a given link is a lookup against immutable data, not a recomputation. If the underlying links are unchanged, the endsets they project onto the tumbler line are the same. So `RETRIEVEENDSETS` over an unchanged set of links is deterministic by construction.

Link *ordering* is also stable, which matters if "identical" means identical sequence and not just identical set:

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)

Deleting an intervening link does not renumber the others, so the order of arrival is permanent. That gives you a stable, reproducible enumeration.

## The critical distinction: "content unchanged" ≠ "links unchanged"

Here is the subtlety your question hinges on. Endsets are properties of *links*, and links are owned and stored separately from the content they touch:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

This means someone can create a *new* link pointing into your region without altering a single byte of your content. The content is unchanged; the set of links touching that region is not. So:

- **If you ask "what are the endsets of *these* links?"** (`RETRIEVEENDSETS` on a fixed link spec-set) — the answer is invariant as long as those links exist. Identical every time.
- **If you ask "what links touch *this region*?"** (`FINDLINKSFROMTOTHREE` over a content span) — the result can grow between the two queries if a third party linked into the region, even with content untouched.

In the second case the *previously returned* endsets remain valid and survive (links attach to bytes, not positions: 4/42), but the returned *collection* is not guaranteed identical across two calls separated in time.

## What Nelson does and does not guarantee

What he guarantees is *stability of what exists* — survivability and permanent ordering — not *snapshot equality of a search over time*. The search model is explicitly additive/monotonic in spirit:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

This describes *which* links match, deterministically, given the current population of links — but it presumes a fixed population.

## Conclusion

For a fixed set of links, yes: endsets are stored structure mapping to permanent tumbler addresses, so the same query returns identical endsets. But "content unchanged" alone is not sufficient to guarantee an identical *result set* for a region query, because links are owned and stored independently of the content they point to — new in-links can appear without any content change.

NEED_RAW: 4/58-4/60, 4/70 — to confirm whether Nelson anywhere states an explicit determinism/idempotence property for `RETRIEVEENDSETS` or the link-search commands, rather than leaving it as an architectural consequence. The curated sources describe the search *satisfaction* rule and endset structure but do not contain an explicit statement that repeated identical queries must return byte-identical responses.
