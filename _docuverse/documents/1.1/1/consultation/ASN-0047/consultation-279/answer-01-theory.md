## Question 1 [theory]

> Does the design intend a link's order-of-arrival position in its home document to be a permanent, unrearrangeable guarantee — or merely that links are withdrawable with no positional-stability promise?

## Answer

The design intends **both**, and they are not in tension: a link's order-of-arrival position **is** a permanent, unrearrangeable guarantee, *and* links are independently withdrawable — but withdrawal does **not** disturb the positions of other links.

### The positional guarantee is explicit and permanent

Nelson distinguishes links sharply from bytes here. Bytes can be rearranged in the Vstream; links cannot. Their address *is* their order of arrival, fixed permanently:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." (4/31)

The link-address subspace encodes serial position by creation order:

> "N.0.U.0.D.V.0.2.1 (the first link of the document, stored in the document's space)" (4/31)

> "N.0.U.0.D.V.0.2.755 (the 755th link to which the document is home)" (4/31)

The Istream address structure reinforces this — the link sub-address is "a link-address designating the link's serial position," and links are "currently not rearrangeable" (`design-intent/i-space-addresses.md`, citing 4/30). So link #1 is always the first link created, #755 always the 755th. There is no REARRANGE-equivalent for links the way there is for bytes.

### Withdrawability is a separate axis — and does not renumber

Links *can* be deleted by their owner, but deletion is non-compacting. A deleted link enters the "not currently addressable" historical state rather than vacating its slot:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

Because addresses are tied to permanent order of arrival, deleting link `2.5` does not renumber `2.6 … 2.N` (`concepts/links.md`, "Permanent Order of Arrival"). So withdrawal removes a link from current addressability without breaking the positional stability of the rest.

### Why the framing's "either/or" is a false choice

The question poses permanence *vs.* mere withdrawability. The sources show the two are orthogonal:

- **Positional identity** — permanent and unrearrangeable (4/31).
- **Lifecycle** — a link can be withdrawn into the historical-backtrack state (4/9), and links made to content survive editing of that content as long as bytes remain at each end (4/42–4/43).

A link is therefore *withdrawable but not relocatable*: you can remove it, but neither you nor anyone else can shuffle its order-of-arrival position, and removing it leaves every other link's position intact.

### Scope caveat

The curated sources are clear that order-of-arrival positions are permanent and that deletion is non-renumbering. They do **not** contain an explicit sentence stating "the slot of a deleted link is never reissued to a future link." That non-reuse follows logically from append-only, permanent-arrival numbering (a new link becomes #756, not a reused #5), but if you need Nelson stating reuse-prohibition verbatim:

NEED_RAW: 4/30–4/31
