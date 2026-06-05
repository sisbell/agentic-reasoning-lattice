## Question 1 [theory]

> When a link is read by its own identity, what must the system return about the relationship that link records?

## What a link records

A Xanadu link is not a simple A-to-B pointer. It records a **three-way relationship** through three endsets:

- the **from-set** — the bytes the link is "from"
- the **to-set** — the bytes the link is "to"
- the **type** (the "three-set") — what kind of connection this is

> "A link is typically directional. Thus it has a from-set, the bytes the link is 'from,' and a to-set, the bytes the link is 'to.' (What 'from' and 'to' mean depend on the specific case.)" [LM 4/42]

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

Each endset is not a single point but an **arbitrary span-set** — it may touch discontiguous bytes anywhere in the docuverse [LM 4/42-4/45].

## What the system must return when reading a link by its own identity

Because a link is itself a first-class object with its own tumbler address, you can name it directly and ask the system for what it connects. The operation that does this is **RETRIEVEENDSETS**:

> "This returns a list of all link end-sets that are in <spec set>." [LM 4/70]

So when a link is read by its own identity, the system must return its **endsets** — the spans that constitute the relationship the link holds together: where it reaches from, where it reaches to, and (as the symmetrical third endset) what type of relationship it is. Critically, these are returned as *sets of spans pointing into the docuverse*, not as positions, which is what lets the recorded relationship survive editing of either end:

> "A Xanadu link is not between points, but between spans of data... it means that links can survive editing. If any of the bytes are left to which a link is attached, that link remains on them." [LM 4/42]

## One note on scope

The curated `operations` source describes RETRIEVEENDSETS as returning "all link end-sets," while the `endsets` concept summary characterizes it more narrowly as returning "the from-set and to-set of specified links." The semantic intent is unambiguous — the relationship a link records is its three endsets (from, to, type) — but if you need the precise wording of exactly which endsets RETRIEVEENDSETS hands back versus what is recovered via other means, that warrants checking the raw page:

NEED_RAW: 4/70
