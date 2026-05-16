## Question 3 [theory]

> Does the Xanadu design contemplate versioning at the account level or node level — i.e., are addresses of the form `[N,0,U,1]` (account-shaped sibling at deeper tumbler depth) or analogous node-level extensions intended as "account versions" or "node versions," or is versioning reserved to documents alone (LM 4/29)?

Let me verify the exact context on LM 4/29 by reading the original page.

[Reading page 196 to verify 4/29 content]

Based on the curated sources, here's my answer:

**Versioning is reserved for documents.** Nelson scopes the "version" concept specifically to the Document field of the tumbler:

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." (LM 4/29)

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (LM 4/29)

The **forking mechanism itself is universal** across all four tumbler fields — but Nelson distinguishes its semantic use:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." (LM 4/19)

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (LM 4/19)

Note the parallel structure: nodes have **descendant nodes**, accounts spin off **accounts**, but only documents are described as having "daughter documents *and versions*."

**The distinction Nelson draws:**
- Node subdivision = network growth, sub-stations descended from parents
- Account subdivision = delegation, sub-accounts under user control ("once assigned a User account, the user will have full control over its subdivision forevermore" — LM 4/29)
- Document subdivision = daughter documents *and versions* (the prismatic document model)

So an address like `N.0.U.1` (sub-account 1 under user U) is a **sub-account** (a delegated child account), not an "account version." There is no concept of "account version" or "node version" with the prismatic, historical-backtrack, correspondence-tracking semantics that "version" carries for documents.

**Caveat on architectural uniformity:** Because the forking mechanism is uniform, the *mechanics* would permit using account-level or node-level subdivisions for versioning-like purposes. But Nelson never describes this, and the version semantics — prismatic storage, intercomparison, historical backtrack, refractive link-following — are presented exclusively in the context of documents (LM 2/13-2/22, 2/26).

NEED_RAW: 4/29 (full context around the "accidental extension" passage to verify whether Nelson explicitly excludes account/node versioning or just doesn't address it)
