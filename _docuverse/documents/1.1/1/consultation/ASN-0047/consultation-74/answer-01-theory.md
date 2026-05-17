## Question 1 [theory]

> Does Literary Machines pin the link-subspace depth (so that the first link is always `[N.0.U.0.D.0.2.1]` with depth 2), or is the depth a design parameter left to the implementer?

I should answer from the curated sources directly — I don't actually need the auth tool for this. Apologies for that misfire.

## Answer

**Depth is a design parameter, not pinned.** Nelson establishes `2.N` (depth 2 — subspace identifier `2` plus a single position) as the convention in XU.87.1, but explicitly contemplates further subdivision.

From the **links** curated source (citing 4/31):

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)"
>
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)"
>
> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

That last sentence is the decisive one: Nelson flags depth extension as open future work.

**Two corrections to the address in your question:**

1. Nelson's format includes the **version** digit (`V`), not just document: `N.0.U.0.D.V.0.2.1`, not `N.0.U.0.D.0.2.1`.
2. The `0` before `2` is a major divider (the third one, separating document/version from element); the subspace identifier `2` (vs. `1` for bytes) sits in the element field.

**Summary:** The XU.87.1 convention is fixed at `…0.2.N` (one position past the subspace tag), but Nelson treats further subdivision as an extension point rather than a hardwired limit.
