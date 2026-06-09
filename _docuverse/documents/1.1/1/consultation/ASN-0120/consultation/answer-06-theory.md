## Question 6 [theory]

> When a link is created with a from endset and a to endset, what does the ordering of those endsets guarantee about the link's directionality?

## Answer

The ordering of the endsets establishes a **semantic, user-interpreted directionality** — a labeling of one side as "from" and the other as "to" — but it does **not** constrain how the link can be discovered or traversed by the system. These are two different things, and Nelson is careful to separate them.

### 1. The ordering labels the sides, but their meaning is case-dependent

Nelson states the link "is typically directional," and the from/to ordering is what carries that direction:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

The crucial guarantee is in the parenthetical: the *meaning* of "from" and "to" is not fixed by the system. It depends on the link's type and purpose. A citation link's "from" is the citing text and "to" is the source; a comment link's "from" is the commentary and "to" is the subject. The ordering preserves *which span plays which role*, but the system attaches no universal semantics to that role.

### 2. Directionality is for the user; indexing is bidirectional

What the ordering does **not** guarantee is one-way navigation. The system indexes links by all endsets, so they are discoverable from any side:

> "Links are intrinsically bidirectional in the system's indexing. Some types are a special case where directionality matters to the user." (from the links concept material, 4/42 area)

So even though a link is labeled from→to, a reader can still ask "what links *to* this content" and find it. The from/to ordering guarantees a *meaningful asymmetry the user can rely on* (you can tell which end is which), not a *restriction on traversal*.

### 3. The ordering survives editing along with the endsets

Because each endset attaches to spans of bytes rather than positions, the from/to assignment remains stable even as documents are edited:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

The "from" bytes stay "from" and the "to" bytes stay "to" as long as any bytes survive at each end.

### Summary

The ordering guarantees that the link carries a **stable, discoverable distinction between its two ends** — a from-side and a to-side whose roles persist through editing. But the *interpretation* of that direction is left to the link's type and the user ("depend on the specific case"), and the directionality does not prevent bidirectional discovery, since the system indexes both ends.

One-sided links are the degenerate case that highlights this: when there is no meaningful "from," only the first endset is used to designate what is pointed at — Nelson notes "since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)
