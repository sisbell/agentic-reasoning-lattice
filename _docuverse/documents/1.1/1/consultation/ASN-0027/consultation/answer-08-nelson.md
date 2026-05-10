## Question 8 [nelson]

> Must every unit of content ever added to the system receive a unique address that is never reused for different content?

# Yes — Absolutely and By Design

Every unit of content in Xanadu receives a unique address that is never reused for different content. This is not merely a policy but an architectural invariant that follows from multiple interlocking design decisions.

## The Permanent Address Guarantee

Nelson states the guarantee directly:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The key phrase is "while the other addresses remain valid." Inserting new content never disturbs existing addresses. Reusing an address for different content would violate this — the old address would no longer be "valid" for its original content.

## Append-Only Storage Enforces It

The storage model is explicitly append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

In an append-only system, content is added to the end of the store. Nothing is overwritten. Every byte gets a fresh position. This is the physical mechanism that prevents address reuse.

## I-Space Immutability

Content in I-space (the permanent identity space) never changes at its address. Nelson describes native bytes as permanently residing at their "home locations":

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

The I-address encodes which server, which user, which document, and which element position created the content. To reuse that address for different content would be to claim a different origin than the content actually has.

## Forking Creates, Never Recycles

The tumbler forking mechanism creates new addresses by subdivision — adding digits to the right:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

This is a tree that only grows. Addresses are "baptized" by their owners, never reclaimed and reassigned. There is no garbage collection of address space.

## Even "Deletion" Preserves the Address

When content is "deleted," it is removed from the document's V-space arrangement but remains at its I-space address:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

"Deleted" bytes are not erased — they become "not currently addressable" in that particular view. The I-address still holds the original content. This is the strongest evidence that address reuse is impossible by design.

## Origin Traceability Depends On It

Nelson guarantees that you can always trace content to its origin:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

If address `1.0.3.0.7.0.42` means "the 42nd byte of document 7 by user 3 on server 1," and that address were later reused for different content, this guarantee would be meaningless. The address IS the provenance. Reuse would be forgery.

## The Ministry of Truth Problem

Nelson was explicitly concerned about systems that allow replacement of content at the same address:

> "A reference article, say, in an encyclopedia can be changed simply by storing another one in its place—and poof! history is changed." [LM 3/19–3/22]

Xanadu's entire architecture is designed to make this impossible. Permanent, unique, never-reused addresses are the mechanism that prevents it.

## Summary

The uniqueness and non-reuse of addresses is not a single stated rule but the convergence of every major architectural decision: append-only storage ensures no overwriting, forking addressing ensures no recycling, I-space immutability ensures no mutation, deletion semantics ensure no erasure, and origin traceability ensures addresses carry permanent meaning. To reuse an address would simultaneously violate the permanence guarantee, the attribution guarantee, the version history guarantee, and the non-destruction guarantee.
