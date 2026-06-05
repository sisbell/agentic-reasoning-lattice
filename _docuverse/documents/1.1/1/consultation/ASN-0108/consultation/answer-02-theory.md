## Question 2 [theory]

> Must the enumeration order over a set of matching links be a property the reader can rely on as total and unambiguous, so that no two links could ever occupy the same position?

## Short answer

Yes. By design, the enumeration is **total and unambiguous**: every link occupies a unique, permanent position, and no two links can ever share a position. This follows from how Nelson addresses and orders links — though I should flag that Nelson states the *mechanism* (unique permanent addresses, ordered lists) more than he states the *guarantee* in those exact words.

## What Nelson explicitly establishes

**1. Links have permanent, unique addresses assigned by order of arrival.**

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

Each link gets a sequential, creation-order address within its home document — `N.0.U.0.D.V.0.2.1`, `...2.2`, `...2.755` — and these never change or get reused:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" ... "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

Because each link's home document determines its residence, and each home assigns distinct sequential positions, **every link in the docuverse has a globally unique tumbler address**. The tumbler line is itself a linear (total) ordering of the whole address space, so any set of links drawn from it inherits a total, unambiguous order. Two distinct links cannot map to the same point on the line.

**2. The pagination operation depends on this total order.**

The cursor-based retrieval `FINDNEXTNLINKSFROMTOTHREE` returns:

> "no more than `<nlinks>` items past that link on that list." (4/69)

"Items *past that link* on *that list*" is only well-defined if the result set has a stable, total order in which each link occupies exactly one position. A reader paginating through matching links can rely on resuming from a precise cursor precisely because positions are unique and ordered.

## The one caveat

What links *match* a request can change over time, because the docuverse grows and links survive editing. So the *membership* of a matching set is not frozen — but the *ordering relation* over whatever links exist is total and unambiguous, since it is the permanent order-of-arrival / tumbler-address order. The reader can rely on "no two links occupy the same position"; they cannot rely on "the set never gains new members."

This also fits Nelson's scaling guarantee that filtering scope, not collisions, governs search:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

## Note on sourcing

Nelson directly states the unique-permanent-address mechanism (4/31) and the cursor pagination semantics (4/69). The conclusion that the result enumeration is therefore *total and unambiguous* is a faithful inference from those two facts plus the linear structure of the tumbler line — Nelson does not phrase it as an explicit reader-facing guarantee in the curated material. If you want his exact wording around the result-list ordering of `FINDNEXTNLINKSFROMTOTHREE`, that would be: NEED_RAW: 4/69, 4/58-4/60.
