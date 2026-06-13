## Question 8 [theory]

> If the content a link's endsets reference is edited after the link is made, must the link's membership in the count stay stable so long as the link itself persists, or may content edits alone move a link in or out of a description's count?

## Ruling

For a description whose endset constraints are grounded in **content identity** (Istream addresses) — which is what the link index is actually built over — a persisting link's membership in the count **must stay stable**. Content edits alone (INSERT / DELETE / REARRANGE) cannot move such a link in or out. This is not an incidental property; it is the count-level expression of the survivability guarantee, and it is mandatory design intent.

Content editing can change membership in only two boundary cases, and neither is "content edits alone, link persisting, identity-grounded count":
1. The link is **destroyed** (all bytes at one endset deleted) — that is non-persistence, which your premise excludes.
2. The description is **anchored to current Vstream positions** rather than to content identity — in which case the description's *referents* move, not the link's endsets.

## Why membership is stable

The mechanism is the byte-identity binding. A link does not hold a position; it holds bytes:

> "A Xanadu link is not between points, but between spans of data."
> — 4/42

> "This has a crucial advantage: it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them."
> — 4/42

Editing operates on the Vstream arrangement, not on the Istream identities the endsets reference. The curated treatment of i-space/v-space states this directly: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" (4/11) — the V-position drifts, the I-identity does not.

Now combine that with what "being in the count" actually means. A link is in a count iff it satisfies the request:

> "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request."
> — 4/58

And the search compares **addresses**, not current content:

> "The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address."
> — 4/44–4/45

So the chain is: count-membership = satisfaction = address overlap between the link's endsets and the description. The endsets are fixed at MAKELINK time and are Istream-grounded; editing changes V, not those I-addresses. Therefore satisfaction is invariant under editing, and the link neither enters nor leaves an identity-grounded count while it persists. Walk the three operations:

- **INSERT** allocates *fresh* I-addresses; the endset gains nothing, so the overlap is unchanged.
- **DELETE** removes bytes from the Vstream but not from the Istream (deleted bytes "remain in Istream"), so the endset's I-addresses still resolve and still match.
- **REARRANGE** moves V-positions only; I-addresses are untouched.

## The two boundaries

**Boundary 1 — destruction is non-persistence.** Survivability is qualified: it holds "if anything is left at each end."

> "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."
> — 4/43

If an edit deletes *every* byte at one endset, the link ceases to exist and drops out of all counts. But that is the link not persisting, not a content edit relocating a live link — your premise ("so long as the link itself persists") rules it out.

**Boundary 2 — version- or position-scoped descriptions.** Survival of an endset is version-relative:

> "This also works for alternative versions in which part of each end has survived."
> — 4/42

So if a count is scoped to a particular version's Vstream positions rather than to content identity, two things can shift membership while the link still lives: (a) deleting the *only* surviving span that overlapped the request drops the link from that version-scoped count even though the link survives elsewhere; (b) an INSERT/REARRANGE re-maps V→I, so a position-anchored request now resolves to different I-addresses and a surviving endset can fall into or out of it. In both, it is the **description's anchors moving under the edit**, not the link's identity-bound endsets — which is exactly why the architecture resolves V-positions to I-addresses (a front-end/middle-end step) *before* hitting the identity-grounded back-end index. The instability lives in the resolution, not in the count.

## Formalizable invariant

> Let `D` be a description whose endset constraints are expressed over Istream identity, and let `L` be a link that persists across an editing sequence `E ∈ {INSERT, DELETE, REARRANGE}*` applied to document content. Then `satisfies(L, D)` is invariant under `E`; hence `L ∈ count(D)` is stable for the lifetime of `L`. Membership changes only via (i) destruction of `L` (an endset emptied), or (ii) re-anchoring `D` against shifted Vstream positions — i.e., `D`'s referents moving, not `L`'s endsets.

This is the whole point of separating Istream from Vstream and strapping links to bytes rather than positions: editing must not silently rewrite the web of connections. A count grounded in content identity is a stable fact about the docuverse for as long as its links live. The matching efficiency principle — "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS" (4/60) — presumes exactly this stable, address-keyed satisfaction relation.

---

**Source note:** The ruling is a synthesis of verified material — survivability (4/42–4/43), the satisfaction model (4/58), address-based matching (4/44–4/45), and the I/V separation (4/11) — rather than a verbatim Nelson statement about "count membership" as such. The curated sources do not spell out the partial-survival counting case in those words. If you want Nelson's exact language on counting behavior when an endset partially survives an edit, that would be in the search/count section:

NEED_RAW: 4/58–4/60
