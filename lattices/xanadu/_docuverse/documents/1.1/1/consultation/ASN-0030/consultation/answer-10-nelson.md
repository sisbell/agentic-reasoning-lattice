## Question 10 [nelson]

> Must the system distinguish between content that is permanently stored but currently inaccessible and content whose address has been invalidated, or are these the same condition?

## They Are Distinct Conditions — and One Cannot Occur

Nelson's architecture makes these two conditions fundamentally different. In fact, address invalidation **does not exist** in the design.

### Addresses Are Permanent by Construction

Tumbler addresses, once assigned, are valid forever. This is not a policy but a structural property of the addressing system:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (4/19)

There is no INVALIDATE operation in FEBE. There is no mechanism by which a tumbler address ceases to be a valid point in the docuverse. The address space only grows; it never contracts.

### Temporary Inaccessibility Is Expected

Nelson explicitly designs for content that exists but cannot currently be reached:

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)

The system handles this through forwarding, backup copies, and subrepresentation. Each server holds "a microcosm that shrinks and grows" (4/71), and "the contents can slosh back and forth dynamically" (4/72). A request that cannot be fulfilled is forwarded to backup locations, with "not currently available" as a last resort — not an error indicating the address is invalid.

### Ghost Elements: Valid Addresses With No Content

Nelson goes further. An address can be valid even when **nothing has ever been stored there**:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." (4/23)

Ghost elements demonstrate that "valid address" and "content exists" are independent properties. You can link to an address before anyone puts content there. The address is real; the content is absent. This is by design, not an error state.

### DELETE Creates a Third Distinct State

Nelson's DELETE produces yet another condition — content exists in I-space but is removed from V-space:

> "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" (4/9)

> "Note that the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included." (4/11)

The content is permanently stored. The I-address is still valid. But the content is not reachable through the current V-space arrangement. It remains accessible through historical backtrack or through other documents that transclude it.

### The Spectrum of States

Nelson's architecture thus implies at least four distinct conditions for a given address:

| State | Address valid? | Content in I-space? | Currently deliverable? |
|-------|---------------|--------------------|-----------------------|
| Normal | Yes | Yes | Yes |
| Network partition | Yes | Yes | Temporarily no |
| V-space deleted | Yes | Yes | Not via current version |
| Ghost element | Yes | No | No (nothing to deliver) |

Address invalidation — where the address itself ceases to be meaningful — is absent from this table because it cannot occur.

### The Unresolved Tension

There is one scenario Nelson does not fully resolve: what happens when storage payment lapses? He requires that "ALL SERVICES MUST BE SELF-SUPPORTING" (4/5) and frames storage as ongoing rental, but never specifies what happens to content when the owner stops paying. The address would remain valid (tumblers are permanent), but the content might become inaccessible — a state analogous to "network partition" but potentially permanent.

Published content adds another constraint: "It is in the common interest that a thing once published stay published" (2/43), and withdrawal requires "lengthy due process." This creates tension with self-supporting storage but does not resolve it.

### Answer

The system **must** distinguish between these conditions because they are architecturally different. "Permanently stored but currently inaccessible" is a real and expected state — the network routes around it. "Address invalidated" is a condition that **cannot arise** in Nelson's design. Tumblers are permanent. The docuverse only grows. An address, once baptized, is a permanent point in the universal address space regardless of what content — if any — exists there.
