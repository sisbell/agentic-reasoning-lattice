## Question 4 [nelson]

> Is the admission of a new node an atomic event — either fully present in the docuverse or fully absent — with no intermediate state?

## No — Node Admission Is Explicitly Gradual, Not Atomic

Nelson describes node integration as an **incremental, always-valid process** with clear intermediate states. The evidence comes from three converging aspects of the design.

### 1. The "Null Case" Progression

The most direct evidence is from 4/72, where Nelson describes server state:

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [4/72]

The phrase **"from the null case on up"** explicitly names the starting state: empty. The server begins with nothing and accumulates incrementally. Each increment leaves it in "canonical operating condition" — there is no invalid transitional state, but there are many intermediate states between empty and fully populated.

### 2. Ghost Elements: Address Before Content

A new node can exist as a **ghost element** — an addressable position with no stored content:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [4/23]

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." [4/23]

This means a node address can be "baptized" (forked from a parent) and be linkable, referenceable, and addressable **before any content exists under it**. The node is neither fully absent (its address is valid, links can target it) nor fully present (it holds nothing). This is an explicit intermediate state.

### 3. The Microcosm Model

Each server is described as a growing/shrinking subset:

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [4/71]

A new node starts with a minimal microcosm and grows it through BEBE exchanges. Content "sloshes" in as demand requires. The server doesn't receive a complete snapshot of the docuverse at admission — it builds its model incrementally.

### What IS Atomic

Two aspects may be atomic, though Nelson does not use the word:

1. **Address baptism** — The parent node owner designates the new node's address. This is a discrete act: "The owner of a given item controls the allocation of the numbers under it" [4/20]. Before baptism, the address doesn't exist; after, it does.

2. **Franchise contract** — The Storage Vendor signs a contract with Project Xanadu [5/14]. This is a legal event, not a technical one.

But neither of these makes the node "fully present in the docuverse." The address exists; the vendor is licensed; the node then begins operating from the null case, incrementally building its model and content.

### The Design Principle

Nelson's architecture is designed so that **every intermediate state is valid**. A server with one document is as "canonical" as a server with a million. There is no bootstrap phase where the node is partially broken. This follows from the same principle that makes the docuverse itself open-ended: a span that "contains nothing today may at a later time contain a million documents" [4/25].

### Summary

Node admission has at least three distinguishable states: (1) address not yet baptized, (2) address exists as ghost element with no content, (3) operational server with growing microcosm. The transition between these is gradual. Nelson explicitly rejects the need for atomicity by ensuring every state along the progression is "unified and operational."

NEED_RAW: [4/72] — The curated BEBE and network extracts give slightly different transcriptions of the same passage ("from the full sweep up" vs "from the null case on up"). The raw page would resolve the exact wording, though both readings support the same conclusion.
