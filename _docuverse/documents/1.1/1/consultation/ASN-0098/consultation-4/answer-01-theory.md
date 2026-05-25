## Question 1 [theory]

> Was the arrangement map M(d) designed to be subspace-stratified — with referential integrity stated per-subspace (M(d)|_text ⊆ dom(C) and M(d)|_links ⊆ dom(L)) — or was a single global constraint ran(M(d)) ⊆ dom(C) intended, in which case link subspaces are arranged differently?

Looking at the question carefully: you're asking about the formal design of M(d) — whether it's a single function with one global constraint, or stratified into per-subspace functions each with its own referential target.

Let me check the original pages to verify the link/byte address structure before answering.

[Reading raw pages would be ideal here. Based on the curated sources, here's what I can establish:]

## Nelson Designed It as Subspace-Stratified

The evidence from Literary Machines supports the **subspace-stratified** interpretation, but with an important asymmetry between subspaces.

### Two Distinct Subspaces in the Document Address Structure

Nelson's tumbler scheme explicitly separates bytes from links within a document:

From the `links` extraction (4/31):
- `N.0.U.0.D.V.0.1.position` — bytes (text subspace, prefix `0.1`)
- `N.0.U.0.D.V.0.2.N` — links (link subspace, prefix `0.2`)

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" — 4/31
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" — 4/31

So a document's local element-space is partitioned: subspace `0.1` for bytes, subspace `0.2` for links. This is structural, not implementation-derived.

### Each Subspace Has Different Arrangement Semantics

This is the crucial point that bears on your question. Nelson explicitly distinguishes how the two subspaces behave:

**Bytes** are rearrangeable in Vstream:
> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." — 4/30

**Links are NOT rearrangeable:**
> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." — 4/31

From the curated `i-space-addresses`:
> "Links: 'The digit after the '3' is a link-address designating the link's serial position' — links are currently not rearrangeable"

### What This Implies for M(d)

A single global `ran(M(d)) ⊆ dom(C)` constraint is **inconsistent with Nelson's design**, because:

1. The link subspace `0.2.N` doesn't reference content bytes — it indexes link objects (which themselves point into the docuverse via endsets).
2. The text subspace `0.1.position` references content via Istream addresses.

These have different domains. A unified `dom(C)` would collapse the distinction Nelson explicitly maintains between byte storage and link storage.

The stratified interpretation matches Nelson's structure:
- `M(d)|_text` lives in the rearrangeable Vstream and maps text-subspace positions to Istream content addresses
- `M(d)|_links` is monotone (creation-order only) and maps link-subspace positions to link records owned by d

### Asymmetry Worth Noting

The stratification is real, but the two strata are not symmetric in degrees of freedom:
- `M(d)|_text` is a **mutable** arrangement (INSERT/DELETE/REARRANGE operate here)
- `M(d)|_links` is **append-only** (links keep permanent serial position; only link creation and link deletion affect it, never rearrangement)

> "Unlike bytes (which can be rearranged in Vstream), links keep their creation-order addresses permanently"

### Nelson's Own Words on Native vs. Non-Native Bytes

The text-subspace mapping is genuinely a referential one, not a content-identity one — transcluded bytes get Vstream positions even though their content lives elsewhere:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." — 4/11

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." — 4/11

This confirms `M(d)|_text` maps into a content-address domain (which can include I-addresses owned by *other* documents), not into local storage offsets.

## Bottom Line

**Subspace-stratified, with per-subspace referential integrity** matches Nelson's design intent. The global `ran(M(d)) ⊆ dom(C)` formulation does not — it would erase the explicit `0.1` vs `0.2` partition and ignore the different arrangement semantics Nelson specifies for each subspace.

## Caveat on Formalization

NEED_RAW: 4/30–4/31 (raw pages 197–198) for direct verification that Nelson treats byte-position assignment and link-position assignment as separately-typed mappings rather than a single function. The formal notation `M(d)`, `dom(C)`, `dom(L)` is not Nelson's — he describes the structure in prose and address-syntax examples, not set-theoretic equations. The stratification is clearly *present* in the address scheme and the arrangement rules; whether Nelson would have endorsed your specific formalization as opposed to some other one (e.g., two separate maps `M_text(d)` and `M_links(d)` rather than a single M restricted by subspace) is a modeling choice the text doesn't decide.
