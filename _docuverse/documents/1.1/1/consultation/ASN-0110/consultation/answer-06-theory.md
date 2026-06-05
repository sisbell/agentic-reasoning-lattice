## Question 6 [theory]

> What must the result reveal about how many distinct links are anchored to the region, given that links are never named in the answer?

## Answer

The result must reveal a **cardinality — a count of distinct links** — and nothing more. It tells you *how many* links satisfy the anchoring constraint on the region, without ever returning, naming, or enumerating the individual links themselves.

This is exactly the division of labor Nelson builds into the FEBE protocol. There are two separate kinds of link operation:

**1. Counting (reveals only a number)**

`FINDNUMOFLINKSFROMTOTHREE` exists precisely to answer "how many" without identifying which. Likewise, `RETRIEVEDOCVSPANSET`:

> "This returns a span-set indicating both the number of characters of text and the number of links in document <doc id>." (4/68)

The result here is a tally. It discloses the quantity of links anchored to/in the region, but the links remain unnamed — their addresses are never surfaced.

**2. Naming/finding (reveals identities)**

Only when you *do* want the links named do you use `FINDLINKSFROMTOTHREE`:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

So for a question whose answer must *not* name links, the constraint forces you to the counting operation: the result is a pure count of distinct links anchored to the region.

### What "distinct" and "anchored" mean here

A link counts as anchored to the region if one of its endsets touches the span. The satisfaction rule is:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

Because a link "is not between points, but between spans of data" and behaves as "a strap between bytes" (4/42), any link with bytes overlapping the region is one of the distinct links the count must include. Each link is a first-class object with its own address, so "distinct" means distinct link-addresses — the count is the number of separate strap-objects landing on those bytes, not a count of bytes or anchor points.

### Why a count alone is meaningful

Critically, the count is reliable even in a docuverse saturated with irrelevant links:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

So the result legitimately reveals the *exact number of distinct links* anchored to the region — junk links elsewhere don't inflate or distort that figure — while the links themselves stay unnamed.

**In short:** the result must reveal the number of distinct links (a cardinality) anchored to the region's bytes, surfacing the count via the counting operations (`FINDNUMOFLINKSFROMTOTHREE` / `RETRIEVEDOCVSPANSET`) rather than the link-listing operation, so that no link is ever named.
