## Question 4 [theory]

> Was document supersession intended to be a strictly linear chain per document, or does the design admit branching (one document superseded by multiple variants)?

The page images can't be read in this session — the file-reading tool isn't enabled here — so everything below rests on the verified curated extracts, with one NEED_RAW flag where a definitive textual check would help.

---

## Verdict

Supersession was **not designed as a structurally enforced linear chain**. The design admits branching — both multiple successors and competing claims — because a supersession link is just a link, and nothing in the link mechanism imposes uniqueness. What *is* linear is the **canonical expected use**: an author publishing a correction declares "this replaces that," and the reader's front end walks to the current version. Linearity is a convention of the authoritative case, not an invariant the back end maintains.

## What I specified

The supersession link is one of the metalinks — "links expected to apply to whole documents, whether from outside or from inside" [LM 4/52]:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." [LM 4/52-4/53]

Note the phrasing: it indicates that one document supersedes *another* — a pairwise assertion, not a chain datatype. The chain is emergent, assembled by following such assertions.

## Why branching is admitted

Three independent features of the design make strict linearity unenforceable — deliberately so:

**1. Supersession is a claim, owned by whoever makes it.** "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user" [LM 4/41]. Anyone may create a supersession link pointing at any published document, just as "the Author link can also be used from outside a document to claim that the author is really someone else" [LM 4/52, footnote]. So a single document may accumulate several supersession links — the author's, a rival editor's, a fork maintainer's. The system records all of them; link search returns all of them; the link's home address tells you whose claim each one is. The system does not adjudicate among claims, and therefore cannot guarantee a unique successor.

**2. The version space itself forks.** "So the docuverse is all really one big forking document" [LM 4/18]. CREATENEWVERSION "creates a new document with the contents of document `<doc id>`... The new document's id will indicate its ancestry" [LM 4/66] — and nothing prevents invoking it twice on the same source, yielding sibling successors. Indeed, "the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation" [LM 4/29]. An author who splits a work into two successor documents could legitimately mark *both* with supersession links from the original. The addressing and link machinery handle this without complaint.

**3. No version is privileged by the storage model.** "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements" [LM 2/19]. Supersession is precisely the instrument by which an owner *overrides* that prismatic neutrality for reading purposes — an explicit, dated, owned assertion. It is social structure laid over a pluralistic substrate, not a constraint within the substrate.

## Why the canonical use reads as a chain

The expected workflow is singular in its language, and that reflects intent:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

"The latest version," "the newer version," "the most recent version" — for the ordinary case of an author maintaining one current text, the owner's supersession links form a chain, and the front-end behavior (check supersession before reading, offer to follow through) presumes there is normally an answer to "am I reading the latest?" That presumption is what makes the link type *canonical* for that question.

## The division of labor with alternative versions

Where variants are meant to **coexist** rather than replace, the design provides a different instrument: the **Alternative-Version Link**, listed as its own type alongside supersession [LM 4/53]. And third parties who want to publish their own variant of a work do so by versioning-by-inclusion — "users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate—without damaging the originals" [LM 2/45] — without any supersession claim at all. So the type system itself encodes the semantic distinction: supersession asserts obsolescence; alternative-version asserts parallel validity. An author choosing to fork a work into named variants would, by intent, use alternative-version links among the variants — reserving supersession for "stop reading that one."

## What is left unspecified

Literary Machines, as far as the verified extracts show, never explicitly discusses the multi-successor scenario — one document with two or more owner-made supersession links (a deliberate split), or the front-end behavior when supersession claims conflict. That resolution is front-end and social: the reader sees the competing claims, sees who made each, and judges — the same posture taken for disputed authorship. NEED_RAW: [4/52-4/55, 2/43-2/47] to confirm no passage addresses multiple simultaneous supersessions directly.

**Summary**: linear-by-convention in the authoritative case, branching-by-construction in the mechanism — and that combination is intentional. The system's job is to make every supersession claim permanent, attributed, and discoverable; deciding which claim to honor belongs to readers and their front ends, never to the back end.
