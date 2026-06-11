## Question 1 [theory]

> When a containing entity (e.g., a whole document) is marked as lifecycle-retired or hidden, does the design intend that its contained parts and sub-addresses also vanish from default presentation, or does retirement apply only to the marked entity itself?

## Short answer

Nelson has no single "retire" flag, and the question splits across his three lifecycle mechanisms — supersession, deletion, and withdrawal. The consistent design intent across all three is: **a mark on the containing entity does scope over everything stored beneath its address for purposes of default presentation, but it never destroys the parts, and it never reaches occurrences of those parts that other documents have included.** Retirement cascades *downward* through the marked entity's own subtree (readers are routed away from the whole thing, internal passages included), but never *outward* through transclusion, and never *backward* into history.

## Why container-level marks naturally cover the parts

Architecturally, a document-level mark is sufficient to scope over every contained part, because containment is implicit in the address hierarchy. There is no stored "document object" to mark separately from its contents — "the only entities actually stored in tumbler-space are content bytes and links" [LM 4/23] — and addresses higher in the tree embrace everything below:

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [LM 4/23]

> "A link to or search of an account or node will find any of the documents under it." [LM 4/23]

Likewise a span over a container implicitly includes its interior: "There is no choice as to what lies between; this is implicit in the choice of first and last point." [LM 4/25]. So a single metalink at the document level — and metalinks are defined as "links expected to apply to whole documents, whether from outside or from inside" [LM 4/52] — is the intended granularity. No per-part retirement marks are needed or contemplated.

## Supersession: the parts recede from default presentation, but nothing vanishes

The supersession link is Nelson's "retired" marker, and it operates at presentation time, in the front end:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." [LM 4/52–4/53]

The cascade to contained parts is explicit in how Nelson expects readers arriving at *internal passages* of a superseded document to be handled — they are redirected to the corresponding place in the successor:

> "When a document is updated, a reader will ordinarily want to see the new version— but the reader may be following a link made to an older version. However, the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version— if it's still there." [LM 2/43]

This works because correspondence is structural: "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]. So yes — when the container is marked superseded, default presentation steers readers away from all of its parts, not just from its "front door." But the marked entity and its parts must stay:

> "However, for corrections and amendments, the author may readily publish a superseding document, but the former version must remain on the network. This is vital because of the links other users may have made to it— which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Note also the granularity is flexible by design — the supersession link covers "one document or version," so an author can retire a single version's subtree or the whole document's subtree.

## Deletion: scoped to the marked arrangement, explicitly *not* cascading outward

The diagram on 4/9 (page-176.png) shows "DELETED BYTES" and "DELETED LINKS" as first-class states within a document's technical contents, annotated identically: "(not currently addressable, awaiting historical backtrack functions; may remain included in other versions.)" [LM 4/9]. Deletion hides parts from the *current arrangement's* default presentation while preserving them for history — and Nelson states the non-cascade rule outright:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

This is the hard boundary on any cascade: hiding or retiring a container cannot make its parts vanish from *other* documents' presentations, because those documents include the content by reference to its permanent Istream identity, and "Non-native bytes are as much a logical part of a document as native bytes." [LM 4/11]

The footnote on that same page (verified directly against page-178.png; it is not in the curated extractions) drives the point to its extreme: Nelson's "Pompeii effect" discussion addresses what happens when an entire *account* is effectively retired — a user dies and storage charges go unpaid. Even then, materials included in others' documents must not vanish: they are to be migrated to the including documents, or kept at their original addresses under new owners or conservators if any of the dead user's own links still point at them. Retirement of the container, even total and involuntary, is required to preserve the contained parts wherever they live on in other contexts.

## Withdrawal: the one true cascade — which is exactly why it's restricted

Withdrawal (removing a document from accessibility entirely) is the only mechanism where retiring the container genuinely takes the parts with it, since the contents are the only thing stored. And that is precisely why Nelson forbids it for published work except "by lengthy due process" [LM 2/43] — withdrawal would break the links and inclusions others have built on the parts: "Other readers and users will come to depend on its accessibility." [LM 2/43]. For private documents the owner retains this power ("Only the owner has a right to withdraw a document or change it." [LM 2/29]), and "privashed" documents trade withdrawal rights for the absence of royalty — dependents knowingly take that risk.

## What is not specified

Nelson does not define an explicit cascade rule for daughter documents and sub-accounts under a withdrawn or retired address (e.g., whether marking document `1.2.3` superseded implies anything about daughter document `1.2.3.1` created by forking), and he does not specify the mechanics of what dependent documents display when a private document is withdrawn. The hierarchy and the Pompeii footnote imply the answers (sub-addresses are independently owned entities; included content must be preserved or re-homed), but no passage states them directly. NEED_RAW: [2/44-2/45, 4/29, 4/79] if a definitive statement on sub-document cascade is required.
