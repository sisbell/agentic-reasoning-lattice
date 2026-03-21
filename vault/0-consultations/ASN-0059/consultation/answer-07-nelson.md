## Question 7 [nelson]

> When content is inserted, does the system guarantee that the new content is immediately and permanently retrievable by its assigned identity from that point forward, with no possibility of loss?

# Permanence of Inserted Content

## The Design Intent: Yes, Permanent from Creation

Nelson's architecture is built around the principle that content, once created, exists permanently. The Istream is append-only:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

Once bytes are appended to the Istream, they receive a permanent I-address — a tumbler encoding their server, account, document, and element position. That address is guaranteed stable:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

And content at an I-address never changes. Even "deletion" only removes content from the Vstream (current arrangement) — the Istream bytes persist:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." [LM 4/11]

The retrieval model assumes immediate availability — Nelson's "pounce" concept:

> "THE PART YOU WANT COMES WHEN YOU ASK FOR IT." [LM 2/16]

## Three Caveats Nelson Himself Acknowledges

### 1. No Technical Guarantee Against Loss

Nelson explicitly disclaims reliability at the infrastructure level:

> "User acknowledges that due to possible unreliability of the software, unreliability and vulnerability of transmission systems, and myriad possibilities for intrusion and malicious mischief by unseen parties throughout the universe, all storage, and transmission of contents and links, and attempts to deliver such material, are at User's risk." [LM 5/18]

The system provides no cryptographic verification of integrity:

> "User acknowledges that all material on the network is stored by users under similar arrangements to User's own, without verification or assurance of truth, authenticity, accuracy, usefulness or other beneficial character of such materials." [LM 5/17]

Trust rests on the Storage Vendor franchise — contractual, not mathematical.

### 2. Economic Conditionality

Permanence requires ongoing payment:

> "ALL SERVICES MUST BE SELF-SUPPORTING. Subsidy between one aspect of the system and another could only work temporarily. This means, for example, that archival storage must be economically self-sustaining." [LM 4/5]

Nelson does not specify what happens if storage rental lapses. The I-address remains permanently *assigned* (no reuse), but *accessibility* depends on someone continuing to pay.

### 3. Network Propagation

Nelson acknowledges that the distributed network is inherently imperfect:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." [LM 4/75]

Content is immediately available at the local server after insertion. But network-wide availability depends on the BEBE protocol's forwarding and subrepresentation mechanisms, which propagate incrementally:

> "Whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." [LM 4/72]

## Summary

| Aspect | Guaranteed? |
|--------|-------------|
| I-address permanently assigned at insertion | **Yes** — by architecture |
| Content never overwritten in Istream | **Yes** — by append-only design |
| Immediately retrievable on local server | **Yes** — by "pounce" model |
| Immediately retrievable network-wide | **No** — propagation delay |
| No possibility of loss (bit-level) | **No** — explicitly disclaimed [LM 5/18] |
| Accessible indefinitely | **Conditional** — requires ongoing storage payment |

Nelson's design *intends* that insertion is a permanent, irrevocable act — the architectural equivalent of writing in ink. But he is honest that the infrastructure beneath this intent is fallible. The permanence guarantee is a **design invariant** (the system is built to preserve it), not a **physical impossibility of loss** (which Nelson acknowledges no system can provide).

The INSERT operation itself [LM 4/66] specifies no atomicity, durability, or acknowledgment semantics. It says what the operation *does* (adds content, shifts V-addresses) but not what happens if the operation is interrupted mid-execution or the server fails before propagation.

NEED_RAW: [4/65-4/67] — The INSERT operation definition on these pages may contain additional detail about operation completion semantics not captured in the curated extracts.
