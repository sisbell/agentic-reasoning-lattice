## Question 8 [theory]

> How must the system let a reader know how far through the full set of matching links it has progressed at any point during windowed reading?

## Short answer

Nelson does not specify a reader-facing "progress bar." Instead, he provides two back-end primitives whose combination *lets a front end compute and display* "you are at link M of N," and he assigns the actual reader-facing presentation to the front end, not the back end.

## The two primitives

The back end exposes a **count** operation and a **paginated retrieval** operation:

- **FINDNUMOFLINKSFROMTOTHREE** — returns the total number of links satisfying the request (the "N"). Listed among the link operations in the FEBE protocol.
- **FINDNEXTNLINKSFROMTOTHREE** — paginates through that result set, returning "no more than `<nlinks>` items past that link on that list" (4/69). This is what "handles avalanches of material from link searches."

Together these give a front end everything it needs to report position: ask once for the total count, then walk the list in pages, tracking how many have been consumed. Progress is "links retrieved so far, out of the total count."

Critically, the search is designed so the total is meaningful and stable: per 4/60, "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." The matching set is well-defined independent of the junk around it, so a count of it is well-defined.

## Why this is a front-end responsibility, not a back-end guarantee

Nelson explicitly pushes all such bookkeeping out of the user's view and into the front end:

> "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." (4/61)

So the *mechanism* the system must provide is the count-plus-pagination pair; the *progress indication itself* (how far through the matching links the reader has gotten) is something the front end synthesizes from those primitives and shows on screen.

## Caveat on the question's framing

The phrasing "how must the system let a reader know how far through..." implies an explicit, mandated progress-display guarantee. **The curated sources do not contain such an explicit reader-facing progress requirement.** What is specified is the count operation, the pagination operation, and the principle that the front end handles user presentation invisibly. The "you are at M of N" experience is a derivable consequence of these, not a separately stated guarantee.

If you need to confirm whether Nelson states any stronger, explicit progress-reporting obligation in the link-search prose:

NEED_RAW: 4/58-4/60, 4/68-4/69
