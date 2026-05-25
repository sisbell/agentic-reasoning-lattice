## Question 5 [theory]

> How does the design reconcile the permanence of historical containment with the currency of present-day document state?

The apparent tension dissolves once you see that permanence and currency are not opposites in this design - they are two views of the same content, addressed differently. The reconciliation rests on five interlocking mechanisms.

## 1. Architectural Separation: Istream / Vstream

The fundamental move is to split *identity* from *arrangement*:

- **Istream** holds content permanently. Once a byte is written, its I-address never changes and never points to different content.
- **Vstream** is the document's current arrangement - a *view* that references Istream content.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

So "editing" never destroys anything - it changes which Istream content the current Vstream arrangement references. Permanence lives in Istream; currency lives in Vstream.

## 2. Append-Only Storage, Not Destructive Replacement

This is the explicit rejection of the conventional model:

> "Virtually all of computerdom is built around the inadequate convention of making whole copies of each current version ... A document is really not just a block of text ... it is an ongoing changing file ... an evolving braid." [LM 2/14]

> "Instead, suppose we create an append-only storage system. User makes changes, the changes flow into the storage system, filed, as it were, chronologically." [LM 2/14]

The "current" state is just the most recent strand in the braid. The braid itself - every past state - remains addressable.

## 3. Prismatic Storage: No Privileged "Current" Version

Crucially, the design refuses to declare any version canonical:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

This is philosophically important. The system does not have to *reconcile* past and present because it does not privilege the present. All versions are equally real, equally accessible. "Currency" is a social/temporal designation, not a structural one.

## 4. Supersession Links: Currency as User-Asserted Metadata

Since the system itself does not declare which version is current, that judgment is expressed through an explicit metalink:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." [LM 4/52-4/53]

The supersession link is *added structure on top of permanent content*, not a replacement of it. The old version remains; the supersession link simply asserts "there is a newer one here."

## 5. Refractive Link Following: Bridging Old to New

This is the most elegant part. Once others have linked into your published document, you cannot withdraw it - their links depend on it. But you may publish updates, and the system bridges the gap:

> "It is in the common interest that a thing once published stay published, as in the world of paper. ... However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it—which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

> "When a document is updated, a reader will ordinarily want to see the new version—but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." [LM 2/43]

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

This works because correspondence is *structural* (shared Istream origin). A link made against last year's version of paragraph 17 can be followed to paragraph 17 in this year's version, because the system can compute which V-positions in the new arrangement share Istream content with the V-positions in the old.

## 6. Transclusion: Two Modes of Currency

For transcluded content, the user chooses which they want:

> "A quotation--an inclusion window--may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

A scholar citing a specific historical state fixes in time. A document republishing live news fixes in location. Both are valid; both are supported by the same underlying mechanism.

---

## The Deep Principle

The conventional view treats "permanence" and "currency" as opposed because conventional systems use destructive replacement: making something current *requires* destroying what was. Xanadu rejects that premise. Permanence is the substrate (Istream + append-only storage). Currency is a *view* over that substrate, asserted through Vstream arrangements, supersession links, and the front end's intelligence about which view the user wants right now.

The user is never forced to choose. They can ask: "Show me what this said in 1987." They can ask: "Show me what this says now." They can ask: "Show me what changed between then and now." All three are first-class operations against the same permanent content. As Nelson puts it:

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

The reconciliation, in short, is that there is nothing to reconcile - the design simply refuses the assumption that making the present visible requires forgetting the past.
