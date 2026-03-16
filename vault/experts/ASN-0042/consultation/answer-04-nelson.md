## Question 4 [nelson]

> What is the relationship between a user's identity and the positions they own — must each user correspond to a unique, non-overlapping region of the address space?

## Identity and Address Space Ownership

**Yes — each account corresponds to a unique, non-overlapping region of the address space.** This is not an additional constraint imposed by policy but a structural consequence of the tree-based tumbler addressing.

### The Tree Makes It Automatic

The tumbler hierarchy is a tree:

```
Node.0.User.0.Document.0.Element
```

Each account occupies a subtree. Because subtrees of a tree are disjoint by construction, no two accounts can overlap. The "tumbler line" (the depth-first ordering of the tree) maps each account's subtree to a contiguous, non-overlapping range:

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

Ownership flows strictly downward through the tree. The node operator assigns you an account address; everything beneath that address is yours:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

### Account vs. Person: A Critical Distinction

The non-overlapping property holds between **accounts**, not between **persons**. Nelson speaks of numbers owned by "individuals or companies" [LM 4/17]. This means:

- **One person, multiple accounts**: A person can hold accounts on different nodes, each a separate non-overlapping region. Nothing in the specification prevents this.
- **One account, multiple persons**: A company or organization is a single account owner but represents many people. Sub-accounts can be delegated: "accounts can spin off accounts" [LM 4/19].
- **Sub-delegation**: An account holder can subdivide their space and delegate sub-accounts to others. The sub-accounts remain within the parent's subtree — still non-overlapping with accounts outside it.

### Ownership vs. Reference

The non-overlapping constraint applies to **where content lives** (I-space addresses), not to **what content references**. Links and transclusions freely cross ownership boundaries:

> "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." [LM 4/12]

> "Document A can include Document B, even though Document B is owned by someone else." [LM 2/35]

When you transclude content from another user's document, that content stays at its original I-address (in the other user's subtree). Your document's V-space references it; your I-space does not absorb it. The address tells you who created it:

> "You always know where you are, and can at once ascertain the home document of any specific word or character." [LM 2/40]

### Why This Matters

The identity-address binding serves three purposes:

1. **Ownership is structural, not metadata.** The User field of any I-address IS the owner. You cannot forge ownership because you cannot create content at someone else's address — you can only create content under your own account's subtree.

2. **Attribution is unforgeable within the system.** Origin traceability follows from the address structure: every byte's I-address encodes which account created it.

3. **Decentralized coordination.** No central authority allocates addresses globally. Each owner subdivides their own space independently: "all numeration in the docuverse is compressed into a single mechanism" [LM 4/19]. The tree structure guarantees non-collision without coordination.

### Summary

Each account maps to a unique subtree — and therefore a unique, non-overlapping region — of tumbler space. This is inherent in the tree structure, not a rule that must be enforced. A person may own multiple accounts (multiple disjoint regions), and an account may represent multiple people, but the account-to-region mapping is always one-to-one and non-overlapping. Content lives exclusively in its creator's region; references (links, transclusions) cross regions freely.
