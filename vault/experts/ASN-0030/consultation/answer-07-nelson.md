## Question 7 [nelson]

> Does the system guarantee that an address assigned today will resolve to the same content a century from now, and what would constitute a violation of that guarantee?

# Address Permanence and Content Resolution

The question touches the deepest architectural commitment in Xanadu. The answer requires separating two guarantees that people habitually conflate: **address permanence** and **content accessibility**.

## The Address Guarantee: Absolute

The tumbler address assigned today will designate that same content forever. This is not aspirational — it is structural:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

The addressing system was designed specifically so that growth never invalidates existing references. Forking creates new sub-addresses beneath existing ones; nothing is renumbered, relocated, or reassigned. The address IS the identity.

In I-space, content is immutable:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control." [LM 4/11]

The append-only storage model means content, once written, is never overwritten:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Even "deletion" does not touch I-space content. Deleted bytes are described as:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

So: **the I-space address assigned today will, by architectural mandate, designate precisely the same bytes a century from now.** The address cannot be reassigned. The content cannot be overwritten. This is not a policy — it is how the storage works.

## What Would Constitute a Violation

Three things would violate this guarantee:

**1. Address reassignment.** If a tumbler address that once designated content X were made to designate content Y, the entire addressing system collapses. Every permanent citation, every link, every transclusion depends on addresses being eternal. This would be the equivalent of reassigning telephone numbers while people are mid-conversation — except worse, because the damage is permanent and retroactive.

**2. Content mutation at an I-address.** If bytes at an I-space address were modified after storage, the guarantee is broken. The system is append-only precisely to prevent this. Modifying stored bytes would silently corrupt every document that transcludes that content, every link that points to it, every version that includes it.

**3. Unauthorized withdrawal of published content.** Publication creates binding obligations:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

Other users will have linked to it. Their links — which they own, at their addresses — depend on the continued existence of the target. Unilateral withdrawal breaks others' property.

## The Harder Question: Accessibility

Now the uncomfortable part. Address permanence and content immutability are architectural guarantees. But **accessibility** — whether you can actually retrieve the content — depends on economics:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Someone must pay ongoing storage rental. If the content owner stops paying and no one else takes over, the content may become inaccessible — not because the address is invalid or the content destroyed, but because no vendor is contractually obligated to serve it for free.

This is the distinction between the address **being valid** (always) and the content **being delivered** (requires economic support). A book's Library of Congress catalog number doesn't expire when the book goes out of print — but the book may become hard to find.

## What Is NOT a Violation

Several things that might appear to violate the guarantee do not:

- **V-space rearrangement.** If you ask for a document's current arrangement and it has been edited since you last looked, the V-space has changed. But V-space is explicitly ephemeral — "the address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11]. The I-address is what's permanent.

- **Content becoming temporarily unreachable.** The system acknowledges that "computer networks are always broken" [LM 4/75]. Temporary unavailability due to network partition or server downtime is expected, not a violation.

- **Supersession.** When a new version supersedes an old one, the old version remains at its address. The supersession link declares "there is something newer," but the original content is untouched.

## The Verification Gap

One final, sobering point. The system provides **no cryptographic verification** that the content returned at an address is what was originally stored:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

> "Storage Vendor makes no guarantee as to the correctness or authenticity of any material received from other Users." [LM 5/18]

The guarantee that an address resolves to the same content rests on **contractual trust** in the Storage Vendor franchise, not on mathematical proof. If a vendor is honest, the guarantee holds. If a vendor is compromised or dishonest, there is no technical backstop to detect the alteration.

This is a pre-cryptographic architecture. The address is permanent. The content is append-only. But the proof that what you receive is what was stored relies on the integrity of the franchise, not on the bits themselves.

## Summary

| Aspect | Guaranteed? | Mechanism |
|--------|-------------|-----------|
| Address permanence | **Yes, absolutely** | Tumbler architecture — addresses never reassigned |
| Content immutability | **Yes, architecturally** | Append-only I-space — bytes never overwritten |
| Published accessibility | **Yes, contractually** | Publication contract — withdrawal only by "lengthy due process" |
| Ongoing accessibility | **Conditionally** | Requires economic support (storage rental) |
| Content authenticity | **No** | Trust in vendor, not cryptographic verification |

The system guarantees that the address assigned today will **mean** the same thing a century from now. Whether you can **reach** what it means depends on whether civilization maintains the economic and institutional infrastructure to keep serving it — which is precisely why I designed it to be distributable into "deep rock and deep space" [LM 3/25].
