## Question 8 [theory]

> Must edited links be visible to the original link's author, or is the successor relationship purely a public record?

# Edited Links: Author Visibility

Nelson does not specify any notification mechanism requiring that edited or successor links be made visible to the original link's author. The successor relationship is purely a public record — structurally discoverable through search, but not pushed to anyone.

## Why "Edited Links" Is an Unusual Framing

In Xanadu, links are owned and only the owner may modify their own link. There is no operation by which one user "edits" another user's link. What can happen is:

1. **The owner edits their own link** — no notification question arises; they did it themselves.
2. **Someone creates a new link** that relates to, supersedes, or points at an existing link (via link-to-link, supersession semantics, or counterpart links). This new link is owned by its creator at their own home address.

The question therefore reduces to: when a *new* link establishes a successor relationship to an existing link, must the original link's author be notified?

## What Nelson Specifies

**Links are owned by the creator, at the creator's address:**

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." (4/41)

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

**Discovery is bidirectional and pull-based:**

> "The reader should be able to ask, for a given document or place in the document, 'What connects here from other documents?'-- and be shown all these outside conections without appreciable delay." (2/46)

Because links have tumbler addresses and link-to-link is supported, an author can search for all links pointing at their link the same way they search for in-links to any content. The data is structurally available — but the author must ask.

**Supersession checking is reader-side, not author-side:**

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52-4/53)

Nelson specifies that the *reader's* front end checks supersession before reading. He does not specify any obligation that the *original author* be informed when a supersession claim is created against their work.

**The no-surveillance principle constrains push notification:**

> "The network will not, may not monitor what is read or what is written in private documents." (2/59)

While this addresses reading rather than linking, it reflects Nelson's general posture: the system makes information available for those who seek it, rather than actively tracking or pushing notifications.

## The Successor Relationship as Public Record

The analogue is academic citation. Anyone can publish a paper claiming to supersede or refute another paper; the original author is not notified, but the claim is publicly indexed and discoverable. Nelson's mechanism works the same way: successor links exist in the docuverse, are indexed by all three endsets, and can be found by anyone — including the original author — through bidirectional search.

## What Is Not Specified

NEED_RAW: 4/52-4/55 (metalinks and link types) and 4/74-4/79 (BEBE/notification mechanisms) — to confirm Nelson does not specify any push-notification facility for authors when their links acquire successors. The curated sources show only pull-based discovery; verifying absence requires checking the raw pages for any author-notification facility I may have missed.

## Answer

**The successor relationship is purely a public record.** Nelson specifies bidirectional discoverability but no author-notification obligation. The original author can always *find* successor links via search, but the system does not push such information to them. This is consistent with Nelson's broader pattern: make connections structurally visible and let users navigate the web of relationships, rather than building active notification machinery.
