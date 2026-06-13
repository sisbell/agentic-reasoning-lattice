## Question 9 [theory]

> When two editors independently supersede the same link, must the design permit the resulting fork to coexist permanently, and what must readers be told about the divergence?

# On Two Editors Superseding the Same Thing

Yes. The design must permit — indeed, it *requires* — the fork to coexist permanently. And the reader must be shown both claims, told who made each, and left to choose. Let me be precise about why, because this case sits exactly where my philosophy of versions, ownership, and reader freedom converge.

## A note on "superseding a link"

First, an honest distinction. What I specified was the **Document Supersession Link**:

> "Document Supersession Link: This link indicates that one document or version supersedes another. It is the canonical way to find out whether you are reading the latest version. A front-end request for supersession links is normally expected before starting to read a new document." (4/52–4/53)

My stated examples are *documents and versions*. Superseding a **link** as such is an extension of that — but a legitimate one, because links are first-class citizens of tumbler-space with their own addresses, and anything addressable can be the target of a link:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

So a supersession link *can* take another link as its target. The architectural answer below is the same whether the superseded thing is a document, a version, or a link — and that uniformity is the point.

## Why coexistence is mandatory, not merely tolerated

Three of my foundational commitments make a single "winning" supersession impossible to impose:

**1. Each editor owns their own link; neither can touch the other's.** A link's home address identifies its owner, and ownership is the boundary of authority:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

> "Only the owner has a right to withdraw a document or change it." (2/29)

Editor A's supersession link lives at A's address; Editor B's lives at B's. Neither can delete or override the other's. There is no operation in the system by which one editor's claim suppresses another's.

**2. Nothing published is destroyed.** Even if an editor *withdraws* their own supersession claim, it does not vanish — it enters historical backtrack:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

And the superseded original itself cannot be pulled out from under the fork:

> "It is in the common interest that a thing once published stay published, as in the world of paper... Consequently its author may not withdraw it except by lengthy due process." (2/43)

**3. There is no privileged version for the system to crown.** This is doctrine, not accident:

> "There is thus no 'basic' version of a document set apart from other versions—'alternative' versions—any more than one arrangement of the same materials is a priori better than other arrangements." (2/19)

A supersession link is a **claim**, not an **authority**. I made this explicit for the parallel case of authorship — the same link mechanism, used from outside, to assert something about a work one does not own:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52, footnote)

Two competing supersession links are structurally identical objects. The system has no notion of "the" supersession, no merge, no arbitration. So the fork *must* persist: there is no mechanism to collapse it, and the non-withdrawal and no-basic-version guarantees forbid resolving it by erasure.

## What the reader must be told

The supersession check I built into the reading flow normally returns *the* successor. Under a fork it returns **more than one**, and the front end must not quietly pick one and hide the rest. Concretely, readers must be told:

**a) That a divergence exists.** The front-end's customary pre-read request for supersession links will surface multiple claims. Showing only one — as though it were canonical — would be a falsification of the record.

**b) Who made each claim.** Because every link's home address identifies its owner, the reader can distinguish the original author's authoritative successor from a third party's competing claim — and weigh them accordingly. The link-comment convention (as with the counterpart link, which "will typically have a comment attached to it," 4/53) is the place an editor explains *why* their version supersedes; the divergence should be annotated, not bare.

**c) That the original still exists and is still readable.** Nothing is deleted; the reader can always step back to what was superseded — "Show me what this originally was."

**d) That the choice is theirs.** This is non-negotiable, and it is exactly where a lesser design would betray the user. I warned against systems that decide for the reader:

> "Some advocates of Artificial Intelligence would have computers decide what the reader shall see. As a filtering service this may be just what you want—but the danger is its evolving into a circumscription of your rights, where the choice is no longer yours."

A fork is precisely the moment a careless front end would "helpfully" choose a branch. It must not. It must present the divergence and hand the decision to the reader.

## The reach-through wrinkle

There is one mechanism the fork strains, and it is worth naming. I designed links to old versions to "reach through" to current ones:

> "...the user's front-end machine may easily be set up to follow the link to the same passage in the most recent version—if it's still there." (2/43)

That convenience assumes a *linear* chain — a single "most recent version." A fork makes "the most recent" no longer single-valued. The correct behavior, faithful to the design, is that auto-follow can no longer silently resolve to one successor; it must surface the branch point and offer the reader both paths. The reach-through becomes a *presentation of alternatives*, not an automatic redirect.

## How divergence is meant to be resolved

Not by the architecture — by the community. The system's job is to make every claim **permanent, attributed, and disputable**; the readers, authors, and any trusted authorities do the adjudicating. This is what the **Certified Link** ("verified by authority, may be applied to versions") is for: an authority or a reputation can mark a preferred branch as canonical *without* destroying the other. The losing branch does not disappear; it simply carries less social weight.

That is the whole shape of my answer: divergence is resolved *socially*, never *structurally*. The fork lives forever in the record, both editors keep their own claims, and the reader is shown the split, told who said what, and trusted to decide. A system that quietly picked a winner would be cheaper to build and a betrayal of everything the docuverse is for.

---

*Note on sources:* The treatment of a **link** (rather than a document or version) as the target of supersession is my inference from the universality of the link mechanism (4/49, 4/12); my text at 4/52–4/53 frames supersession explicitly for "document or version." All quoted passages above are verified against the curated extractions.
