## Question 2 [theory]

> Once content has been assigned an address, must that address forever return the identical content, with no possibility of substitution or alteration?

# Address Immutability in Xanadu

The answer depends on **which address space** you mean — and it requires separating Nelson's *design intent* from his *enforcement model*.

## Istream addresses: yes, content is immutable

For **Istream (identity) addresses**, the answer is an emphatic yes. This is the foundational guarantee of the entire system. Content lives permanently at its Istream address, and that address always returns that exact content.

From `_docuverse` concept material (i-space-v-space):
- "Content at an Istream address **never changes**"
- "Content you create gets a permanent Istream address / That address will always return that exact content / Content is immutable - it never changes after creation"

This rests on the append-only storage model. Nelson rejects "destructive replacement":

> "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." (2/14)

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." (2/14)

And tumbler addressing guarantees the address itself stays valid forever:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

Even "deletion" doesn't violate this — DELETE removes content from a document's *Vstream arrangement*, not from Istream. The bytes remain at their I-address (the 4/9 diagram labels deleted bytes "not currently addressable, awaiting historical backtrack functions, may remain included in other versions").

## Vstream addresses: no, the same address can return different content

For **Vstream (version) addresses** — positions in a document's *current arrangement* — the answer is the opposite. A V-address like "byte 5" returns different content after editing, because editing rearranges the view over the permanent Istream.

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." (4/11)

This is by design: Vstream is ephemeral and dense; Istream is permanent and immutable. Links point to Istream precisely so they survive Vstream editing.

## The critical caveat: intent vs. enforcement

Your phrase "no possibility of substitution or alteration" asks about *enforcement*, and here Nelson is candid that the immutability guarantee is **semantic and contractual, not cryptographic**. The system has no hashing, signing, or tamper-detection. Identity rests on trusting the licensed Storage Vendor:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." (5/17)

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." (5/18)

So an *honest* vendor never substitutes content at an Istream address — that is the whole point of the model. But the design provides no *technical* mechanism that would make substitution detectable or impossible. The guarantee is "trust the franchise, not the bits" (a pre-cryptographic, 1981–87 architecture).

## Summary

| Address space | Returns identical content forever? |
|---|---|
| **Istream** (identity) | Yes — content is immutable by design; this is the core permanence guarantee |
| **Vstream** (arrangement) | No — the same V-address returns different content after edits |

So *intent*: once content is assigned an **Istream** address, that address must forever return identical content — this is a load-bearing invariant of the whole system. But *enforcement* of "no possibility of substitution" is contractual/social, not cryptographic; Nelson explicitly disclaims technical authenticity guarantees.
