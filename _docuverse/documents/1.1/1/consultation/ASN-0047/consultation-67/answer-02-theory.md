## Question 2 [theory]

> At document creation, are a document's content and link sub-allocators conceptually one allocator with two reserved frontiers, or two distinct allocators sharing a document-level root?

# Two Distinct Allocators Sharing a Document-Level Root

Under the document-version root `N.0.U.0.D.V`, the document branches into two sibling subspaces, each with its own independent sequential allocator:

- Subspace `1` allocates **bytes**
- Subspace `2` allocates **links**

From LM 4/31:
> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)"
> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)"

The two allocators are **semantically distinct** — this is the deeper reason they cannot be a single allocator with two frontiers:

- **Bytes** live in V-space and can be rearranged. Their positions reflect the current ordering, which "may be constantly changing" (LM 4/11).
- **Links** "are in their permanent order of arrival. A document includes only the links of which it is the home document" (LM 4/31). They are not rearrangeable.

This follows the general forking principle: "The owner of a given item controls the allocation of the numbers under it" (LM 4/20). The document owns its root number; under that root it baptizes two child subspaces with different allocation rules.

The `0.2` notation reveals the structure: the `0` is a delimiter (one of the "three major dividers" of LM 4/28), then `2` designates the link subspace as a distinct branch. The further open-endedness — "The subdivision of links by further digits (after '2' and the position) is a distinct possibility" (LM 4/31) — confirms that subspace `2` is its own tree, not a partition of a unified counter.

So conceptually: one document, one ownership root, two independent sub-allocators below it.

NEED_RAW: 4/30 for direct confirmation of the bytes-subspace prefix (curated sources show links use `0.2.N` and imply bytes use the parallel `0.1.N` form, but I don't have a verbatim quote for the byte-side prefix).
