## Question 2 [theory]

> Did the design intend MAKELINK to be the sole link-creation primitive, or did it contemplate a distinct facility for creating type endsets that reference ghost/non-content addresses (L9)?

## Answer

The design intended **MAKELINK to be the sole link-creation primitive**. Nelson did *not* contemplate a distinct facility for creating type endsets that reference ghost/non-content addresses — and the reason is architectural: ghost addresses require no creation step at all.

### MAKELINK takes the type endset directly

In the XU.87.1 command set, MAKELINK accepts all three endsets (including the type) as arguments:

> "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." (4/68)

The type — the "three-set" — is just a parameter. There is no companion command to "register" or "instantiate" a type. The full list of 17 operations in XU.87.1 contains no type-creation or ghost-element-creation primitive; the only link-creating operation is MAKELINK.

### Ghost addresses need no facility because nothing is stored

The whole point of the ghost-element design is that you reference an address *without* anything existing there. Search matches the address, not stored content:

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

And from the tumbler-space model:

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage." (4/23)

So a type endset pointing to a ghost address is not "created" in any sense — you simply choose an address and pass it to MAKELINK as the three-set. Because matching is by address rather than by content, there is nothing to allocate, store, or initialize. A separate facility would be redundant.

### Why this matters to the design

This is a deliberate consequence of treating all three endsets symmetrically:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

Type-extensibility — "any user may define his or her link types for a particular purpose" (4/43) — is achieved precisely *because* no creation facility is needed. Defining a new type means nothing more than picking an address and using it as the three-set in MAKELINK. Requiring a distinct creation step would undermine the open-ended, schema-free type system Nelson describes.

### Conclusion

MAKELINK is the single link-creation primitive. Type endsets that reference ghost/non-content addresses are handled within MAKELINK by passing the chosen address as the three-set; the ghost-element design intentionally eliminates any need for a separate creation facility, since matching is by address and ghost addresses store nothing.

(One caveat: the curated sources cover the XU.87.1 command set and the ghost-element semantics thoroughly, but they don't contain an explicit sentence stating "there shall be no separate type-creation command." That conclusion follows from the absence of such a command in the operation list plus the explicit "no need for the presence of elements" principle. If you want to confirm no auxiliary facility is mentioned in the full protocol discussion: NEED_RAW: 4/43-4/45, 4/61-4/70.)
