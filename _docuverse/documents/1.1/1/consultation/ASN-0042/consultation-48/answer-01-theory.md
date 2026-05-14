## Question 1 [theory]

> Did the design require that a principal's ownership prefix come into existence *at* the moment of delegation (a fresh baptism), or did Nelson contemplate principals being assigned prefixes that had previously been allocated as ordinary sub-positions within the delegator's domain?

Based on the curated sources, I'll lay out what Nelson explicitly says, then flag what remains uncertain.

## What Nelson Says

The dominant model in Literary Machines is **fresh baptism at the moment of delegation**, not repurposing of pre-existing sub-positions.

The architectural language is consistently generative:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies on whatever basis the owners choose. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." [LM 4/17]

The verbs — *bestowed*, *designate*, *forking*, *baptism* — all point to creation events, not transfers of pre-existing addresses.

Similarly, on the mechanics of forking:

> "One digit can become several by a forking or branching process. This consists of creating successive new digits to the right; we call these 'under' the previous digit." [LM 4/20]

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus 2.1, 2.2, 2.3, 2.4... are successive items being placed under 2." [LM 4/20]

## Structural Reason This Matters

The four-field tumbler structure (Node.0.User.0.Document.0.Element) has *fixed* zero-dividers marking the boundaries between principal levels [LM 4/26-4/28]. A Document-level sub-position within Alice's domain is structurally at the third field, not the second. "Promoting" it to be a User-level prefix would require re-interpreting where the zero-divider falls — which conflicts with the lexical significance Nelson assigns to those dividers:

> "A tumbler address may have at most three zero digits... These are interpreted as the major dividers, and have lexical significance as punctuation." [LM 4/28]

This structural argument suggests that principals (users, accounts) must be baptized *as* principals at their proper field level — they cannot be retroactively elevated from being a Document-level item under someone else's account.

## The Ambiguous Case

There is one passage that leaves room for ambiguity:

> "Typically, the user will have no control over the node address he, she or it is assigned; but once assigned a User account, the user will have full control over its subdivision forevermore." [LM 4/29]

The word "assigned" is neutral — it could describe either fresh baptism or transfer of a pre-existing slot. But Nelson never describes the latter mechanism, and the broader framing of "baptism" and "designation of new numbers" suggests assignment means fresh creation.

## NEED_RAW

The curated sources don't explicitly address the inverse scenario: could a delegator first allocate item 2.4 as an ordinary document, and *later* re-designate 2.4 as a user account belonging to a different principal? To verify whether Nelson contemplated and rejected this (or simply didn't address it), I'd want to check:

**NEED_RAW: 4/17-4/19 (raw 184-186), 4/26-4/30 (raw 193-197)**

These pages cover the baptism mechanism and the four-field structure most directly, and may contain commentary about delegation timing that the curated extracts don't include.
