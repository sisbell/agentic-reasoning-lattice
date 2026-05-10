## Question 9 [nelson]

> Does the permanence guarantee extend to the address itself, or only to the content-to-address binding — could the system relocate content so long as the original address still resolves?

## Both — But Physical Location May Change

The permanence guarantee covers two distinct things:

**1. The address itself is permanent.** Forking ensures addresses are never reused or invalidated:

> "New items may be continually inserted in tumbler-space while the other addresses remain valid. This means that any address of any document in an ever-growing network may be specified by a permanent tumbler address." [LM 4/19]

**2. The content-to-address binding is permanent.** Content at an I-space address never changes. I-space is append-only; bytes stored there are immutable.

**3. But physical location is explicitly allowed to change.** This is what BEBE exists for. Nelson says content can migrate between servers freely:

> "The contents can slosh back and forth dynamically." [LM 4/72]

> "Material is moved between servers for a number of purposes: 1. for more rapid access to final material, 2. for more rapid access to needed material which indexes material on other servers, 3. for rebalance in keeping with demand, 4. for redundancy and backup purposes." [LM 4/71]

> "Each server contains a map and a subset of the whole — a microcosm that shrinks and grows." [LM 4/71]

## The Node Field Records Provenance, Not Current Location

The tumbler's Node field (the first major field) identifies the *originating* server — where the content was born. But the system routes around that:

> "Each server contains a continuously valid model or subrepresentation of the entire docuverse and (because of tumbler addressing) a model of the entire network." [LM 4/72]

The user never specifies which server to contact. They present a tumbler address; the system finds the content. If it has migrated, been cached, or been replicated to a closer server, the user is none the wiser.

## The Design Is Explicitly Location-Transparent

Nelson separates what the user sees from where bits physically live:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

This quote refers to internal storage addresses, but the principle extends to network location. The entire BEBE protocol exists to "meld the contents of separate Xanadu servers into a single unified space" [LM 4/70] — meaning physical distribution is an implementation detail hidden from users.

Even vendor failure triggers relocation:

> "Upon notice of cancellation, Storage Vendor will arrange for the orderly transition of all customer-stored materials to other Xanadu locations." [LM 5/16]

Content moves. The address doesn't.

## Summary

| What | Permanent? |
|------|-----------|
| Tumbler address (identity) | Yes — never reused, never invalidated |
| Content at that address (binding) | Yes — I-space is append-only, immutable |
| Physical server location | No — content "sloshes" between servers via BEBE |
| Node field meaning | Records *origin*, not current location |

The system could — and was designed to — relocate content freely, so long as the tumbler address continues to resolve. That's the entire point of the BEBE protocol and the subrepresentation model. Permanence lives in the address and the binding, not in the physical bits.
