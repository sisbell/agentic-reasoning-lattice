## Question 6 [theory]

> When new content is added to a document that links already point into, must the count for an unchanged description remain stable?

## Short answer

Yes — **if the description refers to the same content (the bytes themselves), the count must remain stable.** Adding new content to a document does not add or remove any links from the pre-existing bytes, because Xanadu links attach to bytes, not to positions. The newly inserted content simply has no links pointing into it yet, so a query describing the *unchanged* region returns the same links and the same count.

The one caveat: if your "description" is expressed as a raw V-stream position range rather than as the content itself, an insertion shifts those positions, so the literally-identical positional query would now cover *different* bytes — and the count could differ. That is a different description in effect, even if it reads the same.

## Why this holds

The governing invariant is link survivability — links are "straps between bytes," not pointers to positions:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

Insertion changes the *arrangement* (Vstream), not the *identity* (Istream) of existing bytes. Nelson states this directly about editorial reordering:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

INSERT only shifts the V-stream addresses of following content; it does not touch what the existing bytes are or what points to them:

> "This inserts <text set> in document <doc id> at <doc vsa>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (4/66)

And because the front end works against permanent byte identity rather than mutable position:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

## The mechanism in terms of link search

Link counting (FINDNUMOFLINKSFROMTOTHREE) is defined by endset satisfaction:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

If the request set is anchored to the unchanged bytes, then:
- Every link that satisfied it before still satisfies it (those bytes still exist, links still strapped on).
- The inserted bytes are new I-addresses with no incoming links, so they add nothing to the matching set.

Hence the count is invariant. New content arriving elsewhere also doesn't interfere with the search, consistent with:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

## The boundary condition to watch

The stability guarantee is a guarantee about **content identity**, not about **positional notation**. Because INSERT renumbers following V-positions (4/66), a description written as "V-positions 10–20" is, after an insertion above position 10, no longer pointing at the same bytes. To get a stable count you must describe the same *content* (or re-anchor the positional span), not reuse a stale positional range. The system's design assumes exactly this: front ends track byte identity, which "may be constantly changing" in V-position (4/11).
