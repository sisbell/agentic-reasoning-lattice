## Question 6 [nelson]

> If two independent links point to the same passage and that passage is later split across two documents, must both links survive and continue to reach their original content?

# Yes. Both links must survive.

This follows directly from three interlocking properties Nelson specifies.

## 1. Links attach to bytes, not positions or documents

> "A Xanadu link is not between points, but between spans of data. Thus we may visualize it as a strap between bytes." [LM 4/42]

The two links each hold I-addresses — permanent references to specific bytes in the append-only Istream. They do not reference a document, a Vstream position, or any arrangement that can change. They reference the bytes themselves.

## 2. Istream content is permanent

In Xanadu, bytes never move and never disappear. "Splitting a passage across two documents" means changing which documents' Vstreams reference those bytes — it does not alter, relocate, or destroy the bytes at their I-addresses.

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

Since both links point to I-addresses, and I-addresses are permanent, the links' targets still exist regardless of how Vstream arrangements change.

## 3. Broken, discontiguous endsets are valid

After the split, the passage that was once contiguous in a single document's Vstream may now appear as fragments in two different documents' Vstreams. Nelson explicitly states this is fine:

> "We see from above that one end of a link may be on a broken, discontiguous set of bytes. This illustrates the endset: a link may be to or from an arbitrary set of bytes. These may be anywhere in the docuverse." [LM 4/42]

The endsets of both links may now span bytes scattered across multiple documents. This is a supported state, not an error.

## The survivability guarantee

Nelson states the condition under which links break:

> "SURVIVABILITY: Links between bytes can survive deletions, insertions and rearrangements, **if anything is left at each end.**" [LM 4/43]

In Xanadu's append-only storage, the bytes are never destroyed — only rearranged in Vstream or removed from a particular version's view. Since all the original bytes still exist at their I-addresses, there is always "something left at each end." Both links survive unconditionally.

## Independence of the two links

The two links are independent objects at their own addresses, owned by their respective creators:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

Neither link's survival depends on the other. Both point to the same I-addresses. Both survive for the same reason: their targets are permanent.

## What changes is the user experience, not the link validity

After the split, following either link may lead to content distributed across two documents rather than appearing in one. The front end must resolve which documents currently show those bytes in their Vstreams. But the link mechanism itself — the "strap between bytes" — remains intact. The system can always locate the bytes because I-addresses are permanent and globally unique.

## Summary

Both links **must** survive. This is not a special case requiring special handling — it is the normal operation of a system where links attach to permanent byte identities (Istream), not to ephemeral arrangements (Vstream). The passage may scatter across any number of documents; the links follow the bytes, not the documents.
