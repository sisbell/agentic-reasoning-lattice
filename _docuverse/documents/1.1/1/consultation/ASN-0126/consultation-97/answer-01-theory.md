## Question 1 [theory]

> Was retraction designed as an unattributed (anonymous) act, as ASN-0086's empty-from Nullify allows, or is it meant to carry attribution to the agent performing it — and if attributed, is attributing it to the whole retracting document acceptable?

## Bottom line

Retraction was **not** designed as an unattributed act, and an empty *from*-set does not make it one. In Xanadu, attribution never lived in the from-set — it lives in the link's **home document**. So a "Nullify" with an empty from-set is still fully attributed: it is owned by whoever owns its home document, and that ownership is structurally encoded in the address. Attributing the retraction to the whole retracting document is therefore not merely *acceptable* — it is the canonical and correct granularity of attribution.

The framing in the question ("empty-from Nullify *allows* anonymity") rests on a category error that the design explicitly forbids. Let me separate the two things being conflated.

## The crux: ownership and endsets are independent axes

There are two orthogonal things about any link:

1. **What it connects** — the three endsets (from-set, to-set, type).
2. **Whose link it is** — the home document, i.e., the owning account.

I decoupled these deliberately:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." [LM 4/12]

An empty from-set is a statement about axis (1) — *what content the link reaches toward*. It says nothing whatever about axis (2). To read "empty from-set" as "anonymous" is to mistake the connective axis for the ownership axis. A link can point nowhere on one side and still be unambiguously owned.

## Why empty-from is still attributed

Every link is an owned object with a home, by construction:

> "A Xanadu link is a connective unit, a package of connecting or marking information. **It is owned by a user.** It is put in by a user (or a front end), and thereafter maintained by the back end through the back end's inter-indexing mechanisms." [LM 4/41]

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." [LM 4/46]

The home sits in tumbler-space, and the User field of that tumbler *is* the owner. So even a Nullify whose from-set is empty has a home, and the home identifies the retracting agent. The whole system is built so that this is always recoverable:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

Retraction is, in my vocabulary, a *marking* act — and I described links precisely as "a package of connecting **or marking** information" [LM 4/41]. A marking link with no content on one side is still a fully owned, fully traceable mark. There is no such thing as a homeless link, hence no truly anonymous Nullify.

## What "anonymous" actually means in Xanadu — and why retraction shouldn't lean on it

The only anonymity I provided is *John Doe publication*, and even that is account-level pseudonymity, not unattributability:

> "Still, there is no reason that anonymous publication by walk-in and transient users of this system should not be allowed. We may call this 'John Doe publication.'" [LM 2/60]

Notice the consequence I attached to it in the very next breath: anonymous material is *more* exposed, not protected —

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge." [LM 2/60]

Retraction is a consequential, accusatory act of the same family as supersession and defamation-by-graffiti. Consequential acts in my design are *more* accountable, not less. Treating empty-from as a license for anonymous retraction inverts that intent — it would manufacture exactly the John-Doe-graffiti problem the peremptory challenge exists to clean up.

## Attributing it to the whole retracting document is the canonical pattern

Your second sub-question — is document-granularity attribution acceptable? — answers itself once you see that retraction belongs to the **metalink** family, which is *defined* by whole-document scope:

> "METALINKS: These are links expected to apply to whole documents, whether from outside or from inside." [LM 4/52]

The closest cousin to retraction I actually named is supersession, and it is whole-document by nature:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version." [LM 4/52–4/53]

And the metalink pattern explicitly connects *to the whole document*, with the asserting party identified — including when the assertion comes from a third party:

> "the 'author' and 'title' links will normally go from the author's name and the principal appearance of the title **to the whole document**." [LM 4/52]

> "Note that the Author link can also be used from outside a document **to claim** that the author is really someone else." [LM 4/52]

That last line is the governing precedent for retraction. A retraction is a **claim**, attributed by its home, evaluated socially by readers — not a system-enforced fact. So whole-document attribution is not a loss of precision; the document/account *is* the native unit of ownership in my ontology. There is no finer "agent" below the home document to attribute to.

If anything, you should go one step *further* than empty-from: have the retracting side **point at the whole retracting document**, exactly as the author/supersession metalinks point "to the whole document." That makes the "who retracts" legible as a navigable connection (discoverable by link search from either end), rather than something a reader must reconstruct from ownership metadata. Empty-from is the impoverished case; whole-document-from is the canonical one.

## Two secondary notes

**On the one-sided convention.** If the Nullify is conceived as a one-sided link, note that my one-sided convention *populates the first endset* — it does not empty it:

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." [LM 4/48]

So an "empty-from" one-sided link runs against the grain of how I defined one-sidedness (first endset carries the target; the *other* side is the vacant one). This is a notation quibble, not the heart of the matter — but it reinforces that emptying the from-set is not something I treated as the natural home for "no source."

**On terminology.** "Nullify" and "retraction" are ASN-0086's terms, not mine — they do not appear in *Literary Machines*. My nearest constructs are **withdrawal** (an owner removing their *own* published work, which I deliberately made hard: "its author may not withdraw it except by lengthy due process" [LM 2/43]) and **supersession** (a whole-document claim, makeable by anyone). The mapping from "Nullify" to these is interpretive, but the attribution principle is invariant across all of them: the act is owned by its home, and the home is the attribution.

## Recommendation for ASN-0086

- Do **not** treat empty-from as authorizing an anonymous retraction. It does not, in my design, produce anonymity — it only omits a connective trace. The act remains owned by the home document either way.
- Keep retraction **attributed**, and attribute it to the **whole retracting document (its home/account)** — that is the canonical metalink granularity, matching supersession and the author link.
- Prefer populating the from (or, per the one-sided convention, first) endset with the whole retracting document over leaving it empty, so the attribution is a navigable connection and not merely derivable from ownership.
- Frame retraction explicitly as a **claim**, not an enforced fact — like the outside-author link — so readers can see *who* retracted *what* and judge it.
