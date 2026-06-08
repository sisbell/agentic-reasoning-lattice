## Question 2 [theory]

> Does the design intend links to carry more than the standard from/to/type triple, and if so what role, if any, do endsets in slots beyond the third bear?

The design does **not** intend a standard link to carry more than the from/to/type triple. The Xanadu link is exactly three endsets, and Nelson is emphatic that this set is complete and symmetrical—not a prefix of some longer list.

## The triple is the whole structure

The three endsets are from-set, to-set, and type ("three-set"):

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.'" [LM 4/42]

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes... The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

The type is explicitly framed as the *third and final* generalization—the design closes the structure at three by treating the type identically to the other two:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

The protocol confirms this: the search/creation operations are named for exactly three slots—`MAKELINK` (from-set, to-set, three-set), `FINDLINKSFROMTOTHREE`, `FINDNUMOFLINKSFROMTOTHREE`. There is no fourth-endset operation, and `RETRIEVEENDSETS` returns the from-set and to-set. The naming itself encodes that "three" is the ceiling.

## Complexity beyond three comes from composition, not extra slots

The important design point is *how* Nelson reaches richer structures. He does **not** add a fourth endset. Instead, because links have their own tumbler addresses, links can point at links, and you build arbitrary structure by chaining the two-sided link mechanism:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below; as well as for many other compound structures." [LM 4/51]

So the "faceted link"—a multi-dimensional relationship that one might naively imagine needing extra endsets—is instead realized as a compound of ordinary links. The CONS-cell analogy is the key tell: just as LISP builds every data structure from two-field cells, Xanadu builds every relational structure from the fixed three-endset link. There is no need for, and no provision for, a fourth slot.

## What endsets "beyond the third" bear: nothing—by design

There are no slots beyond the third in a single link. The role they would play—grouping, faceting, hierarchy, meta-commentary on a connection—is instead borne by **link-to-link composition**. The three-endset link is the irreducible primitive; everything else is assembled from it.

One nuance worth flagging on the addressing side (not the endset side): Nelson notes the link *address space* could be subdivided further—

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

—but this concerns subdividing a link's *tumbler address*, not adding endsets to the link's connective structure. It does not contradict the three-endset model.

**Bottom line:** the triple is intentionally exhaustive. The symmetry argument at 4/44 and the explicit reliance on link-to-link CONS-style composition at 4/51 show Nelson deliberately kept the link a fixed three-endset object and pushed all additional expressive power into composition rather than into extra slots.
