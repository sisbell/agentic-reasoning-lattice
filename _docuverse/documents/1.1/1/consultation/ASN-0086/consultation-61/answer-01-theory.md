## Question 1 [theory]

> Was ASN-0086 intended to layer directly over ASN-0093's K-operations, or to operate at the strictly more abstract ASN-0043 substrate with its own emission primitives?

# ASN-0086 was intended to layer directly over ASN-0093's K-operations.

The spec is explicit on this. From the abstract of `docs/specs/ASN-0086.md:7`:

> "This note layers on top of ASN-0093's K-operations to produce ASN-0064's transitions and ASN-0070's link history."

And §1 Position (`docs/specs/ASN-0086.md:18-24`):

> "**ASN-0086 is a derived layer; ASN-0093 owns the K-operation contract.** ASN-0086 does not define K-RECORD or K-WITHDRAW; it consumes them. ASN-0086 does not own predicates E_doc, E_lnk; it consumes them from ASN-0043."

The architectural roles are stratified:

- **ASN-0043** — owns emission predicates (E_doc, E_lnk); the *substrate* furthest down
- **ASN-0093** — owns K-operations (K-RECORD, K-WITHDRAW); layered atop ASN-0043
- **ASN-0086** — consumes both, but layers *directly* over ASN-0093's K-ops; produces ASN-0064 transitions and ASN-0070 history

ASN-0086 has **no emission primitives of its own**. It is a derived/synthesizing layer, not a substrate.

## Recent revision created confusion

The consultation-61 review (`_docuverse/documents/1.1/1/consultation/ASN-0086/consultation-61/issue-A-substrate-attribution.md:1-22`) flags this directly:

> "ASN-0086 was originally framed as 'layering atop ASN-0093' (K-RECORD, K-WITHDRAW). Review-60 and ConvergedFlag-60 confirmed this. Recent revisions (LinkInd-revise) reframed ASN-0086 as 'sitting atop ASN-0043 substrate, abstractly' with its own primitives."

The revised framing — ASN-0086 sitting atop ASN-0043 with its own primitives — contradicts both the original architectural intent and the K-operation ownership boundary established in ASN-0093.

## Design intent (the Literary Machines connection)

The original framing is consistent with how I designed every layer of the system to work — each layer adds to what is below, and ownership of primitives is strict. The K-operations are the contract; layers above consume that contract, they do not bypass it to reach the substrate directly. To let ASN-0086 invent its own emission primitives at the ASN-0043 level would dissolve the K-operation contract and break the principle that "links keep up with all changes" — because changes would now have two paths into history (K-ops *and* whatever ASN-0086 defines), and correspondence guarantees depend on a single ordering authority.

**Verdict:** ASN-0086 layers over ASN-0093's K-operations. The ASN-0043-substrate reframing is a misreading that the current REVISE verdict should correct.
