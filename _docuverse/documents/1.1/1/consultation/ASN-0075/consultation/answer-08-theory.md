## Question 8 [theory]

> Should users be able to share the result of a "show deletions" comparison with other users, and must that shared view remain stable over time?

# Sharing and Stability of Comparison Views

**Yes to both.** Users must be able to share the result of any version comparison, and that shared view must remain stable over time. Both guarantees follow directly from the foundational architecture.

## On Sharing

The comparison itself is data—`SHOWRELATIONOF2VERSIONS` returns "a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. In Xanadu, anything that is data can be a document, and any document can be linked to, transcluded, published, or commented upon. There is no privileged class of "system results" that resist being shared.

This is the entire point of the docuverse: literature builds on literature. A scholar who has done the work of comparing two versions—identifying what changed, what was deleted, what corresponds—has produced something of intellectual value. That work must be shareable, just as a footnote in a book must be quotable.

The **counterpart link** is the explicit mechanism for this:

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link. Note that a counterpart link will typically have a comment attached to it." [LM 4/53]

A user comparing two versions can capture the correspondences they care about as counterpart links in their own document, with their own commentary. Those links live at their address, under their control, but are visible to anyone who looks at either version.

## On Stability

Stability is not something we have to add to the system—it falls out of version permanence. Both versions in any comparison are immutable:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

If V1 and V2 are both permanent arrangements over permanent Istream content, then the correspondence between them is a deterministic function of two stable inputs. Compute it today, compute it in fifty years—the same pairs of spans correspond, because nothing about either version has changed.

> "The user may scroll through any two versions to see corresponding parts; and much more." [LM 2/21]

This is true today, and must remain true for any reader who follows your shared comparison tomorrow.

## The User's Choice: Pinned vs. Evolving

There is one design subtlety worth being explicit about. A "comparison" is technically a function of two version identifiers. The user has two ways to share:

1. **Pinned to specific versions** — Share the comparison between V1.3 and V1.7. This is permanently stable because both endpoints are permanent.
2. **Pinned to current** — Share "the comparison between V1.3 and whatever is current." This evolves as new versions are created.

This parallels the same choice we make for windowing transclusions:

> "A quotation—an inclusion window—may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." [LM 2/37]

The user must be able to express both intentions. A historian comparing two specific drafts wants pinned-to-versions. A reviewer tracking how a document evolves against a baseline wants pinned-to-current. Both are legitimate.

## Why This Matters

The deeper principle is this: a "show deletions" view is not a transient artifact of the user's session. It is a piece of intellectual work. The system that produces it must treat it as first-class—shareable, citeable, durable.

> "What connects here from other documents?" [LM 2/46]

If I read your shared comparison of two versions of someone else's document, I should be able to follow that link backward and find your analysis, comment on it, link to it, refer to it in my own writing. The comparison is part of the literature once you've shared it. Anything less would be a regression from what paper publishing already provides.

The system must preserve the structure of literature. Comparisons are part of that structure.
