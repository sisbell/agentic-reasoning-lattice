## Question 2 [theory]

> In the EnfiladeOSMM design, is address allocation a separate transition from value emission (allowing "spawned but unfilled" addresses), or is each address materialized only when something is deposited there?

Looking at this question, I need to flag something important: **"EnfiladeOSMM" is not a term from Literary Machines.** It appears to be an implementation/design term specific to this project's work, not part of my (Ted Nelson's) original Xanadu specification.

NEED_RAW: The specific EnfiladeOSMM design decision is not addressed in Literary Machines. You'd need to consult the implementation design notes (likely in `docs/design-notes/` or `_docuverse/`) for that specific design choice.

## What Literary Machines DOES Say About This

The closest principle in my work is the concept of **ghost elements** — addresses that exist conceptually without stored content:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links." [LM 4/23]

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." [LM 4/23]

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage." [LM 4/23]

## Design Intent

My design clearly **separates address allocation from content storage** at the structural levels (servers, accounts, documents). Addresses are allocated through the **baptism/forking** mechanism:

> "Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

So at the **conceptual level**, "spawned but unfilled" addresses are not just permitted — they are the normal state for non-content entities. A document address baptized today might contain nothing until bytes are deposited later.

## The Open Question for EnfiladeOSMM

Whether enfilades at the **byte/link storage layer** allow spawned-but-unfilled positions is an implementation choice within my framework. Both approaches are consistent with my design intent:
- **Separate allocation** preserves the ghost-element pattern uniformly
- **Materialize-on-deposit** is also valid since I noted "the only entities actually stored... are content bytes and links"

I'd recommend checking the project's design notes — particularly `docs/design-notes/scout-extraction-pipeline.md` or `docs/design-notes/scout-lattice.md` which appear in your working directory — for the EnfiladeOSMM-specific answer.
