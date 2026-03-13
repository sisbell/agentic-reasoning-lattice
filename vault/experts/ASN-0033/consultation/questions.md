# Sub-Questions — Node Ontology

**Inquiry:** What is a node in the Xanadu system? How do nodes enter the docuverse, what invariants govern the node set, and what is the relationship between a node and the accounts it contains?

1. [nelson] What defines the identity of a node — how is each node permanently distinguished from every other node in the docuverse?
2. [nelson] What must be true of the global address space when a new node enters the docuverse — must the node receive a unique, permanent portion of that space?
3. [nelson] Must every piece of content in the docuverse belong to exactly one node, or can content exist independent of any node?
4. [nelson] Does a node define an ownership boundary — is the node the authority over the accounts and documents it contains?
5. [nelson] Can a document within one node contain content that originates from a different node, or is each document confined to material held locally?
6. [nelson] Can links created within one node reference content held in a different node, and if so, must the target node participate in establishing that link?
7. [nelson] Must node identities be ordered — does the sequence in which nodes enter the docuverse carry permanent meaning in the address space?
8. [nelson] What invariants must hold over the set of all nodes — must their address portions be non-overlapping, contiguous, or satisfy some other structural property?
9. [nelson] Does a node impose any visibility boundary on its content, or is all content within every node universally addressable across the entire docuverse?
10. [gregory] What tumbler structure identifies a node — is a node always a single non-zero digit (e.g., `1`), or can node addresses be multi-digit (e.g., `1.3`), and how many tumbler fields does the node occupy before the first `.0.` separator?
11. [gregory] When a fresh backend instance starts for the first time, what initialization steps create the node's identity — is there a node address written into the granfilade or spanfilade root, or is the node address purely a configuration parameter external to the enfilade state?
12. [gregory] Is there a node-level data structure (analogous to a document's POOM) that indexes accounts under a node, or is the node→account relationship implicit in the tumbler prefix convention with no dedicated orgl?
13. [gregory] Does the node's tumbler prefix propagate into I-address space — i.e., does every I-address allocated under node `1` begin with `1.`, making the node recoverable from any I-address by inspecting the first field?
14. [gregory] Are the granfilade and spanfilade per-node structures (one pair per node) or single global structures that contain entries from all nodes, distinguished only by their tumbler prefixes?
15. [gregory] What defines the boundary of a node's address range — is there an explicit upper-bound tumbler stored somewhere, or does the node own everything matching its prefix with no mechanism to prevent another node's addresses from colliding in the same enfilade?
16. [gregory] When `findisatoinsertmolecule` or `findisatoinsertnonmolecule` searches for the current maximum I-address, does the search scope itself to the node's address range, or does it walk the entire granfilade and rely on hierarchical tumbler sorting to land in the right region?
17. [gregory] In the original multi-node design intent, was each node expected to carry a complete copy of its own content in its local granfilade, or could a node hold granfilade entries for content originating from other nodes (e.g., after a transclusion from a remote document)?
18. [gregory] Is the set of valid node addresses fixed at system genesis (a finite, pre-allocated set), or can new node addresses be minted at runtime — and if so, what operation creates a new node entry?
19. [gregory] What is the structural relationship between a node tumbler and the account tumblers it contains — does the system enforce that account `N.0.A` can only allocate documents under `N.0.A.0.D`, or is the nesting purely conventional with no backend check preventing an account from writing outside its node's prefix?
