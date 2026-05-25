## Question 7 [theory]

> What permissions or ownership claims must govern who may create an edited successor to an existing link?

# Permissions for Creating an Edited Successor to an Existing Link

The question of "edited successor to a link" is not a concept Nelson directly addresses in the curated sources. Links in Xanadu are described as having permanent addresses in their order of creation, with no explicit UPDATELINK operation among the 17 FEBE commands. Nelson's framework handles this case by combining several ownership principles.

## Core Ownership Rule

A link is owned by whoever owns its **home document**, regardless of what the link points to:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to. Conversely, links connecting parts of a document need not reside in that document." (4/12)

> "Only the owner has a right to withdraw a document or change it." (2/29)

## Two Cases

**Case 1: Editing your own link.** You can delete your own link and create a new one. Deleted links enter a "not currently addressable" state but remain in Istream for historical backtrack:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Link addresses are permanent in creation order — they do not get rewritten:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

So "editing" your own link effectively means delete + create new, producing a new tumbler address.

**Case 2: Creating a successor to someone else's link.** Anyone can create their own link relating to another link, because links have addresses and any address can be a target:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

This includes supersession claims. Nelson explicitly allows third-party metalink claims:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52, footnote)

By the same principle (per the curated supersession-authority extraction), Bob can create a supersession link claiming his link supersedes Alice's. But this is a **claim**, not an **authority** — its weight depends on who made it.

## Synthesis

The governing principles are:

1. **The link's home document determines ownership** — only that owner may delete or replace the original
2. **Anyone may create a new link** at their own address relating to an existing link (link-to-link, supersession, commentary)
3. **No link is ever truly destroyed** — deletion makes it "not currently addressable," and previous document versions may still contain it
4. **All claims are visible and attributable** — a successor's authority is social, not technical; users see who made the claim and judge it

NEED_RAW: 4/49-4/51 (link-to-link details), 4/52-4/53 (supersession and metalink specifics). The curated extractions cover the principles but Nelson does not appear to address "edited successor of a link" as a distinct concept. The concept must be assembled from ownership rules, deletion semantics, and link-to-link mechanics. The closest direct treatment is document supersession, which Nelson handles via metalinks rather than via link versioning.
