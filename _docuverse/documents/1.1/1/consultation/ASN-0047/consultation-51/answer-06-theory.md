## Question 6 [theory]

> Does the Xanadu design require all node addresses to descend from a single bootstrap root as a structural property of the abstract model, or is node lineage a protocol-level concern that may admit disconnected ownership trees?

# Single Bootstrap Root: Structural, Not Merely Protocol-Level

In my design, the single root is **a structural property of the abstract model**, not a protocol convention that could be relaxed.

## The Tree Is Singular by Design

The docuverse is one tree, not a forest. As I wrote:

> "So the docuverse is all really one big forking document." [LM 4/18]

The numbering system reflects this unity:

> "The entire tumbler works like that: nodes can spin off nodes; accounts can spin off accounts; nodes can spin off accounts; and so on. Thus all numeration in the docuverse is compressed into a single mechanism." [LM 4/19]

The phrase "compressed into a single mechanism" is deliberate—there is one tree, one tumbler line, one address space.

## The "1" Is Not Accidental

The first digit being "1" looks like redundancy. It isn't:

> "The server address always begins with the digit 1, since all other servers are descended from it. This may seem an unnecessary redundancy, but it permits referring to the entire docuverse by '1' on the first position." [LM 4/28]

Two things matter here:
1. **"since all other servers are descended from it"** — this is a structural claim about derivation, not a labeling convention
2. **"permits referring to the entire docuverse by '1'"** — the single root provides a semantic affordance: spans and links can address "everything" with one digit in the right position

If ownership trees were disconnected, neither claim would hold. You could not write a span that means "the docuverse," and there would be no canonical ancestry for new servers.

## Baptism Requires an Owner

The forking mechanism itself presupposes an existing owner whose number is being subdivided:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

For any new server to come into existence, something must baptize it. That something must itself have been baptized. The regress terminates at the root.

## What Implementations May Vary

Protocol concerns may govern *how* servers discover each other and *when* BEBE forwarding is necessary—those are operational. But the abstract model's commitment to a single ancestry is structural: it is what makes the tumbler line a line, what makes spans subtree-shaped, and what justifies the claim that all addresses are commensurable.

A "Xanadu" with disconnected ownership trees would no longer be a single docuverse. It would be a federation of address spaces—which is precisely what BEBE was designed to prevent:

> "The function of BEBE is to meld the contents of separate Xanadu servers into a single unified space." [LM 4/70]

The melding is required because the model demands unity. If disconnected trees were structurally admissible, BEBE would not need to meld anything.
