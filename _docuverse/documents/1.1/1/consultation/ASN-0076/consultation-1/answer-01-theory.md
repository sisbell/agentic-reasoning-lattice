## Question 1 [theory]

> Does the design include a "type registry" concept for link types, and what structural form (element-level vs document-level tumbler, content vs link subspace) was intended for type-address tumblers like τ_sup?

# Type Registry: What I Intended vs What's Been Interpreted

## No Formal Registry Concept

I did NOT specify a formal "type registry" mechanism in Literary Machines. What I said is that types are **open-ended and arbitrary**:

> "Links are meant to be extensible for the arbitrary needs of any user. Thus the set of link types is open-ended, and indeed any user may define his or her link types for a particular purpose." [LM 4/43]

> "What the 'type' designation points to is completely arbitrary. This is because of the way we will be searching for links. The search mechanism does not actually look at what is stored under the 'type' it is searching for; it merely considers the type's address." [LM 4/44-4/45]

I acknowledged standardization as future work, not specified architecture:

> "Standardization of a working set of link types is now a high priority, but has less priority than establishing a robust demonstration rig." [LM 4/52]

> "A TENTATIVE LISTING OF SOME LINK TYPES. Link types are open-ended, so this is not the original beginning, but a first provisional, to give the flavor of current thinking." [LM 4/52]

## Structural Form: Anywhere in Tumbler-Space

I was deliberately permissive about where type-address tumblers live. The type endset is symmetrical with from/to endsets — it can point **anywhere**:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." [LM 4/44]

> "There is a universal address space, the tumbler line... We may visualize a link's endsets as mapping to it." [LM 4/45]

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." [LM 4/45]

I did NOT prescribe element-level vs document-level, nor content (0.1) vs link (0.2) subspace. The type is just an address. What matters is that everyone agrees what address means what.

## On τ_sup Specifically

I called this the "Document Supersession Link" [LM 4/52-4/53]. I did not assign it a specific tumbler address. The notation τ_sup and any specific address (e.g., something under the bootstrap document) is implementation work that goes beyond what I specified.

## What I Left to Implementors

NEED_RAW: 4/52-4/53 for any further detail on whether I sketched even informal addressing conventions for the tentative type list. The curated extracts give the principles (arbitrary, ghost elements permitted, address-matched search) but do not show me prescribing where standardized types should be baptized in tumbler-space.

The implementation choice to baptize standard types as ghost elements under doc 1 is **consistent with my design** — it uses ghost elements as I intended — but it is a convention the implementors established to fill the gap I left open.
