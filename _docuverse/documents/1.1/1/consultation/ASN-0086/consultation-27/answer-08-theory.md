## Question 8 [theory]

> In Nelson's design, was content always intended to be s_C-resident (i.e., is the content/link subspace partition a structural commitment that fixes content's first element-field at s_C), or is the subspace identifier a free parameter at content emission?

I'll read the raw pages covering the address subspace structure (4/30-4/31) to verify the design commitment before answering.

Let me check the raw pages for the precise subspace structure.

Based on the curated sources covering Nelson's tumbler design (4/26-4/31):

## Answer: Yes — structural commitment, not free parameter

The content/link partition is **fixed by the design**, not a free parameter at emission. Nelson explicitly assigns numerical subspace markers within the Element field:

**Byte addresses** use subspace `1`:
> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

**Link addresses** use subspace `2`:
> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" [LM 4/31]
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" [LM 4/31]

Nelson treats these as the only two element types stored in tumbler-space:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." [LM 4/23]

The subspace partition is therefore a **structural invariant**, not a choice exercised per emission:

1. **The address scheme itself encodes the type** — a byte cannot be emitted into the `0.2.N` pattern, nor a link into the `1.x` pattern, without violating the addressing semantics
2. **The two subspaces have different ordering disciplines**: bytes are V-stream-rearrangeable; links keep their creation-order addresses permanently:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

## What IS a free parameter

Nelson does leave room for **further subdivision within each subspace** as an extension point:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

So the *commitment* is: content's first element-field digit is always `s_C` (the byte subspace marker). The *extension* room is: digits *after* the position/serial number within either subspace.

## Caveat

NEED_RAW: 4/30-4/31 (raw pages 197-198) — to verify whether Nelson uses `1` literally as the byte-subspace marker (vs. it being implicit/elided) and whether `0.2` is one delimiter+marker or `0` followed by subspace `2`. The curated quotes are consistent with the structural-commitment reading, but the exact lexical form of the byte address ("`N.0.U.0.D.V.1.position`" vs "`N.0.U.0.D.V.position`" with implicit subspace) is worth confirming against the raw page.
