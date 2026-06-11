## Question 1 [theory]

> Was the direct read of a link by its address intended as a precondition-gated operation the caller must only invoke on existing links, or as a total request whose contract includes reporting that no link lives at the given address?

The raw page images aren't readable in this session (the file-reading tool is disabled here), so I'm answering from the curated, verified extracts — and I flag below where the verbatim command definitions should be checked.

---

## Answer: a total request. Absence is an answer, not a caller error.

I never designed link retrieval as an operation you may only invoke after establishing that a link exists. The contract is total: you hand the back end an address (a spec-set covering it), and the back end tells you what is there — which may be nothing. Three lines of design intent converge on this.

### 1. The retrieval commands are phrased over spec-sets, where emptiness is a legitimate result

There is no "dereference this one link, which must exist" primitive in FEBE. Reading a link by its address means presenting a spec-set that covers that address — a span of 1 on the link, as I describe for link-to-link pointing: "The to-set of the link need simply point to the actual link address in the tumbler line, with a span of 1 to designate that unit only" [LM 4/49]. The retrieval commands over such sets are all defined as *all-that-is-there* operations:

> "This returns a list of all link end-sets that are in <spec set>." — RETRIEVEENDSETS [LM 4/70]

> "This returns a list of all links which are (1) in <home set>, (2) from all or any part of <from set>, and (3) to all or any part of <to set> and <three set>." — FINDLINKSFROMTOTHREE [LM 4/69]

A contract of the form "return all links in the set" degrades gracefully to the empty list. Nothing in these definitions restricts the input to occupied addresses, and the companion counting command (FINDNUMOFLINKSFROMTOTHREE) presupposes that zero is a reportable answer. Compare: "THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS." [LM 4/60] — the system is built around requests that mostly *don't* match.

### 2. Tumbler-space is sparsely occupied by design — addressing the unoccupied is well-formed

Ghost elements make this explicit. The address space is conceptual; storage populates only selected points of it:

> "Thus the address population of tumbler-space is also an abstraction, since things may be addressed even though nothing is there to represent them in storage." [LM 4/23]

> "It is possible to link to a node, or an account, even though there is nothing stored in the docuverse corresponding to them." [LM 4/23]

An address naming no stored object is not malformed input — it is a valid coordinate in the docuverse. The same holds for spans: "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." [LM 4/24] And occupancy is time-varying by design: "A span that contains nothing today may at a later time contain a million documents." [LM 4/25] A request over a region carries no assertion about what occupies it; the back end's reply is precisely how you learn.

### 3. The caller *cannot* maintain such a precondition, so I couldn't have intended one

Three facts make existence unknowable at call time:

- **Links are deletable by their owners.** "DELETED LINKS (not currently addressable, awaiting historical backtrack functions, may remain included in other versions.)" [LM 4/9]. And because links sit in permanent order of arrival — "The links designated by a tumbler address are in their permanent order of arrival" [LM 4/31] — the address of a deleted link remains a permanently valid coordinate with nothing currently living there. The permanence guarantee ("New items may be continually inserted in tumbler-space while the other addresses remain valid" [LM 4/19]) is about *addresses*, deliberately decoupled from *occupancy*. So "valid address, no current link" is a routine, anticipated state, and the deleted-links state is exactly the system's report of it.
- **The docuverse is distributed and concurrently edited.** Any reference a front end holds may be stale by the time it's used; the back end is the sole authority on current state. The whole point of the find/retrieve family is discovery of what exists.
- **The network itself is unreliable.** "It is a truism that 'computer networks are always broken.'" [LM 4/75] A protocol whose read operations were violated by absence could not function in that world; absence and unavailability must be reportable outcomes.

Add the architectural stance that "the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things" [LM 4/61] — the front end shields the *user* from these cases, which only makes sense if the protocol *surfaces* them to the front end rather than forbidding them.

---

### Caveat on verbatim wording

The curated extracts establish the design intent firmly, but they do not preserve the exact response-format language of XU.87.1 — e.g., whether an unoccupied link address yields an empty list, a distinguished "nothing stored" reply, or an error token at the wire level. NEED_RAW: 4/61-4/70 (raw pages 228-237, the 17-command definitions), 4/23 (raw 190, ghost elements context). If you can pull those pages, check the RETRIEVEENDSETS and FINDLINKSFROMTOTHREE definitions for any explicit empty-result or failure wording.

**For your formalization:** model the read as a total function over all syntactically valid link addresses, returning an option/empty-set on unoccupied addresses — not as a `requires link_exists(addr)` operation. A precondition-gated contract would falsify the deleted-link state, the ghost-element doctrine, and the permanence-without-occupancy split that the tumbler design depends on.
