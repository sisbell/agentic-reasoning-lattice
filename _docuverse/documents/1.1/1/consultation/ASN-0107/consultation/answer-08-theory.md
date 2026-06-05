## Question 8 [theory]

> Must a count taken at one moment and the same count taken later differ only by the net of links added and links retracted in between?

Short answer: As a matter of design intent, **only conditionally**. The conservation identity — count(t₂) − count(t₁) = (links added) − (links retracted) — holds for a *stable existence-count specified against permanent addresses*, but it is **not** a guarantee Nelson states explicitly, and it fails outright for the delivery counter and for requests pinned to ephemeral positions.

## Why it can hold

Two operations change which links exist and are addressable: creation (MAKELINK) and retraction (deletion). Deletion doesn't destroy the link or recycle its address — it moves it to a "not currently addressable" state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

And link addresses are never renumbered, so retracting one link doesn't perturb the count by shifting others:

> "The links designated by a tumbler address are in their permanent order of arrival." (4/31)

So if you take a *count of currently-addressable links* matching a fixed request, and between the two readings the only mutations are creations and retractions of links that match that request, then the difference is exactly net-added-minus-retracted. That is the natural reading of an existence count.

## Two ways it breaks

**1. The delivery counter (cash register) is monotonic, not conserved.** A document's cash register counts *deliveries*, not *existence*. It only ever climbs and never decrements when a link is retracted:

> the cash register "increments whenever bytes or links are delivered out of the document. The cash register has no size limit." (5/13)

So if "count" means this counter, the identity is false — retractions don't subtract from it.

**2. Survivability + ephemeral V-positions can move membership without any add/retract.** Links attach to bytes, not positions, and survive editing:

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43)

If a request is specified against permanent Istream addresses, a surviving link keeps matching, so the count is stable except for genuine add/retract events — and the identity holds. But if a request is pinned to current *V-stream* positions (which "may be constantly changing," 4/11), intervening edits can shift content into or out of the requested span, changing the matching count *without a single link being created or deleted*. In that case the difference is not accounted for by net links added and retracted.

A related subtlety: searches whose endsets embrace ghost elements (e.g., "all links to this account") will see the count rise as new links appear under that address — but those *are* additions, so the identity still holds for them.

## Bottom line

The invariant is a faithful expression of Nelson's existence/identity model *when* the count is over currently-addressable links and the request is anchored to permanent addresses. It is not something Nelson asserts as a stated guarantee, and it does not hold for the cash-register delivery counter or for position-relative queries over an edited document.

NEED_RAW: 4/69 (exact FINDNUMOFLINKSFROMTOTHREE semantics — to confirm whether the documented count is defined over currently-addressable links only, which would pin down condition (1) precisely)
