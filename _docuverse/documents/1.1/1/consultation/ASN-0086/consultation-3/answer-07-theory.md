## Question 7 [theory]

> When the link model identifies a link's "type" with its third endset, was type-equality intended to be coverage-equivalence (so that any two endsets covering the same address set count as the same type) or strict endset-value identity (so that the same coverage realized via different spans counts as different types)?

# Type-Equality: Coverage vs. Endset-Value Identity

The curated sources do not directly resolve this question — Nelson never poses it explicitly. But the operational semantics he describes lean clearly toward **coverage-equivalence**.

## What Nelson Explicitly Says

The type endset, like the from-set and to-set, is "an arbitrary collection of spans, pointing anywhere in the docuverse" (4/43). Crucially, types are matched by **address**, not by content stored at that address:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

And the type can itself be plural:

> "Note that a link's type--the three-set--may be several pointers." (4/44)

## The Decisive Clue: Set-Theoretic Search Semantics

The link-search rule (4/58) tells us how a link "matches" a type query:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58, as preserved in `links.md`)

This is a **coverage predicate**: the search succeeds when the type endset's spans intersect the queried address(es). The internal structure of how that coverage is realized — whether as one span or several, contiguous or discontiguous — is invisible to the satisfaction test. From the matching machinery's perspective, two endsets that cover the same address set are indistinguishable.

Combined with Nelson's emphasis that:
- types can be "ghost elements" with nothing stored at the address (4/45),
- types are "open-ended" and user-extensible (4/43),
- the system "merely considers the type's address" (4/44-4/45),

…the design intent is functional: a "type" is effectively the *set of addresses it points at*, not the syntactic span-collection used to express that set.

## What This Means in Practice

- Two links whose third endsets cover identical address sets via *differently structured* spans behave identically under every type query.
- "Same type" is therefore best understood as **coverage-equivalence on the third endset's address-set**.
- Strict endset-value identity would make the type system fragile in ways inconsistent with Nelson's stated principle that types are "completely arbitrary" with respect to internal representation.

## The Caveat

Nelson treats the type endset as a *pointer-set used for searching*, never as an object whose identity is at stake. He does not address the corner case where two endsets have identical coverage but different span structures, because in his framework that distinction does no work — both produce the same matches against the same queries.

NEED_RAW: 4/56-4/60 (link search detail), 4/43-4/47 (full endset/type discussion) — to confirm there is no passage where Nelson disambiguates type-identity from coverage-equivalence that the curated extracts elided.
