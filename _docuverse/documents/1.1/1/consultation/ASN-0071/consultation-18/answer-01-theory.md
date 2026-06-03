## Question 1 [theory]

> When a user names content at a coarser granularity than the source document's leaves (a depth-2 anchor over depth-3 content), is the transclusion query intended to discover everything in the named subtree, or must the query match the content's native granularity?

## Answer

**The transclusion query is intended to discover everything in the named subtree. A coarser-granularity anchor embraces all content beneath it — the query does *not* need to match the content's native (leaf) granularity.**

This follows directly from how Nelson defines spans. A span is not a flat range of leaves; it is a *subtree*, and its contents are determined implicitly by its endpoints, whatever their depth:

> "A span may be visualized as a zone hanging down from the tumbler line—what is called in computer parlance a depth-first spanning tree." (4/25)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

The crucial phrase is *"There is no choice as to what lies between; this is implicit."* When you name content at a depth-2 anchor, the depth-3 leaves below it are *implicitly* included — you don't enumerate them and you don't have to descend to their native level. The boundary determines the contents.

Nelson makes the coarse-over-fine case explicit in his "1-positions" design, where a single coarse address deliberately stands for everything below it:

> "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server—or the entire docuverse." (4/38)

The same principle governs searches and links made to a coarse address. Even when nothing is stored at the depth-2 position itself (a ghost element), the address still reaches the finer content under it:

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

> "A link to or search of an account or node will find any of the documents under it." (4/23)

So a depth-2 anchor over depth-3 native content behaves like a link/search to a node over its leaves: it *embraces all the contents below.*

For the transclusion path specifically, the relevant operations confirm subtree-discovery semantics rather than granularity-matching:

- **COPY** (the transclusion operation) takes a spec-set of spans: *"The material determined by `<spec set>` is copied…"* (4/67). The spec-set is span-based, so a coarse span carries its whole subtree.
- **FINDDOCSCONTAINING** is defined to match *any portion* of the named material, regardless of where the native copies live: *"This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located."* (4/63)

"Any portion … regardless of where the native copies are located" is the opposite of a native-granularity-match requirement: the query resolves against the implicit subtree, not against the leaves' own depth.

### Bottom line
Naming content at depth-2 over depth-3 content selects the entire subtree hanging from that anchor. The span's contents are *implicit in its boundaries* (4/25), coarse addresses *embrace all the contents below them* (4/23), and discovery returns *any portion* of the named material (4/63). The query discovers everything in the named subtree; it does not require the request to match the content's native granularity.

(Note: this is Nelson's *design intent* from the span/ghost-element model. Whether a given implementation enforces a depth restriction is a separate, implementation-level question — the spec intent is subtree-discovery.)
