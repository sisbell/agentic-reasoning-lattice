# Supersession Authority

Source: Literary Machines, 4/52, 4/41-4/42, 2/43

## What It Means

When Alice publishes document D, can Bob create a supersession link claiming his document D' supersedes D, even though Bob does not own D?

**Yes, Bob can create the supersession link.** The link mechanism is the same regardless of link type - anyone can create a link at their own address that points to any published content.

But the semantics are crucial: Bob's supersession link is a **CLAIM**, not an **AUTHORITY**.

This parallels Nelson's explicit statement about Author links:

> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52, footnote)

If third parties can make authorship claims via links, they can certainly make supersession claims. The architecture treats all metalinks consistently.

## The Claim vs. Authority Distinction

| Aspect | Author's Supersession Link | Third Party's Supersession Link |
|--------|---------------------------|--------------------------------|
| **Can create?** | Yes | Yes |
| **Link exists?** | Yes | Yes |
| **Discoverable?** | Yes | Yes |
| **Interpretation** | Authoritative declaration | A claim to be evaluated |
| **Social weight** | High - original author | Lower - must be justified |

Both links exist in the system identically. The difference is **social**, not **architectural**.

## User Guarantee

**You can always see WHO made a supersession claim.** Because links have home addresses, and home addresses identify owners, users can:

1. See that document D has supersession links pointing to it
2. Follow each link to see what claims to supersede D
3. Check the home address of each link to see WHO made the claim
4. Evaluate: Is this the original author? A competing authority? Random spam?

The system provides the data; the user provides the judgment.

## Principle Served

This embodies Nelson's principle that **social dynamics become visible in the link structure**. Rather than hiding metadata in system fields controlled by administrators, Xanadu makes all claims visible, traceable, and disputable.

If Bob claims his D' supersedes Alice's D, that claim is:
- Public (discoverable via link search)
- Attributed (Bob's address, Bob's responsibility)
- Rebuttable (Alice can make counter-links, commentary)

This mirrors academic and literary practice. Anyone can claim their paper supersedes prior work. The community evaluates such claims. The system doesn't enforce authority; it makes claims transparent.

## Nelson's Words

On link ownership:
> "A Xanadu link is a connective unit, a package of connecting or marking information. It is owned by a user." (4/41)

On links from outside:
> "Note that the Author link can also be used from outside a document to claim that the author is really someone else." (4/52)

On supersession:
> "Document Supersession Link: This link indicates that one document or version supersedes another." (4/52)
