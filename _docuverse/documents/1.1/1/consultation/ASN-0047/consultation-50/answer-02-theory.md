## Question 2 [theory]

> Does the design intend that each link in a document's link subspace appear at exactly one V-position — i.e., is link-arrangement multiplicity within a single home document constrained to ≤1, or may the same ℓ be placed at multiple link-subspace V-positions?

## Answer

**Yes, the design intends link-arrangement multiplicity within a single home document to be constrained to ≤1.** Each link in a document's link subspace occupies exactly one V-position, fixed by its order of creation; deleted links occupy zero positions.

### Direct evidence from Nelson

From page 4/31 (raw page 198), in the section "The link section":

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document."

The address format Nelson gives is unambiguous about serial identity:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)
> N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)"

The position digit (1, 755) is the link's "serial position," not an arrangement slot that could be reassigned. Note also Nelson's explicit asymmetry on the same page (4/31) between bytes and links: bytes "may be rearranged at the conceptual level of viewing on a screen... visible only through the layer of links" — but for links themselves he specifies only the permanent order-of-arrival numbering. There is no parallel statement of a rearrangeable link layer.

### Structural argument from the operation set

The FEBE operation set (LM 4/61–4/70) includes no operation to place an existing link at a new position in its home document's link subspace:

- **MAKELINK** allocates a fresh sequential link address ("It returns the id of the link made," 4/68) — it does not accept an existing ℓ
- **COPY** is defined for content spans (bytes); there is no COPY-link operation
- **REARRANGE** acts on byte regions, not link positions

Bytes can be multiply-positioned within a document via transclusion (COPY creates a V→I mapping to existing Istream content). Links have no analogous mechanism — every MAKELINK produces a new link object at a new serial position.

### What ≤1 (not =1) covers

The diagram on 4/9 (raw page 176) lists "DELETED LINKS" as a valid document state, annotated:

> "(not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

A deleted link sits at 0 positions in the current link-subspace view (still recoverable via historical backtrack at its serial address). An active link sits at exactly 1. Hence ≤1, with 0 reserved for the deleted/retracted case.

### Caveat on future extension

Nelson does flag, on 4/31, that the position-digit structure could be elaborated:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed."

But this is offered as a future possibility for what additional digits *under* a link's position could mean — not a mechanism for placing the same link at multiple positions in the link subspace.

### Why the asymmetry

Links are themselves first-class addressable objects (so they can be link-to-link targets, LM 4/49–4/51). A stable, single, permanent address per link is required for that downstream addressability to work. If a link could appear at multiple V-positions, "the address of link ℓ" would not be well-defined, and link-to-link references would be ambiguous.

NEED_RAW: nothing in the curated sources states "each link appears at exactly one V-position" verbatim — the constraint is derived from (a) "permanent order of arrival" (4/31), (b) the absence of any link-rearrangement or link-transclusion operation in the FEBE set (4/61–4/70), and (c) the requirement that link addresses be stable targets for link-to-link (4/49–4/51). If you want a categorical Nelson quote forbidding multi-positioning, none exists; the prohibition is structural rather than stated.
