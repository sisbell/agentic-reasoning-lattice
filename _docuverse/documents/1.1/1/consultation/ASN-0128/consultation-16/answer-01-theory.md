## Question 1 [theory]

> In Literary Machines' whole-document supersession metalink (LM 4/52–4/53), which endpoint carries the newer (superseding) document and which the older (superseded) — i.e., does the link assert "this supersedes that" from new to old, or point from an old version toward its replacement?

**Answer: The supersession link runs from the new document to the old one — the from-set carries the newer (superseding) document and the to-set carries the older (superseded) document. It asserts "this supersedes that," not "here is my replacement."**

### What Nelson's prose says (and doesn't say)

The text on 4/52–4/53 describes the link's purpose but never explicitly names which endset is which:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52–4/53)

Nelson also explicitly leaves directional semantics type-dependent: "What 'from' and 'to' mean depend on the specific case." (4/42)

### The diagram settles it

The OCR of the original page (`resources/literary-machines/pages/page-219.txt`, LM 4/52) records the accompanying diagram: two boxes labeled "OLD VERSION" and "NEW VERSION," with the arrow drawn **from the NEW VERSION box to the OLD VERSION box**, labeled "supersedes." Note this is the OCR pipeline's description of the figure, not verbatim Nelson prose (the page image itself is not readable in this session), but it directly answers the directionality question: new → old.

### Why this direction is coherent with the rest of the system

- **Grammatical framing.** "One document or version supersedes another" puts the new document in subject position — the link is a claim made *by* (or about) the newer document against the older one.
- **Pattern of neighboring link types on 4/53.** The asserting, newer material consistently sits on the "from" side: the quote link "shows the origin of a quotation; it acknowledges the material's origin. Made by the quoting author" (4/53) — new material pointing back to its older source. The alternative-version link likewise "notes that another version of a passage, or of a whole document, exists elsewhere, and points to it" (4/53).
- **Ownership practicality.** The old document is already published and cannot be edited to add a forward pointer; the author "may readily publish a superseding document, but the former version must remain on the network" (2/43). The natural moment to create the link is at publication of the new version, pointing back at what it replaces.
- **Discovery still works for readers of the old document.** Xanadu link search is indexed by all endsets, so direction doesn't impede the canonical use case. A front end opening document D searches for supersession-type links whose **to-set** includes D (via FINDLINKSFROMTOTHREE, which finds links "from all or any part of \<from set\>, and... to all or any part of \<to set\> and \<three set\>" — 4/69). A hit means something newer claims to supersede D, which is exactly why "a front-end request for supersession links is normally expected before starting to read a new document."

One caveat worth keeping in mind: because anyone can create links into published work, a supersession link from a third party's document is a *claim* of supersession, not an authoritative one — the same way "the Author link can also be used from outside a document to claim that the author is really someone else" (4/52, footnote). The direction is the same (new → old); the authority depends on whose home document the link lives in.
