## Question 1 [theory]

> Was the retraction/withdrawal operation intended to target only already-allocated link addresses, or is targeting ghost (never-emitted) addresses — including allocator anchors that cover entire future sibling streams — a permitted use?

## Ruling

Retraction/withdrawal was intended to act on **already-allocated, existing targets** — specific content or links the owner actually created. Aiming a destructive retraction at **ghost (never-emitted) addresses**, and above all at an **allocator anchor whose span embraces entire future sibling streams**, is *not* a permitted use. Let me explain why this follows directly from the design intent, then flag where the curated text stops and my reasoning extends.

## What the deletion model actually targets

Every deletion operation I specified is scoped to something that exists:

- Content deletion is a V-span removal: *"This removes the given span from the given document."* (4/66) It names existing bytes in a document's current arrangement.
- Link deletion produces the state *"DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"* (4/9) — a link that was made, then withdrawn by its owner.

Both presuppose an emitted thing. Neither is a sweep across an address range, and neither reaches forward into addresses that hold nothing yet.

## Ghost addressability is a *constructive* grant, not a destructive one

Ghost elements are real in tumbler-space, but look carefully at what they are *for*:

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

> "these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

> "A link to or search of an account or node will find any of the documents under it." (4/23)

The capability granted to ghosts is **linking** and **searching**. That is deliberate. A link or search that "embraces all the contents below" an anchor is *additive* — it gathers, it annotates, it discovers. When new siblings appear under that anchor later, the link harmlessly comes to include them. That is the same property I gave spans generally:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

> "There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

For a *link* or *search*, dynamic forward-embrace is a feature. For a *retraction*, the identical span semantics become catastrophic: pointing a destructive operation at a ghost allocator anchor would mean withdrawing content that has not been written, by owners who may not yet have acted. That inverts every guarantee the system exists to protect.

## Why the principles forbid it

1. **Non-destruction.** The whole point is that operations do *not* damage what they touch — *"making whatever changes seem appropriate—without damaging the originals"* (2/45). A retraction that reaches into unallocated future siblings is destruction at its most unbounded.

2. **Ownership.** *"Only the owner has a right to withdraw a document or change it."* (2/29) Future siblings under an allocator anchor are addresses the owner has *not yet baptized into existence*, and some may later be delegated. A retraction that pre-emptively covers them withdraws things no one yet owns — a contradiction in terms.

3. **Withdrawal is deliberately narrow and hard.** Published material *"may not [be withdrawn] except by lengthy due process."* (2/43) Withdrawal is the most constrained act in the system, precisely the opposite of a broad forward-reaching span sweep.

So the asymmetry is intentional: a ghost anchor may be the *target of a link* (it embraces the future safely) but must not be the *target of a retraction* (it would destroy the future).

## Where the text stops — flagging the gap

The terms in your question — "retraction operation," "allocator anchors," "future sibling streams" — are implementation vocabulary; they do not appear in *Literary Machines*. I specified two concrete removal operations (DELETEVSPAN at 4/66, link deletion at 4/9), and I specified ghost addressability for linking/search (4/23). I did **not** specify a generalized retraction primitive that takes an arbitrary tumbler range, and I never sanctioned a destructive operation that consumes unallocated address space.

NEED_RAW: 4/9, 4/23 — to confirm there is no additional text on either page describing deletion/withdrawal that targets unallocated or sub-tree-spanning addresses beyond what the curated extracts quote. My ruling above is grounded in the verified quotes plus the non-destruction, ownership, and ghost-element principles; the specific claim that retraction is *forbidden* from targeting ghost anchors is my design-intent determination, not a verbatim statement in the source.

## Bottom line

Allocate-then-retract on something that exists: yes. Retract a ghost: no. Retract an allocator anchor covering whole future sibling streams: emphatically no — that weaponizes the forward-embrace property I built for links and search against the non-destruction and ownership guarantees that property was meant to serve.
