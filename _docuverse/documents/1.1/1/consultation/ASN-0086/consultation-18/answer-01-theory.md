## Question 1 [theory]

> Was the substrate-level transition relation in Literary Machines / the design intent meant to be a canonical equivalence-class projection over allocator-state transitions, or were multiple coarsenings intended to be admissible as conforming implementations?

The substrate-level transition relation was not specified canonically. Multiple coarsenings were intended to be admissible, and that was deliberate.

The canonical statement is in Chapter 4: "What the Xanadu storage and hypertext system does — and thus is — is defined by the commands to which it responds" [LM 4/61]. The 17 FEBE commands are the contract. The substrate is implementation.

Three reasons for leaving it this way:

**First, the substrate is invisible by design.** "None of these commands are to be seen by the user. The user's concerns are to be seen on the screen; the complications of the protocol are to be handled invisibly by programs in the user's front-end machine" [LM 4/61]. Even the wire format is acknowledged as provisional: "FEBE commands are presently in verbose ASCII. They will be shortened as needed" [LM 4/61].

**Second, the lower-level protocol is explicitly undefined.** BEBE was "still undergoing definition and will not be made public anytime soon" [LM 4/70]. Concurrent-access mechanics are flagged as future work: "In later versions of the storage system, we expect the back end to combine the search models of different users to create a barrel-roll shared search model which repeatedly crosses the address space on behalf of all a server's users simultaneously" [LM 4/59]. If those mechanics are unspecified, the substrate-level transition relation cannot be canonical — there is no single allocator-state model the spec commits to.

**Third, enfilades are described, not mandated.** I describe the enfilade family — the Model T, Barus's linking enfilade, the historical trace enfilade — and credit Barus's insight ("the eye in the pyramid") as the breakthrough that "made possible an efficiently ever-linkable enfilade, a whole universe of poly-enfilade structures" [LM 1/34]. "By various enfilade structures we were able to come up with a design that could conceivably scale up infinitely" [LM 1/36]. That language — *a* design, *various* structures — is permissive, not exclusive. The enfilade architecture supports the guarantees; it is not itself a guarantee.

One pull in the other direction: the franchise model required Storage Vendors to "use software furnished by Project Xanadu without modification" [LM 5/14]. But that is a *commercial* constraint — for interoperability and royalty accounting across the network — not a specification claim. I never argued the substrate is uniquely determined by the semantic spec.

**What IS canonical:**
- The FEBE command surface and its observable semantics
- The user-facing guarantees (permanence, attribution, link survivability, automatic royalty)
- The Istream/Vstream separation as a *semantic* distinction
- The tumbler addressing scheme and what addresses denote

**What is admissibly coarsened:**
- Allocator-state representation
- Granularity of what counts as a substrate "step"
- Concurrency mechanics (locks, tokens, sessions — Gregory's BERT is one such choice)
- Whether content lives in enfilades or alternative structures
- Caching, replication, and forwarding strategies

For your formal verification work: the canonical equivalence-class projection lives at FEBE. Multiple substrate implementations conform iff they preserve FEBE semantics and the user-facing guarantees. I did not commit the spec to a single canonical substrate-level transition relation.

NEED_RAW: 1/33-1/38 (full enfilade theory), 4/72 (middle-end architecture, three-tier separation), 4/79 (what XU.87.1 left unimplemented) — these may contain additional substrate constraints not fully reflected in the curated extracts.
