## Question 4 [theory]

> What does reading a link directly reveal about its relationship that following the link to its endpoints would not?

Reading a link as an object reveals the **nature of the relationship** — its type, direction, ownership, and any attached commentary — none of which you can recover merely by arriving at the connected content.

## What the endpoints alone tell you

Following a link to its endpoints reveals only **what is connected** — the spans of bytes at each end. Two passages sit at the from-set and to-set; the content is there. But the bytes themselves don't announce why they're connected or who connected them.

## What reading the link itself adds

**1. The type — what kind of connection this is.** A link's relationship is carried in its third endset, not in its endpoints:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

The endpoints look identical whether the link is a citation, a refutation, or a comment. Only the link object distinguishes them. As the three-endset analysis puts it, the type endset establishes WHAT KIND of connection it is — "Without the type endset... [there is] No way to distinguish citations from comments from refutations."

**2. Direction — which end is "from" and which is "to."**

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

Standing at an endpoint, you cannot tell whether you are at the source or the target of the assertion. The link object encodes that asymmetry.

**3. Ownership — who asserts the relationship.** The link's home document determines its owner:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

This matters because a relationship is a *claim*. Reading the link reveals who made it — letting you see, for instance, whether a supersession claim comes from the original author or a third party (a distinction the supersession-authority notes is "social, not architectural").

**4. Attached commentary.** Some link types carry explanatory content of their own. The counterpart link is the clearest example:

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link. Note that a counterpart link will typically have a comment attached to it." (4/53)

That comment lives on the link, not at either endpoint — you only get it by reading the link.

**5. The complete set of endsets at once.** Because a link is a first-class object, reading it returns all three endsets together (`RETRIEVEENDSETS` "returns a list of all link end-sets that are in <spec set>," 4/70). Arriving at one endpoint by traversal gives you that one location; reading the link gives you the whole structure — both ends plus the type — simultaneously.

## Why this is possible

It works because links are themselves addressable objects in tumbler-space, not markup embedded in content:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

A link is "a meta-virtual structure connecting parts of documents" (4/41) — a thing you can read in its own right. The endpoints carry the *content*; the link carries the *relationship*: its type, its direction, its owner, and its commentary.
