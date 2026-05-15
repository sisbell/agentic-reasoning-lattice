## Question 1 [theory]

> In Literary Machines, is a link defined as exactly three endsets (from, to, type) with a required non-empty type-endset, or is it an n-ary structure with N ≥ 3 endsets and an optional type?

A link is **exactly three endsets** (from-set, to-set, type/three-set), not an n-ary structure. The type endset is structurally required, though it may point to addresses with no content ("ghost elements").

## Exactly three endsets

From 4/42-4/44:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.'" [LM 4/42]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The protocol confirms this structurally. MAKELINK takes exactly three sets:

> "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." [LM 4/68]

Search operations use the same three-fold structure (FINDLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE).

## Each endset is a span-set, but still one endset

The confusing point: each of the three endsets is itself an arbitrary collection of spans. From 4/43-4/44:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "Note that a link's type—the three-set—may be several pointers." [LM 4/44]

So the type endset can contain *multiple addresses* — but it's still **one endset** (the third). Multiple pointers within one endset ≠ multiple endsets.

## Type is required structurally, but can be a "ghost"

The type cannot simply be omitted, but the address it points to need not have content:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

This means the type is *structurally present in every link* but its target address may be a ghost (unoccupied). This is distinct from "optional" — the slot is always there.

## One-sided links: the structure still has three slots

A potential ambiguity: Nelson mentions one-sided links (e.g., paragraph designators):

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

This is **semantic**, not structural — the from-set carries the meaningful content; the to-set may be unused. The link still has the three-endset structure; it just uses only one of them meaningfully.

## Compound structures use link-to-link, not more endsets

When Nelson needs richer structure (faceted links, hierarchies), he does NOT extend the link to have more endsets. He builds compound structures via link-to-link:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

The "two-sided link structure" Nelson refers to is the from→to directionality (with type as classification on top). Arbitrarily complex relational structures emerge from chaining these three-endset primitives, not from adding endsets.

## Summary

| Claim | Verdict |
|---|---|
| Exactly 3 endsets per link | **YES** (from-set, to-set, type) |
| N ≥ 3 with variable arity | **NO** — n-ary structure achieved via link-to-link composition |
| Type structurally required | **YES** — every link has a 3-set |
| Type semantically required to be non-empty | **NO** — may point to ghost elements |
| Each endset can hold multiple spans | **YES** — but that's *within* one endset, not multiple endsets |

Nelson's design is: **three endsets, each an arbitrary span-set, with the type endset permitted to point at ghost addresses.** Compound structures emerge from composition (links-to-links), not from extending the link primitive itself.
