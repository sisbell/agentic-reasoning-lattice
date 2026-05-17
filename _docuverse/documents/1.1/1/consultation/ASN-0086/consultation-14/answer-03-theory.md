## Question 3 [theory]

> Was sibling-frontier link emission (links sited only at sibling-frontier positions, never as descendants of existing links) intended as a substrate-level structural guarantee, or merely as the conventional behavior of one allocation routine?

Looking at this carefully, the question turns on whether the flat sibling-frontier arrangement of link addresses (2.1, 2.2, 2.3, ...) is mandated by the addressing substrate or simply convention. Let me verify the critical passage by reading the relevant page.

[I'll read page 198, which corresponds to chapter page 4/31 where link address structure is discussed]

Looking at the curated sources for the link address structure on 4/31:

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link to which the document is home
```

Nelson states:
> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

And critically:
> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

## Answer

**Sibling-frontier link emission is conventional behavior, not a substrate-level structural guarantee.**

The evidence in Nelson's text points clearly in one direction:

**1. The substrate permits subdivision.** The tumbler addressing system is universally forkable. Any owned address can spawn sub-addresses by adding digits to the right. This is the core "baptism" mechanism described at 4/20:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." (4/20)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

Nothing in the addressing substrate distinguishes link addresses from any other addresses with respect to forkability. Links live in tumbler-space like everything else.

**2. Nelson explicitly contemplates link subdivision.** The quote at 4/31 is decisive — he treats it as an open possibility, not a forbidden state:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." (4/31)

If sibling-frontier emission were a substrate guarantee, Nelson would describe subdivision as impossible or forbidden. Instead, he describes it as "a distinct possibility" with discussed use cases. This is the language of an unused option, not an architectural prohibition.

**3. What IS guaranteed at the substrate level.** Nelson does make firm structural commitments about link addresses:

- **Permanent order of arrival** — link N is always the Nth-created link (4/31)
- **No renumbering on deletion** — deleting link 2.5 doesn't shift 2.6 onward
- **Home document determines ownership** — the 2.x subspace belongs to the document owner

The flat sibling structure is consistent with these guarantees but not entailed by them. A subdivided link (e.g., 2.7.1, 2.7.2 as descendants of link 2.7) would still preserve permanent order, non-renumbering, and ownership semantics.

**4. The substrate-level principle is universal addressability.** From the link-to-link section at 4/49:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." (4/49)

The whole point of the design is that links are first-class citizens in the same address space as everything else. Forbidding descendant addresses under a link would be an asymmetry foreign to Nelson's design philosophy.

## Implementation reading

The phrasing "one allocation routine" in the question is apt: a specific allocator that always emits the next sibling at the current frontier (incrementing the trailing digit) is one valid strategy. Nelson's text describes this strategy as the current state of practice while explicitly leaving the door open to allocators that subdivide existing link addresses for purposes that "have been discussed." Any conformant implementation may emit sibling-frontier addresses, but the substrate does not require this and Nelson anticipated alternatives.

NEED_RAW: 4/31 — I would want to read raw page 198 directly to confirm the surrounding context of the "distinct possibility" passage and see whether Nelson hints at which uses were discussed. The curated extract captures the operative quote but may omit nearby qualifying discussion.
