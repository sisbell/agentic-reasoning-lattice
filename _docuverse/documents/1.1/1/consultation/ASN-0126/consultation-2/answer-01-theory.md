## Question 1 [theory]

> Is an *unattributed* retraction — one with no source/proposer recorded — an intended, essential capability of the retraction design, or may every retraction legitimately carry a single attributing source span?

## Short answer

In Nelson's design, an *unattributed* retraction — one with no source recorded at all — is **not an intended, essential capability**. It is closer to architecturally impossible. Whatever models a "retraction" in Xanadu is a *link*, and every link is owned and carries a home document that records who made it. So every retraction necessarily carries attribution. The question's second alternative is the correct reading: every retraction legitimately — indeed unavoidably — carries a single attributing source.

A note first: **"retraction" is not Nelson's term.** The nearest primitives in *Literary Machines* are the **Document Supersession Link** (a metalink), **link deletion**, and **content deletion**. My answer treats a retraction as whatever link asserts "this is withdrawn/replaced," because that is how the design would express it.

## Why attribution is structural, not optional

Nelson's most categorical statement forecloses ownerless objects:

> "By this convention, then, everything in the system is part of a document. No free-floating materials exist." (2/29)

A retraction is connective marking information, so it is a link, and links are owned:

> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." (4/41)

And ownership is exactly the attribution channel — carried by the link's *home*, independent of where its endsets point:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." (4/12)

The supersession link — the canonical "this is replaced" mechanism — is a metalink and is subject to all of the above. It is a *claim* with a recorded author, which is precisely why the design lets a third party assert one:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52)

The intent there is transparency of who-said-what, not anonymity. The supersession claim exists at its maker's address and is traceable to that maker. There is no slot in the model for a retraction that exists with *no* home.

## The distinction that resolves the question

There are two different things one might mean by "source," and the design treats them differently:

1. **Home / owner (attribution).** Always present. Every link, including a retraction, has a home document = an owner = a recorded source. This cannot be omitted; even "John Doe publication" (2/60) is pseudonymous — there is still an address.

2. **A from-set / proposer span in the endsets.** *Optional.* Nelson explicitly allows **one-sided links**, where there is no meaningful "from" end:

   > "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)

So a retraction may legitimately be *one-sided in its endsets* — it points at the retracted material with no separate proposer span in the link body — while still being fully attributed by its home. If your "single attributing source span" lives in the endsets, it is a design choice (you may include it or use a one-sided link). If it means attribution as such, it is guaranteed by the home and is not optional.

## Bottom line

- A retraction with **no source recorded anywhere** is not an intended capability; the design's "no free-floating materials" rule and link-ownership model mean attribution is inherent.
- Every retraction **legitimately (and necessarily) carries a single attributing source** via its home document.
- Whether that source *also* appears as an explicit from-set/proposer span is a representational choice the design leaves open (one-sided links are permitted, 4/48).

NEED_RAW: 4/48, 4/52–4/53 — if you want me to confirm the exact wording of the one-sided-link passage and the Document Supersession Link entry against the raw pages before you rely on them as load-bearing for a spec, those two are worth a direct check (the curated text covers them, but they sit at the center of this answer).
