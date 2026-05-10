## Question 6 [nelson]

> If a set of contiguous regions collectively covers a larger contiguous region without gaps, must the system guarantee that this complete-coverage property is verifiable?

## Complete Coverage Verifiability

The question touches on the internal correctness of the system, not on a user-facing guarantee. Let me be precise about what I designed and why.

### The V-Stream Is Always Complete

The virtual byte stream of a document is, by definition, contiguous and gap-free. V-addresses "always form a contiguous sequence starting at 1" — if you have 100 bytes, you have addresses 1 through 100. There are no holes. This is not a property that needs to be "verified" at the user level; it is what a V-stream IS.

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

The V-stream is composed of native spans and inclusions (transclusions). Together, these MUST cover the entire V-stream without gaps or overlaps — otherwise the V-stream would not be contiguous, which would contradict its definition.

### Coverage Is Maintained by Construction, Not by Verification

This is the implementor's problem, not the user's concern. The enfilade data structures — specifically what we called the POOM enfilade (the "eye in the pyramid") — maintain the V→I mapping such that every V-position resolves to exactly one I-position. The data structure's invariants guarantee coverage:

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The FEBE editing operations (INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND) are defined to preserve V-stream contiguity. INSERT shifts following addresses. DELETE closes the gap. REARRANGE transposes regions. None of these can produce gaps, because:

> "The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

### What the User Sees

The user's guarantee is simpler and more powerful than "coverage is verifiable":

> **"THE PART YOU WANT COMES WHEN YOU ASK FOR IT."** [LM 2/16]

When you request content via RETRIEVEV, you get the material. When you request RETRIEVEDOCVSPAN, you get "a span determining the origin and extent of the V-stream" [LM 4/68]. When you request RETRIEVEDOCVSPANSET, you get "a span-set indicating both the number of characters of text and the number of links" [LM 4/68].

The system knows the total extent and composition. The user need not verify coverage — the system's job is to deliver complete, correct content.

### Where Coverage Matters Semantically

There are two places where coverage analysis becomes semantically meaningful at the user level:

**1. Version comparison.** SHOWRELATIONOF2VERSIONS "returns a list of ordered pairs of the spans of the two spec-sets that correspond" [LM 4/70]. For this to be useful, the corresponding pairs must account for all shared content. But the operation returns the correspondence — the user receives the result, not a proof of its completeness.

**2. Royalty accounting.** When a compound document is read, "the original owner and the modifier split the royalty in proportion to who wrote what, as determined automatically" [LM 2/45]. This requires the system to partition the V-stream into native vs. transcluded spans — a coverage decomposition. But again, this is internal bookkeeping, not a user-facing verification.

### The Direct Answer

No, the system need not expose "complete-coverage verifiability" as a user guarantee. The system must MAINTAIN coverage internally — the V-stream is always complete by construction, the enfilade invariants preserve this through edits, and the FEBE operations are defined to never produce gaps. But this is a correctness property of the implementation, not a promise the user needs to check.

The user's promise is: ask for content, receive all of it. The internals that make this work — including the span coverage invariant — are, as I put it:

> "None of these commands are to be seen by the user. The user's concerns are document content and links, and the complications of the protocol are to be handled invisibly by programs in the user's front-end machine, leaving the user free to think about other things." [LM 4/61]

The coverage invariant is real and essential. But it lives in the machinery, not in the contract.
