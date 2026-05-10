## Question 7 [nelson]

> Must two regions that share no positions in common be guaranteed to produce an empty result when intersected, and must this emptiness be distinguishable from a region of zero width?

# Intersection of Disjoint Regions and the Distinction from Zero Width

## The Short Answer

Yes to both. These are categorically different things in Xanadu's architecture, and confusing them would break the system.

## Disjoint Spans Must Produce Empty Results

The link search mechanism depends on this absolutely. When you search for links, the system checks whether a link's endset spans *overlap* with the search criteria:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

If two non-overlapping address ranges could somehow produce a non-empty intersection, the entire link search mechanism would return false matches. The guarantee that:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

...depends on overlap detection being correct. A link whose from-set is in one region of tumbler-space and whose search criterion covers a completely disjoint region must *not* satisfy the request.

The tumbler line provides the ordering that makes this deterministic:

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

Two subtrees either share nodes or they don't. If they don't share nodes, their intersection is empty — no spans, no addresses, nothing.

## Emptiness Is Not Zero Width

A zero-width span (a span designating a single element) is a *valid reference to a specific thing*. An empty result is *no reference at all*. These serve entirely different purposes:

**A single-element span** addresses one specific byte, one specific link, one specific document. It has a real tumbler address. You can link to it. You can retrieve it. You can search for it.

**An empty span-set** (no spans whatsoever) is the answer to "what do these disjoint regions share?" — which is: nothing. There is no address to link to, no content to retrieve, no position to reference.

The ghost elements principle reinforces this distinction:

> "Things may be addressed even though nothing is there to represent them in storage. Consider what we may call 'ghost elements.'" [LM 4/23]

A zero-width span pointing to a ghost element is *still a valid reference* — "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them" [LM 4/23]. The address exists; it simply happens to have no stored content at the moment.

An empty intersection result has *no address at all*. It is not pointing to a ghost element — it is pointing to nothing.

## Why This Matters: The Span-That-Contains-Nothing

I was very deliberate about this distinction:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24]

A span over an unpopulated region of tumbler-space is *not empty* — it is a valid address range that happens to have no stored elements yet. It designates a zone of the docuverse. Content can appear there later.

This gives us three distinct states, not two:

| State | Meaning | Can you link to it? |
|-------|---------|-------------------|
| **Non-empty span** | Contains stored elements | Yes |
| **Span over unpopulated space** | Valid address range, no stored elements (yet) | Yes — ghost elements |
| **Empty result (no spans)** | No address range at all | No — nothing to reference |

Collapsing the last two would mean you could not distinguish "these regions don't overlap at all" from "these regions overlap at an unpopulated address." That distinction is essential for the link search mechanism and for the ghost element principle.

## The Design Principle

The spans are address ranges on the tumbler line. The tumbler line is a flat mapping of the docuverse tree:

> "The tumbler line is an abstract representation of a particular tree... finite but unlimited." [LM 4/22]

Intersection on this line is well-defined by the ordering of tumblers. Two ranges either share positions or they do not. If they share a single position, the intersection is a zero-width span at that position. If they share no positions, the result is the empty set — categorically different from any span, however narrow.

This is not a detail I left to implementors. It falls out necessarily from the nature of tumbler-space as an ordered line where spans designate contiguous ranges. The system would not work if these were conflated.

---

NEED_RAW: [4/32-4/39] — The curated sources cover the key quotes from these pages about request sets and span manipulation, but there may be additional detail about span operations and their algebra that would further illuminate the intersection question.
