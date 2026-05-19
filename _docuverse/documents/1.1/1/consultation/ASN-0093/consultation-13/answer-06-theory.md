## Question 6 [theory]

> In LM 4/9's tombstone-style withdrawal, is the withdrawn link's entry preserved in the address space with a tombstone-marked value, or is it removed entirely from the link store?

# LM 4/9 Withdrawal: Preserved as Tombstone, Not Removed

Nelson's diagram on page 4/9 ("Technical Contents of a Document") explicitly places **DELETED LINKS** as a recognized category within the document's technical contents — meaning the entry is *preserved* in the address space, not removed.

## The Diagram Structure (4/9)

The document's "TECHNICAL CONTENTS" divides into two branches:

- **CURRENT**
  - LIVE BYTES (currently addressable)
  - LIVE LINKS (currently addressable)
- **WITHDRAWN**
  - DELETED BYTES
  - DELETED LINKS

Both withdrawn categories carry the same annotation:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" — 4/9

## What This Tells Us

Three phrases settle the question:

1. **"not currently addressable"** — the entry is not removed; it's reachable in a non-current sense. Removal would not need this qualifier.
2. **"awaiting historical backtrack functions"** — the data is preserved precisely so that historical backtrack can restore or display it. Removed entries would have nothing to await.
3. **"may remain included in other versions"** — the link's underlying record persists; other versions still reference it.

The withdrawal is bookkeeping over a preserved record. The link's identity (its tumbler address) remains assigned and its content remains in the docuverse — it is simply absent from the *current* view of the document.

## Consistency with Surrounding Principles

This is the same model Nelson applies to bytes (see [memory/delete-semantics.md](memory/delete-semantics.md)):

- The permascroll is append-only (2/14)
- "The user may go back in time to any previous version" (2/15)
- "Without damaging the originals" (2/45)

A removed-entirely link would violate all three. A tombstoned link satisfies them.

## Answer

The withdrawn link is **preserved in the address space with a tombstone-marked (withdrawn/not-currently-addressable) state**. It is not removed from the link store. Nelson's own taxonomy on 4/9 treats "DELETED LINKS" as a first-class subdivision of the document's technical contents, not as an absence.
