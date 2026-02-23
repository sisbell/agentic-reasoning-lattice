# BEBE (Back-End/Back-End Protocol)

Source: Literary Machines, pages 4/70-4/73 (raw pages 237-240)

## Semantic Intent

### What It Means

BEBE is the protocol by which Xanadu servers communicate with each other to form a unified docuverse. Where FEBE connects users to the system, BEBE connects the system to itself - allowing distributed servers to present a single coherent information space.

The user never sees BEBE directly. They experience only a seamless docuverse where any address works, regardless of which server physically holds the content. BEBE is how that illusion becomes reality.

### User Guarantee

**What users can rely on:**

- Any address works from any access point
- The docuverse appears as one unified space
- Performance is optimized automatically
- Content is replicated for reliability
- Material remains available even as servers change

**What happens invisibly:**

- Servers forward requests to each other
- Popular content migrates closer to users
- Reference information is cached and replicated
- The network self-organizes around demand patterns

### Principle Served

**Universal accessibility.** Every address in the docuverse resolves to content, no matter where you access from or where the content physically lives. BEBE is the mechanism that makes permanent addressing work across a distributed system.

**Resilience through distribution.** Content exists in multiple places. The network routes around failures. The docuverse survives individual server failures.

**Performance through locality.** Content migrates toward users who need it. The system gets faster as it's used, not slower.

### How Users Experience It

Users don't experience BEBE directly - they experience its effects:

- Request content from halfway around the world - it arrives quickly
- Access obscure content - it exists somewhere and you can reach it
- Return to content later - it's still there, often faster now
- The system works even when parts are down

### The Docuverse Model

Each server contains:
- A "microcosm" - a subset of the whole docuverse
- A "map" - knowledge of where other content lives
- Growing and shrinking as demand changes

Nelson's diagram (page 4/71) shows servers as amoeba-like shapes, overlapping and connected, each holding part of the whole but knowing about the rest.

### Functions of BEBE

**A. Request Forwarding**
> "First, by the forwarding of requests as they fan out from users to servers able to supply..."
> — page 4/70

When a server doesn't have requested content, it forwards the request to servers that do.

**B. Subrepresentations and Co-modelling**
> "Material is moved between servers for a number of purposes:
> 1. for more rapid access to final material,
> 2. for more rapid access to needed material which indexes material on other servers,
> 3. for rebalance in keeping with demand,
> 4. for redundancy and backup purposes."
> — page 4/71

The network self-organizes. Popular content replicates. Index information caches near users. Load balances automatically.

### Nelson's Words

> "BEBE (Back End-Back End) is the protocol for connecting nodes of the Xanadu network. It is still undergoing definition and will not be made public anytime soon. The intent is to make public some of the internal codes, structures and forms of numeration, which are presently proprietary."
> — page 4/70

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space. This is done basically in two ways."
> — page 4/70

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows."
> — page 4/71

> "A server's network model, from the full sweep up, is at all times unified and operational; whenever information moves between servers is incremental on its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically."
> — page 4/72

## Relationship to FEBE

FEBE is the user-system contract.
BEBE is the system-system contract.

Users speak FEBE to their front end. The back end speaks BEBE to other back ends. Together they present the illusion of a unified, eternal, universal docuverse.
