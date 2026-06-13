## Question 1 [theory]

> When a link's endsets must be modified, must the system allocate a wholly new link with its own permanent identity, leaving the original untouched in every respect?

## Short answer

**Yes — in the system Nelson specifies, that is the only available path.** There is no operation to edit a link's endsets in place. A link's address *is* its identity, and that identity is fixed at the moment of creation. So to make a link connect anything different, you create a *new* link with `MAKELINK`, which allocates a fresh, permanent, never-reused identity. The original is not touched by that act: its from-set, to-set, type, and address all persist unchanged. The most the owner can additionally do to the original is *delete* it — a separate, non-destructive operation — but deletion still does not alter the original's endsets.

This is, however, an inference from the documented design rather than a sentence in which Nelson states the rule outright. Let me lay out the support.

## 1. The system has no "modify link" operation

Nelson is explicit that the system *is* its command set:

> "What the Xanadu storage and hypertext system does--and thus is--is defined by the commands to which it responds." (4/61)

> "Of the 17 current commands in XU.87.1, only one command (RETRIEVEV) is concerned with delivery of the actual content fragments." (4/61)

Of those commands, the ones that touch links are: **MAKELINK** (create), the **FIND…FROMTOTHREE** family (search/count/paginate), and **RETRIEVEENDSETS** (read). There is no `MODIFYLINK`, `EDITLINK`, or `CHANGEENDSETS`. The only writer is creation:

> "MAKELINK… This creates a link in document <doc id> from <from set> to <to set> connected to <three set>. It returns the id of the link made." (4/68)

`RETRIEVEENDSETS` reads endsets; nothing writes them back. So the documented surface offers no way to mutate an existing link's connections.

## 2. A link's identity is permanent and fixed at creation

Links are addressed by **order of arrival**, and that ordering is permanent:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The first link is always `N.0.U.0.D.V.0.2.1`; the 755th is always `…0.2.755` (4/31). Unlike bytes, links are not rearrangeable, and deleting one does not renumber or free up the others — so every `MAKELINK` yields a genuinely new identity that is never reused. Combined with §1, this means a "changed" link is necessarily a *different* link.

Nelson did note that link sub-structure (which could one day support something like link versioning) was contemplated but not built:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

"A distinct possibility… discussed" = not part of XU.87.1. So even a versioned-in-place modification isn't specified; new-link-via-`MAKELINK` is the only documented route.

## 3. "Untouched in every respect" — the precise nuance

Creating the replacement link does **not** touch the original. Its endsets and address remain exactly as made. The only thing that can subsequently happen *to* the original is deletion by its owner —

> "Only the owner has a right to withdraw a document or change it." (2/29)

— and deletion is itself non-destructive, preserving the link in history:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

So: the original's endsets are never altered in place. Either it is left fully intact, or it is deleted (which preserves it in Istream/history and *still* doesn't rewrite its endsets). One could alternatively point a superseding/metalink at it — again leaving the original's own endsets untouched.

## 4. Why this need rarely even arises

It's worth stressing that ordinary editing does *not* require endset changes, because endsets reference permanent Istream content, not positions:

> "A Xanadu link is not between points, but between spans of data… it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

The back end maintains the attachment automatically as content moves in Vstream — so you don't modify the link, it simply stays attached. The scenario where you genuinely *want* different endsets means you want to connect *different content*, which is, semantically and architecturally, a different link.

## Caveat on sourcing

The curated material contains no passage that directly poses the question "what if I want to change a link's endsets?" My conclusion is derived from three things Nelson *does* state: (a) the system is defined by an exhaustive 17-command set that contains no link-modify operation (4/61, 4/68), (b) link identity is permanent order-of-arrival (4/31), and (c) deletion is non-destructive (4/9, 2/29). If you want certainty that no edit-link command was omitted from the curated summaries, the page to verify is the FEBE link-operations listing — NEED_RAW: 4/68–4/70.
