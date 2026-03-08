## Question 9 [nelson]

> If a user inserts new content into a document, must that content first be committed to permanent storage before the document can arrange it, or can the two happen simultaneously?

## Content Must Exist in I-Space Before V-Space Can Reference It

Nelson's architecture logically requires that content be committed to permanent storage (I-space) before or simultaneously with its arrangement in V-space — but the user never sees this as a two-step process. The FEBE protocol presents it as a single atomic command.

### The Logical Dependency

V-space is a **mapping** from virtual positions to I-space addresses. You cannot create a mapping to something that doesn't exist:

> "Native bytes of a document are those actually stored under its control and found directly in storage under its control; all other bytes are obtained by front-end or back-end requests to their home locations." [LM 4/11]

> "Logical addressing of the byte stream is in the form of virtual spans, or vspans. These are sequences of bytes in the document's virtual byte stream, regardless of their native origin." [LM 4/11]

V-space entries point TO I-space addresses. The I-space address is the identity. Without it, there is nothing for V-space to reference.

### The Protocol Hides This

INSERT is defined as a single FEBE command:

> "This inserts \<text set\> in document \<doc id\> at \<doc vsa\>. The v-stream addresses of any following characters in the document are increased by the length of the inserted text." [LM 4/66]

The user provides text and a V-space position. The system handles I-space commitment internally. Nelson explicitly says users don't see I-space:

> "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing; the front-end application is unaware of this." [LM 4/11]

### The Enfilade Manages Both Together

The data structure handles storage and arrangement as a unified concern:

> "a data structure that manages huge agglomerates of text and their arrangement in and out of core." [LM 1/33]

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." [LM 1/34]

The "canonical order" mandate means that after any operation, the system is in a fully valid state — I-space and V-space are consistent. This implies atomicity: the two happen together, not as separable steps.

### COPY Confirms the Dependency

The COPY (transclusion) operation is revealing by contrast. It creates a V-space mapping to **already-existing** I-space content:

> "The material determined by \<spec set\> is copied to the document determined by \<doc id\> at the address determined by \<doc vsa\>." [LM 4/67]

COPY needs no new I-space storage because the content already has permanent addresses. INSERT must create those addresses. The append-only model describes how:

> "Instead, suppose we create an append-only storage system. User makes changes, the changes difflessly into the storage system, filed, as it were, chronologically." [LM 2/14]

### Summary

**Logically**, I-space commitment must precede or be simultaneous with V-space arrangement — V-space is a mapping layer that references I-space, so the referent must exist. **Operationally**, Nelson treats this as a single atomic step. The FEBE protocol exposes one command (INSERT), the enfilade manages both concerns in one data structure, and the user never sees I-space directly. The ordering is an implementation detail that Nelson deliberately hides behind the protocol abstraction.
