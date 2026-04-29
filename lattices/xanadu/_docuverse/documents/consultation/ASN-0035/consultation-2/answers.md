# Revision Consultation — ASN-0035

**Review:** review-2.md
**Date:** 2026-03-14 15:41

## Summary

3 REVISE items analyzed: 2 internal, 1 consulted (1 nelson, 0 gregory)

## Consultation Results

### Issue 3: N15 introduces authorization concepts with no formal integration

**Category:** NELSON
**Reason:** The core question is whether allocation authority should be formalized as a precondition on BAPTIZE at this layer or deferred to the account ontology. This is a design-intent question about where authorization enters the specification — Nelson's architectural decision, not an implementation question.

**Nelson question:** Should the node ontology formally constrain who may baptize children under a node (via an abstract authorization predicate on BAPTIZE), or is allocation authority purely an account-level concern that belongs in a downstream ASN?

**Nelson's Answer:**

## Answer: The Node Ontology Should Include an Abstract Authorization Predicate

Nelson establishes baptism authority as a **structural property of the tree itself**, not as something that emerges only at the account level. The constraint applies uniformly at every tier of the hierarchy, which means the node ontology is the right place to capture it — albeit abstractly.

### Nelson's Evidence

The baptism principle is stated at the **tumbler level**, not the account level:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

The recursive pattern — owner of parent authorizes creation of children — is stated as a property of tumbler-space, not of any particular level within it. It applies to nodes spawning nodes, accounts spawning accounts, documents spawning versions, and so on uniformly.

### The Node/Account Asymmetry

Nelson does distinguish authorization *semantics* between levels, which further argues for an abstract predicate rather than a concrete one:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

This tells us:
- **Node-level baptism**: controlled by infrastructure/administrative authority (not the end user)
- **Account-level baptism and below**: controlled by the user who owns the account

The authorization *principle* is the same at both levels (parent owner authorizes child creation), but the *concrete authority* differs. An abstract predicate captures the invariant while allowing downstream ASNs to refine what "owner" means at each tier.

### Why It Belongs in the Node Ontology

If BAPTIZE is an operation in the node ontology (which it must be — it's how the tree grows), then specifying it without the authorization constraint leaves the operation semantically incomplete. Nelson does not describe baptism as "anyone can fork any address" — he describes it as "the owner of an item controls allocation under it." The constraint and the operation are inseparable in his formulation.

An abstract predicate like:

```
predicate CanBaptize(actor: Principal, parent: Node)
```

states the invariant that Nelson established — baptism requires authorization from the parent's owner — without committing to concrete mechanisms (authentication, delegation, ACLs) that belong downstream.

### What the Downstream ASN Would Add

The account-level ASN would refine the abstract predicate with concrete rules:
- How ownership is established for accounts (assignment by node owner)
- How ownership is established for documents (creation)
- Whether and how delegation works ("bestowed on other individuals and companies on whatever basis the owners choose" [LM 4/17])
- The specific asymmetry Nelson identifies at 4/29 between node-level and account-level authority

### Recommendation

Include `CanBaptize` (or equivalent) as an **abstract predicate** in the node ontology, with the invariant that it requires parent ownership. Leave the predicate uninterpreted — no concrete refinement. The node ontology states the *structural law*; the account/session ASN states the *authorization mechanics*.

This mirrors how Nelson himself presents it: the principle is stated once at the tumbler level (4/17, 4/20), then the concrete differences between levels emerge later (4/29).
