## Question 1 [theory]

> Was RETRIEVEV's spec-set intended to designate only ordinal, deepest-action-point spans (one position per deepest digit), or may a single span name a coarser tumbler range that spans a subspace boundary?

The curated material is enough to give a confident answer on the conceptual through-line. Here's the synthesis.

## Short answer

RETRIEVEV's spec-set was **not** intended to be limited to ordinal, deepest-action-point spans. It inherits the full generality of the span machinery, where a single span is a *subtree* whose contents are implicit in its endpoints — so a span can legitimately name a coarse tumbler range. But there's an important caveat about the *subspace boundary* specifically, which I'll flag as inference rather than something Nelson states outright.

## The reasoning

**1. Spans are subtrees, not enumerations of deepest points.**

Nelson is explicit that a span's interior is determined by its endpoints, and those endpoints may sit at *any* level of the tree, not just the deepest:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

> "A span may be visualized as a zone hanging down from the tumbler line--what is called in computer parlance a depth-first spanning tree." (4/25)

So the "one position per deepest digit" reading is the *degenerate* case, not the intended general form. Nelson even names that degenerate case as such in the curated spans material ("or merely to a series of elements of the same type, which is a degenerate case of a subtree," 4/24).

**2. Coarse ranges are explicitly in scope.**

> "In fact, a tumbler-span may range in possible size from one byte to the whole docuverse on the whole network." (4/24)

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." (4/38)

Spec-sets ("request sets") are simply sets of these spans (4/37). Nothing in the curated description of RETRIEVEV narrows that generality:

> "RETRIEVEV: This returns the material (text and links) determined by <spec set>." (4/67)

The phrase **"text and links"** is the tell. A single deepest-digit byte span lives in the byte subspace only. The fact that RETRIEVEV is documented as returning *both* text and links from one spec-set means the spec-set is expected to reach across the byte (`0.1`) and link (`0.2`) subspaces — it is not confined to a single ordinal byte run.

## The caveat — where I'm inferring

Whether a *single span* is meant to **cross** the byte/link subspace boundary (start in `0.1`, end in `0.2`, sweeping both as one depth-first zone), versus a *spec-set of two spans* (one in `0.1`, one in `0.2`) doing the boundary-spanning, is **not settled by the curated text.**

The depth-first-spanning-tree definition (4/25) technically permits one span from the first byte to the last link to enclose both subspaces. But the design of the companion operation cuts the other way:

> "RETRIEVEDOCVSPANSET: This returns a span-set indicating both the number of characters of text and the number of links in document." (4/68)

Returning a document's full extent as a span-*set* with **separate** byte and link counts strongly implies that bytes and links are normally addressed as *distinct spans within a set*, not as one coarse span straddling the `0.1`→`0.2` divide. That is the more natural reading of Nelson's intent: coarse spans are fine *within* a homogeneous region, and boundary-spanning is achieved by *composing spans into a spec-set* rather than by one span jumping subspaces.

## Bottom line

- **Coarse spans: intended.** A single span may name a range above deepest-digit granularity (up to whole documents, authors, servers, the docuverse). The "one position per deepest digit" form is the degenerate special case.
- **Subspace boundary: handled by the spec-set, most likely not by a single span.** RETRIEVEV's "text and links" result is achieved because the *spec-set* spans both subspaces; the span-set design of RETRIEVEDOCVSPANSET suggests Nelson pictured bytes and links as separate spans composed together, not one span crossing the boundary.

The first point is well-grounded in Nelson's own words. The second is my inference from how the paired retrieval operations are shaped — Nelson never explicitly rules a boundary-crossing single span in or out.
