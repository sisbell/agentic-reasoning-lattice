## Question 4 [theory]

> Why must the count of text and the count of links be reported as separate measures rather than as a single combined extent?

## Why text-count and link-count are reported separately

The short answer: in Xanadu, text and links live in **different subspaces** of a document's address tree, with **different ordering rules**, so they cannot be captured by one contiguous span. That is why `RETRIEVEDOCVSPANSET` returns a *span-set* (two spans) rather than a single extent.

### Two distinct subspaces under the document

Within a document version, bytes and links occupy separate branches of the tumbler tree:

- Bytes (text): `N.0.U.0.D.V.0.1.position` — the **1** subspace
- Links: `N.0.U.0.D.V.0.2.N` — the **2** subspace

Because a tumbler-span designates a *subtree* — "a zone hanging down from the tumbler line" (spans, 4/25) — and the text and links hang from two different subspaces (0.1 vs 0.2), no single start-to-end span can cover both at once. To name "this much text *and* this many links" you need a span-set, which is precisely Nelson's mechanism for designating separated regions: "if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans" (4/25).

This is exactly the distinction between the two operations:

- `RETRIEVEDOCVSPAN` — "returns a span determining the origin and extent of the V-stream" (4/68): a single span.
- `RETRIEVEDOCVSPANSET` — "returns a span-set indicating both the number of characters of text and the number of links in document <doc id>" (4/68): two measures, two spans.

### Different ordering semantics

The two subspaces are not just separated — they count differently. Bytes can be rearranged by editing (their Vstream order is fluid), while links keep their **permanent order of arrival**:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

So the link "extent" is a creation-ordered count (link 1 through link N), whereas the text "extent" is a positional count in the current arrangement. These are categorically different quantities. Collapsing them into one number would be meaningless, since a tumbler-span "does not designate the number of bytes contained. It does not designate a number of anything" (4/24) — it designates a region of a particular subtree.

### Why this matters

Reporting them separately lets a front end know, in one call, both how much content and how many links a document has — each measured in its own subspace, by its own rule. A combined extent would conflate two different address regions with two different ordering disciplines, losing the information a front end actually needs (e.g., to paginate text versus to iterate links).

**Summary:** text and links are separate measures because they live in separate document subspaces (0.1 vs 0.2), are counted under different rules (rearrangeable byte positions vs. permanent link arrival order), and a tumbler span only covers one contiguous subtree — so the honest representation is a span-set with one span per subspace, which is what `RETRIEVEDOCVSPANSET` returns (4/68, 4/31, 4/24-4/25).
