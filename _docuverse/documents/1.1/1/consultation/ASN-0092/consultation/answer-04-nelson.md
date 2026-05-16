## Question 4 [nelson]

> If the same content appears in multiple documents through placement, must the system guarantee that all appearances resolve to identical bytes?

## Yes — and the guarantee is stronger than identity of value. It is identity of instance.

When content appears in multiple documents through the COPY operation (Nelson's "inclusion," "quote-window," or "transclusion"), all appearances resolve to **the same bytes** — not merely equal bytes, but the very same Istream content at the very same permanent address.

### The Architectural Basis

The Istream/Vstream separation makes this a structural invariant, not a runtime check:

1. **COPY creates a reference, not a duplicate.** The COPY operation maps Vstream positions in the target document to existing Istream addresses from the source. No new bytes are created in Istream.

> "Non-native byte-spans are called inclusions or virtual copies." [LM 4/11]

> "No copying operations are required among the documents throughout the system, and thus we solve the problems of update—especially the problem of updating documents which depend on other documents." [LM 2/36]

2. **Istream content is immutable.** Bytes at an Istream address never change. The permascroll is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

3. **All appearances fetch from the same home location:**

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

When Document A and Document B both include the same passage through COPY, both documents' Vstreams contain mappings to the same Istream addresses. Rendering either document fetches the same bytes from the same location.

### Identity vs. Equality

This distinction matters. Two users who independently type "hello" create **different** Istream bytes at different addresses. Those bytes are *equal* in value but *distinct* in identity. But when one user transcludes the other's "hello," both appearances share the **same** Istream address — they are identical in the strongest sense.

As the provenance documentation captures: "Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address."

This is also how the system knows to pay royalties to the right person and how FINDDOCSCONTAINING works — it traces shared Istream origin.

### The Caveat: Trust, Not Verification

The guarantee is **architectural**, not **cryptographic**. Nelson explicitly specifies no tamper detection:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

If a Storage Vendor is compromised or dishonest, the bytes at an Istream address could theoretically be altered. Nelson's enforcement model relies on contractual trust in the franchise, not on hashes or signatures. The system guarantees identical resolution *given honest infrastructure* — which is the same assumption that makes permanent addresses meaningful at all.

### Summary

The answer is not merely "yes, the system guarantees identical bytes" but something deeper: **there is only one copy.** The COPY operation does not duplicate content — it creates an additional Vstream reference to the same Istream content. Identical resolution is not a property that must be *enforced*; it is a consequence of there being nothing to diverge from. The content exists once; all placements are views of that single instance.
