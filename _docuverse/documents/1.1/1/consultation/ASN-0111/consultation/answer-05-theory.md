## Question 5 [theory]

> When a link names multiple endsets, what ordering or grouping among them must the read preserve?

## The grouping that must be preserved: the three-way role distinction

When a link names multiple endsets, the essential structure the read must preserve is **which spans belong to which of the three endsets** — the from-set, the to-set, and the type (three-set). These three are mechanically symmetrical but **semantically distinct by role**, and that role-grouping is what carries meaning.

Nelson establishes the three roles:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

So while the three endsets share one mechanism, the read cannot collapse them into one pool of bytes — a byte in the from-set means something different from the same byte in the to-set or the type. The directional from/to grouping and the separate type grouping must survive retrieval.

## Within a single endset: a set, not a sequence

Inside any one endset, the spans form an **arbitrary collection** — set semantics, where membership (which spans) matters rather than their order:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

An endset can be discontiguous ("one end of a link may be on a broken, discontiguous set of bytes," 4/42), and each span's content is fixed by its boundaries, not by position in a list. Nelson does not specify an ordering requirement *among* the spans within a single endset.

## In search, the correspondence between endset and request-part must be preserved

The satisfaction model makes the role-grouping load-bearing: each endset is matched against its **corresponding** part of the request, not against the request as a whole.

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58)

A request supplies a home-set, from-set, to-set, and three-set, and the link's from-set must be tested against the request's from-set, the to-set against the to-set, and so on. This "AND of the ORs" only works if the read keeps each endset aligned with its role.

## Summary

- **Must preserve:** the three-way grouping — which spans are from-set vs. to-set vs. type — because these roles are semantically distinct (directional from/to, plus type), and search matches each endset to its *corresponding* request part (4/42, 4/44, 4/58).
- **Need not impose ordering:** within a single endset, spans are an "arbitrary collection" (a set), so no intra-endset sequence is mandated (4/43).

NEED_RAW: 4/58-4/60, 4/70 — to confirm whether RETRIEVEENDSETS / the link-search return format specifies any ordering of results beyond the role-grouping described above; the curated sources state the satisfaction rule and that RETRIEVEENDSETS "returns a list of all link end-sets that are in <spec set>" (4/70) but do not detail result ordering.
