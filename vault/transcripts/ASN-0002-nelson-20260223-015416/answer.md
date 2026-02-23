# Yes — Fresh Content Requires Fresh Addresses

Every act of storing genuinely new content in Xanadu must produce an address that has never been used before and will never be reused. This is not a single explicit rule but the convergence of several interlocking guarantees Nelson specifies.

## 1. Addresses Are Permanent and Immutable

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

Once an address is assigned, it is occupied forever. This immediately implies that new content cannot be placed at an existing address — the address is already taken.

## 2. Content at an I-Address Never Changes

I-space addresses are "absolute and immutable" — content at an I-space address never changes after creation. If content is immutable at its address, and addresses are permanent, then storing different content requires a different address. There is no alternative.

## 3. Storage Is Append-Only

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

The append-only model means the address space grows monotonically forward. New content is appended; nothing is overwritten. This structurally prevents address reuse.

## 4. Address Creation Is Monotonic Forking

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

New addresses are created by sequential forking: 2.1, then 2.2, then 2.3. The process only moves forward. Nelson's example makes the monotonicity explicit — you fork successive items, never returning to reuse a previously allocated position.

## 5. "Deleted" Content Still Occupies Its Address

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Even deletion does not free an address for reuse. The bytes remain in I-space; only the V-space mapping is removed. The address continues to be occupied by its original content.

## The Crucial Distinction: New Content vs. New Arrangement

Not every operation that touches storage produces fresh I-space addresses. The distinction is between creating **new content** and creating **new arrangements of existing content**:

| Operation | Fresh I-addresses? | What happens |
|-----------|-------------------|--------------|
| **INSERT** | Yes | New bytes enter I-space at fresh addresses |
| **APPEND** | Yes | New bytes appended to I-space |
| **COPY** | No | V-space mapping to existing I-addresses (transclusion) |
| **CREATENEWVERSION** | No (for content) | New document address, but text content shares existing I-addresses |
| **REARRANGE** | No | Pure V-space operation |
| **DELETE** | No | V-space mapping removed; I-space unchanged |

Nelson makes this explicit for COPY:

> "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

Transclusion reuses I-addresses by design — that is exactly what makes attribution structural and royalty tracking automatic. The same bytes, at their permanent home addresses, are referenced from multiple V-space arrangements.

## Why This Matters

The freshness requirement is not arbitrary. It is load-bearing for three of Nelson's fundamental guarantees:

1. **Attribution**: Every byte traces to its origin through its I-address. If addresses were reused, origin traceability would break — you could not distinguish "wrote the same words independently" from "quoted from the original."

2. **Permanence**: Citations and links point to I-addresses. If an address could be recycled for different content, every existing reference to the old content would silently become a reference to something else — a silent corruption of the docuverse.

3. **Correspondence**: Version comparison works because shared I-addresses reveal which parts of two versions came from the same origin. Address reuse would create false correspondences.

## Summary

Yes. Every act of storing new content must produce a fresh address. This follows necessarily from the conjunction of permanent addresses, immutable content at those addresses, append-only storage, and monotonic forking. The address, once baptized, belongs to that content forever. The system grows; it never overwrites.