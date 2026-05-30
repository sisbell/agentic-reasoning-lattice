## Question 1 [theory]

> Did the design intend a faceted link relating more than three roles to be a single higher-arity link, or to be composed from a chain of three-endset links via link-to-link references — and is one of these the primary mechanism with the other merely permitted?

## Answer

The design intends faceted links — relationships among more than three roles — to be **composed from a chain of three-endset links via link-to-link references**. This is not merely "permitted" alongside a higher-arity primitive; it is the *only* mechanism the architecture provides. There is no variable-arity or higher-arity link in Nelson's design.

### The link primitive is fixed at three endsets

A Xanadu link always has exactly three endsets — from-set, to-set, and type (the "three-set"). The architecture never widens the link itself to accommodate additional roles. (Note: the type endset "may be several pointers" per 4/44, but that adds *targets to one role*, not new roles.)

### Higher arity is built by composition, not by widening the link

The decisive statement comes from the link-to-link discussion (`mcp` curated source, links.md / link-to-link.md):

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

The CONS-cell analogy is the design tell. LISP does not have variable-arity cells; it has one fixed pairing primitive (CONS) from which arbitrarily complex structures are assembled. By invoking this analogy explicitly for the faceted link, Nelson signals that Xanadu likewise keeps a single fixed link primitive and builds higher-arity structure by *chaining* links — each link pointing to other links.

This composition is possible only because links are first-class, addressable objects:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." (4/49)

### Which is primary?

There is no second option to rank against. The single higher-arity link is not a contemplated design alternative — the link structure is fixed, and faceted/compound relationships exist solely as composed structures over that fixed primitive. So:

- **Primary (and exclusive) mechanism:** compound construction via link-to-link references (the CONS-cell / faceted-link pattern, 4/51).
- **The "single higher-arity link":** not a Xanadu construct at all.

This follows Nelson's broader pattern of providing "minimal powerful mechanisms rather than feature catalogues": one link primitive, made universal by addressability, from which users assemble whatever relational complexity they need.

### Verification note

The 4/49–4/51 quotes are verified in the curated sources. Nelson's actual *Chapter 2 discussion of the faceted link* (referenced parenthetically at 4/51) is not included in the curated extracts, so its exact framing there is unverified by me.

NEED_RAW: 2/21–2/25 (Chapter 2 "Links" section, to confirm how the faceted link is first introduced and whether Chapter 2 independently characterizes it as composed rather than higher-arity).
