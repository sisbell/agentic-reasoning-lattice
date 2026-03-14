# Sub-Questions — Node Ontology

**Inquiry:** What is a node in the Xanadu system? How do nodes enter the docuverse, and what invariants govern the node set?

1. [nelson] What is the minimal set of properties that define a node at the moment it enters the docuverse?
2. [nelson] Must every node receive a permanent, globally unique identity, and is that identity assigned by the system or derived from the node's content?
3. [nelson] Once a node has entered the docuverse, can it ever be removed, or must the node set grow monotonically?
4. [nelson] Is the admission of a new node an atomic event — either fully present in the docuverse or fully absent — with no intermediate state?
5. [nelson] Does the design distinguish different kinds of nodes (content-bearing, linking, versioning), or is there a single universal node type?
6. [nelson] Must the set of all nodes carry a total ordering that reflects the sequence in which they entered the docuverse?
7. [nelson] Can two distinct nodes hold identical content, or must every node differ from every other node in at least one property?
8. [nelson] What preconditions must hold before a node is permitted to enter — must all nodes it references already exist, or can forward references be admitted?
9. [nelson] Must the identity of a node remain stable across all subsequent versions, or does versioning produce a new node with a new identity?
10. [nelson] If multiple users simultaneously create nodes, what must the system guarantee about the consistency and disjointness of the resulting node identities?
11. [gregory] In the tumbler hierarchy `Node.0.User.0.Doc.0.Element`, what concrete entity does the node field (e.g., `1.1`) represent — a running backend instance, a persistent address partition, or something else?
12. [gregory] How is a node's tumbler address assigned — is there a global allocation authority, a bootstrap configuration file, or does the first backend instance self-assign from a convention?
13. [gregory] When udanax-green initializes via `entexit.c`, does it bind to exactly one node address, and if so, where is that node identity stored and how is it threaded through I-address allocation in `findisatoinsertmolecule`?
14. [gregory] Is the node set fixed at system genesis, or can new nodes enter the docuverse after initial startup — and if so, what mechanism registers them and ensures their tumbler prefix doesn't collide with existing nodes?
15. [gregory] Can a single backend process serve multiple node addresses simultaneously, or is there a strict one-process-per-node invariant enforced somewhere in the event loop (`bed.c`)?
16. [gregory] What invariant prevents two different nodes from allocating the same I-address — is it the tumbler prefix partitioning alone, or is there an additional coordination mechanism beyond address-space separation?
17. [gregory] Does a node have any mutable state of its own (e.g., a node-level counter, capability list, or configuration record), or is a node purely an address prefix whose existence is implied by the presence of accounts and documents beneath it?
