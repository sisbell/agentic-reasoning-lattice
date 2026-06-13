## Question 3 [theory]

> Must a reader who encounters the superseded link be able to discover that a successor exists, or is it acceptable for the old link to give no sign that it has been replaced?

## Short answer

Discoverability is **required by design**. A reader who lands on a superseded version must be able to find out that a successor exists — that is the entire reason the supersession link exists. An old version (or an old link) that gives *no sign whatsoever* that it has been replaced runs against Nelson's design intent. But note the important qualification: the successor must be *discoverable*, not *forced on the reader*. The old version is never hidden or deleted, and the reader stays free to read it.

A small terminology note first: in Nelson's vocabulary supersession holds between *documents or versions*, and the **supersession link** is the metalink that *declares* one supersedes another. So "the superseded link" really means "the superseded document/version" or "a link pointing into it."

## The canonical mechanism: the supersession link

Nelson built a dedicated metalink precisely so that "am I reading the latest?" is always answerable:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52–4/53)

Two things follow from this. First, supersession is *the canonical way to find out* — i.e., the system's designed answer to the discoverability question is "yes, you can find out." Second, checking is part of the expected reading flow: a supersession request is "normally expected before starting to read a new document." Discoverability isn't an afterthought; it's woven into how reading is supposed to begin.

## Old links reach through to the successor

The question's "old link" case is also explicitly handled. Because a former version "must remain on the network," links made to it are not orphaned — they connect forward:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." (2/43)

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." (2/43)

This reach-through is supported structurally by refractive link-following over versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

So even arriving via an old link, the path to the current version is available.

## Discoverable ≠ coerced

Crucially, the requirement is that the successor be *findable*, not that the reader be silently redirected. The old version is preserved and remains readable on demand:

> "(The old viewpoint is still present too—you can always say, 'Show me what this originally was.')" (2/45)

So the supersession "sign" informs the reader and lets them choose; it does not overwrite, hide, or force. The reader "will ordinarily want to see the new version" — but it's the front end that "may easily be set up" to follow forward (2/43), and the reader can still ask for the original.

## The deeper principle: silent replacement is the failure mode Nelson designed against

"Giving no sign of replacement" is not a neutral implementation choice — it is precisely the Ministry-of-Truth scenario Nelson identifies as the thing to avoid:

> "A reference article, say, in an encyclopedia can be changed simply by storing another one in its place—and poof! history is changed. There is no typography or watermark to check." (Literary Machines, Ch. 3, on freedom; 3/19–3/22)

The supersession model is the inverse of "poof! history is changed": you publish a *superseding* document, the old one *remains*, and the replacement is *discoverable*. A successor that left no trace would reintroduce exactly the silent-rewrite problem the design exists to prevent.

## Caveats worth flagging

Three limits on how strong this guarantee is in practice:

1. **It depends on the supersession link being created and the front end checking for it.** Nelson says the front-end request is "normally expected" (4/52–4/53), but enforcement lives at the front-end layer, which Nelson generally leaves to front-end designers. The back end makes supersession *discoverable*; it does not force a reader's tool to look.

2. **Version-address ancestry alone is not a supersession signal.** A version number indicates lineage but not authority to replace: "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." (4/29) The *explicit* supersession link is the canonical signal — not the address.

3. **A supersession link is a claim, identifiable by who made it.** By analogy with the Author metalink, which "can also be used from outside a document to claim that the author is really someone else" (4/52), anyone may assert supersession. Because links are discoverable from either end, a reader on the old version can find the incoming supersession link *and* see whose address it lives at — so "discoverable" includes "attributable and evaluable," not "authoritative by fiat."

## Bottom line

It is **not** acceptable, by Nelson's design intent, for the old version to give no sign it has been replaced. The supersession link is "the canonical way to find out whether you are reading the latest version" (4/52–4/53), the former version "must remain on the network" with links that "reach through... into the newer version" (2/43), and silent replacement is the very Ministry-of-Truth pattern the system is built to prevent (3/19–3/22). The guarantee is *discoverability of the successor*, paired with *preservation of and continued access to the original* — informing the reader without coercing them.
