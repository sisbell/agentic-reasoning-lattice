## Question 8 [theory]

> Can a link's endsets reference other links, and must a direct read disclose that nesting faithfully?

## Yes — links can reference other links, and the read returns those references faithfully

### Endsets can point at links

This follows directly from the universality of tumbler-space. Links are first-class citizens with their own addresses, living in the same address space as content, so anything that can be addressed can be referenced by an endset.

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

The mechanism is the ordinary endset mechanism — no special machinery:

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." (4/49)

And endsets are universally unconstrained in where they reach:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse." (4/43)

> "ENDSETS MAY POINT TO SPANS ANYWHERE IN THE DOCUVERSE" (4/45, diagram caption)

This is what enables compound/faceted links — nested link structures built like LISP CONS cells:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

### A direct read must disclose the nesting faithfully

The retrieval operation that exposes a link's endsets is RETRIEVEENDSETS:

> "This returns a list of all link end-sets that are in <spec set>." (4/70)

Because an endset is nothing but a set of tumbler addresses, and a link that points at another link does so by placing that link's *actual address* in its to-set (with span 1), the read returns those addresses unchanged. There is no transformation that flattens or hides the fact that a target address is itself a link rather than content. The search/retrieval machinery is address-based, not content-based:

> "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

This same address-fidelity is why the structure is searchable in both directions — you can find the links that point *to* a given link (meta-backlinks):

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below; as well as for many other compound structures." (4/51)

### Summary

- **Can endsets reference links?** Yes. Links have tumbler addresses; endsets point anywhere in tumbler-space; therefore an endset can name a link (4/49, 4/43, 4/45).
- **Does a direct read disclose the nesting faithfully?** Yes. RETRIEVEENDSETS returns the endsets as the tumbler addresses they actually are (4/70), and the address-based design preserves the reference exactly — a link-target reads back as that link's address, not as flattened content.

One caveat on scope: the curated sources confirm that the endset *addresses* are returned faithfully by RETRIEVEENDSETS, but they do not spell out a front-end obligation to *render* or *traverse* that nesting in any particular way to the human reader — that is left to front-end design. If you need Nelson's exact wording on how deeply a single RETRIEVEENDSETS call recurses into nested links versus returning one level of addresses, that detail isn't in the curated material. NEED_RAW: 4/49-4/51, 4/70
