## Question 4 [theory]

> When the same content appears in multiple documents through transclusion, what must the design guarantee about the shared identity those documents hold in common?

## The Shared Identity: A Common Istream Address

When the same content appears in multiple documents through transclusion, the design must guarantee that those documents **share the very same Istream (I-stream) content identity** — not duplicate copies. The content has *one* permanent home address, and every transcluding document references that single address rather than holding its own copy.

This is the foundational distinction Nelson draws between **native bytes** and **included bytes**:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." (4/11)

The critical guarantee is that transclusion is **inclusion by reference, not copy** (see `concepts/transclusion.md`). The content exists once, in Istream, and transcluding documents create Vstream arrangements that point at that shared Istream origin. Identity is based on *creation*, not on byte-value coincidence: two documents that independently type the same words get *different* I-addresses, while two documents where one transcludes the other *share* the same I-address (see `design-intent/sporgl-provenance.md`).

### What This Shared Identity Must Guarantee

**1. Traceability to a single home document.** Because the I-address structurally encodes origin (`Node.0.User.0.Document.0.Element`), the shared identity means every appearance traces back to one home:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." (2/40)

**2. Correspondence across documents.** Shared Istream origin is precisely what lets the system know that two appearances *are the same content*. Per `concepts/correspondence.md`, "Shared Istream origin is the basis for correspondence." This is what enables refractive link-following:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

**3. Survival of the connection under editing.** Because links and inclusions attach to the shared bytes (via I-address) rather than to positions, the shared identity persists even as documents are independently edited:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

**4. Updates and attribution flow through the shared reference.** Since no copying occurs, a change at the source can propagate to all location-fixed windows, and attribution/royalty can be apportioned because the system knows the one true origin:

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update--especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." (2/36)

### In Short

The design must guarantee that transcluded content is **one identity referenced from many places, never many copies of one identity**. That single permanent Istream address is the shared common identity — and it is what makes attribution traceable (2/40), correspondence computable (2/26), links survivable (4/11), and updates coherent (2/36). The moment content is genuinely *copied* rather than transcluded, that shared identity is severed and, in Nelson's terms, the copy becomes "frozen and dead, lacking access to the new linkage" (2/48).
