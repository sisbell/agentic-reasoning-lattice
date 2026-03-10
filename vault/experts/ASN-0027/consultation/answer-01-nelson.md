## Question 1 [nelson]

> Once content is assigned a permanent address, must that address remain valid and resolvable for the entire lifetime of the system?

# Yes — With an Important Distinction

The answer is **yes**, but Nelson distinguishes between two forms of permanence: **address validity** (the address is never reassigned) and **address resolvability** (content is actually accessible). Both are intended to be permanent, but they rest on different foundations.

## Address Validity Is Absolute

The tumbler addressing system is specifically designed so that no address is ever invalidated or reassigned:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This is an architectural guarantee, not a policy choice. The forking mechanism ensures new content gets new sub-addresses without disturbing existing ones. An address once baptized belongs to that content forever.

In I-space, this permanence is even stronger. Every byte ever created has an immutable I-address, and content at that address never changes. DELETE operations remove content from V-space (the document's current arrangement) but never from I-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

The bytes remain. The address remains. Only the current view changes.

## Resolvability of Published Content Is a Social Obligation

For **published** documents, Nelson is emphatic that resolvability must persist:

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process." [LM 2/43]

The reason is structural, not sentimental. Other users will have created links to the content — links they own, at their addresses. Withdrawing the target would destroy their property:

> "This is vital because of the links other users may have made to it — which can now reach through from the previous version (to which they were originally attached) into the newer version." [LM 2/43]

Nelson frames the entire system as a permanent archive for civilization:

> "This attrition of the heritage can in principle be stopped." [LM 3/25]

> "Only digital archives give us long-term hope for preserving our heritage — not just writings, but text, paintings (stored as detailed photographs), sculpture, architecture, whatever." [LM 3/25]

## The Tension: Perpetual Storage Requires Perpetual Funding

Here is where honesty compels a caveat. Nelson explicitly states:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Storage is funded through ongoing rental paid by the content owner. If the owner stops paying, Nelson does not specify what happens. The storage-funding design intent in the curated sources notes this gap: **permanence of the address (once assigned, never reused) is distinct from permanence of accessibility (requires ongoing payment).**

So the full picture is:

| Aspect | Permanent? | Basis |
|--------|-----------|-------|
| **Address validity** (never reassigned) | Yes, unconditionally | Architectural — tumbler design |
| **I-space content** (bytes exist) | Yes, unconditionally | Architectural — append-only storage |
| **Published accessibility** (content resolvable) | Yes, by obligation | Contractual — publication contract, franchise obligations |
| **Private accessibility** | No — owner may withdraw | Owner's prerogative |
| **Funded accessibility** | Requires ongoing payment | Economic — self-sustaining storage model |

## My Intent

The address must remain valid forever — this is non-negotiable and is why the entire tumbler system exists. For published content, resolvability is equally non-negotiable as a matter of principle: the web of links that others have built depends on it. The economic mechanism to sustain this indefinitely is the combination of storage rental, per-byte delivery charges, and the franchise structure that distributes content across multiple vendors for resilience.

The system was designed to "be put in deep rock and deep space — Iron Mountain or the asteroid belt" [LM 3/25]. I meant it to last as long as humanity endures. Whether the funding model sustains that aspiration is an implementation challenge, not a retreat from the principle.
