## Question 2 [theory]

> Does the design treat creation of a document's second-and-later versions as the same "fork"/version-creation-with-ancestry operation as the first version, or is "fork" specifically the first-version act?

## Short answer

The design treats version creation as a single, **uniform, recursive forking operation** — not as a special "first-version" act. Creating a document's second, third, or Nth version is the same `CREATENEWVERSION`-with-ancestry operation each time. "Fork" is the general subdivision mechanism, applied repeatedly, not a one-time event tied to the first version.

## Why

**1. Forking is "a single mechanism" applied recursively to any numbered item.**

Nelson is explicit that the same branching process governs all levels of the docuverse, and that it composes — a daughter item can itself fork daughters:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." (4/19)

> "if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." (4/20)

The forking concept page makes the recursion concrete: "Item 2 can become 2.1, 2.2, 2.3... and item 2.4 can become 2.4.1, 2.4.2, 2.4.3... with no limit." Item `2.4` forks exactly the way item `2` does. There is no privileged "first" subdivision.

**2. The version/subdocument number is created by the same continual subdivision of the Document field.**

> "The Document field of the tumbler may be continually subdivided, with new subfields in the tumbler indicating daughter documents and versions." (4/29)

"Continually subdivided" describes an ongoing, repeatable act — every version is just another daughter under the document, addressed the same way as the one before it. Nelson also flattens any special semantics here:

> "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

**3. The operation itself (`CREATENEWVERSION`) is parameterized over *any* document, and versions are documents.**

> "This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry." (4/66)

Because a version is itself a "subdocument" (4/29), it can be supplied as the `<doc id>` to `CREATENEWVERSION` in turn — so version 3 can be forked from version 2 using the identical operation that produced version 2 from the original. Ancestry is recorded uniformly ("will indicate its ancestry"), regardless of which generation you are on. The versions concept page summarizes this as "Alternative versions branch from common ancestors."

## The one genuine asymmetry (and it isn't "first version")

The only distinct operation is bringing a document into existence at all:

> `CREATENEWDOCUMENT` — "This creates an empty document. It returns the id of the new document." (4/65)

This forks a document out of an *account* and starts empty, whereas `CREATENEWVERSION` forks a daughter that **inherits content and records ancestry** (4/66). So the meaningful boundary is *create-document* (empty, forked from account) vs. *create-version* (content-inherited, ancestry-bearing) — and the latter is the same act for the second version as for the hundredth. The "fork = version-with-ancestry" operation is uniform across all versions, not reserved for the first.

One caveat: the curated sources show the recursion of forking in general (2 → 2.4 → 2.4.1) and confirm versions are continually-subdivided subdocuments, but they don't contain a worked example explicitly forking "version 3 from version 2." That conclusion follows from combining the uniform forking mechanism (4/19–4/20) with versions-as-subdocuments (4/29) and `CREATENEWVERSION` over any `<doc id>` (4/66), rather than from a single direct statement.
