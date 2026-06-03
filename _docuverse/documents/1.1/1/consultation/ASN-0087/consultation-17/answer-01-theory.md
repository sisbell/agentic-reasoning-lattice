## Question 1 [theory]

> Did the design intend links to occupy a canonical depth within a document's link subspace, or is the depth at which a document's first link is placed semantically arbitrary?

I don't have the Read tool available in this context, so I'll answer from the curated sources, which contain verified quotes from the relevant page (4/31).

## Answer

The design intends links to occupy a **canonical depth** within a document's link subspace. The depth of a document's first link is **not** semantically arbitrary — it is fixed by the address structure.

### The link subspace has a fixed shape

A document's local address space is partitioned into subspaces by a numeric marker after the version digit:

| Subspace | Address pattern | Contents |
|----------|-----------------|----------|
| Bytes | `version.position` (`0.1`) | Text content |
| Links | `version.0.2.N` | Links the document is home to |

The first link of a document sits at a canonical position — serial number `1` within the `0.2` link subspace:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

So the first link is at depth/position `...0.2.1`, the 755th at `...0.2.755`. The depth (the subspace marker plus serial position) is structurally determined, not chosen.

### Links are placed by permanent order of arrival

The serial position is canonical because it reflects creation order, which never changes:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

This means link `2.1` is *always* the first link created in that document, and deleting an earlier link does not renumber the others. There is no freedom to place the first link at an arbitrary depth — it is the first arrival, at serial position 1.

### Contrast with what *is* arbitrary

Nelson explicitly marks a *different* part of the address as semantically arbitrary — the version/subdocument digit, whose value implies nothing about derivation:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

That arbitrariness applies to version numbering, **not** to link depth. Link depth is canonical; the system relies on it for permanent, order-stable link addresses.

### Caveat on further subdivision

Nelson notes that links *could* be subdivided further beneath their serial position, but treats this as open/future, not as a reason the base depth is arbitrary:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

### One inconsistency worth flagging

The curated sources contain two representations of the link-subspace marker. The link-address material (4/31) uses `0.2` for the link subspace; the Istream element-field description gives the marker as `3` ("The digit after the '3' is a link-address designating the link's serial position"). Both agree that the *serial position* is canonical and order-of-arrival, but they disagree on the subspace digit itself.

NEED_RAW: 4/30–4/31 — to confirm the exact subspace marker (`2` vs `3`) and verify the canonical depth claim against Nelson's original diagram.

**Bottom line:** the depth is canonical. A document's first link is deterministically placed at serial position 1 in the link subspace, in permanent order of arrival — not at an arbitrary depth.
