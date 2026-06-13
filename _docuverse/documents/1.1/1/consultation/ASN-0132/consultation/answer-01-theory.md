## Question 1 [theory]

> When the system reports how many links match a four-set description, must the unit counted be the link's permanent identity, so that each link contributes exactly one to the count regardless of how it is anchored or displayed?

The raw page images aren't present in this checkout (the `resources/literary-machines/raw/` tree referenced in the inventory isn't here), so I'll answer from the verified curated extracts and flag the one spot where raw confirmation would help.

---

# Yes — the link itself is the unit, and it counts once

When the system reports how many links match a four-set description (home-set, from-set, to-set, three-set), the thing being counted **is the link as a first-class object with a permanent identity**. Each qualifying link contributes exactly **1** to the count, no matter how many spans its endsets touch, no matter how many places it shows up when a front end paints it, and no matter how many versions it refracts into.

This is not an incidental implementation choice. It is forced by three load-bearing facts of the design.

## 1. The link is what satisfies the request — not a span, anchor, or display

The matching rule is a predicate over a *link*:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." `[LM 4/58]`

A link is either satisfying or not satisfying. There is no smaller satisfying unit. And the counting language treats links exactly that way — as a discrete quantity:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." `[LM 4/60]`

The companion retrieval command makes the unit explicit: it returns *links*, one per match —

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." `[LM 4/69]`

`FINDNUMOFLINKSFROMTOTHREE` is the cardinality of that list. The list holds links; therefore the count counts links.

## 2. A link *has* a permanent identity to count

A link is "a connective unit, a package of connecting or marking information. It is owned by a user." `[LM 4/41]` It lives at its own permanent tumbler address, fixed at creation:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." `[LM 4/31]`

The 755th link a document is home to is permanently `N.0.U.0.D.V.0.2.755` `[LM 4/31]`; deleting an earlier link never renumbers it. So "the link's identity" is a well-defined, stable thing — and the **home-set** in your four-set query is precisely the dimension that selects links *by that identity/residence*:

> "The document must be specified because that determines the actual residence of the link..." `[LM 4/63]`
> "If the home-set is the whole docuverse, all links between these two elements are returned." `[LM 4/63]`

You are asking "how many distinct links, resident here, satisfy these endset constraints?" The home-set guarantees the answer is keyed to identity.

## 3. "Regardless of how it is anchored or displayed" — both follow directly

**Anchoring** cannot multiply the count. An endset is an arbitrary, possibly broken span-set:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." `[LM 4/42]`

The satisfaction rule says only *one* span of each endset need fall in the request — "from all or any part of <from set>" `[LM 4/69]`, "one span of each endset satisfies" `[LM 4/58]`. A link whose from-set seizes five passages and whose to-set seizes three is still **one** satisfying link. The "AND of the ORs" model collapses any number of matching anchor spans into a single yes for that link.

**Display** is a front-end concern and never touches the count. The same link is rendered at every anchor point it holds, and it can be followed refractively into every version of a prismatic document:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." `[LM 2/26]`

"A link to all versions" is still **one link**. Refraction is something the *front end does on retrieval*; it does not mint new link-identities for the back end to tally. The back end counts what is stored and owned, not what a viewer is shown.

## What the count is therefore *not*

To make the guarantee sharp, the count is not:
- the number of matching **byte-pairs** (that would contradict "any part" / "one span... satisfies"),
- the number of **anchor spans** a link presents,
- the number of **display occurrences** across passages, or
- the number of **versions** the link reaches into.

A link with a 5-span from-set and a 3-span to-set, shown at eight anchor points across four versions, is counted **once**. That is the user-facing guarantee: a link is a *thing*, with one owner and one permanent address, and the census counts things.

---

### One verification caveat

The curated extracts give me the verbatim definitions of the *list* command (`FINDLINKSFROMTOTHREE`, `[LM 4/69]`) and the satisfaction/quantity model (`[LM 4/58]`, `[LM 4/60]`), but they do **not** quote the `FINDNUMOFLINKSFROMTOTHREE` command text itself. My conclusion follows necessarily from the matched list/count command pair and the per-link satisfaction rule, so I'm confident in it — but if you want the count command's exact wording on the page (only to *confirm*, not to change, the above):

NEED_RAW: 4/68–4/69 (the `FINDNUMOFLINKSFROMTOTHREE` / `FINDNEXTNLINKSFROMTOTHREE` command definitions)
