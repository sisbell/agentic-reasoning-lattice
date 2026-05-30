## Question 1 [theory]

> Was account/document delegation intended to allocate the next sequential subnumber, or may an owner bestow an arbitrary subnumber skipping intervening stream positions?

Those tool calls were a misfire — I have no local file-reading tool available here, so I'll answer from the curated sources and flag what needs raw-page verification.

## Answer

The curated sources point toward **owner discretion** — meaning an owner *may* bestow an arbitrary subnumber rather than being forced to allocate the next sequential one — but Nelson never explicitly addresses skipping intervening stream positions, so this is not fully settled by the verified text.

**The evidence for owner discretion:**

The baptism principle is framed entirely in terms of owner control, with explicit latitude:

> "The basic principle is that of owned numbers. Numbers are owned by individuals or companies, and subnumbers under them are bestowed on other individuals and companies **on whatever basis the owners choose**. Whoever owns a specific node, account, document or version may in turn designate (respectively) new nodes, accounts, documents and versions, by forking their integers. We often call this the 'baptism' of new numbers." (4/17)

> "The owner of a given item controls the allocation of the numbers under it." (4/20)

"On whatever basis the owners choose" and "controls the allocation" both grant the owner authority over how subnumbers are assigned, which is consistent with bestowing a non-sequential subnumber.

**The countervailing evidence (sequential framing):**

Every example Nelson gives describes *successive* allocation, not arbitrary jumps:

> "One digit can become several by a forking or branching process. This consists of **creating successive new digits to the right**; we call these 'under' the previous digit." (4/20)

> "For instance, if there is an item 2, it can branch into several more items, each of which is a daughter item. Thus **2.1, 2.2, 2.3, 2.4... are successive items** being placed under 2." (4/20)

**Assessment:** The *principle* (owner control "on whatever basis they choose") permits arbitrary bestowal, including skipping. The *illustrations* only ever show dense, successive allocation. Because tumbler addressing requires only that assigned addresses remain permanently valid — not that they be contiguous (a span "that contains nothing today may at a later time contain a million documents," per 4/25 in spans.md) — there is no structural barrier to skipping positions. Sequential allocation appears to be a convention/default in the examples, not a stated rule.

NEED_RAW: 4/17, 4/19–4/20 — to confirm whether Nelson anywhere states that baptism must be sequential, or explicitly sanctions skipping subnumbers. The verified excerpts above do not directly resolve the skip question.
