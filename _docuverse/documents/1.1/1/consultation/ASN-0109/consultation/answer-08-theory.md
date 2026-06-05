## Question 8 [theory]

> What invariant ensures the endsets a read returns are consistent with what is actually stored — that the system cannot report endpoints the link does not hold?

## Short answer

Nelson does not name a formal "read-consistency invariant" for `RETRIEVEENDSETS` in the way the question frames it. What he provides instead is something stronger and more structural: **the endsets are not a description of the link that could drift out of sync with it — the endsets *are* the link.** A read cannot report endpoints the link does not hold because there is no separate stored "truth" for the report to diverge from. The link's identity is precisely its mapping onto the tumbler line.

## Why this holds structurally

**1. Endsets are positions on the universal address space, not cached metadata.**

A link is defined as three endsets mapped onto the tumbler line. There is no other representation of "what the link connects":

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." (4/45)

> "A link's home (any home) is an element located on one side; and its three endsets map to the other sides." (4/46)

So `RETRIEVEENDSETS` — "This returns a list of all link end-sets that are in <spec set>" (4/70) — returns the link's actual mapping, not a summary of it. The thing read and the thing stored are the same object.

**2. Endsets attach to bytes by permanent I-address, so they cannot acquire phantom endpoints.**

Endsets point to spans of bytes by their content addresses, which are permanent (Istream). Editing can only remove bytes from an end, never invent new ones:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." (4/42)

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

This is the asymmetry that protects read consistency: survivability is *attrition only*. A link's endset can shrink as bytes are deleted, but no operation grafts addresses onto an endset that the link never held. So a read can under-report (an endpoint whose bytes were all deleted vanishes) but cannot over-report.

**3. Type endsets matched by address, not content — so even "ghost" endpoints are exactly what was stored.**

Even where an endset points at an address with nothing stored there, the endset is still the literal address the link holds:

> "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." (4/44-4/45)

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

This rules out the inverse failure too: the system reporting a *real* endpoint is just reporting the stored address, regardless of whether content sits there.

## What Nelson does *not* explicitly guarantee

NEED_RAW: 4/68-4/70 — The curated sources give `RETRIEVEENDSETS` semantics (4/70) and the endset/tumbler structure, but Nelson does **not** state a named invariant of the form "a read cannot report endpoints the link does not hold." That property is an *implication* of (a) endsets being the link's actual stored structure and (b) survivability being attrition-only — not a guarantee Nelson articulates in those words. If you need the precise operational wording around the link-retrieval commands, the raw protocol pages (4/68-4/70) should be checked, since the concurrency/locking discipline that would enforce consistency *during* concurrent editing is part of the implementation's session layer, not Nelson's specification (his model is stateless at the command level).
