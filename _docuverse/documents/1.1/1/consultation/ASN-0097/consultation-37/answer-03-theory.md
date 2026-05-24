## Question 3 [theory]

> Was link discovery intended to operate over content addresses only, or as a general I-space query admitting link-address queries (reverse-link traversal, type-hierarchy lookup)?

# Link Discovery: General I-Space Query

Link discovery was designed as a **general I-space query mechanism**, not restricted to content addresses. The architecture admits link-address queries — including reverse-link traversal and type-hierarchy lookup — as first-class operations, not as special cases bolted onto a content-only model.

## Three Architectural Commitments

**1. Universal tumbler-space.** Links are first-class citizens in the same address space as content. Mark Miller's insight was explicitly this unification [LM 4/16]:

> "everything could be named within a common structure, and that an arithmetic could be developed for this structure to be the common internal language throughout the search procedures of the system."

A link has its own tumbler address (within the document's `0.2.N` subspace). To the search mechanism, a link address and a content address are the same kind of thing: a position on the tumbler line.

**2. Endsets point anywhere — including at links.** From [LM 4/49]:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)."

This is not a separate feature. It falls out of the design: if links are addressable and endsets are arbitrary span-sets pointing anywhere, then endsets can name link addresses.

**3. Search matches addresses, not content.** From [LM 4/44-4/45]:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."

The search engine is agnostic about *what* lives at a queried address. Ghost addresses with nothing stored are valid query targets. Link addresses are valid query targets. The address space is the universal currency.

## The Canonical Operation Embodies It

FINDLINKSFROMTOTHREE [LM 4/69] takes four independent span-sets — home-set, from-set, to-set, three-set — and returns matching links. Each of these span-sets may name content positions, link positions, ghost elements, or arbitrary combinations. There is no separate "find-links-by-link-address" operation, because the general one already does it.

- **Reverse-link traversal:** supply the target's address as the to-set. To find what points at a *link*, supply that link's address as the to-set. Same operation.
- **Type-hierarchy lookup:** searching by type-address returns all links of that type. If types are themselves connected by link-to-link relations [LM 4/51], the hierarchy is navigable through repeated calls — "searchable for upper- and under-links, and all final data matter below."

## The Underlying Principle

Specialcasing "content addresses" vs "link addresses" in the query layer would betray the unification. The whole point of putting links in tumbler-space was that one mechanism — address-matching search over span-sets — would serve every retrieval need, from "what does this paragraph cite?" to "what comments on that citation link?" to "what links use this type?" The asymmetry the user is asking about doesn't exist in the design; it would be a regression imposed by an implementation that failed to honor universality.
