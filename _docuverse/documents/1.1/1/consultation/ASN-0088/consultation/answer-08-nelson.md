## Question 8 [nelson]

> Is the set of discovered links guaranteed to have a defined order, and if so, what property determines that order?

## Link Order in Search Results

**Yes, discovered links are guaranteed to have a defined order.** This is established by two properties: the permanent tumbler addresses of links, and the pagination mechanism that depends on stable ordering.

### Evidence for Defined Order

The `FINDNEXTNLINKSFROMTOTHREE` operation makes ordering mandatory. It returns:

> "no more than \<nlinks\> items past that link on that list." (4/69)

The phrase "past that link on that list" requires a stable, deterministic ordering — otherwise you could not resume pagination from a known position.

### What Determines the Order

**Within a single document**, the order is explicitly creation order (order of arrival), encoded permanently in the link's tumbler address:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Links are addressed sequentially — `...0.2.1` is the first link created, `...0.2.755` is the 755th — and unlike bytes, **links are not rearrangeable**:

> "Unlike bytes (which can be rearranged in Vstream), links keep their creation-order addresses permanently."

**Across documents**, the tumbler line provides a total ordering. All tumblers form a linear sequence through depth-first tree traversal. Since every link has a unique tumbler address, the tumbler line defines a total order over all links in the docuverse.

### The Search Constraint Model

The search itself uses a satisfaction model to determine *which* links are returned:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

The `home-set` parameter constrains *where* to look for links. If the home-set is the whole docuverse, all matching links are returned. If it's a single document, only that document's links are searched. The ordering of results follows the tumbler-line position of the links found.

### Implications

This design means:
- Pagination is deterministic — you can resume exactly where you left off
- The order is permanent — it never changes, since link addresses never change
- Within a document, order reflects chronological creation
- Across documents, order reflects the tumbler-line hierarchy (server → account → document → link instance)

NEED_RAW: [4/58-4/60, 4/69] — The curated sources establish that pagination requires stable ordering and that link addresses are permanent creation-order, but do not contain an explicit statement like "results are returned in tumbler order." The raw pages for the search model and `FINDNEXTNLINKSFROMTOTHREE` may contain a more explicit specification of result ordering.
