## Question 1 [theory]

> Did Nelson intend a link's endsets to attach only to the content that existed at creation time, or was a link meant to also capture content later inserted or appended within the spanned region?

**Short answer: both, depending on the level of the endset — and the duality is deliberate.** An endset is not a frozen snapshot of bytes, but it is also not an elastic region of the document's text. It is a span-set on the tumbler line, defined purely by its boundary addresses and evaluated whenever it is used. Whether later content falls inside it depends on where that new content lands in tumbler space — and Nelson's addressing design makes the two cases come out differently:

**1. At the fine-grained text level, a link attaches to the bytes that existed at creation time, and only those.**

Nelson is consistent that links hold onto specific bytes, not regions of the evolving document:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

Notice that all of the survivability language is about *shrinkage* — "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**" (4/43). Nelson never describes an endset *growing* to absorb edits. The mechanism explains why: endsets resolve to Istream addresses, and Istream is append-only ("an append-only storage system," 2/14). When you insert text into the middle of a linked passage, the new bytes receive fresh I-addresses appended elsewhere in the document's content space; only the V-stream positions shift ("The v-stream addresses of any following characters in the document are increased by the length of the inserted text," 4/66). The inserted bytes therefore land *outside* the link's I-span. The link is undisturbed by the insertion, but it does not capture the new material — the strap stays on the original bytes, with the new bytes sitting between them in the V-stream but not in the endset.

This is reinforced by how Nelson handles supersession: a link made to an old version can be followed "to the same passage in the most recent version — if it's still there" (2/43). The system traces *surviving original content* forward via correspondence; it does not pull newly written content into the old link's endsets.

**2. At the coarse-grained, hierarchical level, an endset explicitly embraces content that arrives later.**

Here Nelson is equally explicit, in the opposite direction. Spans are defined by their endpoints, with the contents implicit and time-varying:

> "There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

And this is precisely how links to ghost elements are meant to work:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." ... "A link to or search of an account or node will find any of the documents under it." (4/23)

Nelson says such links "embrace all the contents below them" (4/23). A link made today whose endset covers an account will find a document created under that account tomorrow — that is a designed feature, not an accident. The same applies to the "1-positions": "A digit of 'one' may be used to designate all of a given version, all versions of a given document, all works of a given author, all documents in a given project, all documents on a given server—or the entire docuverse" (4/38). An endset using such a span necessarily covers versions and documents that do not exist yet. The type endset depends on this too — types are matched by address alone and "may be ghost elements" (4/45), meaningful regardless of what is ever stored there.

**Reconciling the two**

There is one uniform rule, not two mechanisms: an endset designates an address region, and its membership is whatever occupies that region when the link is used. The apparent difference in behavior comes from where new content lands. Newly inserted text gets brand-new I-addresses outside any existing fine-grained byte span, so text links behave as creation-time attachments. Newly created documents and versions land *under* existing account/document addresses, so hierarchical endsets behave as live, growing regions. Nelson got creation-time semantics for prose links and forward-capturing semantics for structural links out of the same boundary-defined span mechanism.

**One unresolved edge case (inference, not direct statement):** if a byte-level endset's span boundaries were drawn wider than the bytes existing at creation time, bytes later *appended natively* to that document could fall numerically inside the span and, by the boundary-implicit rule of 4/25, would join the endset. The curated sources never address this case directly — Nelson's examples assume endsets are drawn exactly over selected bytes. NEED_RAW: 4/24-4/25, 4/42-4/47 to check whether Nelson states anything explicit about byte-span endsets whose boundaries exceed currently existing content.
