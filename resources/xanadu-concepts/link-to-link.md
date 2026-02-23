# Link-to-Link

Source: Literary Machines, 4/49-4/51 (pages 216-218)

## Semantic Intent

### What It Means

Because links are first-class citizens in tumbler-space with their own addresses, a link can point *at* another link. This is not a special mechanism requiring new machinery - it falls out naturally from the universality of the addressing system. Links live in the same address space as data, so anything that can point to data can point to links.

This enables a layer of meta-structure above ordinary linking. Users can make commentary about connections, build hierarchical relationships between links, and construct arbitrarily complex associative structures - all using the same fundamental link mechanism.

### User Guarantee

- **Any link can be a target.** If you can address it, you can link to it. Links have addresses, therefore links can be linked.
- **Meta-commentary is built-in.** You don't need a special "comment on link" feature. Just create a link whose to-set points to another link's address.
- **Compound structures compose.** By chaining link-to-link relationships, users can build tree structures, type hierarchies, faceted classifications - whatever relational structure serves their purpose.
- **No special permission needed.** If you can see a link (have access to its address), you can create your own link pointing to it. Your meta-link lives at your address under your control.

### Principle Served

**The docuverse is self-describing.** The same mechanisms that connect content can connect connections. There is no privileged layer where "the system" lives apart from "user data." Links are data. Commentary on links uses links.

**Universal addressability enables universal reference.** Nelson designed tumbler-space to hold everything - content, documents, links - in one unified addressing scheme. Link-to-link is the natural consequence: if links have addresses, and linking means pointing at addresses, then links can point at links. The principle isn't "links should point to links" but rather "nothing should be unaddressable."

**User-defined structure without system changes.** Rather than building specific features for "link hierarchies" or "link annotations" or "link-type subtypes," the system provides the primitive (link-to-link) and lets users build whatever structures they need. This follows Nelson's pattern of providing minimal powerful mechanisms rather than feature catalogues.

### How Users Experience It

- Comment on someone's link without modifying it - your commentary link points to their link
- Build a hierarchy of link types using links between type-designators
- Create "super-links" that group related links together
- Annotate relationships, not just content (e.g., "this citation link is disputed")
- Construct faceted classification schemes mapping to tumbler-space
- Search for all links pointing to a particular link (meta-backlinks)

### Nelson's Words

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

> "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only." (4/49)

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

> "Note that this mechanism can be used for hierarchical link types, subtypes and supertypes. It is searchable for upper- and under-links, and all final data matter below; as well as for many other compound structures." (4/51)

## Compound Links

Link-to-link enables **compound links** - complex relational structures built from chains of simple links. Nelson compares this to LISP's CONS cell: the fundamental pairing mechanism that enables arbitrarily complex data structures.

A compound link can represent:
- **Type hierarchies** - supertype/subtype relationships between link types
- **Faceted classifications** - multiple independent dimensions of categorization
- **Grouped connections** - several related links bundled as one conceptual unit
- **Tree structures** - hierarchical organizations mapped to flat tumbler-space

The diagram on 4/51 shows how a virtual tree structure (with ubertype, undertype, and data leaves) maps to a flat sequence of links in tumbler-space. Each link-to-link connection builds one edge of the tree. The result is searchable - you can find upper-links, under-links, and all terminal data "below" a given node.

This is not a special "compound link type" but an emergent capability from the link-to-link primitive.
