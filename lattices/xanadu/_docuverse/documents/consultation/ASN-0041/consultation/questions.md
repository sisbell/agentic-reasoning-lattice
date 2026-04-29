# Sub-Questions — Tumbler Ownership

**Inquiry:** What does it mean to own a tumbler position? How is ownership established, delegated, and what does it confer?

1. [nelson] What rights does owning a position in the address space confer upon the owner?
2. [nelson] Does ownership of a position automatically extend to all positions subordinate to it in the hierarchy?
3. [nelson] Can an owner delegate partial rights over a portion of their address space to another party without transferring ownership itself?
4. [nelson] Is ownership of a position permanent once granted, or can the system revoke it under any circumstances?
5. [nelson] Must the system record and preserve the provenance of every ownership grant — who granted what to whom?
6. [nelson] Can ownership be transferred from one party to another, and if so, does the original owner retain any residual rights?
7. [nelson] Does the design distinguish between owning a position and merely having permission to act within it?
8. [nelson] What obligations does ownership impose on the owner — are there responsibilities the system enforces, not just rights it grants?
9. [nelson] If an owner delegates a sub-range of their space, can the delegate further sub-delegate portions of that range to others?
10. [nelson] Must the system guarantee that no two parties can independently hold ownership of the same position?
11. [gregory] Is ownership of a tumbler position determined structurally from the tumbler hierarchy (e.g., `1.1.0.2` is owned by whoever owns the `1.1.0.2` account prefix), or is there a separate ownership table or data structure that records who owns what?
12. [gregory] In `makehint`, what exact predicate determines whether the current session "owns" the source document — is it a tumbler prefix match between the session's account address and the document's I-address, or something else?
13. [gregory] Does ownership of a node-level tumbler (e.g., `1.1`) automatically confer ownership of all descendant tumblers beneath it (accounts `1.1.0.x`, documents `1.1.0.x.0.y`), or is each level independently assigned?
14. [gregory] Is there a delegation mechanism where an owner of a tumbler range can grant another account the right to allocate new children within that range — for example, a node operator granting a new user the right to create documents under their allocated account prefix?
15. [gregory] Does the system distinguish between "owns this specific tumbler" and "has allocation rights under this tumbler prefix"? For example, can an account own document `1.1.0.2.0.5` without having the right to create `1.1.0.2.0.6`?
