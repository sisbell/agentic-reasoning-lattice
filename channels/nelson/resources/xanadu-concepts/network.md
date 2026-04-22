# Network

Source: Literary Machines, 4/70-4/75

## Semantic Intent

### What It Means

The Xanadu network is not merely a collection of connected computers exchanging messages. It is a distributed system where every node holds a continuously valid model of the entire docuverse. Each server contains a "microcosm that shrinks and grows" - a map and subset of the whole that expands in resolution where demand requires and contracts where it does not.

This design means the network presents itself to users as a single unified space, not as a collection of separate repositories. When you request content, you don't need to know where it lives - your local server either has it, has a map that points to it, or can find it through the forwarding system.

Four key semantic properties:

1. **Unified space** - BEBE melds separate servers into one logical docuverse; users see one world, not many repositories
2. **Subrepresentation** - Each node holds a continuously valid model of the whole that grows and shrinks with demand
3. **Resilience by design** - The system assumes "networks are always broken" and handles disconnection gracefully through redundancy and backup copies
4. **Invisible distribution** - Users work with tumbler addresses, never with server locations; physical distribution is an implementation detail

### User Guarantee

The network appears as a single, unified docuverse regardless of where content actually resides. Users interact with one logical space, not many servers. Content is accessible even when its home node is unreachable, through distributed copies and backups.

### Principle Served

Literature should be interconnected without boundaries. The physical distribution of storage should be invisible to users - they work with ideas and documents, not with servers and network addresses. The system accommodates the reality that "computer networks are always broken" by design, not as an afterthought.

### How Users Experience It

- Request content by its tumbler address; the network finds it
- Local server handles all communication; users never specify which remote server
- Content remains available when some nodes are disconnected
- Response times improve as popular content is replicated closer to demand
- The entire docuverse is navigable from any entry point

### Nelson's Words

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." (4/72)

> "Each server contains a map and a subset of the whole -- a microcosm that shrinks and grows." (4/71)

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." (4/70)

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere. The contents can slosh back and forth dynamically." (4/72)

> "Any resemblance to the Vulcanian mind-meld is intentional." (4/72)

> "It is a truism that 'computer networks are always broken.' Meaning that on the average some nodes are disconnected or not working." (4/75)
