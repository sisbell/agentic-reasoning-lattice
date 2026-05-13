## Question 1 [theory]

> When the design says type matching "considers the type's address," does it mean two type endsets match iff they are identical as sets of spans, or iff they cover the same addresses (allowing different span decompositions)?

# Type Endset Matching: Address Coverage, Not Span Identity

Matching is by **address coverage** (or more precisely, address overlap), not by identity as span-sets. Two type endsets that cover the same addresses with different span decompositions match.

## The Two Key Passages

The "consider the address" rule (4/44–4/45):

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."

The satisfaction rule (4/58):

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request."

## Why This Settles It

The satisfaction rule is **existential, not equality-based**: "*one* span of each endset satisfies *a corresponding part* of the request." The match is asymmetric (link-against-request, not endset-against-endset), and the criterion is "one span falls within a part of the request" — i.e., address overlap.

Consequences:

- Two endsets `{[A,B]}` and `{[A,M], [M,B]}` (same addresses, different decomposition) are interchangeable for search purposes — each will satisfy a request the other satisfies.
- Even **partial** address overlap suffices to match. Full address-set equality is stronger than required.
- This is consistent with Nelson's broader stance that types are "ghost-element" addresses whose *content* is irrelevant (4/45): if the content at the address doesn't matter, neither does the particular span-decomposition that names that address.

## Caveat

Nelson frames matching as request-against-link, not endset-against-endset. There is no primitive "are these two type endsets equal?" operation specified. The address-coverage reading is what falls out of the search semantics — which is the only place matching is actually defined.
