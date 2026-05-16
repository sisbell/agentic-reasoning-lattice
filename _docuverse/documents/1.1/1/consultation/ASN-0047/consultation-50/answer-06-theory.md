## Question 6 [theory]

> When a link is created without a type-endset (empty Θ), does the design intend it to participate in type-matching equivalence (all untyped links sharing a trivial type-class), or to stand outside the type-matching relation entirely?

The curated sources do not explicitly address empty type-endsets as a designated case. What I can establish from design intent:

**Type matching is address-based, not content-based**: "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

**Search requires at least one span per endset**: "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." [LM 4/58]

By this satisfaction rule, a link with empty Θ has no span available to satisfy any type-side criterion — it would stand outside type-matching entirely (Option B), not form a "trivial untyped class" (Option A). The symmetry I emphasized between all three endsets [LM 4/44] reinforces this: empty Θ is structurally analogous to empty from-set or to-set — a malformed or degenerate link, not a distinguished equivalence class.

There is no "ghost address for untyped" in my design. Ghost elements are real addresses with nothing stored at them [LM 4/45]; absent endsets are different — there is no address at all.

NEED_RAW: 4/55-4/60 (link-search semantics in detail), 4/47-4/48 (one-sided links — Nelson explicitly discusses links with only one populated endset, which may bear on the empty-endset question)
