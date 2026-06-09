## Question 1 [theory]

> Is a typed relation's source meant to denote a single address, or may a single source span legitimately cover a range/subtree of addresses?

A link's source (the from-set) is **not** restricted to a single address. It is an arbitrary span-set that may legitimately cover a discontiguous collection, a contiguous range, or even a whole subtree of the docuverse.

## The from-set is an arbitrary collection of spans

Nelson generalizes all three of a link's endsets — from-set, to-set, and type — to be arbitrary span-sets, not single points:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.'" (4/42)

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

So the source is a *set* of spans, which subsumes the single-byte case as a degenerate one.

## A single span may itself cover a range or subtree

Even one span — not just a set of them — can span much more than one address. Spans are defined by tumbler boundaries, and a tumbler-span denotes a subtree:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse, (or merely to a series of elements of the same type, which is a degenerate case of a subtree)." (4/24)

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." (4/24)

The contents of a span are implicit in its boundaries:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

## A source can even point at "ghost" container addresses

Because the address space includes ghost elements (accounts, nodes, documents with no stored object), a source endset can point at such a position and thereby embrace everything beneath it:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

> "A link to or search of an account or node will find any of the documents under it." (4/23)

## Conclusion

A typed relation's source is **meant to be able to span a range or subtree**. The single-address case is just the smallest (degenerate) instance of the general from-set, which is an arbitrary span-set capable of covering discontiguous bytes, contiguous ranges, or whole subtrees up to the entire docuverse. This generality is deliberate — it is what lets, e.g., "a critique that touches three separate passages" or a link from "all documents under an account" be expressed as a single source (4/42, 4/43).

One caveat on terminology: the curated sources use "from-set" for the *source* end. If by "typed relation's source" you specifically meant the **type** endset (the "three-set"), the same answer holds — the type is also an arbitrary span-set and may even point to ghost addresses (4/44–4/45).
