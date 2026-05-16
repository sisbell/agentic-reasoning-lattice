## Question 9 [theory]

> Does the design require that single-link withdrawal at arbitrary V-positions be supported, with the withdrawn link transitioning to "not currently addressable" status while retaining its arrangement position — or is tombstoning a separate state attribute orthogonal to V-position arrangement?

I need to check the relevant pages directly to answer this precisely, since the question conflates two address regimes.

[Reading the relevant raw pages to verify the specific language about link deletion state and addressing.]

Let me look at pages 4/9 and 4/31 for the authoritative language.

Based on the curated sources, the question's premise needs unpacking: **links do not have "V-positions" in the same sense as bytes**. Links live in a separate subspace (`0.2.N`) with addresses assigned by **permanent order of arrival**, not by rearrangeable byte position.

## What the Specification Says

**Links live in the 2.x subspace with creation-order addresses:**

The link address structure (from `links.md` curated source, derived from 4/31):

```
N.0.U.0.D.V.0.2.1    → first link in document
N.0.U.0.D.V.0.2.755  → 755th link in document
```

The key invariant, per Nelson (4/31):

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document."

This means:
- Link `2.1` is **always** the first link created
- Link `2.755` is **always** the 755th link created
- Deleting link `2.5` does **not** renumber `2.6` through `2.N`

**Deletion is a state transition, not a positional operation.** Per 4/9:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)"

## Answer to Your Question

**Tombstoning is the model, and it is essentially the only model — because links don't have a rearrangeable "V-position arrangement" to be orthogonal to.**

The architecture works as follows:

1. **A link's address is fixed at creation** by its permanent ordinal position (the N in `0.2.N`). This is not a Vstream arrangement — it is a permanent serial position.

2. **Withdrawing a link transitions it from "addressable" to "not currently addressable"** — that is, it tombstones. The address slot remains; the link's content/endsets enter the historical-backtrack state.

3. **The state attribute (addressable / not currently addressable) is the entire model.** There is no separate V-position arrangement for links to manage — Nelson explicitly defers rearrangement of links to a possible future ("The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." — 4/31).

So the answer is **neither A nor B exactly, but closer to a degenerate form of A**: the withdrawn link retains its permanent serial address (which is its only "arrangement"), and the addressability flag is the state change. There is no orthogonal V-position attribute because links don't have one — they only have their creation-order position.

## Caveat

NEED_RAW: 4/31, 4/9 — to confirm whether Nelson explicitly addresses *what happens to a withdrawn link's serial address* (does the next-created link get N+1, or does it reuse the tombstoned slot?). The curated source strongly implies addresses are never reused (consistent with permanence), but I should verify the exact language on 4/31 about whether the link counter increments past tombstones. The diagram on 4/9 showing "DELETED LINKS" as a parallel state to "DELETED BYTES" is also worth seeing in original to confirm visual semantics.
