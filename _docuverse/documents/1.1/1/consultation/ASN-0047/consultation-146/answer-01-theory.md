## Question 1 [theory]

> Is the link-subspace V-position depth intended to be a specific fixed value (and in particular to match the content-subspace V-position depth), or is the design satisfied by any fixed per-document link depth?

## Answer

The design does **not** pin the link-subspace V-position depth to a specific fixed value, and in particular it is **not** intended to be forced to match the content-subspace depth. The two subspaces are distinguished by their *subspace marker*, not by their depth — and Nelson explicitly leaves the link depth open to extension.

### What the addressing actually does

Within a document's version, content and links live in distinct subspaces marked by a leading digit:

- **Bytes** sit under the `1` subspace. Per 4/30: *"The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address."*
- **Links** sit under the `2` subspace, numbered by arrival. Per 4/31: *"N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)"* and *"N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)."*

So disambiguation between content and links is handled by the `0.1` vs `0.2` subspace marker — *not* by the two having equal position depth. In XU.87.1 both happen to use a single position digit after their marker, but that coincidence is not the load-bearing mechanism.

### Why the depth is not fixed-and-matched by intent

Nelson explicitly flags that the link subspace may grow deeper:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

This is the decisive design-intent signal: Nelson did not commit links to a single position digit, let alone to *content's* depth. He anticipated links acquiring additional digits below the position. Therefore the design tolerates a link depth that differs from (and may exceed) the content depth.

The one invariant that does matter is **consistency of interpretation**: links are addressed "in their permanent order of arrival" (4/31), so a document needs a stable, parseable scheme. A fixed *per-document* link depth satisfies that requirement. But matching the content depth is incidental, not mandated.

### Summary

- The content/link distinction rests on the subspace marker (`1` vs `2`), so depths need not be equal to keep addresses parseable.
- A fixed per-document link depth is consistent with the design.
- Matching the content-subspace depth is **not** a design requirement — Nelson explicitly reserves the right to subdivide links "by further digits" (4/31).

NEED_RAW: 4/30–4/31 — I read the page images at `resources/literary-machines/raw/page-197.png` and `resources/literary-machines/raw/page-198.png` to confirm structure, but my claim that depth-equality is "incidental rather than mandated" is an inference from the subspace-marker design plus the subdivision quote, not an explicit statement by Nelson. If you want a verbatim statement that depth need not match, none exists; the support is the subdivision-possibility quote above.
