## Question 2 [theory]

> For `idem = ⊤` shapes, was duplicate-suppression intended to be a substrate-level rejection at emission time, or a higher-layer policy that the substrate trusts but does not check?

# Duplicate-suppression for idempotent shapes

The terminology `idem = ⊤` and "substrate-level" is not mine — these are implementation terms from your spec work. I'll answer in terms of what I actually wrote about how the substrate should behave.

## What I specified

In Chapter 4 I describe links as accumulating in **permanent order of arrival**:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The link instance addresses are sequential — `N.0.U.0.D.V.0.2.1`, `N.0.U.0.D.V.0.2.755` — and they "keep their creation-order addresses permanently." `MAKELINK` is specified as a creation operation that **returns the id of the link made**, with no semantics for "this already exists, here's the prior id."

I do not anywhere specify that the back end checks whether an equivalent link already exists before accepting a new emission.

## What this implies about layering

My consistent architectural pattern is to keep the back end minimal and push semantic policy outward. On scanning specifically:

> "Many people, particularly those who are accustomed to the assorted 'model' of other file systems, have a hard time getting used to our link model, and insist that scanning should be part of the Xanadu back end." [LM 4/72]

I push back — scanning belongs in the middle end. Duplicate detection requires exactly the kind of cross-link scan I refused to put in the substrate. To suppress duplicates at emission, the back end would have to scan existing links for endset-equivalence before accepting each `MAKELINK` — that is back-end scanning by another name.

The substrate's job is permanence and addressability of what users emit. Filtering — "Link filters... is a key aspect of front-end design" [LM, links] — is where I locate the work of deciding which links are interesting, redundant, or junk:

> "The junk-link problem... Filtering out junk links (links in a universe full of them) is important for system performance."

## Direct answer to your question

Based on what I specified: **higher-layer policy that the substrate trusts but does not check.** The substrate accepts emissions, assigns them permanent order-of-arrival addresses, and exposes them through search. Whether two emissions are "the same" under some `idem = ⊤` shape is a semantic judgment that belongs in the middle end (filters, search constraints) or the front end (the application deciding not to emit again).

This is consistent with my general stance that the back end stores what users emit and the legitimacy or redundancy of emissions is not the substrate's business: "perforce all use whatever is legitimate" [LM 2/47, paraphrased context on terminal-level control].

## Caveat

NEED_RAW: 4/56-4/60, 4/72-4/73 — the curated extracts cover link search and the junk-link problem but I want to verify I did not give a more direct answer about idempotent emissions in the search/middle-end sections that wasn't pulled into the concept files. If there is a passage where I explicitly assign duplicate-checking to a layer, it would most likely be there.
