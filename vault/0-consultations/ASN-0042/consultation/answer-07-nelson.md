## Question 7 [nelson]

> If delegation is possible, what structural constraints govern how an owner may partition their region among delegates?

## Structural Constraints on Tumbler Delegation

Nelson specifies a small but precise set of constraints on how owners partition their address regions. The constraints are architectural — they fall out of the tumbler design rather than being imposed as policy.

### 1. Downward Only (Tree Containment)

Delegation is strictly hierarchical. You can only create addresses *under* addresses you own:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "The owner of a given item controls the allocation of the numbers under it." [LM 4/20]

You cannot create sibling addresses, ancestor addresses, or addresses in someone else's subtree. Your entire delegatable region is the subtree rooted at your own address.

### 2. Sequential Creation

New sub-addresses are created as successive integers:

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

This implies allocation proceeds in order — you baptize 2.1, then 2.2, then 2.3. The numbering is a creation-order sequence, not an arbitrary assignment.

### 3. Field-Semantic Level Constraints

The four major fields (Node, User, Document, Element) define what kind of entity each forking level creates:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers." [LM 4/17]

The word "respectively" is doing significant work. A node owner forks to create sub-nodes or accounts. An account owner forks to create documents. A document owner forks to create versions. The semantic level constrains what forking *means* at each position.

The cross-level delegation chain:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

### 4. Permanence (No Reallocation)

Once created, an address cannot be reassigned, reused, or reorganized:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

This means delegation is irrevocable. If you assign sub-region 3.5 to a delegate, you cannot reclaim it, renumber it, or give it to someone else. The tree only grows; it never reshapes.

### 5. Contiguity on the Tumbler Line

Each owner's region forms a contiguous range on the tumbler line. This is a mathematical consequence of the depth-first tree-to-line mapping, not an explicit rule:

> "In a sense the tumbler line is like the real line... But the tumbler line is a different kind of abstraction from the real line. The tumbler line is an abstract representation of a particular tree." [LM 4/22]

> "A span in the tumbler line, represented by two tumblers, refers to a subtree of the entire docuverse." [LM 4/24]

Because every subtree maps to a contiguous span, an owner's delegatable region can be expressed as a single span. This is what makes span-based searching and addressing efficient.

### 6. Owner's Full Discretion Within Their Region

Within these structural constraints, the owner has complete freedom:

> "Subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose." [LM 4/17]

And once assigned an account, the user's autonomy is permanent:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

### 7. Recursive Delegation

Delegation is inherently recursive. A delegate who receives a sub-region becomes the owner of that region and can further subdivide it without permission from the parent:

> "A server node, or station, has ancestors and may have possible descendant nodes. An account, too, and a document, all have possible descendants." [LM 4/19]

### What Nelson Does NOT Constrain

- **No capacity limits** per region — each digit has "no upper limit" [LM 4/19]
- **No depth limits** — forking can continue indefinitely
- **No categorization requirement** — "Tumblers do not affect the user-level structure of the documents; they only provide a mapping mechanism, and impose no categorization and no structure on the contents of a document." [LM 4/17-4/18]
- **No semantic constraint on version numbering** — "In a sense the version, or subdocument number is only an accidental extension of the document number, and strictly implies no specific relationship of derivation." [LM 4/29]

### Summary

The constraints form a compact set: **downward, sequential, permanent, semantically-typed by field, contiguous, and fully autonomous within the allocated region**. This is the minimum needed to ensure global consistency (no address collisions, no coordination required) while preserving local autonomy (owners freely subdivide their regions).

NEED_RAW: [4/20-4/21] — The curated sources cover the main quotes from these pages, but they may contain additional detail about whether sequential allocation is a hard constraint or merely the typical pattern, and whether any exceptions to the "respective" field-semantic delegation are discussed.
