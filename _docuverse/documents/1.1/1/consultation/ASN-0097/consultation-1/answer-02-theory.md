## Question 2 [theory]

> What is the complete enumeration of K.μ operation families, and which were intended to displace existing link projections versus create new structure?

The term "K.μ operation families" does not appear in Literary Machines. This is not my terminology, and I want to be precise about what I authored versus what implementations or later interpretations may have introduced.

What I *did* enumerate in Chapter 4 of Literary Machines was the FEBE protocol — 17 commands in XU.87.1, organized by purpose [LM 4/61]:

**Editing operations** (modify document content):
- INSERT, DELETEVSPAN, COPY, REARRANGE, APPEND [LM 4/66-4/67]

**Document operations** (create/manage documents):
- CREATENEWDOCUMENT, CREATENEWVERSION [LM 4/65-4/66]

**Link operations** (the more "esoteric" commands):
- MAKELINK, FINDLINKSFROMTOTHREE, FINDNEXTNLINKSFROMTOTHREE, RETRIEVEENDSETS [LM 4/68-4/70]

**Retrieval operations**:
- RETRIEVEV, RETRIEVEDOCVSPAN, RETRIEVEDOCVSPANSET, FINDDOCSCONTAINING, SHOWRELATIONOF2VERSIONS [LM 4/67-4/70]

As I said: *"What the Xanadu storage and hypertext system does — and thus is — is defined by the commands to which it responds."* [LM 4/61]

I never used the symbol μ or the prefix K. to classify operations. I never wrote about "displacing link projections" as a design concept — links *survive* editing in my design precisely because they attach to spans of bytes via I-addresses, not because operations displace them: *"Links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end."* [LM 4/43]

NEED_RAW: none — the question is using terminology external to Literary Machines. If "K.μ" refers to an implementation framework (udanax-green, udanax-gold) or a downstream specification effort, you'd need to consult that source. I can speak only to what I designed and wrote.
