## Question 6 [theory]

> Did the design treat the substrate's (C, M, L) triple as the complete state model, or did it contemplate layer-maintained state outside the substrate (timestamps, metadata, external accessors) as part of the overall system?

# Answer: The Substrate Was Not the Complete State Model

Nelson explicitly contemplated layer-maintained state outside the content/mapping/links substrate. The substrate stores what is permanent and addressable; other state lives at adjacent layers.

## What Nelson Says Lives Outside the Substrate

**1. Time is kept separately.** This is the clearest direct statement:

> "Note that 'time' is not included in the tumbler. Time is kept track of separately." (4/18)

So timestamps on links, dates on mail-links ("since links will be dated, the time of mailing is shown" — 4/55), and historical-backtrack indexing are layer-maintained, not encoded in addresses.

**2. Cash registers, passwords, accounting** sit in a separate user system area:

> "Each published document has a cash register. This is a system-maintained counter which increments whenever bytes or links are delivered out of the document. The cash register has no size limit. It is in the user's system area, along with passwords and accounting information." (5/13)

**3. Network maps and subrepresentations** are per-server state about where content lives:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." (4/72)

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." (4/71)

**4. A "middle end" layer** sits between front and back end for parsing, scanning, search — explicitly NOT in the back-end substrate:

> "Many people, particularly those who are accustomed to the assorted 'model' of other file systems, have a hard time getting used to our link model, and insist that scanning should be part of the Xanadu back end." (4/72)

Nelson pushes back: search and indexing belong in the middle end.

**5. The Author's Fund** — an escrow accounting system for charitable funding (5/12) — is layer state.

## What IS in the Substrate

The substrate canonically holds only two things:

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links." (4/23)

The V→I mapping is *derived* via enfilades (POOM) over the same content. Documents, accounts, and servers are "ghost elements" — addressable positions, not stored objects (4/23).

## Architectural Pattern

Nelson's three-tier architecture makes the separation explicit:

| Layer | State maintained |
|-------|------------------|
| Front End | UI, local viewing, user encryption for privacy |
| Middle End | Parsing, scanning, search indices, version comparison |
| Back End | Content bytes, links, V→I mapping |
| Per-server (BEBE) | Maps, subrepresentations, caching, routing |
| Vendor / accounting | Cash registers, passwords, Author's Fund, royalty flow |

## One Notable Inversion

Privacy is realized by state *not kept*: the network "may not monitor what is read or what is written in private documents" (2/59). So the layer model also constrains what state may exist outside the substrate.

## Summary

The (C, M, L) substrate is the **permanent, addressable** state. Nelson explicitly placed timestamps, accounting, network topology, search indices, and access metadata in adjacent layers — front-end, middle-end, per-server, and vendor accounting. The substrate is the part guaranteed to be permanent and content-addressed; everything else is layer-maintained and may be reconstructed, cached, or vary across servers.
