## Question 10 [theory]

> What invariant about the total population of documents must hold after creation — that exactly one new addressable document now exists and nothing else changed?

## The Document-Creation Invariant

After `CREATENEWDOCUMENT`, the docuverse must satisfy a **monotonic, non-disruptive growth** invariant: exactly one new addressable document position comes into being, and the entire pre-existing address population is left untouched. Three sub-conditions express this.

### 1. Exactly one new address is baptized under the owner's account

Creation is *forking* — the owner mints one new sub-number beneath an account they control. This is "baptism":

> "The basic principle is that of owned numbers... Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (`tumblers`, 4/17)

> "The owner of a given item controls the allocation of the numbers under it." (`forking`, 4/20)

The operation returns precisely that one id:

> "This creates an empty document. It returns the id of the new document." (`operations`, 4/65)

So the population of addressable documents increases by *exactly one*, and that one falls strictly under the creating account — no other account's subtree is touched.

### 2. Every pre-existing address remains valid and unchanged (no renumbering)

This is the core "nothing else changed" guarantee. Forking adds digits to the right and never reorganizes what already exists:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." (`tumblers`, 4/19)

> "No reorganization ever happens — once an address is forked, its relationship to its parent is permanent." (`forking`)

> "creation never exhausts the space; insertion never invalidates existing references." (`forking`)

Thus every other document keeps its identity, its tumbler address, its contents, and its links. The new document neither displaces nor shifts any sibling.

### 3. The new document is empty — addressable but with nothing stored

The newly created position is, at the instant of creation, a **ghost element**: a conceptually occupied position with no stored bytes or links yet.

> "While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links." (`ghost-elements`, 4/23)

> "the only entities actually stored in tumbler-space are content bytes and links." (`ghost-elements`, 4/23)

So creation changes the *address population* (one new occupied position) without yet changing the *stored population* of bytes or links. Its Vstream is empty; its cash register, if/when published, starts at zero.

### Summary of the invariant

| Quantity | Before | After |
|---|---|---|
| Addressable document positions | N | N + 1 |
| Which existing addresses are still valid | all | all (unchanged) |
| Existing documents' contents/links | as-is | identical |
| Stored bytes/links of the new doc | — | none (empty) |
| Owner of the new address | — | the creating account, strictly under it |

In short: **one address is added by baptism strictly beneath the owner's account; all prior addresses remain permanently valid and unaltered; and the new document begins empty (a ghost position with no stored bytes or links).** This follows directly from tumbler forking — "the docuverse is all really one big forking document" (`forking`/`tumblers`, 4/18) — where growth is purely additive and never invalidates or reorders existing references.

One caveat: Nelson states these principles (permanence of existing addresses, owned-number baptism, empty-document creation, ghost elements) but does not frame them together as a single named "creation invariant." The synthesis above — that the *only* change is +1 addressable document and nothing else — is my reconstruction from those guarantees, not a verbatim Nelson formulation.
