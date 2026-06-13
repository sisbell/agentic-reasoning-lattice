## Question 8 [theory]

> Must the system guarantee that a reader asking for the current version of an edited link receives exactly one unambiguous answer, even after many successive edits?

# Must "the current version of an edited link" resolve to exactly one answer?

No. The system neither makes nor needs that guarantee — and it would betray the design if it tried. What the system guarantees is *identity* and *reconstructability*, not *singularity of "current."* Let me separate the two questions that are tangled together in yours, because the precision matters.

## Two different questions wearing one phrase

"The current version of an edited link" hides two distinct queries:

1. **"Given a version and a position, what content is there?"** — This *is* single-valued and exact. Every byte has one permanent Istream address; ask for a given part of a given version at a given moment and you get precisely that. "THE PART YOU WANT COMES WHEN YOU ASK FOR IT" (2/16). No ambiguity.

2. **"Which version is *current*, and where does my old link land in it?"** — This is *not* single-valued, by construction. The word doing all the damage is "current." It is a query-time resolution policy, not a stored fact, and the policy can legitimately return zero answers, one, or several.

When I say the system gives an unambiguous answer, I mean (1). The ambiguity you are asking about lives entirely in (2).

## Why "current" is not a function

**A link is to *all* versions, not one.** This is deliberate:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." (2/26)

A link does not *select* a version. It spans them. "Refractive following" is a fan-out, not a lookup.

**Following to "the most recent" is a front-end policy, and it is conditional.** I never put this in the back end as an invariant:

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—**if it's still there**." (2/43)

Read that closing clause carefully. "If it's still there." After many successive edits the corresponding passage may have been deleted — in which case following-to-current yields *nothing*, not one answer.

**After editing, an endset can become several places, not one.** Links bind spans, not points:

> "A Xanadu link is not between points, but between spans of data." (4/42)

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes." (4/42)

Survival is per-byte: "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43). So after a rearrangement, the surviving end may be a *discontiguous* set scattered across the latest version. Resolving the link there returns a span-set — many landing points — not a single unambiguous spot.

**"Current" is itself contested, because supersession is a claim, not an authority.** This is the deepest reason. The supersession link is the canonical *way to ask*, but it does not produce a *unique* answer:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52–4/53)

Note "supersession links" — plural — and "a request for" them, to be sorted out by the front end. Anyone can assert one, just as anyone may assert authorship from outside a document: "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52). If third parties can claim authorship, they can claim supersession. An author may even publish *two* superseding documents — a fork. The supersession graph is therefore a graph of *claims*, and "which is latest" can have competing answers that the system surfaces but does not adjudicate.

## This multiplicity is the point, not a defect

I built Prismatic storage precisely so that no version is privileged:

> "There is thus no 'basic' version of a document set apart from other versions... any more than one arrangement of the same materials is a priori better than other arrangements." (2/19)

A system that *forced* "current" to a single canonical answer would have to throw away versions, or appoint an authority to declare the One True Latest. Both are exactly what Xanadu refuses to do. The former breaks the historical-backtrack guarantee; the latter installs a Ministry of Truth over the version graph.

Instead, the reader holds the policy. That is why windowing offers two modes, and the *reader* chooses:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." (2/37)

## What I *do* guarantee, after any number of edits

So the honest accounting is:

- **Identity is unambiguous.** Every byte and every link has exactly one permanent address; editing never reassigns it.
- **Reconstruction is unambiguous.** Pin the version and the moment, and exactly one content comes back.
- **Survival is honest.** A link persists iff bytes remain at each end — and may then designate a discontiguous set.
- **"Current" is a query, resolved by policy, and may be zero-, one-, or many-valued.** The system's duty is to make every claim *visible and traceable*, not to collapse them into one.

In the vocabulary your formalization is reaching for: link-identity resolution is a **function** (single-valued); "follow this link to the current version" is a **relation** (multi-valued, and partial — it can be empty). Do not formalize the second as a function; that would encode a guarantee I never made and never wanted.

---

*A small note on your phrase "edited link": links keep their permanent creation-order addresses and are created/deleted rather than mutated in place, so "editing a link" in practice means editing the content its endsets bind to. I answered on that reading; if you meant something narrower — e.g., a re-pointed endset treated as a new link version — the conclusion is unchanged, since that only adds another claim to the version graph.*
