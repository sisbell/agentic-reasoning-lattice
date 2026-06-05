## Question 4 [theory]

> When new links come into existence partway through a windowed reading, where in the ordering must they appear relative to links the reader has already received?

## Answer

New links must appear **after** every link the reader has already received. The ordering is append-only: links occupy a permanent order of arrival, and anything that comes into existence later is necessarily later in the sequence.

### Why the ordering forces this

In Xanadu, links are addressed sequentially by creation order, and that order is fixed forever:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

A link's serial position is part of its permanent address — the first link is `N.0.U.0.D.V.0.2.1`, the 755th is `N.0.U.0.D.V.0.2.755`. Crucially, this numbering is never reshuffled:

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

Unlike bytes, which can be rearranged in the Vstream, links keep their creation-order addresses permanently. Deleting link `2.5` doesn't renumber `2.6` onward (see `links` concept, "Permanent Order of Arrival"). Because the next link to arrive always takes the next-higher serial number, a link created partway through a reading lands at the tail of the ordering — past everything already delivered.

### Why this matters for the reader

This append-only ordering is exactly what lets a reader distinguish "new" from "already seen." Nelson relies on it explicitly in the mail mechanism, where the reader queries for material newer than what they've consumed:

> "The user 'opens the mailbox' with a front-end request for items with a mail link more recent than the material already seen." (4/55)

The same property underwrites paginated link retrieval (`FINDNEXTNLINKSFROMTOTHREE`), which iterates through links in order: links appended at the end while you read won't disturb the portion you've already traversed. And it's consistent with the search guarantee that link volume doesn't interfere with ongoing retrieval:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

### Summary

Because link addresses reflect a permanent order of arrival and are never renumbered, any link that comes into being during a windowed reading must fall **after** all links already received — at the current end of the sequence. This is what makes "show me what's arrived since I last looked" a well-defined operation.

(One note on scope: the curated sources establish the permanent-arrival ordering of links and the "more recent than already seen" reader model directly. They don't contain a passage discussing this specifically in the context of *windowed* reading, so the application to windowing is an inference from the general link-ordering guarantee rather than an explicitly stated rule. If you want Nelson's exact treatment of link delivery during windowed reads, NEED_RAW: 4/55–4/60.)
