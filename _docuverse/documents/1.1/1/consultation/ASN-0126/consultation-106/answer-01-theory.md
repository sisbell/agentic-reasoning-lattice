## Question 1 [theory]

> Was retraction/deletion of a link intended as a mandatory, fixed-form act of the system (one attributed act withdrawing one link), or did the design admit configurations with no retraction at all, or acts that withdraw whole regions of links at once?

Verified what I needed: the 4/9 contents diagram (deleted-links state), the link subspace at 4/31, the complete XU.87.1 command inventory at 4/65–4/70, and the not-yet-implemented list at 4/79. Here is my answer.

---

## Short answer

Retraction of a link was **not** designed as a mandatory, fixed-form system act. I specified no link-retraction command at all: the published FEBE command set lets you *make* links but gives you no operation to unmake one. So a configuration with no retraction is not merely admitted — it is the configuration I documented. What the design *does* fix is **who** may withdraw a link (the owner of its home document — attribution is structural, not procedural) and **what withdrawal means** (a change of addressability, never destruction). And region-scale withdrawal is not an exotic extension; the structure of the design makes whole-region withdrawal the natural case.

## Retraction lives in the storage model, not the interface contract

I wrote: "What the Xanadu storage and hypertext system does--and thus is--is defined by the commands to which it responds." (4/61). By that definition, examine the 17 commands of XU.87.1 (verified against `resources/literary-machines/raw/page-232.txt` through `page-237.txt`): **MAKELINK** exists; no DELETELINK, UNLINK, or retract exists. The only removal command is **DELETEVSPAN** — "This removes the given span from the given document" (4/66) — and vspans are defined over the *byte* stream: "Logical addressing of the byte stream is in the form of virtual spans, or vspans" (4/11). Nothing extends it to the link subspace. The unimplemented-features list at 4/79 names private documents, accounting, and multiple-server methods — it does not even register link deletion as a pending operation.

Yet the *conceptual* model anticipates withdrawn links. The contents diagram at 4/9 (`resources/literary-machines/raw/page-176.png`) shows **DELETED LINKS** as a standing state of a document: "not currently addressable, awaiting historical backtrack functions, may remain included in other versions." So deletion was intended as a state a link can enter — but I deliberately left it out of the mandated protocol surface. Retraction is a property of the docuverse model, not a required verb.

## When withdrawal happens, attribution is fixed — by ownership, not by act-form

A link "is owned by a user" (4/41), and "Its home document indicates who owns it, and not what it points to" (4/12). Since "Only the owner has a right to withdraw a document or change it" (2/29), only the home-document owner can withdraw a link homed there. That is the one thing the design pins down: any retraction is attributable through the home address. But note the scope is *per arrangement*, not global — a deleted link "may remain included in other versions" (4/9). Even the cleanest single-link retraction only removes the link from the current version's arrangement; history and other versions keep it. There is no act in my design that annihilates a link from the docuverse.

## Whole-region withdrawal is structurally primary

Three mechanisms in the design withdraw links in bulk, none of them per-link acts:

1. **Document withdrawal.** A document "consists of its contents (including history and alternatives) and its out-links" (2/31). Withdrawing a document — the owner's right for private documents (2/29), and only by "lengthy due process" for published ones (2/43) — takes the entire home link space (`...0.2.1` through `...0.2.N`, per 4/31) with it in one act.
2. **Versioning.** Since link inclusion is per-version (4/9), publishing a new version that simply omits a set of links retires that whole region from the new arrangement, with no retraction acts at all. Supersession then steers readers to the link-free arrangement while the old one persists.
3. **The span algebra itself.** "Thus we may have spans of characters, spans of links, spans of documents, spans of versions" (4/24). Regions of links are first-class addressable objects; and because links sit "in their permanent order of arrival" (4/31), withdrawal never renumbers or compacts the region — fully consistent with withdrawal-as-state-change rather than removal.

There is also a fourth, *unattributed* path: a link's effect can lapse without anyone touching the link. Links survive editing only "if anything is left at each end" (4/43) — so if other owners delete all the bytes at one end from their current arrangements, the link is effectively withdrawn from current view by acts that were never acts upon the link.

## Mapped to your three alternatives

- **Mandatory fixed-form single-link act:** No. No retraction primitive was specified, and the only fixed elements are ownership-attribution and non-destruction.
- **Configurations with no retraction:** Yes — XU.87.1 as published is exactly such a configuration; the deleted-link state was anticipated for the future ("awaiting historical backtrack functions") but never contractually required.
- **Region-withdrawing acts:** Yes — via document withdrawal, version arrangements, and the span algebra, bulk withdrawal is the design's natural grain; single-link retraction would be the degenerate case, not the canonical one.
