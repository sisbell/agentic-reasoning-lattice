## Question 1 [theory]

> When matching links are delivered to a reader in successive windows rather than all at once, what must the system guarantee about the order in which those links arrive?

## The Guarantee: A Stable, Permanent Ordering

When links are delivered in successive windows (via `FINDNEXTNLINKSFROMTOTHREE`), the system must guarantee that they arrive in a **consistent, deterministic order that does not change between calls** — specifically, their **permanent order of arrival**. This is what makes paginated retrieval coherent: each window must pick up exactly where the previous one ended, with no duplication and no omission.

### Why this ordering must exist

The pagination operation works by reference to a position in a *list*:

> **FINDNEXTNLINKSFROMTOTHREE**: Paginated link retrieval — "no more than `<nlinks>` items past that link on that list." (4/69)
> — `prompts/.../operations.md`

The phrase "items past that link on that list" only has meaning if there is a single, well-defined, stable list. The front end hands back the last link it saw and asks for the next N "past" it. If the ordering were unstable or recomputed differently each call, "past that link" would be undefined and windows could overlap or skip links.

### What defines the order

For links homed in a document, that order is fixed at creation and never changes:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)
> — `prompts/.../links.md`

This is reinforced by the rule that link addresses are assigned sequentially and are *not* rearrangeable like bytes:

> "Unlike bytes (which can be rearranged in Vstream), **links keep their creation-order addresses permanently**" ... "Deleting link `2.5` doesn't renumber `2.6` through `2.N`."
> — `prompts/.../links.md` (citing 4/31)

So the ordering is **tumbler-address order, which equals permanent order of arrival** — and because deletion does not renumber survivors, the order is stable across the lifetime of the search.

### Why windowing is necessary in the first place

The reason links come in successive windows rather than all at once is the sheer volume — link searches can produce "avalanches of material." The windowing design is tied to Nelson's guarantee that search remains tractable:

> "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." (4/60)
> — `prompts/.../links.md`

A reader can page through matching links incrementally; the stable arrival-order ordering is what lets the system resume the result stream correctly across those increments.

---

**Summary:** The system must guarantee a single, stable, deterministic ordering of matching links — their permanent order of arrival (equivalently, tumbler-address order) — so that each successive window continues exactly past the last link returned, without re-ordering, duplication, or gaps.

One caveat: the curated sources establish the *existence and stability* of the order (4/31, 4/69) but do not contain Nelson's verbatim wording for any explicit ordering guarantee inside the `FINDNEXTNLINKSFROMTOTHREE` command specification itself. If you need his exact phrasing for that command, see NEED_RAW: 4/69.
