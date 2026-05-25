## Question 6 [theory]

> In the Literary Machines design, are document-level containers (the entities at `dom(Σ.M)` with `zeros = 2`) intended to be first-class targets of typed relations, or are relations specifically meant to target content-level addresses (the entities at `dom(Σ.C)` with `zeros = 3`) within those containers?

**Document-level containers are first-class targets of typed relations.** The system is designed so that endsets may point to *any* address in the docuverse — at any granularity from a single byte to the entire docuverse. Document-level addresses are not merely accessible to relations; certain link types exist *specifically* to operate at that level.

## Three lines of evidence

**1. Metalinks are defined as document-targeting link types.**

Nelson establishes an entire link-type category for whole-document relations:

> "METALINKS: These are links expected to apply to whole documents, whether from outside or from inside." [LM 4/52]

> "While the title and the author's name ordinarily reside inside a document (though not necessarily at the beginning), the 'author' and 'title' links will normally go from the author's name and the principal appearance of the title to the whole document." [LM 4/52]

Title, Author, and Document Supersession are explicitly document-level types. The Document Supersession Link "indicates that one document or version supersedes another" [LM 4/52-4/53] — its semantics require it to target a document container, not a byte span within one.

**2. Ghost elements make container-level addresses valid link targets.**

Nelson explicitly addresses what happens when nothing is stored at a container's address:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them. A link to or search of an account or node will find any of the documents under it." [LM 4/23]

So linking to a container is not a degenerate case — it has defined semantics: the link "embraces all the contents below" the addressed node. This works *above* document level (accounts, nodes) and therefore certainly at document level.

**3. The span system explicitly supports container-level granularity.**

> "The first point of a span may designate a server, an account, a document or an element; so may the last point." [LM 4/25]

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server--or the entire docuverse." [LM 4/38]

Because endsets are span-sets and spans can target documents directly, the link mechanism inherits this granularity for free.

## Important nuance: BOTH levels are first-class

The design is not "containers OR content" — it is "any address, any granularity." Ordinary text links (connection, comment, citation, quote-link) typically target content-level spans because they connect *passages*. Metalinks target document containers because they describe *works*. Both are equally legitimate.

The architectural reason this works uniformly is that endsets, types, and homes all share one mechanism:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

There is no privileged address level. The container/content distinction is semantic (chosen by the link type and the author's intent), not structural (enforced by the system).

## Answer

**Yes** — document-level containers are intended to be first-class targets of typed relations. Nelson designed an entire link-type family (metalinks) for exactly this purpose, defined ghost-element semantics so that container addresses behave as valid targets even without stored elements, and built the span system so that any address level (server, account, document, element) can appear as a span endpoint. Content-level targeting and container-level targeting are both first-class; the choice between them is a semantic decision belonging to the link type, not a structural restriction imposed by the system.
