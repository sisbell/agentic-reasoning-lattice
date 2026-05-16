## Question 6 [theory]

> For spans with action-points in the document-prefix region (server, account, document fields), did the design intend their coverage to grow monotonically as new nodes/accounts/documents are allocated within their reach, and is this growth bounded by any allocator discipline?

Yes — monotonic growth of prefix-region span coverage was explicitly intended, and the discipline that produces it is the ownership-based "baptism" rule for forking new sub-numbers.

## Direct evidence of intentional monotonic growth

The clearest statement is at LM 4/25:

> "A span that contains nothing today may at a later time contain a million documents."

This is Nelson stating directly that a span's coverage expands as new content is allocated within its reach. The mechanism is structural:

> "A span may be visualized as a zone hanging down from the tumbler line—what is called in computer parlance a depth-first spanning tree." (4/25)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

Because a span's content is *implicit* in its endpoints (the entire subtree between them), and because the addressing tree grows by forking under existing prefixes, any new item baptized within a span's reach automatically becomes part of that span. The "1-position" convention makes this explicit:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server—or the entire docuverse." (4/38)

A span addressed as `1.2.0.1` (all documents on server 1, account 2) covers whatever exists under that prefix *at the time of evaluation* — not at the time of creation.

## The allocator discipline

Growth is produced by — and bounded only by — the baptism rule for forking numbers:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." (4/20)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

> "New items may be continually inserted in tumbler-space while the other addresses remain valid." (4/19)

What this gives the span:

- **Append-to-the-right only.** New items get fresh digits beyond the existing ones; no renumbering, no insertion between existing siblings. So the *identity* of every previously-covered item is preserved as the span grows.
- **Owner-gated allocation.** Only the owner of a prefix can introduce new daughters under it. So the entities that cause a prefix-region span to grow are exactly those baptized by the prefix's owner (or, recursively, by sub-owners they delegated to).
- **No size bound.** "Each integer has no upper limit" (4/19); each field is "expandable indefinitely" (4/26). The discipline shapes *how* growth happens; it does not cap *how much*.

## Net answer

The design intent is: prefix-region spans grow **monotonically and automatically** (today's empty span may hold a million tomorrow), the growth is **disciplined by ownership-gated, append-only forking** (so existing membership is never disturbed), and the growth is **unbounded in quantity** — Nelson's address fields are designed precisely to accommodate this.
