## Question 3 [nelson]

> If the same content appears in multiple documents through sharing, does removing it from one document affect its presence or position in any other document?

# No. Removing content from one document has absolutely no effect on any other document.

This is one of the most fundamental guarantees of the architecture, and it follows directly from the separation of Istream and Vstream.

## The Mechanism

When content appears in multiple documents through transclusion, each document has its own **Vstream** (arrangement) that maps to shared **Istream** (permanent storage). "Deleting" content from a document removes only that document's Vstream mapping. The Istream content is untouched.

Nelson states this explicitly:

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

Each document's Vstream is independent. Editing one document's arrangement — inserting, deleting, rearranging — changes only that document's V-to-I mapping. No other document's mapping is affected.

## Why This Works

The key is that transclusion is **reference to Istream**, not reference to another document's Vstream. When Document B transcludes content from Document A, Document B's Vstream points to the same Istream addresses as Document A — but it does not point *through* Document A. The relationship is:

```
Document A's Vstream ──→ Istream address X
Document B's Vstream ──→ Istream address X  (same content, independent mapping)
```

If Document A deletes that content from its arrangement, Document A's Vstream no longer references address X. But Document B's Vstream still does. The Istream content at address X is permanent and unchanged.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The bytes remain at their home location regardless of what any document does with its own arrangement.

## The Broader Principle

This is a direct consequence of Nelson's rejection of destructive replacement:

> "Thus users may create new published documents out of old ones indefinitely, making whatever changes seem appropriate — without damaging the originals. This is done by inclusion links." [LM 2/45]

And the append-only storage model:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Content in Istream is never removed. DELETE is a Vstream-only operation:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

## What About Position?

Positions in other documents are also unaffected. Each document's Vstream addresses are dense and independent — V-address 1 is always the first byte of *that* document's current arrangement. Editing Document A changes Document A's V-addresses but has no effect on Document B's V-addresses, even if they share Istream content.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

## Summary

The Istream/Vstream separation guarantees complete isolation between documents. Each document is an independent view over permanent content. No operation on one document can affect any other document's content, arrangement, or addresses.
