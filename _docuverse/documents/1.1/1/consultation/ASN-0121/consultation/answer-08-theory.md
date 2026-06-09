## Question 8 [theory]

> Must the discovery reach across all documents whose arrangements could surface the same links, and what guarantee covers that cross-document scope?

## Short answer

Yes. Because links point to **Istream** content (not document positions), and that content can be homed-elsewhere, transcluded into other documents, and re-arranged across versions, a complete link discovery must reach across **all** documents whose arrangements surface the targeted bytes — not just the document you happen to be reading. The guarantee that covers this is the **whole-docuverse scope of link search** (`FINDLINKSFROMTOTHREE` / `FINDDOCSCONTAINING`), backed by the search-efficiency invariant that irrelevant links don't impede the search.

## Why discovery is inherently cross-document

A document's *out-links* live in it, but its *in-links* live somewhere else entirely:

> "Ordinarily a document consists of its contents (including history and alternatives) and its out-links... By contrast, a document's in-links are those stored elsewhere which point to it. These out-links are under control of its owner, whereas its in-links are not." (2/31)

And a link's *home* says who owns it, not what it touches — so links connecting your content can reside in any document anywhere:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

Worse, the *same* link surfaces in every arrangement that includes the bytes it straps to, because links attach to spans of content and follow them across versions:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

So "all documents whose arrangements could surface the same links" = the home documents of the links **plus** every document that transcludes or versions the connected content. None of these are knowable from the local document alone.

## The guarantee covering cross-document scope

The FEBE operations are defined to span the entire address space:

- `FINDLINKSFROMTOTHREE` — "If the home-set is the whole docuverse, all links between these two elements are returned." (4/63)
- `FINDDOCSCONTAINING` — "This returns a list of all documents containing any of the material specified by the span addresses, **regardless of where the native copies are located**." (4/63)

This is what makes the cross-document reach a *guarantee* rather than a best effort: you set the home-set to the docuverse and you get **all** matching links, wherever they are homed. It is also why the system indexes links by all three endsets — discovery is bidirectional regardless of which document you start from.

The scalability invariant that makes searching that whole space tractable:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)

Combined with the back-end's "barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously" (4/59), this is how docuverse-wide discovery stays within the "soft corridor" of logarithmic slowdown rather than degrading as the network grows.

## Summary

Discovery must be docuverse-wide because in-links, link homes, transclusions, and versions all place the relevant links outside the document being read. The covering guarantee is the **whole-docuverse home-set of link search** (`FINDLINKSFROMTOTHREE` / `FINDDOCSCONTAINING`, 4/63), which returns *all* matching links and *all* containing documents regardless of native location — made practical by the invariant that non-matching links don't impede the search (4/60).
