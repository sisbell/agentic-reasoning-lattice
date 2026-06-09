## Question 7 [theory]

> What relationship must the returned set bear to the body of links as it stands at the exact moment the inquiry is made?

## Answer

The returned set must be **complete and current**: it must contain *every* link that exists in the docuverse at the moment of the query and satisfies the request criteria — no qualifying link omitted, and (because deleted links become "not currently addressable") nothing that has ceased to exist. It is a faithful snapshot of the satisfying subset of the live body of links as it stands when the inquiry is made.

### The completeness guarantee

Nelson defines the search operations to return *all* matching links, not a sample or a best-effort subset:

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." (4/69)

> "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)

So the relationship is one of exhaustive correspondence: the returned set = exactly those currently-existing links whose endsets satisfy the request.

### The satisfaction criterion that defines membership

What it means for a link to belong in the returned set is precisely specified:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

Every link meeting this test must appear; every link failing it must not.

### Completeness is not degraded by irrelevant links

Critically, the guarantee of completeness holds *regardless of how many non-matching links exist*. The presence of an arbitrarily large body of junk links cannot cause qualifying links to be missed:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

This is what lets the returned set stay faithful to the *whole* current body of links: the relationship is to the entire live link population, sieved down to exactly the satisfying members, no matter how vast the surrounding non-matching set is.

### Why "as it stands at this moment" matters

Links are durable but not immutable in their addressability. Deleted links enter a "not currently addressable" state (link-deletion.md, 4/9), and links retain their permanent order-of-arrival addresses (4/31). The returned set therefore reflects the body of links *as currently addressable* — current additions included, current deletions excluded — rather than a historical or projected state. (Time itself is tracked separately from the address structure — "Time is kept track of separately" (4/18) — so the snapshot is governed by what is presently addressable, not by encoded timestamps in the tumblers.)

---

**Summary:** The returned set must stand to the live body of links as the *exact and exhaustive satisfying subset* — every currently-existing link matching the request criteria, and only those — with that completeness guaranteed irrespective of the quantity of non-matching links present.
