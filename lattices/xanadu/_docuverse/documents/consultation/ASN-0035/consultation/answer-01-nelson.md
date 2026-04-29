## Question 1 [nelson]

> What is the minimal set of properties that define a node at the moment it enters the docuverse?

# The Minimal Properties of a Node Entering the Docuverse

The answer has two layers, because Nelson's architecture distinguishes between conceptual existence and operational function.

## Layer 1: Conceptual Existence (Ghost Element)

At its most minimal, a node needs only **one thing**: a tumbler address, baptized by its parent.

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [4/23]

A node can exist in the docuverse as pure address — no content, no accounts, no stored representation whatsoever. Other nodes can already link to it. A link to a node "will find any of the documents under it" [4/23] — even if there are none yet.

The address itself carries two facts:
1. **Ancestry** — the node descends from a parent. "A server node, or station, has ancestors and may have possible descendant nodes." [4/19] The server address "always begins with the digit 1, since all other servers are descended from it" [4/28].
2. **Ownership** — "The owner of a given item controls the allocation of the numbers under it." [4/20] Someone baptized this number and controls what spawns beneath it.

That is the conceptual minimum. Address plus ownership. Everything else is operational.

## Layer 2: Operational Function (Live Server)

For a node to actually *serve* — to participate in the docuverse as a functioning station — it needs three additional properties:

### A. A Network Model (Even If Null)

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [4/72]

> "A server's network model, from the null case on up, is at all times unified and operational; whatever information moves between servers is assimilated at once to its overall structure, leaving each server in canonical operating condition with a slightly improved map of what is elsewhere." [4/72]

The phrase **"from the null case on up"** is critical. A new node starts with a null subrepresentation — an empty microcosm — and this is already "unified and operational." The model grows incrementally as requests flow through: "The contents can slosh back and forth dynamically" [4/72].

### B. Protocol Capability (FEBE and BEBE)

The node must speak both protocols:
- **FEBE** to serve users — "the protocol for handing off what the user wants to see, retrieve and follow" [4/62]
- **BEBE** to join the network — "the protocol for connecting nodes of the Xanadu network" whose "function is to meld the contents of separate Xanadu servers into a single unified space" [4/70]

### C. Contractual Standing

> "Storage Vendor agrees to honor requests for material from customers connected to servers operated by other Xanadu-licensed storage vendors." [5/14]

> Storage Vendor must "use software furnished by Project Xanadu without modification." [5/14]

Without the franchise contract, a node cannot participate in the trust model that holds the docuverse together. The contract is as much a part of the system as the code.

## Summary: The Minimal Set

| Property | Ghost Node | Live Node |
|----------|-----------|-----------|
| Tumbler address (baptized) | Required | Required |
| Ownership (who controls sub-numbers) | Required | Required |
| Network model (subrepresentation) | Not needed | Required (null is valid) |
| Protocol capability (FEBE/BEBE) | Not needed | Required |
| Franchise contract | Not needed | Required |

A ghost node is **two properties**: address and ownership. A live node adds **three more**: a (possibly null) network model, protocol compliance, and contractual standing.

The deeper point: the docuverse is populated by concepts, not objects. A node exists the moment its number is baptized. It *functions* the moment it can speak the protocols and honor the contract. Between those two moments, it is a ghost — addressable, linkable, but empty.

NEED_RAW: [4/74-4/75] — these pages discuss the connection model and network resilience in detail; they may contain additional specifics about what a node must establish when it first joins the network (handshake, initial synchronization).
