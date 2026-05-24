## Question 5 [theory]

> Does the design intend endset coverage to forward-reference addresses allocated after link creation? When a future K.α allocates an I-address that falls within an existing endset's coverage, is that address considered part of the link's effective referenced set, and what discipline (if any) governs "well-behaved" endset specifications to prevent or admit this?

Looking at this question, I need to verify a few specifics. Let me read the original pages on spans and link search semantics first.

[Reading page-192.png (LM 4/25) on spans]

[Reading page-225.png (LM 4/58) on link search]

Let me look at what the raw pages add to the curated sources.

# Forward-Reference in Endset Coverage

**Yes — the design intends endset coverage to forward-reference future allocations.** This is not an edge case but a direct consequence of three architectural commitments. The discipline question, however, is less fully specified.

## Spans are coverage regions, not enumerations

A span designates a range in tumbler-space; its contents are *implicit in its boundaries*, not enumerated:

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

The temporal dimension is explicit and definitional:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

Forward-reference is therefore intrinsic to span semantics, not an unintended consequence. When K.α is later forked under an address that falls within an existing endset's range, the new K.α is *already inside* that span by definition — no link update is needed.

## Ghost elements legitimize empty targets

Endsets do not require content to exist at their addresses at creation time:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them." (4/23)

And explicitly for coverage that grows:

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

> "A link to or search of an account or node will find any of the documents under it." (4/23)

"Embrace all the contents below them" is the key phrase — an endset over an account-level address covers contents not yet allocated. As new K.α forks under that scope, it becomes part of the link's effective referenced set automatically.

## Address space populates conceptually before storage

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage." (4/23)

Tumbler-space is treated as a coordinate system that storage selectively populates. Endsets describe coordinate regions; what storage exists in those regions is a separate, mutable matter resolved at query time.

## What governs "well-behaved" endset specifications?

The curated sources establish the *capability* without documenting explicit restraint conventions. Several structural facts bear on the question:

1. **Ownership scopes who can populate under an endset.** "The owner of a given item controls the allocation of the numbers under it." (4/20) An endset over `1.2` admits only K.α allocated by the owner of `1.2` — the link creator does not have to anticipate every possible future, only contents allocated within that ownership subtree.

2. **Discontiguous endsets enable precision.** Endsets are span-sets, not single spans. A creator who wants exact coverage (no forward-reference) can express the endset as the union of currently-existing pieces. The capability for forward-reference does not force it.

3. **Search uses overlap, not membership.** "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request." (4/58) Queries can target the originally-intended subset without false hits, provided the queries themselves are precise about the region they want.

4. **Survivability is evaluated dynamically.** "Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end." (4/43) Endset coverage is computed at the time of search — "what is left at each end" includes whatever has been added since.

NEED_RAW: 4/56–4/60 (raw pages 223–227) and 4/48–4/55 (raw pages 215–222) — whether Nelson offers explicit conventions for "well-behaved" endset specifications (e.g., guidance favoring precise enumeration over scope-level addresses, or recommended practices when the link's intended meaning would be distorted by future allocations) is not visible in the curated sources. The capability is unambiguously designed in; whether Nelson discusses discipline around its use is uncovered ground.
