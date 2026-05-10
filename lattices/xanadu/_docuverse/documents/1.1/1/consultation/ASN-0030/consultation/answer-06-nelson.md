## Question 6 [nelson]

> If a new version of a document rearranges its content, must the addresses of the individual content elements remain unchanged across versions?

# Address Stability Across Versions

The answer depends on **which** address you mean. Xanadu has two address spaces, and they behave oppositely under rearrangement.

## I-Space Addresses: Permanently Unchanged

I-space addresses are **immutable by definition**. They encode the permanent identity of content — which server, which user, which document created each byte. Rearranging a document's content does not and cannot change these addresses.

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

I-space is append-only. Content, once created, lives at its I-address forever. A new version does not create new content — it creates a new *arrangement* of existing content.

## V-Space Addresses: Explicitly Designed to Change

V-space addresses — the positions in the document's virtual byte stream — are **expected to change** during rearrangement. This is the entire point of V-space.

> "Note that this order may be continually altered by editorial operations, but since the links are to the bytes themselves, any links to those bytes remain stably attached to them." [LM 4/30]

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

The REARRANGE operation explicitly transposes regions of text [LM 4/67], which shifts V-space positions. INSERT increases V-addresses of following characters by the length of the inserted text [LM 4/66]. These are normal, expected operations.

## The Design Principle

A version **is** a V-space arrangement. Creating a new version means creating a new mapping from V-addresses to I-addresses, over the same underlying I-space content:

```
Version 1 (V→I mapping):    Version 2 (V→I mapping):
  V-pos 1 → I-addr A          V-pos 1 → I-addr C
  V-pos 2 → I-addr B          V-pos 2 → I-addr A
  V-pos 3 → I-addr C          V-pos 3 → I-addr B
```

The I-addresses (A, B, C) are unchanged. The V-addresses have been rearranged. This is precisely what Nelson means by:

> "There is thus no 'basic' version of a document set apart from other versions — 'alternative' versions — any more than one arrangement of the same materials is a priori better than other arrangements." [LM 2/19]

## Why This Matters

Links point to I-space addresses, not V-space positions. This is why links survive editing:

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes. This has a crucial advantage: it means that links can survive editing." [LM 4/42]

And it is why correspondence across versions works — two versions that share I-space content can be compared automatically:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail — unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

## Summary

**I-space addresses must remain unchanged** — they are permanent, immutable identifiers. **V-space addresses are expected to change** — that is what rearrangement, versioning, and editing *are*. The separation of identity (I-space) from arrangement (V-space) is the architectural foundation that makes both permanence and flexibility possible simultaneously.
