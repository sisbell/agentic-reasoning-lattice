## Question 1 [theory]

> In your design, are subspace identifiers (specifically the content subspace `s_C` and the link subspace `s_L`) intended as primitive distinct constants of the address-space partition, or is their distinctness an emergent property derivable from other design commitments?

# Subspace Identifiers: Primitive Distinct Constants

The distinction is **primitive**, not emergent.

When I designed the address structure, the partition between bytes and links was a foundational commitment, not something derived from other properties. The element field of a tumbler address contains a deliberate subspace marker that says *what kind of thing this address designates*: `0.1` for bytes (content), `0.2` for links.

You can see this in the link address structure I specified at 4/31:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)"
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]

And for bytes at 4/30:

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

## Why Primitive, Not Emergent

The two subspaces have **fundamentally different semantics** that cannot be derived from anything else:

1. **Bytes are rearrangeable in Vstream**; links are not. Bytes have V-positions that shift under editing; links retain their creation-order position permanently. As I noted: "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

2. **Bytes and links have different population rules**. Bytes are populated by INSERT/APPEND into the document's text space. Links are populated by MAKELINK and keyed by serial arrival order.

3. **The partition pre-exists any content**. An empty document already has a 1-subspace (for future bytes) and a 2-subspace (for future links), even though nothing inhabits either. This is the signature of a primitive distinction, not an emergent one.

## What Could Be Emergent (But Isn't)

One might imagine deriving the partition from element behavior — "links are whatever has three endsets, bytes are whatever doesn't." But this gets the design backwards. The address-space partition is what *enables* the system to know which storage and indexing machinery to invoke before it ever examines the element. The subspace identifier is consulted at lookup time; the element's structure isn't.

I also flagged at 4/31 that further subdivision was an open design space:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

This anticipates **additional** primitive subspaces (link sub-types, perhaps) — again pointing to subspace identifiers as designed partitions rather than emergent properties.

## What Is Conventional

The *specific numerals* (`1` vs `2`) are conventional — they could have been any distinct integers. What is non-negotiable is that the partition exists and that its members are distinct constants chosen at design time.

---

**NEED_RAW: 4/30-4/31** — for the full element-field specification including the precise subspace layout. The curated sources confirm `0.1` for bytes and `0.2` for links, but the original pages would let me verify whether I documented any additional subspaces (e.g., a `3` subspace) that the curated extracts may have collapsed. The mention of "the digit after the '3'" in one curated note conflicts with the `0.2` link convention elsewhere, and only the raw text resolves that.
