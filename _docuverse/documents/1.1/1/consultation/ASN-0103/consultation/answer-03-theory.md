## Question 3 [theory]

> What distinguishes a freshly authored document from one born by versioning, from the standpoint of what each shares with prior documents?

## What distinguishes them: native content vs. inherited content

The core distinction is **what each document shares with prior documents at the level of Istream (content identity)** — and whether that sharing is automatic or deliberate.

### A freshly authored document shares nothing by default

A new document is created empty. Per Nelson's operations (4/65):

> "CREATENEWDOCUMENT: This creates an empty document. It returns the id of the new document."

Everything written into it becomes **native bytes** — new content stored under that document's control, with fresh Istream addresses:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." (4/11)

Because the content is born here, it shares **no Istream origin** with any prior document. Crucially, content identity is based on creation, not on value — two documents that independently contain the same words have *different* I-addresses. A fresh document therefore has no automatic correspondence to anything else, even if it happens to say the same thing.

A fresh document *can* come to share content with prior documents — but only through a **deliberate act of transclusion** (COPY/windowing), which makes specific spans inclusions that retain the source's I-addresses. Sharing is opt-in and span-by-span.

### A document born by versioning shares everything by inheritance

A versioned document begins as a complete inclusion of its parent. Per Nelson's operations (4/66):

> "CREATENEWVERSION: This creates a new document with the contents of document <doc id>. It returns the id of the new document. The new document's id will indicate its ancestry."

So versioning differs in two ways a fresh document does not:

1. **Shared Istream by default.** Every byte of the new version initially maps to the *same* Istream content as the parent — it is "effectively transclusion of entire document." The two are different Vstream arrangements over a shared Istream. This shared origin is what makes **correspondence** automatic and structural, not metadata that must be tracked:

   > "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

   This is also why a new version doesn't damage its source: "users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals. This is done by inclusion links." (2/45)

2. **Ancestry encoded in the address.** The version's tumbler ID is forked beneath the parent's document number, recording lineage. Nelson adds an important caveat that this lineage is positional, not semantically binding:

   > "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29)

   So the tumbler shows *where* the version sits in the forking tree, but the meaningful shared substance is the shared Istream content, not the number.

### Summary

| | Freshly authored | Born by versioning |
|---|---|---|
| Initial content | Native bytes, new Istream | All content inherited as inclusions of parent's Istream |
| Sharing with prior docs | None — unless author deliberately transcludes | Total by default — shares parent's Istream |
| Correspondence | None automatically (same words ≠ shared identity) | Automatic and structural, via shared I-addresses |
| Address/ancestry | New document number, no lineage | ID forked under parent, "indicates its ancestry" (4/66) |

The deepest point: a fresh document's relationship to others is something an author *builds* (by linking and windowing); a version's relationship to its parent is something the system *inherits* the moment it's created.
