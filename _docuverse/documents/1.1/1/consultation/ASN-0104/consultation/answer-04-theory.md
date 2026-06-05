## Question 4 [theory]

> Does reading a fragment by address ever change, consume, or affect that fragment in any way?

No. Reading a fragment by address never changes, consumes, or alters the fragment itself. Xanadu's storage model is built on permanence and non-destruction, and retrieval is a pure read.

## Content is immutable

Istream content never changes after creation. From the curated sources:

- "Content at an Istream address **never changes**" and "Content is immutable - it never changes after creation" (i-space-v-space)
- The store is **append-only**: "suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

Because nothing is ever overwritten or removed, there's no mechanism by which a read could mutate stored content.

## Retrieval is a pure return

The retrieval operation simply returns content without side effects on it:

- **RETRIEVEV**: "This returns the material (text and links) determined by `<spec set>`." (4/67)

Nelson's "pounce" metaphor reinforces that retrieval materializes a view without altering the source: "You pounce like a cat on a given thing, and it seems to be there, having been constructed while you are, as it were, in midair... this materializes when you pounce on it." (2/16)

## Not even deletion affects stored bytes — so reading certainly doesn't

Even an explicit DELETE does not destroy a fragment; it only removes it from a document's current Vstream arrangement. "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9). If destructive editing leaves bytes intact, a non-destructive read leaves them intact too.

## One side effect — but on accounting, not on the fragment

The only thing a read triggers is **royalty/usage accounting**, which is external to the fragment. For published documents, delivery increments a counter:

- The cash register "increments whenever bytes or links are delivered out of the document." (5/13)
- "There is a royalty on every byte transmitted. This is paid automatically by the user to the owner every time a fragment is summoned, as part of the proportional use of byte delivery." (2/43)

This affects the document's cash register and the reader's/owner's balances — it does not change, consume, or degrade the fragment. The same bytes remain at the same permanent Istream address and can be read again identically and indefinitely. Reading is idempotent with respect to the content: a fragment is "summoned," never "spent."

## Summary

- The fragment's content: **unaffected** (immutable, append-only).
- The fragment's address: **unaffected** (permanent).
- The fragment's availability for future reads: **unaffected** (can be re-read identically forever).
- External accounting (cash register, royalty): incremented — but this is a property of the document's economic counters, not a change to the fragment itself.
