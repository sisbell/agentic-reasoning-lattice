## Question 4 [nelson]

> Is ownership of a position permanent once granted, or can the system revoke it under any circumstances?

## Ownership Is Permanent — With Obligations

Nelson is explicit: once you are assigned a position in tumbler-space, your control over it is **permanent and irrevocable**.

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore."
> — [LM 4/29]

The word "forevermore" is deliberate. Combined with the permanence guarantee on addresses themselves:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address."
> — [LM 4/19]

The system never reassigns or reclaims tumbler positions. The owner "baptizes" sub-addresses freely, and those sub-addresses belong to their designees permanently in turn.

## What Ownership Does NOT Grant

Permanence of ownership does not mean unlimited freedom. Nelson imposes **obligations that flow FROM ownership**:

**Published documents create binding constraints on the owner:**

> "It is in the common interest that a thing once published stay published, as in the world of paper. Other readers and users will come to depend on its accessibility. Consequently its author may not withdraw it except by lengthy due process."
> — [LM 2/43]

You own the document. You cannot easily withdraw it. Publication constrains the owner — it does not transfer ownership to anyone else.

**Link freedom constrains the owner's control over incoming connections:**

> "Each author of a published work is relinquishing the right to control links into that work. This relinquishment must also be part of the publishing contract."
> — [LM 2/43]

Again, this limits what ownership means in practice, but does not revoke it.

## Edge Cases Where Content Can Be Removed

Nelson describes two scenarios where content is removed, but neither revokes ownership of the position:

**1. Peremptory challenge (anonymous content only):**

> "Consider libelous or uncomplimentary John Doe graffiti defaming specific individuals. If John Doe is not available, the affected individual must be able to effect removal of the materials by peremptory challenge."
> — [LM 2/60]

This removes the *content*, not the address or its ownership. The John Doe is absent, so the challenge succeeds by default.

**2. "Lengthy due process" (accountable publishers):**

For identified publishers, peremptory challenge "no longer holds water" — removal requires "negotiation or court order." This is legal process external to the system, not a system mechanism for revoking ownership.

## Storage Vendor Failure

When a vendor goes down, ownership is preserved through migration:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations."
> — [LM 5/16]

The owner's content and position transfer intact. The system is designed so that infrastructure failure never becomes ownership revocation.

## The Unspecified Gap: Storage Payment Lapse

Nelson requires that "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5] and storage requires ongoing rental. He does **not** specify what happens if an owner stops paying. The address itself cannot be reassigned (permanence guarantee), but accessibility may lapse. This is a gap in the specification — ownership of the position is permanent, but whether the content remains *accessible* without ongoing payment is unresolved.

## Summary

| Scenario | Ownership Revoked? | Content Affected? |
|----------|-------------------|-------------------|
| Normal operation | No | No |
| Publication | No (constrained) | Cannot withdraw easily |
| Peremptory challenge | No | Removed (anonymous only) |
| Court order | No | Possibly removed |
| Vendor failure | No (migrated) | Transitions to new vendor |
| Payment lapse | No (address permanent) | Accessibility unspecified |

**The system has no mechanism for revoking ownership of a tumbler position.** Ownership is structural — encoded in the address itself — and permanent by design. What the system does constrain is what owners may *do* with their positions once publication creates obligations to others.
