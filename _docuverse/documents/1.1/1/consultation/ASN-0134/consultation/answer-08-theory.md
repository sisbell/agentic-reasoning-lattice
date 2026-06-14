## Question 8 [theory]

> When a writer's change and a reader's view of the same shared content meet, what must hold so the reader never sees that change counted twice nor counted as a broken fragment?

# When Edit Meets Shared View: The Correspondence Invariant

You've described the exact moment Xanadu was built to survive: shared content (a window/transclusion into someone else's material) being *changed* by its owner while a *reader* holds a view that includes it. The two ways this can go wrong are precisely the two you name — the change shows up **twice** (duplication), or the change leaves the reader staring at a **torn piece** (severing). Let me be precise about what must hold to forbid both, because the answer is one structural commitment with two consequences.

## The governing invariant: identity lives in Istream, not in arrangement

The thing that must hold is the **separation of permanent content-identity (Istream) from mutable arrangement (Vstream)**, with all sharing done **by reference, never by copy**. A writer's change acts on the *arrangement* (the V→I mapping); it never touches the *identity* of the bytes. That single discipline is what makes both failure modes structurally impossible rather than merely unlikely.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." — 4/11

> "Non-native byte-spans are called inclusions or virtual copies." — 4/11

The reader's view of shared content is a *reference home-ward*, not a held copy. Everything below follows from that.

## Why the change is never *counted twice*

There is only ever **one** instance to count. Because inclusion is reference and not copy, the writer's content and the reader's view are not two objects that must be reconciled — they are the *same* Istream identity seen from two places. You cannot double-count a thing of which there is structurally only one.

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update — especially the problem of updating documents which depend on other documents. We solve this problem simply by windowing to a changing document." — 2/36

The relation that *guarantees* the system knows the reader's view and the writer's edit are the same content is **correspondence** — shared Istream origin. A change therefore *refracts* to the corresponding place in the reader's view instead of arriving as a fresh, separate insertion alongside the old:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." — 2/26

This is the precise answer to "what must hold so it isn't counted twice": **correspondence by shared I-address must be preserved**, so the writer's change is recognized as *that same content, moved or amended*, not as a second copy. The system can always emit the correspondence explicitly — that is exactly what `SHOWRELATIONOF2VERSIONS` exists to return:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." — 4/70

> "highlighting the corresponding parts is a vital aspect of intercomparison." — 3/13

## Why the change is never seen as a *broken fragment*

The reader's window is a **strap to bytes, addressed by their permanent Istream identity — not to positions**. An edit re-maps positions; the strap stays whole on whatever bytes survive. A fragment could "break" only if the reference were to positions (which shift) or if the bytes could be destroyed (they cannot).

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them. This also works for alternative versions in which part of each end has survived." — 4/42

> "Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end**." — 4/43

And the writer's *deletion* — the most dangerous case — does **not** remove the bytes the reader is windowing. DELETE is a Vstream operation; the Istream content persists, and remains included everywhere it was shared:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." — 4/11

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, **may remain included in other versions**.)" — 4/9

So an insertion that splits the windowed span leaves it *discontiguous but intact* (still the same bytes), and a deletion in the writer's own version leaves the reader's inclusion *untouched*. Either way: no torn fragment.

## The binding mode decides *which* change, not *whether* the invariant holds

Whether the reader sees the writer's change at all depends on how the window is bound — but the no-duplication / no-breakage guarantee holds in **both** modes:

> "A quotation — an inclusion window — may be fixed to another document in two ways: at a certain point in time, in which case revisions are seen by the user only when he or she asks, 'What has this passage become?' Or second, at a relatively fixed location in the document space, in which case updates are seen automatically." — 2/37

- **Time-fixed:** the reader sees a frozen prior state; the later change simply isn't present — trivially neither doubled nor broken.
- **Location-fixed:** the change propagates automatically — and *here* the correspondence + survivability invariants do the real work, delivering the update once, in place, intact.

In all cases the part is reconstructed canonically on demand:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." — 2/16

## What must hold — stated as a conservation law

For the reader to see the writer's change exactly **once** and **whole**, three things must hold, and they are facets of one commitment:

1. **Single identity / reference-not-copy** — shared content has exactly one Istream address; there is only one thing to count, so duplication is impossible.
2. **Correspondence preserved** — V-positions sharing an I-address are recognized as the same content, so a change *refracts* into the reader's view at the right place instead of arriving as a second insertion.
3. **Span-survivability over permanent Istream** — the window attaches to bytes by permanent address; DELETE acts only on Vstream; "if anything is left at each end" the inclusion stays whole and stays included everywhere.

A design note on intent: this guarantee is **structural, not a matter of locking or timing**. I never specified a concurrency-control mechanism to police the "meeting" of writer and reader, because none is needed for this property — the permanence and singularity of Istream identity is what makes the change uncountable-twice and unbreakable. The bytes have one home; every view refracts to it; editing re-arranges the map but never forks the identity nor orphans the reference.

---

*One scope caveat I'll flag honestly:* the curated sources establish the structural invariants above conclusively, but they describe the **structural** guarantee, not a real-time read-during-write race protocol. If you specifically want my treatment of *concurrent* access mechanics (back-end request handling while an edit is in flight), that is implementation territory I deliberately left to the back end rather than specifying in *Literary Machines* — and it would be **NEED_RAW: 4/58–4/60, 4/74–4/75** to say more about the shared-search/forwarding behavior under live contention.
