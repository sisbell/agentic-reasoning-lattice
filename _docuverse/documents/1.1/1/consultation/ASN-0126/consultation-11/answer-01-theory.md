## Question 1 [theory]

> Was a citation/link designed so it must carry at least one target, or is a zero-target (empty-G) typed relation a legitimate (if degenerate) form whose "must cite something" rule belongs to the operational/front-end layer rather than the structural shape?

## Short answer

Structurally, the link is a **triple of arbitrary span-sets** (from-set, to-set, type), and Nelson does **not** impose a per-endset "must carry a target" requirement on the structural shape. He explicitly sanctions degenerate forms — most clearly the **one-sided link** — and explicitly calls links only *"typically"* directional. So a zero-target / empty-G typed relation is a legitimate (if degenerate) structural form, and the "must cite something" rule properly belongs to **link-type semantics and the operational/front-end layer**, not to the shape of the link itself.

## The structural shape imposes no nonempty-target rule

The link is defined as three symmetric endsets, each an *arbitrary* collection:

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

> "A link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." (4/42)

Crucially, directionality (the from→to "target" relation) is presented as a *default*, not a structural mandate:

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" (4/42)

The word *"typically"* is doing real work here: it tells us the from/to pairing is the common case, not a structural invariant.

## Nelson explicitly endorses a degenerate, single-endset form

The decisive evidence is the one-sided link, where the to-set is simply not used:

> "An important variation where a link has only one side - something pointing to material, but not from other material. The paragraph designator is an example. This avoids terminological confusion by using only the from-set to designate the matter pointed at." (4/48)

> "Unfortunate terminological problem: since it has only one side, we use the first endset to designate the matter pointed at. To call this 'from' is inane." (4/48)

So an endset being empty is not a structural error — it is a recognized, named form. The "from/to" target structure can collapse to a single populated side.

## The type endset can even point at nothing stored

Emptiness-of-content is also explicitly tolerated on the type endset:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

This reinforces that the structural machinery does not validate the *occupancy* of an endset's targets; it only records and indexes addresses.

## Where the "must cite something" rule lives

Nelson keeps semantic constraints out of the back-end's structural model and pushes them up:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." (4/43)

The back end stores three endsets (`MAKELINK ... from <from set> to <to set> connected to <three set>`, 4/68) and searches them by the satisfaction model — *"A link satisfies a search request if one span of each endset satisfies a corresponding part of the request"* (4/58). Neither operation encodes a "this type must have a nonempty target." That obligation is a property of a *particular type's meaning* — a quote-link or citation-link is semantically pointless without a source — and Nelson is explicit that front-end programs carry the user-facing semantics: *"the complications of the protocol are to be handled invisibly by programs in the user's front-end machine"* (FEBE, 4/61).

## Important caveat (beyond what Nelson states verbatim)

Nelson's *described* degenerate case — the one-sided link — still has **exactly one populated endset** (the from-set, used as the pointer-at-target). He never describes a *fully* empty link in which every endset is empty and the relation connects nothing at all. So:

- **Empty-G specifically (empty to-set/target endset):** clearly legitimate — that is precisely the one-sided link (4/48), and directionality is only *"typically"* present (4/42).
- **A truly zero-endset link (nothing populated anywhere):** not addressed by Nelson and would be vacuous; the practical structural floor implied by the one-sided link is "at least one populated endset overall," not "at least one populated *target* endset."

This last distinction is my inference from the one-sided-link passage and the "typically directional" qualifier; Nelson does not state the all-empty case explicitly.

NEED_RAW: 4/48, 4/58 — to confirm verbatim whether Nelson anywhere states a lower-bound (nonempty) requirement on any endset, or describes a link with no populated endset at all.
