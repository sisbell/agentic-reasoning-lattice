# Sub-Questions — Tumbler Ownership

**Inquiry:** What does it mean to own a tumbler position? How is ownership established, delegated, and structurally determined?

1. [nelson] Does owning a position in the address space mean exclusive authority over that region, or can multiple users share ownership of the same position?
2. [nelson] Is ownership inherently hierarchical — does owning a position automatically confer ownership of all positions subordinate to it in the address structure?
3. [nelson] Is ownership structurally encoded in the address itself, so that inspecting an address reveals its owner, or is ownership a separate association the system maintains?
4. [nelson] What is the relationship between a user's identity and the positions they own — must each user correspond to a unique, non-overlapping region of the address space?
5. [nelson] Can ownership of a position be permanently transferred from one user to another, or is the original assignment irrevocable?
6. [nelson] Can an owner delegate partial authority over a subregion to another user while retaining ownership of the larger region?
7. [nelson] If delegation is possible, what structural constraints govern how an owner may partition their region among delegates?
8. [nelson] Must the system guarantee that every valid position in the address space has a determinable owner at all times, with no orphaned or unowned regions?
9. [nelson] Must ownership boundaries align with the natural structural boundaries of the address hierarchy, or can ownership be assigned at arbitrary granularity?
10. [nelson] What happens to owned positions when the owning user permanently leaves the system — does the design require a succession or inheritance guarantee for those positions?
11. [gregory] In the tumbler hierarchy `Node.0.User.0.Doc.0.Element`, is ownership a pure structural predicate — i.e., can the system determine "user U owns tumbler T" solely by comparing tumbler prefixes, without consulting any separate ownership table?
12. [gregory] How is a user's tumbler range initially established on a node — does the node allocate a `Node.0.User` prefix via the same `findisatoinsertnonmolecule` max+1 mechanism used for documents, or is there a separate user-provisioning path?
13. [gregory] `makehint` (do2.c:78-84) branches version allocation based on whether the caller "owns" the source document — what exact comparison does it perform to determine ownership, and at which level of the tumbler hierarchy does it match (node, user, or document prefix)?
14. [gregory] Can a user delegate a sub-range of their tumbler space to another entity — for example, granting `1.1.0.2.0.100` through `1.1.0.2.0.200` to a collaborator — or is address-space authority strictly one level deep (node delegates to user, user delegates to documents, no further)?
15. [gregory] When a user creates a version of a document they do NOT own, the version is allocated under the versioning user's account — does this mean the versioning user now owns that version's entire sub-tree, including the right to create sub-versions and allocate further addresses beneath it?
16. [gregory] Is there a structural boundary between "this is my address space" and "this is someone else's" that the backend enforces, or is the ownership boundary purely conventional — could user `1.1.0.2` in principle write a POOM entry under `1.1.0.3`'s document range if no check prevents it?
17. [gregory] The type namespace lives at `1.0.2.x` — who owns this range? Is it a system-level or node-level allocation that sits outside any user's tumbler prefix, and how is write authority to the type namespace determined?
18. [gregory] In a multi-node topology, does ownership of a tumbler prefix on node `1.1` imply anything about that user's authority on node `1.2`, or is ownership strictly local to the node prefix — meaning the same human would have separate ownership roots on each node?
19. [gregory] Does the `.0.` separator play any role in ownership computation, or is it purely a human-readable convention — specifically, does any code path use the position of zero digits to determine where one ownership level ends and another begins?
