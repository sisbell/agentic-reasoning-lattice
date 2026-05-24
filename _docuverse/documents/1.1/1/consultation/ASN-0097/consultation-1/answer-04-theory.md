## Question 4 [theory]

> At link creation, did the design intend endset coverage to be restricted to already-allocated I-addresses, or are forward references (to addresses not yet in `dom(C)`) permitted?

## Forward references ARE permitted in Nelson's design

Endset coverage is **not** restricted to already-allocated I-addresses. The addressing system is purely conceptual — tumbler-space is populated by positions, while storage fills in only selected points. Links can address positions where nothing is stored.

### Direct evidence: Ghost elements

Nelson explicitly defines and endorses "ghost elements" — addressable positions that have no corresponding stored object:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them. A link to or search of an account or node will find any of the documents under it." [LM 4/23]

This last quote is unambiguous: links may be created targeting addresses where nothing is stored.

### The type endset is explicitly ghost-eligible

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

### Symmetry principle extends this to all three endsets

Nelson's design treats the three endsets identically:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

"Anywhere in the docuverse" includes ghost positions, since the docuverse is "the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage" [LM 4/23].

### What this enables architecturally

1. **Hierarchical embrace** — A link to an account or node address implicitly covers all content beneath it, even content created after the link.
2. **User-defined link types** — Type addresses serve as semantic tags; nothing need be stored at them.
3. **Forward-reference compatibility** — Because endsets attach to addresses (not stored bytes), allocation order is irrelevant.

### Caveat: survivability is asymmetric

Nelson's survivability statement is about *deletion* of previously-existing bytes, not about *never-existing* bytes:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." [LM 4/43]

He does not explicitly address the case of a from-set/to-set pointing to an address where data never existed (as opposed to ghost type endsets, which he discusses directly). But the addressing model permits it, and the hierarchical-linking quote at 4/23 confirms the system supports endsets covering ranges that may be populated later.

### Bottom line

Design intent: **No restriction.** A FEBE `MAKELINK` operation should accept endsets that reference positions outside `dom(C)`. The address space is the universe; storage is a subset of populated points within it. Restricting endsets to `dom(C)` would violate the ghost-element principle and break hierarchical linking semantics that Nelson explicitly calls out at LM 4/23.
