## Question 2 [theory]

> Was FINDNUMOFLINKS intended to count only currently-addressable links (so that deletion/nullification lowers the count), or the total stored link population regardless of withdrawal?

## Answer

**Intended to count currently-addressable links — deletion/withdrawal lowers the count.** This is the reading the architecture supports, though Nelson never states it explicitly for the count operation itself, so part of this is inference.

### What the curated sources establish

**1. The count operation is a search over the current docuverse.**
`FINDNUMOFLINKSFROMTOTHREE` is the counting sibling of `FINDLINKSFROMTOTHREE`, governed by the same satisfaction model:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

The count is "how many links satisfy this request," evaluated against the current state — not a tally of everything ever stored.

**2. Deleted/withdrawn links are explicitly "not currently addressable."**
Nelson's own state diagram puts deleted links outside the addressable space:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

This is the decisive point. A withdrawn link is moved out of the addressable population and parked for *historical backtrack functions* — a separate facility. Since the ordinary search/count operates on what is currently addressable, a withdrawn link no longer satisfies a request, so it drops out of the count.

**3. Withdrawal removes from the count without destroying or renumbering.**
Deletion doesn't reclaim the address — links "keep their creation-order addresses permanently" and "deleting link 2.5 doesn't renumber 2.6 through 2.N" (links.md, citing 4/31). So the population becomes *sparse* (the link still exists in Istream, recoverable via backtrack), but the current addressable count is lower. This matches Nelson's broader non-destruction principle: nothing is truly destroyed, but the *current view* reflects only what is currently addressable.

### Summary

- **Default count = currently-addressable links.** Withdrawal lowers it.
- **Total stored population** (including withdrawn links) is reachable only through the separate "historical backtrack functions," not through an ordinary `FINDNUMOFLINKS` request.

This is consistent with how DELETE works for content generally: it removes from the current Vstream/addressable view while preserving the underlying bytes/links in Istream (delete-semantics.md, 4/9–4/11).

### Caveat / verification gap

The raw page images are not present in this checkout (`resources/literary-machines/raw/` is absent), and the curated operations text does not include a verbatim definition of `FINDNUMOFLINKSFROMTOTHREE` specifying its search domain. My conclusion is inferred from (a) the link-search satisfaction model and (b) Nelson's "not currently addressable" characterization of deleted links — not from a direct statement about the count operation.

NEED_RAW: 4/69 (to confirm the exact wording of the FINDNUMOFLINKSFROMTOTHREE / FINDLINKSFROMTOTHREE definitions and whether Nelson specifies the search domain as the current vs. total link population)
