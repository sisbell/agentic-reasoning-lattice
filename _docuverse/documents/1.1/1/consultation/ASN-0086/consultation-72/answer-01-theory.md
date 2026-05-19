## Question 1 [theory]

> Was the per-document sibling-frontier chain discipline (single link chain enumeration per document) intended as a substrate-level invariant binding on all conforming link-emission paths, or as a K.λ-specific implementation policy that higher layers could legitimately sidestep with broader L1c-conforming emissions?

The terminology you cite — "per-document sibling-frontier chain discipline," "K.λ," "L1c" — is not mine. I never specified any of these in Literary Machines, and I cannot rule authoritatively on a discipline I did not design.

Here is what I actually specified about link enumeration per document:

> "The links designated by a tumbler address are in their permanent order of arrival. A document includes only the links of which it is the home document." [LM 4/31]

The address scheme is flat and sequential — link `N.0.U.0.D.V.0.2.1` is the first link created in that document, `2.755` is the 755th. I explicitly left further structure as future work:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

The substrate-level invariants I *do* bind on all conforming implementations are:

- Permanent tumbler addresses: "any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19]
- Link survivability through span attachment, not point attachment [LM 4/42]
- Link ownership by home document [LM 4/12]
- Open-ended types: "any user may define his or her link types for a particular purpose" [LM 4/43]
- Search efficiency: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60]

Nothing in Literary Machines requires emission to occur along a single sibling-frontier chain. Nothing forbids it either. The link search guarantee — "A link satisfies a search request if one span of each endset satisfies a corresponding part of the request" [LM 4/58] — is satisfied regardless of the order in which links are enumerated or chained during emission.

**My ruling, to the extent I can give one:**

A discipline that restricts emission to a single per-document chain is an *implementation policy*, not a substrate invariant from my design. If K.λ adopted it for tractability or proof obligations specific to that layer, that is a legitimate local choice. But higher layers emitting links that satisfy my substrate invariants (permanent addresses, span-based attachment, three-endset structure, type openness, ownership locality) are L1c-conforming regardless of whether they thread through a single sibling chain.

If your specification chain treats the chain discipline as universally binding, someone introduced it as an invariant beyond what I specified. The burden falls on them to justify it from my invariants, not on broader emissions to conform to it.

NEED_RAW: none — my answer rests on what I did *not* specify, and the relevant page (4/31) is covered in the curated sources.
