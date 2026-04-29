## Question 1 [nelson]

> Must every document's content occupy a single unbroken sequence of positions, or can a document's address space contain gaps where no content exists?

The answer depends on which address space you mean. Xanadu has two, and they behave differently.

---

## V-Space: No Gaps — Always a Contiguous Stream

A document's **virtual byte stream** (V-space) is always a single unbroken sequence with no gaps. Nelson consistently describes it as a "stream" with ordinal positions:

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

> "The digit after the one indicates the byte position in the current ordering of bytes. This is its virtual stream address." [LM 4/30]

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document." [LM 4/11]

The editing operations confirm this — they maintain contiguity structurally:

- **INSERT**: "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66] — Insertion shifts everything after it; no gap is created.
- **DELETEVSPAN**: "This removes the given span from the given document." [LM 4/66] — Deletion closes the gap; remaining bytes renumber to stay contiguous.

If a document has 100 bytes, V-addresses run 1 through 100 with no holes. Delete bytes 20–30 and you have 89 bytes at addresses 1 through 89.

---

## I-Space: Permanent, Append-Only — No Gaps by Construction

A document's native content in I-space is stored append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Since content is only appended, never overwritten or removed, the I-space addresses for a document's native bytes form a contiguous, growing sequence. There are no gaps because nothing is ever removed from I-space — "deleted" content merely loses its V-space mapping:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

---

## Tumbler Address Space: Gaps Are Normal and Expected

At the broader level of the tumbler address space — spanning servers, accounts, documents — gaps are the norm, not the exception. Nelson explicitly defines **ghost elements**:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "The docuverse is the occupied tumbler-space — as occupied by conceptually assigned positions, even if nothing represents them in storage." [LM 4/23]

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it." [LM 4/23]

And spans can cover empty regions:

> "A span that contains nothing today may at a later time contain a million documents." [LM 4/25]

So the docuverse-wide address space is inherently sparse.

---

## Link Subspace: Gaps Possible After Deletion

One subtle case: links within a document occupy the `0.2.N` subspace and are numbered by **permanent order of arrival**:

> "The links designated by a tumbler address are in their permanent order of arrival." [LM 4/31]

Unlike bytes (which renumber in V-space when edited), link addresses are permanent. If you delete link `0.2.5`, links `0.2.6` through `0.2.N` do not renumber. The gap in the link numbering persists — that address becomes a "deleted link" awaiting historical backtrack, analogous to deleted bytes in I-space.

---

## Summary

| Address Space | Gaps? | Why |
|---|---|---|
| **V-Space** (virtual byte stream) | **Never** | Insert shifts; delete closes gaps. Always a contiguous stream. |
| **I-Space** (native content) | **Never** | Append-only; nothing is removed. |
| **Tumbler space** (docuverse-wide) | **Always** | Ghost elements; address space is sparse by design. |
| **Link subspace** (within a document) | **After deletion** | Link addresses are permanent; deleted links leave gaps. |

The key architectural insight: V-space is the user's view, and it is always dense and contiguous. The permanent address spaces (I-space, tumbler space) can have gaps, but this is either invisible to users (I-space) or intentional by design (ghost elements in the broader docuverse).
