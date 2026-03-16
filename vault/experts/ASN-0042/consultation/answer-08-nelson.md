## Question 8 [nelson]

> Must the system guarantee that every valid position in the address space has a determinable owner at all times, with no orphaned or unowned regions?

## Yes — Ownership Is Structural, Encoded in the Address Itself

The tumbler address system makes ownership determinable by inspection. Every address has the form `Node.0.User.0.Document.0.Element`, and the **User field IS the owner**:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The forking mechanism guarantees a complete chain of ownership delegation:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

Every position in tumbler-space exists on a tree where each node was "baptized" by a parent who owned the level above. The User field of any address tells you the owner. This is not metadata that can be stripped — it is the address itself.

## Ghost Elements Are Owned Too

Even positions where nothing is stored have determinable owners:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

A ghost element at `1.3.0.7.0.42.0.1` has a determinable owner (User 7 on Node 1.3) even though nothing is stored there. The ownership tree covers the entire address space, occupied or not.

## But Nelson Does Not Address Practical Orphanage

While ownership is always **determinable**, Nelson does not guarantee that the owner is always **reachable or active**. Several scenarios create what we might call practical orphanage:

**1. Anonymous publication.** Nelson explicitly allows "John Doe publication" — anonymous, walk-in users [LM 2/60]. The address still has a User field, but the identity behind it is unknown. Nelson never specifies who exercises ownership rights when John Doe vanishes.

**2. Owner death or disappearance.** Nelson says "Only the owner has a right to withdraw a document or change it" [LM 2/29], but never addresses succession when the owner ceases to exist. The address still encodes ownership; the owner is simply gone.

**3. Storage payment lapse.** Nelson requires "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5] and envisions ongoing storage rental. He does not specify what happens to content — or to ownership — when payment stops.

**4. Vendor failure.** The contract requires "orderly transition of all customer-stored materials to other Xanadu locations" [LM 5/16] upon cancellation, but does not address whether ownership transfers or merely persists in its original (possibly unreachable) form.

## The Root Problem

The entire tree descends from server 1:

> "The server address always begins with the digit 1, since all other servers are descended from it." [LM 4/28]

Nelson does not specify who owns the root. Implicitly it is Project Xanadu (the franchisor), but this is never stated explicitly. The ownership chain terminates at a point that is organizationally defined, not structurally specified.

## Summary

**The system guarantees that every position has a determinable owner — yes.** The tumbler address encodes ownership structurally. There are no positions in the address space where you cannot determine who the owner is by reading the address.

**The system does not guarantee that every owner is reachable, alive, or solvent — and Nelson acknowledges this gap only obliquely.** He builds for the optimistic case (honorable participants in a libertarian system) and leaves the pathological cases — death, abandonment, anonymity, insolvency — to what he calls "the printing press of the future" analogy, where such issues are handled socially and legally rather than technically.

The design principle is: **ownership is a fact of the address, not a fact of the world.** The address always tells you who owns it. Whether that person still exists to exercise ownership is a problem Nelson leaves to the contractual and social layers, not the technical architecture.
