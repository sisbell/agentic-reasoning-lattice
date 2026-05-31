## Question 1 [theory]

> Is document arrangement modification (non-empty, mutable `Σ.M(d)`) intended to be part of the substrate this relational layer sits on, or is the empty-arrangement constraint (M2) a permanent design commitment?

## Design intent: arrangement mutability is foundational, not optional

In Nelson's design, **a document's arrangement is inherently mutable, and a non-empty arrangement is the normal state.** The empty-arrangement constraint (M2) cannot be a permanent commitment without contradicting the core of what a Xanadu document *is*. It can only be a scaffolding simplification in the current formalization layer.

### Why mutable, non-empty arrangement is the substrate

The whole point of the Istream/Vstream split is to make arrangement (Vstream) the thing that changes while content (Istream) stays fixed. The arrangement `M(d)` — the V→I mapping — is precisely the mutable object:

> "A document is really an evolving ONGOING BRAID" (versions, 2/14)

> "Think of the process of making editorial changes as re-twisting this braid when its parts are rearranged, added or subtracted." (versions, 2/15)

Editorial operations are *defined as* mutations of this arrangement. From `v-space-addresses`:

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." (4/30)

And `REARRANGE` is a **pure Vstream operation** — it does nothing *but* modify `M(d)`:

> "Rearrange transposes two regions of text. With three cuts, the two regions are from cut 1 to cut 2, and from cut 2 to cut 3..." (operations, 4/67)

INSERT, DELETE, and APPEND likewise change the arrangement. INSERT explicitly shifts V-positions:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." (operations, 4/66)

A document that is constrained to an empty arrangement can hold no content and undergo none of these operations — which would exclude essentially the entire FEBE editing model.

### Why the relational layer in particular needs non-empty arrangement

The relational concepts this layer formalizes (correspondence, versions, links surviving edits) are *defined by* arrangement change. Correspondence exists because two arrangements map to shared Istream:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version." (correspondence, 2/26)

Version comparison (`SHOWRELATIONOF2VERSIONS`) only has content to compare if `M(d)` and `M(d')` are non-empty and differ. So the relational layer is *about* the variation of `M(d)`, not something that can sit on top of a permanently-empty arrangement.

### Conclusion

Non-empty, mutable `Σ.M(d)` is intended to be part of the substrate. M2 (empty-arrangement) reads as a deliberate, temporary restriction to get the relational layer formalized before arrangement-mutation is wired in underneath — not a permanent design commitment. Treating it as permanent would contradict the "ongoing braid" model and make INSERT/DELETE/REARRANGE/APPEND and version-correspondence unrepresentable.

---

**One caveat on scope:** the specific notation `Σ.M(d)` and the label "M2" are from this project's formal model, not from Nelson's text, so I can't verify the *exact* constraint statement against the curated sources. My answer addresses Nelson's design intent (which is authoritative for what the system *should* do); if you want me to confirm how M2 is currently written and where it's meant to be relaxed, point me at the relevant `formal-statements.md` and I'll check the constraint against this intent directly.
