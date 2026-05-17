## Question 1 [theory]

> Was the link retraction operation in Literary Machines intended to nullify a single link or its entire prefix-subtree, and is link-under-link nesting a designed possibility or an unintended degree of freedom?

I need to examine the relevant pages directly to answer this question precisely. Let me check pages 4/9 (deleted link state), 4/31 (link subspace addressing), and 4/49-4/51 (link-to-link).

[Read tool would be called here on relative paths page-176.png, page-198.png, page-216.png, page-217.png, page-218.png — but they appear to be inaccessible from the path given in the prompt]

Based on the curated sources, here is what I can establish from my own text:

## Part 1: Scope of Link Retraction

I did not specify in *Literary Machines* whether retracting a link nullifies just that link or its entire prefix-subtree. The book establishes the existence of the deleted-link state:

> "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]

This parallels the `DELETED BYTES` state but says nothing about whether deletion cascades through a subtree of nested addresses. **NEED_RAW: 4/9, 4/31 to verify whether the original text discusses cascade semantics for deletion.**

What I *did* commit to is that ownership controls retraction — the owner of the home document controls the link's lifecycle — and that nothing is truly destroyed; deleted material "awaits historical backtrack functions." Whether retraction at address `2.5` reaches `2.5.1` is left to the implementor.

## Part 2: Link-Under-Link Nesting

Two distinct concepts must be separated here.

**Link-to-link (pointing)** is unambiguously *designed*. I am explicit:

> "Because of the universality of tumbler-space, and the fact that links are located there as well as data, it becomes easy for a link to point at another link (or, indeed, to point at several)." [LM 4/49]

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." [LM 4/51]

**Link-under-link (addressing/nesting in the tumbler hierarchy)** is a different matter. Here I left it deliberately open:

> "The subdivision of links by further digits (after '2' and the position) is a distinct possibility, and several possible uses have been discussed." [LM 4/31]

This is the key sentence. It signals **a designed possibility, not an accident** — I knew the tumbler system permitted nesting links under links, I considered uses for it, and I chose to leave the slot open rather than freeze it. The forking semantics of the address space make such nesting structurally available; whoever owns an address may baptize sub-addresses beneath it, and that rule applies uniformly. So nesting is not an "unintended degree of freedom" — it falls out of the universal addressability that is itself a design commitment.

But I did not specify *the meaning* of a nested link sub-address, and I did not pair it with retraction semantics. The hierarchical-link discussion at 4/51 mentions "upper- and under-links" as searchable, which suggests one envisioned use was hierarchical typing — but that is constructed via link-to-link *pointing*, not necessarily via address-subordination.

## Summary

- **Retraction scope**: I did not specify. The deleted-link state exists [LM 4/9], but cascade behavior is undefined in *Literary Machines*. **NEED_RAW: 4/9, 4/31** to confirm no further discussion.
- **Link-under-link nesting**: A *designed possibility* — I explicitly acknowledged subdivision of the link subspace as available and discussed [LM 4/31] — but left underspecified. It is a structural consequence of universal tumbler addressing, which is itself intentional. So: designed in principle, unspecified in detail. An implementor must choose semantics consistent with the broader ownership-and-baptism model.
