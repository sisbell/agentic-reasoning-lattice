## Question 4 [theory]

> In the design of typed relations with retraction semantics, did Nelson intend a canonical direction (to-set carries retraction targets) or treat retraction as direction-symmetric over the link's endsets?

# Did I Intend a Canonical Retraction Direction?

The short answer: I established directional structure but did not prescribe a canonical retraction direction in `Literary Machines`. The architecture is **structurally directional**, **semantically type-dependent**, and **deliberately under-prescribed** at the convention level.

## What I Did Specify

**Links are directional, but meaning is case-dependent:**

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

That parenthetical is load-bearing. I explicitly punted on prescribing what from/to mean for any specific link type.

**Endsets are architecturally symmetric:**

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." [LM 4/43]

The mechanism treats all three endsets identically — "powerful and symmetrical" [LM 4/43].

## What I Said About Retraction

Retraction in the strong sense — withdrawal — is **forbidden** for published material:

> "It is in the common interest that a thing once published stay published, as in the world of paper... Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The substitute is **supersession**, expressed through a metalink:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version." [LM 4/52-4/53]

Note: I described this as "supersedes another" without specifying which endset holds which document.

## The Closest Convention I Established

The Author metalink offers the strongest direction precedent:

> "the 'author' and 'title' links will normally go from the author's name and the principal appearance of the title to the whole document." [LM 4/52]

The pattern: **from = the asserting/referring element, to = the subject of reference**. By analogy, a supersession link might go from the new/asserting document to the old/superseded one — but I did not state this explicitly.

## My Design Intent

Reading the architecture as a whole:

1. **Structural symmetry** is real — the mechanism doesn't privilege from over to.
2. **Semantic direction** is carried by the type endset, not by which side is "to."
3. **Bidirectional discovery** is guaranteed regardless of which side holds what: `FINDLINKSFROMTOTHREE` lets you constrain any combination [LM 4/58, see `links.md`].
4. **Conventions emerge by type**, not by architectural decree.

So: I intended retraction targets to be carried by a **directional link of a specific type**, but I did not canonicalize whether the retraction target sits in the to-set or the from-set. The decision was left to whoever standardizes the working set of link types — a task I called "high priority, but [with] less priority than establishing a robust demonstration rig" [LM 4/52, via `link-type-system.md`].

NEED_RAW: 4/52-4/55 for any further endset-direction specifications I may have given for specific link types beyond what the curated sources captured (counterpart, mail, alternative-version, certified). The curated metalinks coverage (`metalinks.md`) only details Title, Author, and Supersession.
