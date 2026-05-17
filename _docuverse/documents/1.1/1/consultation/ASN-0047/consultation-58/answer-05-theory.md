## Question 5 [theory]

> Does the T10a-conformance requirement for link allocators (L1c) permit "virtual" intermediate addresses in the inc-chain that are never themselves allocated, or must every chain-step address be a live allocation?

The terminology you cite — "T10a-conformance," "L1c," "inc-chain" — is implementation specification language, not mine. I designed the semantics; the conformance taxonomy is the work of those building the system. So let me speak to the underlying design intent, and you can map that to your conformance requirements.

## What I established about addresses vs. allocation

The architecture explicitly separates **addressability** from **storage occupancy**. From the curated extract on ghost elements (LM 4/23):

> "In the present implementation (XU.87.1), the only entities actually stored in tumbler-space are content bytes and links. While a number on the line may represent a document or an account, that doesn't mean there's an object stored for it. What's stored is the contents — bytes and links."

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage. Consider what we may call 'ghost elements'."

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them. A link to or search of an account or node will find any of the documents under it." [LM 4/23]

And for link types specifically (LM 4/45):

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements."

## What this means for chains

My design intent is unambiguous on the principle: **the address space is conceptual; only content bytes and links require live storage.** A link's endset can point at an address where nothing is stored, and the system must still resolve it correctly (typically by finding everything underneath that address in the tumbler tree).

For an inclusion chain specifically — what you call "inc-chain" — the semantic question is whether intermediate references in a transclusion lineage must each correspond to a live allocation. My intent was that **each step is a reference to content** (an Istream address with actual bytes), but the *containers* through which the chain passes (documents, accounts, nodes) need not have any stored representation beyond what the addressing convention implies.

The crucial distinction: a link points at *bytes* or *another link*, and those must exist as stored entities. But a link's address position can be reached through ghost containers (an account that has stored nothing, a document position that exists conceptually under an owner's subtree).

## Where I must defer

NEED_RAW: 4/45-4/51

The curated material covers the principle (ghost elements are valid; types may point to addresses with no stored element), but the specific question of whether **every step in a chain of links-to-links** requires a live link allocation at each intermediate address is not something I addressed at the level of detail your conformance requirement needs. My link-to-link mechanism (4/49-4/51) establishes that links can point at links, and that compound structures can be built — but whether the *traversal path* through such a structure may include virtual waypoints is an implementation interpretation of my semantics.

My guidance to implementers would be: preserve the principle. If a link is a real connective object with an owner and an address, it must be allocated. If you are describing a *path* through tumbler-space whose intermediate positions happen to be ghost containers, that is permitted and indeed expected. The test is whether the endpoints — the actual connective units doing work — are stored, not whether every notional position along an address path is occupied.
