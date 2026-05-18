## Question 2 [theory]

> Does the foundational link-model design intend depth-N recursive sub-link allocation as a core principle, or is depth-2 the intended specification with deeper structure handled by other mechanisms?

# Depth-2 is the Specification; Deeper Structure Comes from Composition

Depth-2 (the `0.2.N` form, where N is the link's permanent creation-order instance number) is what I specified as the core link address structure. Recursive sub-link allocation was deliberately **left as a possibility, not built as a principle** — deeper relational structure is handled by **link-to-link composition** instead.

## What the link address actually is

The link sits at a flat, two-digit position within its home document's space:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]

The `2` selects the link subspace; the trailing digit is the link's permanent serial position. That's the specification.

## What I said about going deeper

I explicitly acknowledged subdivision as a possibility, but framed it as a future design door, not the intent:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

"A distinct possibility" — not "the principle." I noted it because the tumbler scheme makes it *available*, not because the link model *requires* it.

## How depth is actually meant to be achieved

The link is a simple object with its own tumbler address. Complexity is meant to emerge from composition, because every link can itself be a target:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

And type hierarchies — the case most likely to tempt an implementer toward recursive sub-link addresses — fall out of the same link-to-link mechanism without any address subdivision:

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below; as well as for many other compound structures." [LM 4/51]

## Why I made that choice

I wanted the link itself to stay a flat, sequentially numbered, three-endset object. The universality of tumbler-space — every link addressable, every address linkable — is what carries the arbitrary depth. That keeps the primitive minimal (one link = one address, one creation order, three endsets) while letting users build whatever relational tree, faceted classification, or supertype lattice serves their work, all out of the same `link-to-link` primitive.

So: **depth-2 is the specified link address; depth-N is composed, not allocated.** Recursive sub-link allocation was a door I left open at [LM 4/31], but the design intent is composition through link-to-link, exactly as in LISP's CONS cell.
